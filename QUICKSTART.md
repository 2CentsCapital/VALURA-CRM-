# Quick Start Guide - Valura CRM Dashboard

## Prerequisites
- Python 3.8 or higher installed
- Freshworks CRM account with API access
- Your Freshworks domain and API key

## Step-by-Step Setup

### 1. Configure Environment Variables
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your credentials:
# FRESHWORKS_DOMAIN=yourcompany
# FRESHWORKS_API_KEY=your_api_key_here
```

### 2. Run Setup Script (Windows)
```bash
setup.bat
```

Or manually:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start the Server
```bash
# Option 1: Use the run script
run.bat

# Option 2: Manual start
venv\Scripts\activate
uvicorn app.main:app --reload
```

### 4. Access the Dashboard
Open your browser and navigate to:
- **Dashboard:** http://127.0.0.1:8000
- **API Docs (Swagger):** http://127.0.0.1:8000/docs

## Dashboard Views

Click on any button in the dashboard to view:

1. **📇 All Contacts** - Complete contact database
2. **💼 Investment Opportunities** - All deals/opportunities
3. **🔍 Contacts Breakout** - Contacts without opportunities
4. **📊 Referral & Walk-ins** - Source-based breakdown
5. **📈 Grouping by Stage** - Pipeline stage analysis
6. **👤 Sales Owner View** - Owner-based lead filtering
7. **🎓 Advisor Analysis** - Advisor performance with stages

## API Endpoints

All endpoints are accessible via REST API:

```bash
# Get all contacts
GET http://127.0.0.1:8000/api/contacts

# Get all opportunities
GET http://127.0.0.1:8000/api/opportunities

# Get contacts not in opportunities
GET http://127.0.0.1:8000/api/contacts-not-in-opportunities

# Get contacts by source
GET http://127.0.0.1:8000/api/contacts-by-source

# Get opportunities by stage
GET http://127.0.0.1:8000/api/opportunities-by-stage

# Get leads by sales owner
GET http://127.0.0.1:8000/api/leads-by-sales-owner

# Get opportunities by advisor
GET http://127.0.0.1:8000/api/opportunities-by-advisor
```

## Features

✅ **Real-time Data** - Fetches live data from Freshworks CRM
✅ **Interactive Tables** - Sortable, filterable tabular views
✅ **Statistics** - Auto-calculated counts, totals, and breakdowns
✅ **Responsive Design** - Works on desktop, tablet, and mobile
✅ **Multiple Views** - 7 different analytical perspectives
✅ **Pagination Support** - Handles large datasets efficiently
✅ **API Documentation** - Built-in Swagger UI

## Troubleshooting

### Server won't start
- Check if Python is installed: `python --version`
- Ensure virtual environment is activated
- Check if port 8000 is available

### No data showing
- Verify .env file has correct credentials
- Check Freshworks API key is valid
- Ensure your Freshworks domain is correct
- Check API rate limits

### Connection errors
- Verify internet connection
- Check firewall settings
- Ensure Freshworks API is accessible

## Next Steps

- Customize the dashboard colors and styling in `static/dashboard.html`
- Add additional filters and views as needed
- Export data to Excel or CSV
- Integrate with other systems via the REST API

## Support

For issues or questions:
1. Check the API documentation at http://127.0.0.1:8000/docs
2. Review Freshworks API docs: https://developers.freshworks.com/crm/api/
3. Check server logs for error messages

---

Enjoy using Valura CRM Dashboard! 🚀
