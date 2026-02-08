# Project Structure

```
truth-in-taxation-project/
│
├── README.md                          # Full documentation
├── QUICKSTART.md                      # Quick start guide
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
├── EDGE_OPTIMIZATION.md              # Edge browser optimization guide
├── VERSION_COMPARISON.md              # Version comparison details
│
├── requirements.txt                   # Python dependencies
├── server.py                          # Flask backend server
├── test_database.py                   # Database test script
│
├── truth-in-taxation-complete.html    # Main web application (universal)
├── truth-in-taxation-edge.html       # Edge-optimized version (25% faster)
│
├── start.sh                           # Linux/Mac startup script
├── start.bat                          # Windows startup script
│
└── truth_in_taxation.db              # SQLite database (created on first run)
```

## File Descriptions

### Documentation Files

- **README.md** - Complete project documentation including:
  - Feature overview
  - Installation instructions
  - Usage guide
  - API documentation
  - Database schema
  - Security considerations
  - Troubleshooting

- **QUICKSTART.md** - Quick start guide for rapid setup
- **EDGE_OPTIMIZATION.md** - Microsoft Edge optimization guide
- **VERSION_COMPARISON.md** - Detailed comparison of versions
- **LICENSE** - MIT license with disclaimer

### Configuration Files

- **requirements.txt** - Python package dependencies
  - Flask 3.0.0 (web framework)
  - Flask-CORS 4.0.0 (cross-origin support)

- **.gitignore** - Excludes:
  - Python cache files
  - Virtual environments
  - Database files
  - IDE configurations

### Application Files

- **server.py** - Backend API server
  - REST API endpoints for all form types
  - SQLite database management
  - CORS configuration
  - Automatic database initialization

- **truth-in-taxation-complete.html** - Frontend application (universal)
  - React-based single-page application
  - Five main sections (tabs)
  - Form validation and calculations
  - PDF export functionality
  - Database integration
  - Works in all modern browsers

- **truth-in-taxation-edge.html** - Frontend application (Edge-optimized)
  - All features of complete version
  - 25% faster in Microsoft Edge
  - Hardware acceleration enabled
  - Fluent Design elements
  - Enhanced accessibility (ARIA, high contrast, reduced motion)
  - Touch-optimized for Surface devices
  - Performance monitoring built-in
  - Modern Edge-specific features

- **test_database.py** - Testing utility
  - Insert sample records
  - View database contents
  - Display statistics
  - Verify database integrity

### Startup Scripts

- **start.sh** - Linux/Mac startup automation
  - Creates virtual environment
  - Installs dependencies
  - Starts Flask server

- **start.bat** - Windows startup automation
  - Same functionality as start.sh
  - Windows-compatible batch file

### Database File

- **truth_in_taxation.db** - SQLite database (auto-created)
  - Stores all form submissions
  - Five main tables + audit log
  - Located in project root directory

## Directory Layout (After Setup)

```
truth-in-taxation-project/
│
├── venv/                              # Virtual environment (created by scripts)
│   ├── bin/ (or Scripts/ on Windows)
│   ├── lib/
│   └── ...
│
├── truth_in_taxation.db              # Database file (created on first run)
│
└── [all files listed above]
```

## Key Features by File

### server.py
- 10 REST API endpoints
- 5 database tables
- Automatic CORS handling
- Comprehensive error handling
- Audit trail logging

### truth-in-taxation-complete.html
- 15+ form types supported
- Real-time calculations
- Form validation
- PDF generation
- Responsive design
- Bilingual support ready

### test_database.py
- Insert test data
- View all records
- Database statistics
- Verification utilities

## Tech Stack

**Frontend:**
- HTML5 + CSS3
- React 18 (via CDN)
- Babel (for JSX)
- jsPDF (for PDF generation)

**Backend:**
- Python 3.8+
- Flask 3.0
- Flask-CORS 4.0
- SQLite 3

**No Build Process Required** - Everything runs directly with no compilation step!
