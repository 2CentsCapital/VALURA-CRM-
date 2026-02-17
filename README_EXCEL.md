# Valura CRM Dashboard - Excel Data Mode

A comprehensive CRM dashboard with FastAPI backend and interactive UI using **hardcoded Excel data**. Features include tabular data visualization, analytics, and multi-view reporting.

## 🎯 Current Status

✅ **Using Excel Files for Data** - Currently reading from hardcoded Excel files
⏳ **API Integration Coming Soon** - Freshworks API will be integrated later

## 📁 Data Sources

The dashboard reads data from these Excel files:
- **Freshsales Contacts.xlsx** - All contact information
- **Investment Opportunities.xlsx** - All opportunities/deals data

## Features

✨ **7 Interactive Dashboard Views:**
1. **All Contacts** - View all contacts in tabular format
2. **Investment Opportunities** - View all investment opportunities/deals
3. **Contacts Breakout** - Identify contacts not associated with any opportunities
4. **Referral & Walk-ins** - Breakdown of contacts by source type (Referral, Walk-in, Online Walk-in)
5. **Grouping by Stage** - Opportunities grouped by pipeline stage
6. **Sales Owner View** - Leads filtered by sales owner with complete details
7. **Advisor Analysis** - Advisor-wise opportunities with stage breakdown

## Quick Start

### 1. Run Setup
```bash
setup.bat
```

This will:
- Check for Python installation
- Create a virtual environment
- Install all dependencies (pandas, openpyxl, FastAPI, etc.)

### 2. Start the Server
```bash
run.bat
```

### 3. Access the Dashboard
Open your browser and navigate to:
- **Dashboard:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8000/docs

That's it! No API configuration needed - it works directly with the Excel files.

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

## Dashboard Features

### 1. All Contacts
- Displays all contacts from Excel in a clean, sortable table
- Shows ID, Name, Email, Phone, Company, and Owner
- Pagination support for easy navigation

### 2. Investment Opportunities
- Lists all deals/opportunities from Excel
- Shows amount, stage, owner, and creation date
- Calculates total value statistics automatically

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
- **Data Source:** Excel files (pandas + openpyxl)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **HTTP Client:** HTTPX (async)

## Project Structure

```
VALURA-CRM/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application & endpoints
│   └── services/
│       ├── __init__.py
│       ├── excel_data_loader.py         # Excel file reader
│       ├── analytics_service_excel.py   # Analytics for Excel data
│       ├── freshworks_service.py        # (For future API use)
│       └── analytics_service.py         # (For future API use)
├── static/
│   └── dashboard.html                   # Interactive dashboard UI
├── Freshsales Contacts.xlsx             # Contact data
├── Investment Opportunities.xlsx        # Opportunities data
├── setup.bat                            # Setup script
├── run.bat                              # Run server script
├── requirements.txt                     # Python dependencies
└── README.md
```

## Excel File Format

### Expected Columns in Freshsales Contacts.xlsx:
- ID, First Name, Last Name, Email
- Mobile Number, Work Number, Phone
- Company Name, Company
- Lead Source, Source, Medium
- Owner, Sales Owner, Owner ID, Owner Email

### Expected Columns in Investment Opportunities.xlsx:
- ID, Deal ID, Deal Name, Name
- Amount, Deal Value
- Stage, Deal Stage, Deal Stage ID
- Contact ID, Sales Account ID
- Deal Owner, Owner, Owner ID, Owner Email
- Created Date, Created Time

**Note:** The system is flexible and will map common column name variations automatically.

## Development

### Run in Development Mode
```bash
# Activate virtual environment
venv\Scripts\activate

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Update Excel Data
Simply replace the Excel files with updated versions and refresh the browser. The data will be reloaded automatically on each API call.

## Future Enhancements

🔄 **Coming Soon:**
- [ ] Freshworks CRM API integration
- [ ] Real-time data sync
- [ ] Data export to Excel/CSV
- [ ] Advanced filtering and search
- [ ] Data visualization charts
- [ ] User authentication

## Notes

- ✅ No API configuration needed
- ✅ Works offline with local Excel files
- ✅ Fast data loading with pandas
- ✅ Automatic column name mapping
- ✅ Responsive design, mobile-friendly
- ✅ Beautiful gradient UI with modern CSS

## Troubleshooting

### Server won't start
- Check if Python is installed: `python --version`
- Ensure virtual environment is activated
- Run `setup.bat` if dependencies are missing

### No data showing
- Verify Excel files are present in the root directory
- Check file names: `Freshsales Contacts.xlsx` and `Investment Opportunities.xlsx`
- Ensure Excel files are not open in another program

### Excel read errors
- Make sure Excel files are in `.xlsx` format (not `.xls`)
- Check that files are not corrupted
- Verify column names match expected format

---

**Valura CRM Dashboard** - Built with ❤️ using FastAPI & Pandas
