from typing import Dict, List, Optional, Any
from collections import defaultdict
from app.services.excel_data_loader import ExcelDataLoader

class AnalyticsServiceExcel:
    """Service for CRM analytics using Excel data"""
    
    def __init__(self, data_loader: ExcelDataLoader):
        self.data_loader = data_loader
    
    async def get_contacts_without_opportunities(self) -> List[Dict]:
        """
        Get all contacts that are not associated with any opportunities/deals
        """
        # Get all contacts and deals
        contacts = self.data_loader.get_all_contacts()
        deals = self.data_loader.get_all_opportunities()
        
        # Extract contact IDs from deals
        contact_ids_in_deals = set()
        for deal in deals:
            # Check for contact_id or sales_account_id
            if deal.get("contact_id"):
                contact_ids_in_deals.add(deal["contact_id"])
            if deal.get("sales_account_id"):
                contact_ids_in_deals.add(deal["sales_account_id"])
        
        # Filter contacts not in deals
        contacts_without_deals = [
            contact for contact in contacts
            if contact.get("id") not in contact_ids_in_deals
        ]
        
        return contacts_without_deals
    
    async def get_contacts_by_source(self, source_filter: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Group contacts by source type (Referral, Walk-in, Online Walk-in)
        
        Args:
            source_filter: Optional filter for specific source type
        """
        contacts = self.data_loader.get_all_contacts()
        
        # Group contacts by source
        grouped = {
            "referral": [],
            "walk_in": [],
            "online_walk_in": [],
            "other": []
        }
        
        for contact in contacts:
            # Check various source fields
            source = contact.get("lead_source_id") or contact.get("medium") or contact.get("source") or ""
            source_lower = str(source).lower()
            
            # Categorize based on source
            if "referral" in source_lower or "reference" in source_lower or "referred" in source_lower:
                grouped["referral"].append(contact)
            elif "walk" in source_lower and "online" not in source_lower:
                grouped["walk_in"].append(contact)
            elif "online" in source_lower:
                grouped["online_walk_in"].append(contact)
            elif source_lower in ["", "none", "null"]:
                grouped["other"].append(contact)
            else:
                grouped["other"].append(contact)
        
        # Apply filter if specified
        if source_filter:
            filter_key = source_filter.lower().replace(" ", "_").replace("-", "_")
            if filter_key in grouped:
                return {filter_key: grouped[filter_key]}
            return {source_filter: []}
        
        return grouped
    
    async def get_opportunities_by_stage(self, stage_filter: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Group opportunities by stage
        
        Args:
            stage_filter: Optional filter for specific stage
        """
        deals = self.data_loader.get_all_opportunities()
        
        # Group by stage
        grouped = defaultdict(list)
        
        for deal in deals:
            stage = deal.get("deal_stage_id") or deal.get("stage") or "Unknown"
            stage_name = deal.get("deal_stage", {}).get("name") if isinstance(deal.get("deal_stage"), dict) else str(stage)
            
            # Handle None stage
            if stage_name is None or str(stage_name).lower() == 'none':
                stage_name = "Unknown"
            
            grouped[stage_name].append(deal)
        
        # Convert to regular dict
        result = dict(grouped)
        
        # Apply filter if specified
        if stage_filter:
            if stage_filter in result:
                return {stage_filter: result[stage_filter]}
            return {stage_filter: []}
        
        return result
    
    async def get_leads_by_sales_owner(self, owner_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get leads/opportunities grouped by sales owner with all details
        
        Args:
            owner_id: Optional filter for specific sales owner
        """
        deals = self.data_loader.get_all_opportunities()
        
        # Group by owner
        grouped = defaultdict(lambda: {
            "owner_info": {},
            "leads": [],
            "total_value": 0,
            "count": 0
        })
        
        for deal in deals:
            owner = deal.get("owner") or deal.get("owner_id")
            
            if isinstance(owner, dict):
                owner_name = owner.get("display_name") or owner.get("email") or f"Owner {owner.get('id')}"
                owner_key = str(owner.get("id", "unknown"))
            else:
                owner_name = f"Owner {owner}" if owner else "Unassigned"
                owner_key = str(owner) if owner else "unassigned"
            
            # Skip if filtering by specific owner
            if owner_id is not None and owner_key != str(owner_id):
                continue
            
            grouped[owner_name]["owner_info"] = {
                "id": owner_key,
                "name": owner_name
            }
            grouped[owner_name]["leads"].append(deal)
            grouped[owner_name]["count"] += 1
            
            # Add to total value if available
            amount = deal.get("amount") or deal.get("deal_value") or 0
            try:
                grouped[owner_name]["total_value"] += float(amount) if amount else 0
            except (ValueError, TypeError):
                pass
        
        return dict(grouped)
    
    async def get_opportunities_by_advisor(self, advisor_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get opportunities grouped by advisor (sales owner) with stage breakdown
        
        Args:
            advisor_id: Optional filter for specific advisor
        """
        deals = self.data_loader.get_all_opportunities()
        
        # Group by advisor with stage breakdown
        grouped = defaultdict(lambda: {
            "advisor_info": {},
            "opportunities": [],
            "stages": defaultdict(lambda: {"count": 0, "deals": [], "total_value": 0}),
            "total_count": 0,
            "total_value": 0
        })
        
        for deal in deals:
            owner = deal.get("owner") or deal.get("owner_id")
            
            if isinstance(owner, dict):
                advisor_name = owner.get("display_name") or owner.get("email") or f"Advisor {owner.get('id')}"
                advisor_key = str(owner.get("id", "unknown"))
            else:
                advisor_name = f"Advisor {owner}" if owner else "Unassigned"
                advisor_key = str(owner) if owner else "unassigned"
            
            # Skip if filtering by specific advisor
            if advisor_id is not None and advisor_key != str(advisor_id):
                continue
            
            # Get stage information
            stage = deal.get("deal_stage_id") or deal.get("stage") or "Unknown"
            stage_name = deal.get("deal_stage", {}).get("name") if isinstance(deal.get("deal_stage"), dict) else str(stage)
            
            # Handle None stage
            if stage_name is None or str(stage_name).lower() == 'none':
                stage_name = "Unknown"
            
            # Get deal value
            amount = deal.get("amount") or deal.get("deal_value") or 0
            try:
                deal_value = float(amount) if amount else 0
            except (ValueError, TypeError):
                deal_value = 0
            
            # Update advisor info
            grouped[advisor_name]["advisor_info"] = {
                "id": advisor_key,
                "name": advisor_name
            }
            grouped[advisor_name]["opportunities"].append(deal)
            grouped[advisor_name]["total_count"] += 1
            grouped[advisor_name]["total_value"] += deal_value
            
            # Update stage info
            grouped[advisor_name]["stages"][stage_name]["count"] += 1
            grouped[advisor_name]["stages"][stage_name]["deals"].append(deal)
            grouped[advisor_name]["stages"][stage_name]["total_value"] += deal_value
        
        # Convert defaultdicts to regular dicts
        result = {}
        for advisor, data in grouped.items():
            result[advisor] = {
                "advisor_info": data["advisor_info"],
                "opportunities": data["opportunities"],
                "stages": dict(data["stages"]),
                "total_count": data["total_count"],
                "total_value": data["total_value"]
            }
        
        return result
    
    async def get_all_sales_owners(self) -> List[Dict]:
        """Get list of all unique sales owners from deals"""
        deals = self.data_loader.get_all_opportunities()
        
        owners = {}
        for deal in deals:
            owner = deal.get("owner")
            if isinstance(owner, dict):
                owner_id = owner.get("id")
                if owner_id and owner_id not in owners:
                    owners[owner_id] = {
                        "id": owner_id,
                        "name": owner.get("display_name") or owner.get("email"),
                        "email": owner.get("email")
                    }
        
        return list(owners.values())
    
    async def get_all_stages(self) -> List[str]:
        """Get list of all unique deal stages"""
        deals = self.data_loader.get_all_opportunities()
        
        stages = set()
        for deal in deals:
            stage_name = deal.get("deal_stage", {}).get("name") if isinstance(deal.get("deal_stage"), dict) else str(deal.get("deal_stage_id", "Unknown"))
            if stage_name and str(stage_name).lower() != 'none':
                stages.add(stage_name)
            else:
                stages.add("Unknown")
        
        return sorted(list(stages))
