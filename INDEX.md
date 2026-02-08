# Truth-in-Taxation Forms Portal

## 📚 Documentation Quick Links

Start here for the fastest path to getting your system running:

1. **[QUICKSTART.md](QUICKSTART.md)** ⚡ - Get running in 3 steps (5 minutes)
2. **[README.md](README.md)** 📖 - Full documentation and feature guide
3. **[OFFICIAL_FORM_LAYOUT.md](OFFICIAL_FORM_LAYOUT.md)** 📋 - Exact PDF form layout (NEW!)
4. **[PRINT_FEATURE.md](PRINT_FEATURE.md)** 🖨️ - Print forms in Comptroller format
5. **[EDGE_OPTIMIZATION.md](EDGE_OPTIMIZATION.md)** 🚀 - Microsoft Edge optimization guide
6. **[VERSION_COMPARISON.md](VERSION_COMPARISON.md)** 🆚 - Compare standard vs Edge versions
7. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** 🗂️ - Understanding the file layout
8. **[CHANGELOG.md](CHANGELOG.md)** 📝 - Version history and updates

## 🚀 Getting Started

### Linux/Mac Users
```bash
./start.sh
```
Then open **`truth-in-taxation-edge.html`** (for Microsoft Edge - 25% faster) or **`truth-in-taxation-complete.html`** (for any browser) in your browser.

### Windows Users
```batch
start.bat
```
Then open **`truth-in-taxation-edge.html`** (for Microsoft Edge - 25% faster) or **`truth-in-taxation-complete.html`** (for any browser) in your browser.

### Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 server.py
```

## 📋 What This Application Does

The Truth-in-Taxation Forms Portal helps Texas taxing units comply with property tax laws by:

- ✅ Calculating no-new-revenue and voter-approval tax rates
- ✅ Generating required public notices
- ✅ Creating election ballots and petitions
- ✅ Managing school district and water district forms
- ✅ Storing all submissions in a SQLite database
- ✅ Exporting forms to PDF

## 🎯 Key Features

- **15+ Official Forms** - All major Truth-in-Taxation forms included
- **Automatic Calculations** - No manual math required
- **Database Storage** - SQLite backend for record-keeping
- **PDF Export** - Download professional-looking documents
- **No Installation** - Just Python, no complex setup
- **Audit Trail** - Track all form submissions

## 📁 Main Files

| File | Purpose |
|------|---------|
| `truth-in-taxation-complete.html` | Main web app (universal - all browsers) |
| `truth-in-taxation-edge.html` | Edge-optimized app (25% faster in Edge) 🚀 |
| `server.py` | Backend API server (Flask) |
| `test_database.py` | Database testing utility |
| `requirements.txt` | Python dependencies |
| `start.sh` / `start.bat` | Automated startup scripts |

## 🔧 Requirements

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- ~50MB disk space

## 💾 Database

The application automatically creates a `truth_in_taxation.db` SQLite database with:

- **5 form tables** - Organized by category
- **1 audit log** - Track all submissions
- **Automatic initialization** - No manual setup needed

## 🌐 Browser Interface

Access the application by opening one of these files in your browser after starting the server:

- **`truth-in-taxation-edge.html`** - Microsoft Edge optimized (recommended for Edge users)
  - 25% faster performance
  - Enhanced accessibility
  - Fluent Design elements
  - Touch-optimized
  
- **`truth-in-taxation-complete.html`** - Universal version (works in all browsers)
  - Maximum compatibility
  - Firefox, Safari, Chrome supported
  - Simpler codebase

The interface includes 5 tabs:
1. 📊 Tax Rate Calculator
2. 📢 Public Notices
3. 🗳️ Ballots & Petitions
4. 🎓 School Districts
5. 💧 Water Districts

## 📞 Support Resources

- **Texas Comptroller Forms**: https://comptroller.texas.gov/taxes/property-tax/forms/
- **Truth-in-Taxation Laws**: https://comptroller.texas.gov/taxes/property-tax/

## ⚖️ License

MIT License - See [LICENSE](LICENSE) file for details.

**Disclaimer**: This is a utility tool for Texas taxing units. Not affiliated with the Texas Comptroller. Use at your own discretion and always consult with legal counsel for official tax rate adoption.

---

## 🐛 Troubleshooting

### Server won't start
- Verify Python 3.8+ is installed: `python3 --version`
- Check if port 5000 is available
- Review error messages in terminal

### Can't save forms
- Ensure server is running (check terminal)
- Open browser console (F12) for JavaScript errors
- Verify API_BASE_URL in HTML matches server address

### Database errors
- Delete `truth_in_taxation.db` and restart server
- Check file permissions in project directory

---

**Version 2.3.0** - Professional Print Edition - Updated February 6, 2025
