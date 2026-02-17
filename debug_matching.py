"""
Debug script to check contact-deal matching
"""
import asyncio
import sys
sys.path.insert(0, 'c:\\Users\\gupta\\Desktop\\AA_Valura_AI\\VALURA-CRM')

from app.services.freshworks_service import FreshworksService
from app.services.analytics_service import AnalyticsService

async def debug_matching():
    freshworks = FreshworksService()
    analytics = AnalyticsService(freshworks)
    
    print("Fetching all contacts...")
    contacts = await freshworks.get_all_contacts_paginated()
    print(f"Total contacts: {len(contacts)}")
    
    print("\nFetching all deals...")
    deals = await freshworks.get_all_deals_paginated()
    print(f"Total deals: {len(deals)}")
    
    # Build deal names set
    deal_names = set()
    for deal in deals:
        if deal.get("name"):
            deal_name = deal["name"].strip().lower()
            deal_names.add(deal_name)
    
    print(f"\nUnique deal names: {len(deal_names)}")
    
    # Show first 5 deal names
    print("\nFirst 5 deal names:")
    for i, name in enumerate(sorted(deal_names)[:5]):
        print(f"  {i+1}. {name}")
    
    # Check contact names
    contact_names = set()
    for contact in contacts:
        first = contact.get("first_name", "")
        last = contact.get("last_name", "")
        full = f"{first} {last}".strip()
        if full:
            contact_names.add(full.lower())
    
    print(f"\nUnique contact names: {len(contact_names)}")
    
    # Find matches
    matches = contact_names & deal_names
    print(f"\nMatching names (contact name = deal name): {len(matches)}")
    
    # Show first 5 matches
    print("\nFirst 5 matches:")
    for i, name in enumerate(sorted(matches)[:5]):
        print(f"  {i+1}. {name}")
    
    # Contacts without deals
    print("\n\nCalling get_contacts_without_opportunities...")
    contacts_without_deals = await analytics.get_contacts_without_opportunities()
    print(f"Contacts without deals: {len(contacts_without_deals)}")
    
    # Show first 5
    print("\nFirst 5 contacts without deals:")
    for i, contact in enumerate(contacts_without_deals[:5]):
        first = contact.get("first_name", "")
        last = contact.get("last_name", "")
        email = contact.get("email", "")
        print(f"  {i+1}. {first} {last} ({email})")

if __name__ == "__main__":
    asyncio.run(debug_matching())
