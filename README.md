# Valura CRM Dashboard

A comprehensive CRM dashboard with FastAPI backend and interactive UI. **Currently using hardcoded Excel data** with future Freshworks CRM API integration planned.

## 🎯 Quick Start

1. **Run Setup:**
   ```bash
   setup.bat
   ```

2. **Start Server:**
   ```bash
   run.bat
   ```

3. **Open Dashboard:**
   - Visit: http://127.0.0.1:8000

**That's it!** No API configuration needed - works directly with Excel files.

## 📊 Data Source

Currently reading from:
- **Freshsales Contacts.xlsx**
- **Investment Opportunities.xlsx**

## Features

✨ **7 Interactive Dashboard Views:**
1. **All Contacts** - View all contacts in tabular format
2. **Investment Opportunities** - View all investment opportunities/deals
3. **Contacts Breakout** - Identify contacts not associated with any opportunities
4. **Referral & Walk-ins** - Breakdown of contacts by source type (Referral, Walk-in, Online Walk-in)
5. **Grouping by Stage** - Opportunities grouped by pipeline stage
6. **Sales Owner View** - Leads filtered by sales owner with complete details
7. **Advisor Analysis** - Advisor-wise opportunities with stage breakdown

## API Endpoints

### Core Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Main dashboard UI |
| GET | `/health` | Health check |
| GET | `/api/contacts` | List all contacts (paginated) |
| GET | `/api/opportunities` | List all opportunities/deals (paginated) |

### Analytics Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/contacts-not-in-opportunities` | Contacts without any opportunities |
| GET | `/api/contacts-by-source` | Contacts grouped by source type |
| GET | `/api/opportunities-by-stage` | Opportunities grouped by stage |
| GET | `/api/leads-by-sales-owner` | Leads filtered by sales owner |
| GET | `/api/opportunities-by-advisor` | Advisor-wise opportunities with stages |
| GET | `/api/sales-owners` | List all sales owners |
| GET | `/api/stages` | List all opportunity stages |

### Query Parameters

- **Paginated endpoints** (`/api/contacts`, `/api/opportunities`):
  - `page` (int): Page number (default: 1)
  - `per_page` (int): Results per page (default: 25, max: 100)

- **Filter endpoints**:
  - `source` (string): Filter by specific source type
  - `stage` (string): Filter by specific stage
  - `owner_id` (int): Filter by sales owner ID
  - `advisor_id` (int): Filter by advisor ID

## Dashboard Features

### 1. All Contacts
- Displays all contacts in a clean, sortable table
- Shows ID, Name, Email, Phone, Company, and Owner
- Pagination support
- Real-time data from Freshworks CRM

### 2. Investment Opportunities
- Lists all deals/opportunities
- Shows amount, stage, owner, and creation date
- Calculates total value statistics
- Pagination support

### 3. Contacts Breakout
- Identifies contacts NOT associated with any opportunities
- Helps find potential new sales targets
- Shows count of unengaged contacts

### 4. Referral & Walk-ins Analysis
- Groups contacts by source: Referral, Walk-in, Online Walk-in
- Provides breakdown statistics
- Shows detailed tables for each source type

### 5. Grouping by Stage
- Groups opportunities by pipeline stage
- Shows count and total value per stage
- Helps visualize sales pipeline

### 6. Sales Owner View
- Filters leads by sales owner
- Shows total count and value per owner
- Displays all lead details per owner

### 7. Advisor Analysis
- Shows opportunities grouped by advisor
- Provides stage breakdown for each advisor
- Displays total count, value, and active stages
- Lists recent opportunities per advisor

## Technology Stack

- **Backend:** FastAPI (Python)
- **Data Source:** Excel files (pandas + openpyxl) - API integration coming soon
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **HTTP Client:** HTTPX (async)
- **Environment:** python-dotenv

## Project Structure

```
VALURA-CRM/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application & endpoints
│   └── services/
│       ├── __init__.py
│       ├── excel_data_loader.py         # Excel file reader (current)
│       ├── analytics_service_excel.py   # Analytics for Excel data (current)
│       ├── freshworks_service.py        # Freshworks API (future)
│       └── analytics_service.py         # Analytics for API (future)
├── static/
│   └── dashboard.html                   # Interactive dashboard UI
├── Freshsales Contacts.xlsx             # Contact data source
├── Investment Opportunities.xlsx        # Opportunities data source
├── .env.example                         # Example environment configuration
├── .gitignore
├── requirements.txt                     # Python dependencies
├── setup.bat                            # Windows setup script
├── run.bat                              # Windows run script
└── README.md
```

## API Usage Examples

### Get All Contacts
```bash
curl http://127.0.0.1:8000/api/contacts?page=1&per_page=25
```

### Get Opportunities by Stage
```bash
curl http://127.0.0.1:8000/api/opportunities-by-stage
```

### Get Leads by Specific Sales Owner
```bash
curl http://127.0.0.1:8000/api/leads-by-sales-owner?owner_id=123
```

## Development

### Run in Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access API Documentation
Once the server is running:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Notes

- The dashboard uses modern CSS with gradient designs and responsive tables
- All data is fetched asynchronously for better performance
- Pagination is implemented for large datasets
- Each view provides statistics and breakdowns
- The UI is fully responsive and mobile-friendly

## Freshworks API Reference

The application uses the Freshworks CRM API with the following pattern:
- Base URL: `https://{DOMAIN}.myfreshworks.com/crm/sales/api`
- Authentication: `Authorization: Token token={API_KEY}`
- Endpoints: `/contacts`, `/deals`

For more info, visit: https://developers.freshworks.com/crm/api/

---

**Valura CRM Dashboard** - Built with ❤️ using FastAPI 
