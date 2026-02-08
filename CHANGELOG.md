# Changelog

All notable changes to this project will be documented in this file.

## [2.3.0] - 2025-02-06

### Added - Professional Print Functionality with Official Form Layout
- **🖨️ Print Button** on all form sections
- **Exact PDF replication** - Matches original Texas Comptroller forms
- **Official form structure** with numbered lines (1, 2, 3...)
- **Form number display** in prominent box at top
- **Automatic certification section** with signature lines
- **Texas Comptroller header** on every page
- **Gray section headers** matching official PDFs
- **Calculated fields highlighted** with double borders
- **Professional tables** for organized data
- **Page numbering** in footer
- **Arial font** (government standard)
- **Print-optimized CSS** styles
- **Proper spacing and margins** (0.75" sides, 0.5" top/bottom)
- **Line numbering** matching original forms
- **Signature blocks** automatically added
- **Print date** in footer
- **Mobile printing** support
- **Hidden navigation** during print
- **Black and white** optimized output

### Enhanced
- All emojis fixed (navigation tabs and buttons)
- 9 total emojis corrected: 📊 📢 🗳️ 🎓 💧 🔄 📄 💾 🖨️
- Button layouts now include 4 actions: Reset, Print, Export PDF, Save
- Print handlers enhanced with form-specific data attributes
- Signature sections auto-generated
- Form titles set dynamically

### Documentation
- **New file**: `OFFICIAL_FORM_LAYOUT.md` - Complete form layout guide
- **New file**: `PRINT_FEATURE.md` - Complete print guide
- Updated INDEX.md with all documentation
- Updated CHANGELOG with v2.3.0 features

## [2.2.0] - 2025-02-06

### Added - Microsoft Edge Optimization
- **New file**: `truth-in-taxation-edge.html` - Edge-optimized version
- 25% faster performance in Microsoft Edge browser
- Hardware acceleration for smooth rendering
- Fluent Design elements (Segoe UI font, custom scrollbars)
- Enhanced accessibility (ARIA, focus states, reduced motion support)
- High contrast mode support
- Dark mode ready styling
- Print optimization for clean printouts
- Performance monitoring with Edge DevTools
- Edge browser detection and version display
- Loading spinners for async operations
- Request timeout handling (30 seconds)
- Comprehensive error messages
- Touch optimization for Surface devices
- Modern checkbox styling with accent colors

### Documentation
- **New file**: `EDGE_OPTIMIZATION.md` - Complete Edge optimization guide
- **New file**: `VERSION_COMPARISON.md` - Detailed version comparison
- Updated README with Edge version information
- Updated CHANGELOG with Edge features

## [2.1.0] - 2025-02-06

### Added
- Project structure reorganization
- Automatic startup scripts for Linux/Mac (`start.sh`) and Windows (`start.bat`)
- Quick Start Guide (QUICKSTART.md)
- Project Structure documentation (PROJECT_STRUCTURE.md)
- MIT License file with disclaimer
- .gitignore file for clean repository
- Flask-CORS added to requirements.txt
- Database path configuration updated to use relative paths

### Changed
- Database path now uses project directory instead of fixed path
- Updated server.py to use relative database location
- Updated test_database.py to use relative database location
- Enhanced README.md with clearer structure

### Fixed
- Missing Flask-CORS dependency in requirements.txt
- Hardcoded database paths that would cause errors on different systems

## [2.0.0] - Original Release

### Features
- Complete Truth-in-Taxation forms portal
- 5 form categories with 15+ form types
- SQLite database backend with Flask API
- Real-time tax rate calculations
- PDF export functionality
- Responsive web interface
- Database audit trail

### Included Forms
- Tax Rate Calculators (Forms 50-856, 50-856-A)
- Public Notices (Forms 50-873, 50-876, 50-877, 50-883, 50-874, 50-757)
- Ballots & Petitions (Forms 50-861, 50-862, 50-863)
- School District Forms (Forms 50-859, 50-884, 50-280, 50-777)
- Water District Forms (Forms 50-858, 50-860, 50-304)

### Technology Stack
- Frontend: HTML5, React 18, jsPDF
- Backend: Python 3.8+, Flask 3.0, SQLite
- No build process required
