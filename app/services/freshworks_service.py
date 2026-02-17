import httpx
import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class FreshworksService:
    """Service to interact with Freshworks CRM API"""
    
    def __init__(self):
        self.domain = os.getenv("FRESHWORKS_DOMAIN")
        self.api_key = os.getenv("FRESHWORKS_API_KEY")
        self.contacts_view_id = os.getenv("CONTACTS_VIEW_ID", "402014829835")
        self.deals_view_id = os.getenv("DEALS_VIEW_ID", "402014829847")
        
        if not self.domain or not self.api_key:
            raise ValueError("FRESHWORKS_DOMAIN and FRESHWORKS_API_KEY must be set in environment")
        
        self.base_url = f"https://{self.domain}.myfreshworks.com/crm/sales/api"
        self.headers = {
            "Authorization": f"Token token={self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        """Make HTTP request to Freshworks API"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params or {},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_all_contacts(
        self, 
        page: int = 1, 
        per_page: int = 25,
        view_id: Optional[int] = None,
        include: str = "owner"
    ) -> Dict:
        """
        Get all contacts from Freshworks CRM
        
        Args:
            page: Page number
            per_page: Results per page
            view_id: Optional view ID to filter contacts
            include: Additional fields to include (e.g., 'owner')
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        # Use the configured view ID or the provided one
        if view_id:
            endpoint = f"contacts/view/{view_id}"
        else:
            endpoint = f"contacts/view/{self.contacts_view_id}"
        
        return await self._make_request(endpoint, params)
    
    async def get_all_deals(
        self,
        page: int = 1,
        per_page: int = 25,
        view_id: Optional[int] = None,
        include: str = "owner"
    ) -> Dict:
        """
        Get all deals (opportunities) from Freshworks CRM
        
        Args:
            page: Page number
            per_page: Results per page
            view_id: Optional view ID to filter deals
            include: Additional fields to include (e.g., 'owner')
        """
        params = {
            "page": page,
            "per_page": per_page,
            "sort": "amount",
            "include": include
        }
        
        # Use the configured view ID or the provided one
        if view_id:
            endpoint = f"deals/view/{view_id}"
        else:
            endpoint = f"deals/view/{self.deals_view_id}"
        
        result = await self._make_request(endpoint, params)
        
        # Map users to dealers
        users = result.get("users", [])
        deals = result.get("deals", [])
        
        # Create owner lookup dict
        owner_map = {user["id"]: user for user in users}
        
        # Add owner object to each deal
        for deal in deals:
            owner_id = deal.get("owner_id")
            if owner_id and owner_id in owner_map:
                deal["owner"] = owner_map[owner_id]
            
            # Add basic stage mapping (common stages)
            stage_id = deal.get("deal_stage_id")
            if stage_id:
                # Create a basic stage object
                # You may want to fetch these from /api/deal_pipelines for actual names
                deal["deal_stage"] = {
                    "id": stage_id,
                    "name": self._get_stage_name(stage_id)
                }
        
        return result
    
    async def get_contact_by_id(self, contact_id: int, include: str = "owner") -> Dict:
        """Get a specific contact by ID"""
        return await self._make_request(f"contacts/{contact_id}", {"include": include})
    
    async def get_deal_by_id(self, deal_id: int, include: str = "owner,contact") -> Dict:
        """Get a specific deal by ID"""
        return await self._make_request(f"deals/{deal_id}", {"include": include})
    
    async def get_all_contacts_paginated(self, max_pages: int = 100) -> List[Dict]:
        """
        Get all contacts across multiple pages
        
        Args:
            max_pages: Maximum number of pages to fetch
        """
        all_contacts = []
        page = 1
        
        while page <= max_pages:
            result = await self.get_all_contacts(page=page, per_page=100)
            contacts = result.get("contacts", [])
            
            if not contacts:
                break
            
            all_contacts.extend(contacts)
            
            # Check if there are more pages
            meta = result.get("meta", {})
            total_pages = meta.get("total_pages", 1)
            
            if page >= total_pages:
                break
            
            page += 1
        
        return all_contacts
    
    async def get_all_deals_paginated(self, max_pages: int = 100) -> List[Dict]:
        """
        Get all deals across multiple pages
        
        Args:
            max_pages: Maximum number of pages to fetch
        """
        all_deals = []
        page = 1
        
        while page <= max_pages:
            result = await self.get_all_deals(page=page, per_page=100)
            deals = result.get("deals", [])
            
            if not deals:
                break
            
            all_deals.extend(deals)
            
            # Check if there are more pages
            meta = result.get("meta", {})
            total_pages = meta.get("total_pages", 1)
            
            if page >= total_pages:
                break
            
            page += 1
        
        return all_deals
    
    def _get_stage_name(self, stage_id: int) -> str:
        """
        Map stage_id to stage name.
        Common stages for a CRM pipeline
        """
        stage_map = {
            # Update these IDs based on your actual Freshworks setup
            402001815652: "Closed Won",
            402001815651: "Closed Lost",
            402001821236: "Account Not Funded",
            402001842536: "Account Funded",
            402001815650: "KYC Created",
            402001815649: "Proposal Sent",
            402001815648: "Qualified",
            402001815647: "Contact Made",
            402001815646: "New Lead",
        }
        return stage_map.get(stage_id, f"Stage {stage_id}")
