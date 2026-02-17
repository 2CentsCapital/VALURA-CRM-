from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from typing import Optional, List
import os
from pathlib import Path

# Using Freshworks API
from app.services.freshworks_service import FreshworksService
from app.services.analytics_service import AnalyticsService

app = FastAPI(
    title="Valura CRM Dashboard",
    description="CRM Dashboard with Freshworks API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with Freshworks API
freshworks_service = FreshworksService()
analytics_service = AnalyticsService(freshworks_service)

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard"""
    dashboard_path = Path(__file__).parent.parent / "static" / "dashboard.html"
    if dashboard_path.exists():
        return FileResponse(dashboard_path)
    return HTMLResponse("<h1>Dashboard not found. Please create static/dashboard.html</h1>")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

# ============================================
# 1. All Contacts
# ============================================
@app.get("/api/contacts")
async def get_all_contacts(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100)
):
    """Get all contacts in tabular format"""
    try:
        contacts = await freshworks_service.get_all_contacts(page=page, per_page=per_page)
        return {
            "success": True,
            "data": contacts.get("contacts", []),
            "meta": contacts.get("meta", {}),
            "page": page,
            "per_page": per_page
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# 2. All Opportunities (Deals)
# ============================================
@app.get("/api/opportunities")
async def get_all_opportunities(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100)
):
    """Get all investment opportunities in tabular format"""
    try:
        opportunities = await freshworks_service.get_all_deals(page=page, per_page=per_page)
        return {
            "success": True,
            "data": opportunities.get("deals", []),
            "meta": opportunities.get("meta", {}),
            "page": page,
            "per_page": per_page
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# 3. Contacts NOT in Opportunities
# ============================================
@app.get("/api/contacts-not-in-opportunities")
async def get_contacts_not_in_opportunities():
    """Get contacts that are not associated with any opportunities"""
    try:
        result = await analytics_service.get_contacts_without_opportunities()
        return {
            "success": True,
            "data": result,
            "count": len(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# 4. Contacts by Source (Referral, Walk-in, Online)
# ============================================
@app.get("/api/contacts-by-source")
async def get_contacts_by_source(source: Optional[str] = None):
    """
    Get contacts grouped by source type (Referral, Walk-in, Online Walk-in)
    Optional: filter by specific source
    """
    try:
        result = await analytics_service.get_contacts_by_source(source_filter=source)
        return {
            "success": True,
            "data": result,
            "breakdown": {
                "referral": len(result.get("referral", [])),
                "walk_in": len(result.get("walk_in", [])),
                "online_walk_in": len(result.get("online_walk_in", [])),
                "other": len(result.get("other", []))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# 5. Opportunities Grouped by Stage
# ============================================
@app.get("/api/opportunities-by-stage")
async def get_opportunities_by_stage(stage: Optional[str] = None):
    """
    Get opportunities grouped by stage
    Optional: filter by specific stage
    """
    try:
        result = await analytics_service.get_opportunities_by_stage(stage_filter=stage)
        return {
            "success": True,
            "data": result,
            "stages": list(result.keys()) if isinstance(result, dict) else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# 6. Leads by Sales Owner
# ============================================
@app.get("/api/leads-by-sales-owner")
async def get_leads_by_sales_owner(owner_id: Optional[int] = None):
    """
    Get leads/opportunities filtered by sales owner with all details
    Optional: filter by specific owner_id
    """
    try:
        result = await analytics_service.get_leads_by_sales_owner(owner_id=owner_id)
        return {
            "success": True,
            "data": result,
            "owners": list(result.keys()) if isinstance(result, dict) else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# 7. Advisor-wise Opportunities and Stages
# ============================================
@app.get("/api/opportunities-by-advisor")
async def get_opportunities_by_advisor(advisor_id: Optional[int] = None):
    """
    Get opportunities grouped by advisor (sales owner) with stage breakdown
    Optional: filter by specific advisor_id
    """
    try:
        result = await analytics_service.get_opportunities_by_advisor(advisor_id=advisor_id)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# Utility Endpoints
# ============================================
@app.get("/api/sales-owners")
async def get_sales_owners():
    """Get list of all sales owners for filtering"""
    try:
        owners = await analytics_service.get_all_sales_owners()
        return {
            "success": True,
            "data": owners
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stages")
async def get_stages():
    """Get list of all opportunity stages"""
    try:
        stages = await analytics_service.get_all_stages()
        return {
            "success": True,
            "data": stages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
