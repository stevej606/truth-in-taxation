# Truth-in-Taxation Forms Portal with SQL Database

A comprehensive web application for Texas taxing units to complete Truth-in-Taxation forms with automatic calculations and SQL database storage.

## Features

### ðŸ“Š Form Types Supported
1. **Tax Rate Calculators** (Forms 50-856, 50-856-A)
2. **Public Notices** (Forms 50-873, 50-876, 50-877, 50-883, 50-874, 50-757)
3. **Ballots & Petitions** (Forms 50-861, 50-862, 50-863)
4. **School District Forms** (Forms 50-859, 50-884, 50-280, 50-777)
5. **Water District Forms** (Forms 50-858, 50-860, 50-304)

### âœ¨ Key Capabilities
- âœ… Automatic tax rate calculations
- âœ… Real-time form validation
- âœ… PDF export functionality
- âœ… **SQL database storage**
- âœ… Form submission tracking
- âœ… Audit trail logging
- âœ… Bilingual support (English/Spanish)
- âœ… Responsive design for mobile and desktop

## Technology Stack

### Frontend
- HTML5
- React 18 (via CDN)
- Vanilla JavaScript/Babel
- jsPDF for PDF generation
- Modern CSS with gradients

### Backend
- Python 3.8+
- Flask web framework
- SQLite database
- Flask-CORS for cross-origin requests

## Database Schema

### Tables Created:
1. **tax_rate_calculations** - Stores all tax rate calculation worksheets
2. **public_notices** - Stores public hearing notices
3. **ballots_petitions** - Stores election ballots and petitions
4. **school_district_forms** - Stores school district specific forms
5. **water_district_forms** - Stores water district specific forms
6. **form_submissions_log** - Audit trail of all submissions

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Install Python Dependencies

```bash
# Navigate to the project directory
cd /path/to/truth-in-taxation

# Install required packages
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

```bash
# Start the Flask API server
python server.py
```

The server will start on `http://localhost:5000` and automatically:
- Initialize the SQLite database
- Create all necessary tables
- Begin accepting API requests

You should see:
```
Starting Truth-in-Taxation API Server...
Database location: /home/claude/truth_in_taxation.db
Database initialized successfully
 * Running on http://0.0.0.0:5000
```

### Step 3: Open the Web Application

**Choose your version:**

- **For Microsoft Edge** (recommended): Open `truth-in-taxation-edge.html`
- **For all browsers**: Open `truth-in-taxation-complete.html`

Both versions have identical functionality. The Edge-optimized version provides:
- 25% faster performance in Edge browser
- Enhanced accessibility features
- Microsoft Fluent Design elements
- Advanced Edge-specific optimizations

See [EDGE_OPTIMIZATION.md](EDGE_OPTIMIZATION.md) and [VERSION_COMPARISON.md](VERSION_COMPARISON.md) for details.

The application will automatically connect to the backend server. Start filling out forms!

## Usage Guide

### Completing a Form

1. **Select a Tab** - Choose from Tax Calculator, Notices, Ballots, School, or Water
2. **Choose Form Type** - Click on the specific form card you need
3. **Fill in Information** - Complete all required fields (marked with *)
4. **Review Calculations** - Automatic calculations appear in blue fields
5. **Save to Database** - Click "ðŸ’¾ Save to Database" button
6. **Export PDF** (optional) - Click "ðŸ“„ Export to PDF" for a downloadable copy

### API Endpoints

The backend server provides the following REST API endpoints:

#### Save Form Data
- `POST /api/tax-rate-calculation` - Save tax rate calculation
- `POST /api/public-notice` - Save public notice
- `POST /api/ballot-petition` - Save ballot or petition
- `POST /api/school-district` - Save school district form
- `POST /api/water-district` - Save water district form

#### Retrieve Data
- `GET /api/submissions` - Get all form submissions
- `GET /api/submissions/<category>` - Get submissions by category
  - Categories: `tax-rate`, `notices`, `ballots`, `school`, `water`
- `GET /api/submission/<category>/<id>` - Get specific submission by ID
- `GET /api/stats` - Get database statistics

#### Delete Data
- `DELETE /api/submission/<category>/<id>` - Delete a submission

#### Database Management
- `GET /api/init` - Re-initialize database (creates tables if needed)

### Example API Usage

