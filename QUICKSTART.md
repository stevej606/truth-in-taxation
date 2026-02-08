# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
# Option A: Use the startup script (recommended)
./start.sh

# Option B: Manual installation
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
# If using startup script (from Step 1)
# Server is already running!

# If manual installation
python3 server.py
```

You should see:
```
Starting Truth-in-Taxation API Server...
Database location: /path/to/truth_in_taxation.db
Database initialized successfully
 * Running on http://0.0.0.0:5000
```

### Step 3: Open the Application

Open `truth-in-taxation-complete.html` in your web browser:
- Double-click the file, or
- Right-click → Open With → Your Browser

## 📋 What's Included

- **Tax Rate Calculator** - Calculate no-new-revenue and voter-approval rates
- **Public Notices** - Generate required public hearing notices
- **Ballots & Petitions** - Create election ballots
- **School District Forms** - Special forms for school districts
- **Water District Forms** - Forms for water districts
- **Database Storage** - All forms automatically saved to SQLite
- **PDF Export** - Download forms as PDF documents

## 🔧 Troubleshooting

### Server won't start?
- Make sure Python 3.8+ is installed: `python3 --version`
- Check if port 5000 is available
- Try a different port by editing `server.py` (change last line)

### Can't save forms?
- Check that the server is running (green terminal output)
- Look for errors in the browser console (F12)
- Verify the API_BASE_URL in the HTML file matches your server

### Need to reset the database?
```bash
rm truth_in_taxation.db
python3 server.py  # Will recreate the database
```

## 📚 Full Documentation

See `README.md` for complete documentation including:
- Detailed API documentation
- Database schema
- Security considerations
- Customization options
- Production deployment guide

## 🆘 Support

For Texas Comptroller forms and official guidance:
- [Texas Comptroller Property Tax Forms](https://comptroller.texas.gov/taxes/property-tax/forms/)
- [Truth-in-Taxation Laws](https://comptroller.texas.gov/taxes/property-tax/)
