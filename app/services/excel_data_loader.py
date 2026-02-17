import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import json

class ExcelDataLoader:
    """Service to load data from Excel files"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.contacts_file = self.base_path / "Freshsales Contacts.xlsx"
        self.opportunities_file = self.base_path / "Investment Opportunities.xlsx"
        
        # Load data on initialization
        self._contacts_df = None
        self._opportunities_df = None
        self._load_data()
    
    def _load_data(self):
        """Load Excel files into pandas DataFrames"""
        try:
            # Load contacts
            if self.contacts_file.exists():
                self._contacts_df = pd.read_excel(self.contacts_file)
                # Clean column names
                self._contacts_df.columns = self._contacts_df.columns.str.strip()
            
            # Load opportunities
            if self.opportunities_file.exists():
                self._opportunities_df = pd.read_excel(self.opportunities_file)
                # Clean column names
                self._opportunities_df.columns = self._opportunities_df.columns.str.strip()
        except Exception as e:
            print(f"Error loading Excel files: {e}")
    
    def _df_to_dict_list(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Convert DataFrame to list of dictionaries, handling NaN values"""
        if df is None:
            return []
        
        # Replace NaN with None
        df_clean = df.where(pd.notnull(df), None)
        return df_clean.to_dict('records')
    
    def get_contacts(self, page: int = 1, per_page: int = 25) -> Dict[str, Any]:
        """Get paginated contacts"""
        if self._contacts_df is None or len(self._contacts_df) == 0:
            return {"contacts": [], "meta": {"total": 0, "total_pages": 0}}
        
        total = len(self._contacts_df)
        total_pages = (total + per_page - 1) // per_page
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        page_data = self._contacts_df.iloc[start_idx:end_idx]
        contacts = self._df_to_dict_list(page_data)
        
        # Transform to match expected format
        transformed_contacts = []
        for contact in contacts:
            # Handle name field - check multiple variations
            first_name = contact.get("First Name") or contact.get("first_name") or contact.get("FirstName") or ""
            last_name = contact.get("Last Name") or contact.get("last_name") or contact.get("LastName") or ""
            
            # If no first/last name, try to get from "Name" or "Full Name" field
            if not first_name and not last_name:
                full_name = contact.get("Name") or contact.get("Full Name") or contact.get("full_name") or ""
                if full_name:
                    name_parts = str(full_name).split(" ", 1)
                    first_name = name_parts[0] if len(name_parts) > 0 else ""
                    last_name = name_parts[1] if len(name_parts) > 1 else ""
            
            transformed = {
                "id": contact.get("ID") or contact.get("id"),
                "first_name": first_name,
                "last_name": last_name,
                "email": contact.get("Email") or contact.get("email"),
                "mobile_number": contact.get("Mobile Number") or contact.get("mobile_number") or contact.get("Phone"),
                "work_number": contact.get("Work Number") or contact.get("work_number"),
                "company_name": contact.get("Company Name") or contact.get("company_name") or contact.get("Company"),
                "lead_source_id": contact.get("Lead Source") or contact.get("lead_source_id") or contact.get("Source"),
                "medium": contact.get("Medium") or contact.get("medium"),
                "source": contact.get("Source") or contact.get("source") or contact.get("Lead Source"),
                "owner": {
                    "id": contact.get("Owner ID") or contact.get("owner_id"),
                    "display_name": contact.get("Owner") or contact.get("owner") or contact.get("Sales Owner"),
                    "email": contact.get("Owner Email") or contact.get("owner_email")
                }
            }
            transformed_contacts.append(transformed)
        
        return {
            "contacts": transformed_contacts,
            "meta": {
                "total": total,
                "total_pages": total_pages
            }
        }
    
    def get_opportunities(self, page: int = 1, per_page: int = 25) -> Dict[str, Any]:
        """Get paginated opportunities/deals"""
        if self._opportunities_df is None or len(self._opportunities_df) == 0:
            return {"deals": [], "meta": {"total": 0, "total_pages": 0}}
        
        total = len(self._opportunities_df)
        total_pages = (total + per_page - 1) // per_page
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        page_data = self._opportunities_df.iloc[start_idx:end_idx]
        opportunities = self._df_to_dict_list(page_data)
        
        # Transform to match expected format
        transformed_opportunities = []
        for opp in opportunities:
            transformed = {
                "id": opp.get("ID") or opp.get("id") or opp.get("Deal ID"),
                "name": opp.get("Deal Name") or opp.get("name") or opp.get("Name"),
                "amount": opp.get("Amount") or opp.get("amount") or opp.get("Deal Value") or 0,
                "deal_value": opp.get("Deal Value") or opp.get("Amount") or opp.get("amount") or 0,
                "deal_stage_id": opp.get("Deal Stage ID") or opp.get("deal_stage_id") or opp.get("Stage ID"),
                "stage": opp.get("Stage") or opp.get("stage") or opp.get("Deal Stage"),
                "contact_id": opp.get("Contact ID") or opp.get("contact_id"),
                "sales_account_id": opp.get("Sales Account ID") or opp.get("sales_account_id"),
                "created_at": str(opp.get("Created Date") or opp.get("created_at") or opp.get("Created Time") or ""),
                "deal_stage": {
                    "name": opp.get("Stage") or opp.get("stage") or opp.get("Deal Stage") or "Unknown"
                },
                "owner": {
                    "id": opp.get("Owner ID") or opp.get("owner_id"),
                    "display_name": opp.get("Deal Owner") or opp.get("owner") or opp.get("Sales Owner") or opp.get("Owner"),
                    "email": opp.get("Owner Email") or opp.get("owner_email")
                },
                "owner_id": opp.get("Owner ID") or opp.get("owner_id")
            }
            transformed_opportunities.append(transformed)
        
        return {
            "deals": transformed_opportunities,
            "meta": {
                "total": total,
                "total_pages": total_pages
            }
        }
    
    def get_all_contacts(self) -> List[Dict[str, Any]]:
        """Get all contacts without pagination"""
        result = self.get_contacts(page=1, per_page=999999)
        return result["contacts"]
    
    def get_all_opportunities(self) -> List[Dict[str, Any]]:
        """Get all opportunities without pagination"""
        result = self.get_opportunities(page=1, per_page=999999)
        return result["deals"]
    
    def get_contacts_count(self) -> int:
        """Get total number of contacts"""
        return len(self._contacts_df) if self._contacts_df is not None else 0
    
    def get_opportunities_count(self) -> int:
        """Get total number of opportunities"""
        return len(self._opportunities_df) if self._opportunities_df is not None else 0