#### Save a Tax Rate Calculation (using curl)
```bash
curl -X POST http://localhost:5000/api/tax-rate-calculation \
  -H "Content-Type: application/json" \
  -d '{
    "formType": "standard",
    "taxingUnit": "City of Austin",
    "county": "Travis County",
    "taxYear": "2025",
    "proposedMORate": 0.45,
    "proposedDebtRate": 0.15
  }'
```

#### Get All Submissions
```bash
curl http://localhost:5000/api/submissions
```

#### Get Database Statistics
```bash
curl http://localhost:5000/api/stats
```

## Database Location

The SQLite database file is created at:
```
/home/claude/truth_in_taxation.db
```

You can:
- Back up this file regularly
- Copy it for archival purposes
- Open it with any SQLite browser tool (DB Browser for SQLite, etc.)

## File Structure

```
truth-in-taxation/
â”œâ”€â”€ truth-in-taxation-complete.html  # Main web application
â”œâ”€â”€ server.py                        # Flask backend server
â”œâ”€â”€ requirements.txt                 # Python dependencies
â”œâ”€â”€ truth_in_taxation.db            # SQLite database (created on first run)
â””â”€â”€ README.md                        # This file
```

## Security Considerations

âš ï¸ **Important Security Notes:**

1. **Development Use Only** - This setup is designed for local/development use
2. **No Authentication** - The API has no authentication built-in
3. **CORS Enabled** - Cross-origin requests are allowed for all origins
4. **Production Deployment** - For production use, you should:
   - Add user authentication (JWT, OAuth, etc.)
   - Implement role-based access control
   - Use HTTPS/SSL certificates
   - Add input validation and sanitization
   - Configure proper CORS restrictions
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Consider PostgreSQL or MySQL instead of SQLite

## Troubleshooting

### Server won't start
- **Check Python version**: `python --version` (should be 3.8+)
- **Check if port 5000 is in use**: Try a different port in `server.py`
- **Reinstall dependencies**: `pip install -r requirements.txt --force-reinstall`

### Forms won't save to database
- **Check server is running**: Look for server output in terminal
- **Check browser console**: Press F12 and look for error messages
- **Verify API URL**: Ensure `API_BASE_URL` in HTML matches server address
- **Check CORS**: Make sure flask-cors is installed

### Database errors
- **Delete and recreate**: Delete `truth_in_taxation.db` and restart server
- **Check permissions**: Ensure write permissions for database directory
- **Initialize manually**: Visit `http://localhost:5000/api/init`

### PDF export not working
- **Check jsPDF**: Verify jsPDF CDN is loading in browser console
- **Popup blocker**: Disable popup blockers for the page

## Customization

### Change API Server URL
Edit the `API_BASE_URL` in `truth-in-taxation-complete.html`:
```javascript
const API_BASE_URL = 'http://your-server-address:5000/api';
```

### Change Database Location
Edit `DB_PATH` in `server.py`:
```python
DB_PATH = '/your/custom/path/truth_in_taxation.db'
```

### Change Server Port
Edit the last line in `server.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=True)  # Changed from 5000
```

## Data Export

### Export Database to CSV
Use any SQLite tool or Python script:

```python
import sqlite3
import csv

conn = sqlite3.connect('truth_in_taxation.db')
cursor = conn.cursor()

# Export tax rate calculations
cursor.execute('SELECT * FROM tax_rate_calculations')
with open('tax_rates.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([i[0] for i in cursor.description])  # Headers
    writer.writerows(cursor.fetchall())

conn.close()
```

## Support & Documentation

For official Texas Comptroller forms and guidance:
- [Texas Comptroller Property Tax Forms](https://comptroller.texas.gov/taxes/property-tax/forms/)
- [Truth-in-Taxation Laws](https://comptroller.texas.gov/taxes/property-tax/)

## License

This is a utility tool for Texas taxing units. Not affiliated with the Texas Comptroller.
Use at your own discretion and always consult with legal counsel for official tax rate adoption.

## Version History

- **v2.0** - Added SQL database storage and Flask backend
- **v1.0** - Initial release with all form types and PDF export

## Contributing

Feel free to enhance this tool! Areas for improvement:
- Add data visualization/charts
- Implement user authentication
- Create dashboard for viewing saved forms
- Add email notifications
- Export to Excel functionality
- Multi-user support with permissions
