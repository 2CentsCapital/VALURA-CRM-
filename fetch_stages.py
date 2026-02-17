"""
Script to fetch and display deal pipeline stages from Freshworks CRM
"""
import asyncio
import httpx
import json
from dotenv import load_dotenv
import os

load_dotenv()

async def fetch_stages():
    domain = os.getenv("FRESHWORKS_DOMAIN")
    api_key = os.getenv("FRESHWORKS_API_KEY")
    
    url = f"https://{domain}.myfreshworks.com/crm/sales/api/deal_pipelines"
    headers = {
        "Authorization": f"Token token={api_key}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
response = await client.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
        
        if response.status_code != 200:
            print(f"\nError: {response.status_code}")
            return
            
        data = response.json()
        
        print("\n=== DEAL PIPELINES AND STAGES ===\n")
        
        for pipeline in data.get("deal_pipelines", []):
            print(f"\nPipeline: {pipeline['name']} (ID: {pipeline['id']})")
            print("-" * 60)
            
            for stage in pipeline.get("deal_stages", []):
                print(f"  Stage: {stage['name']:30} | ID: {stage['id']}")
        
        # Save as Python dict for easy integration
        print("\n\n=== STAGE MAP FOR CODE ===\n")
        print("stage_map = {")
        for pipeline in data.get("deal_pipelines", []):
            for stage in pipeline.get("deal_stages", []):
                print(f"    {stage['id']}: \"{stage['name']}\",")
        print("}")

if __name__ == "__main__":
    asyncio.run(fetch_stages())
