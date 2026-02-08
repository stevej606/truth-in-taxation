from flask import Flask, request, jsonify, send_from_directory
import json
from datetime import datetime
import os
import sqlite3

# Try to import optional database drivers
try:
    import pyodbc
    HAS_PYODBC = True
except ImportError:
    HAS_PYODBC = False

try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR)

# Database mode detection:
# 1. DATABASE_URL env var -> PostgreSQL (Render)
# 2. SQL_CONN_STR env var -> SQL Server
# 3. USE_LOCAL_SQLSERVER=true -> local SQL Server Express
# 4. fallback -> SQLite
DATABASE_URL = os.environ.get('DATABASE_URL', '')
SQL_CONN_STR = os.environ.get('SQL_CONN_STR', '')
DB_PATH = os.path.join(BASE_DIR, 'truth_in_taxation.db')

if DATABASE_URL and HAS_PSYCOPG2:
    DB_MODE = 'postgres'
elif SQL_CONN_STR and HAS_PYODBC:
    DB_MODE = 'sqlserver'
elif HAS_PYODBC and os.environ.get('USE_LOCAL_SQLSERVER', '').lower() == 'true':
    SQL_CONN_STR = (
        r'DRIVER={ODBC Driver 18 for SQL Server};'
        r'SERVER=localhost\SQLEXPRESS;'
        r'DATABASE=truth_in_taxation;'
        r'Trusted_Connection=yes;'
        r'TrustServerCertificate=yes;'
    )
    DB_MODE = 'sqlserver'
else:
    DB_MODE = 'sqlite'

# PostgreSQL uses %s, SQLite and SQL Server use ?
PARAM = '%s' if DB_MODE == 'postgres' else '?'

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
    return response

def get_conn():
    """Get a new database connection"""
    if DB_MODE == 'postgres':
        return psycopg2.connect(DATABASE_URL)
    elif DB_MODE == 'sqlserver':
        return pyodbc.connect(SQL_CONN_STR)
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def row_to_dict(cursor, row):
    """Convert a row to a dictionary"""
    if DB_MODE == 'postgres':
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    elif DB_MODE == 'sqlserver':
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    else:
        return dict(row)

def rows_to_dicts(cursor, rows):
    """Convert rows to a list of dictionaries"""
    if DB_MODE in ('postgres', 'sqlserver'):
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    else:
        return [dict(row) for row in rows]

def p(sql):
    """Replace ? placeholders with the correct parameter marker for the current DB"""
    if DB_MODE == 'postgres':
        return sql.replace('?', '%s')
    return sql

def init_db():
    """Initialize the database with all necessary tables"""
    conn = get_conn()
    cursor = conn.cursor()

    if DB_MODE == 'sqlserver':
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tax_rate_calculations' AND xtype='U')
            CREATE TABLE tax_rate_calculations (
                id INT IDENTITY(1,1) PRIMARY KEY,
                form_type NVARCHAR(255) NOT NULL, taxing_unit NVARCHAR(255) NOT NULL,
                county NVARCHAR(255), tax_year NVARCHAR(50),
                last_year_levy FLOAT, last_year_mo_rate FLOAT, last_year_debt_rate FLOAT,
                current_total_value FLOAT, new_property_value FLOAT, lost_property_levy FLOAT,
                proposed_mo_rate FLOAT, proposed_debt_rate FLOAT, total_debt FLOAT,
                tax_increments FLOAT, is_disaster_area BIT,
                no_new_revenue_rate FLOAT, voter_approval_rate FLOAT,
                de_minimis_rate FLOAT, proposed_rate FLOAT,
                created_at DATETIME DEFAULT GETDATE(), updated_at DATETIME DEFAULT GETDATE()
            )
        ''')
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='public_notices' AND xtype='U')
            CREATE TABLE public_notices (
                id INT IDENTITY(1,1) PRIMARY KEY,
                notice_type NVARCHAR(255) NOT NULL, form_number NVARCHAR(255),
                taxing_unit NVARCHAR(255) NOT NULL, proposed_rate FLOAT,
                no_new_revenue_rate FLOAT, voter_approval_rate FLOAT,
                meeting_date NVARCHAR(255), meeting_time NVARCHAR(255),
                meeting_location NVARCHAR(MAX), notice_text NVARCHAR(MAX),
                created_at DATETIME DEFAULT GETDATE(), updated_at DATETIME DEFAULT GETDATE()
            )
        ''')
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ballots_petitions' AND xtype='U')
            CREATE TABLE ballots_petitions (
                id INT IDENTITY(1,1) PRIMARY KEY,
                ballot_type NVARCHAR(255) NOT NULL, form_number NVARCHAR(255),
                taxing_unit NVARCHAR(255) NOT NULL, proposed_rate FLOAT,
                election_date NVARCHAR(255), language NVARCHAR(255), ballot_text NVARCHAR(MAX),
                created_at DATETIME DEFAULT GETDATE(), updated_at DATETIME DEFAULT GETDATE()
            )
        ''')
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='school_district_forms' AND xtype='U')
            CREATE TABLE school_district_forms (
                id INT IDENTITY(1,1) PRIMARY KEY,
                form_type NVARCHAR(255) NOT NULL, form_number NVARCHAR(255),
                school_district NVARCHAR(255) NOT NULL, county NVARCHAR(255), tax_year NVARCHAR(50),
                current_value FLOAT, mo_portion FLOAT, debt_portion FLOAT,
                total_rate FLOAT, has_chapter_313 BIT,
                created_at DATETIME DEFAULT GETDATE(), updated_at DATETIME DEFAULT GETDATE()
            )
        ''')
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='water_district_forms' AND xtype='U')
            CREATE TABLE water_district_forms (
                id INT IDENTITY(1,1) PRIMARY KEY,
                district_type NVARCHAR(255) NOT NULL, form_number NVARCHAR(255),
                district_name NVARCHAR(255) NOT NULL, county NVARCHAR(255), tax_year NVARCHAR(50),
                proposed_rate FLOAT, hearing_date NVARCHAR(255), hearing_time NVARCHAR(255),
                hearing_location NVARCHAR(MAX),
                created_at DATETIME DEFAULT GETDATE(), updated_at DATETIME DEFAULT GETDATE()
            )
        ''')
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='form_submissions_log' AND xtype='U')
            CREATE TABLE form_submissions_log (
                id INT IDENTITY(1,1) PRIMARY KEY,
                form_category NVARCHAR(255) NOT NULL, form_id INT,
                action NVARCHAR(255) NOT NULL, user_info NVARCHAR(MAX),
                ip_address NVARCHAR(255), submitted_at DATETIME DEFAULT GETDATE()
            )
        ''')
    elif DB_MODE == 'postgres':
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tax_rate_calculations (
                id SERIAL PRIMARY KEY,
                form_type VARCHAR(255) NOT NULL, taxing_unit VARCHAR(255) NOT NULL,
                county VARCHAR(255), tax_year VARCHAR(50),
                last_year_levy DOUBLE PRECISION, last_year_mo_rate DOUBLE PRECISION,
                last_year_debt_rate DOUBLE PRECISION, current_total_value DOUBLE PRECISION,
                new_property_value DOUBLE PRECISION, lost_property_levy DOUBLE PRECISION,
                proposed_mo_rate DOUBLE PRECISION, proposed_debt_rate DOUBLE PRECISION,
                total_debt DOUBLE PRECISION, tax_increments DOUBLE PRECISION,
                is_disaster_area BOOLEAN,
                no_new_revenue_rate DOUBLE PRECISION, voter_approval_rate DOUBLE PRECISION,
                de_minimis_rate DOUBLE PRECISION, proposed_rate DOUBLE PRECISION,
                created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS public_notices (
                id SERIAL PRIMARY KEY,
                notice_type VARCHAR(255) NOT NULL, form_number VARCHAR(255),
                taxing_unit VARCHAR(255) NOT NULL, proposed_rate DOUBLE PRECISION,
                no_new_revenue_rate DOUBLE PRECISION, voter_approval_rate DOUBLE PRECISION,
                meeting_date VARCHAR(255), meeting_time VARCHAR(255),
                meeting_location TEXT, notice_text TEXT,
                created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ballots_petitions (
                id SERIAL PRIMARY KEY,
                ballot_type VARCHAR(255) NOT NULL, form_number VARCHAR(255),
                taxing_unit VARCHAR(255) NOT NULL, proposed_rate DOUBLE PRECISION,
                election_date VARCHAR(255), language VARCHAR(255), ballot_text TEXT,
                created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS school_district_forms (
                id SERIAL PRIMARY KEY,
                form_type VARCHAR(255) NOT NULL, form_number VARCHAR(255),
                school_district VARCHAR(255) NOT NULL, county VARCHAR(255), tax_year VARCHAR(50),
                current_value DOUBLE PRECISION, mo_portion DOUBLE PRECISION,
                debt_portion DOUBLE PRECISION, total_rate DOUBLE PRECISION,
                has_chapter_313 BOOLEAN,
                created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS water_district_forms (
                id SERIAL PRIMARY KEY,
                district_type VARCHAR(255) NOT NULL, form_number VARCHAR(255),
                district_name VARCHAR(255) NOT NULL, county VARCHAR(255), tax_year VARCHAR(50),
                proposed_rate DOUBLE PRECISION, hearing_date VARCHAR(255),
                hearing_time VARCHAR(255), hearing_location TEXT,
                created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS form_submissions_log (
                id SERIAL PRIMARY KEY,
                form_category VARCHAR(255) NOT NULL, form_id INTEGER,
                action VARCHAR(255) NOT NULL, user_info TEXT,
                ip_address VARCHAR(255), submitted_at TIMESTAMP DEFAULT NOW()
            )
        ''')
    else:
        # SQLite DDL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tax_rate_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                form_type TEXT NOT NULL, taxing_unit TEXT NOT NULL,
                county TEXT, tax_year TEXT,
                last_year_levy REAL, last_year_mo_rate REAL, last_year_debt_rate REAL,
                current_total_value REAL, new_property_value REAL, lost_property_levy REAL,
                proposed_mo_rate REAL, proposed_debt_rate REAL, total_debt REAL,
                tax_increments REAL, is_disaster_area BOOLEAN,
                no_new_revenue_rate REAL, voter_approval_rate REAL,
                de_minimis_rate REAL, proposed_rate REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS public_notices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notice_type TEXT NOT NULL, form_number TEXT,
                taxing_unit TEXT NOT NULL, proposed_rate REAL,
                no_new_revenue_rate REAL, voter_approval_rate REAL,
                meeting_date TEXT, meeting_time TEXT,
                meeting_location TEXT, notice_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ballots_petitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ballot_type TEXT NOT NULL, form_number TEXT,
                taxing_unit TEXT NOT NULL, proposed_rate REAL,
                election_date TEXT, language TEXT, ballot_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS school_district_forms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                form_type TEXT NOT NULL, form_number TEXT,
                school_district TEXT NOT NULL, county TEXT, tax_year TEXT,
                current_value REAL, mo_portion REAL, debt_portion REAL,
                total_rate REAL, has_chapter_313 BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS water_district_forms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                district_type TEXT NOT NULL, form_number TEXT,
                district_name TEXT NOT NULL, county TEXT, tax_year TEXT,
                proposed_rate REAL, hearing_date TEXT, hearing_time TEXT,
                hearing_location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS form_submissions_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                form_category TEXT NOT NULL, form_id INTEGER,
                action TEXT NOT NULL, user_info TEXT,
                ip_address TEXT, submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    conn.commit()
    conn.close()
    print(f"Database initialized successfully ({DB_MODE})")

def insert_and_get_id(cursor, sql, params):
    """Insert a row and return the new ID"""
    if DB_MODE == 'sqlserver':
        sql = sql.replace(') VALUES', ') OUTPUT INSERTED.id VALUES')
        cursor.execute(sql, params)
        return cursor.fetchone()[0]
    elif DB_MODE == 'postgres':
        sql = p(sql.rstrip().rstrip(')') + ') RETURNING id')
        cursor.execute(sql, params)
        return cursor.fetchone()[0]
    else:
        cursor.execute(sql, params)
        return cursor.lastrowid

@app.route('/')
def serve_home():
    """Serve the main HTML page"""
    return send_from_directory(BASE_DIR, 'truth-in-taxation-complete.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory(BASE_DIR, filename)

@app.route('/api/init', methods=['GET'])
def initialize():
    """Initialize the database"""
    try:
        init_db()
        return jsonify({"status": "success", "message": "Database initialized"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/tax-rate-calculation', methods=['POST'])
def save_tax_rate_calculation():
    """Save tax rate calculation"""
    try:
        data = request.json
        conn = get_conn()
        cursor = conn.cursor()

        form_id = insert_and_get_id(cursor, '''
            INSERT INTO tax_rate_calculations (
                form_type, taxing_unit, county, tax_year, last_year_levy,
                last_year_mo_rate, last_year_debt_rate, current_total_value,
                new_property_value, lost_property_levy, proposed_mo_rate,
                proposed_debt_rate, total_debt, tax_increments, is_disaster_area,
                no_new_revenue_rate, voter_approval_rate, de_minimis_rate, proposed_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('formType'), data.get('taxingUnit'), data.get('county'),
            data.get('taxYear'), data.get('lastYearLevy'), data.get('lastYearMORate'),
            data.get('lastYearDebtRate'), data.get('currentTotalValue'),
            data.get('newPropertyValue'), data.get('lostPropertyLevy'),
            data.get('proposedMORate'), data.get('proposedDebtRate'),
            data.get('totalDebt'), data.get('taxIncrements'),
            data.get('isDisasterArea'), data.get('noNewRevenueRate'),
            data.get('voterApprovalRate'), data.get('deMinimisRate'),
            data.get('proposedRate')
        ))

        cursor.execute(p('''
            INSERT INTO form_submissions_log (form_category, form_id, action, ip_address)
            VALUES (?, ?, ?, ?)
        '''), ('tax_rate_calculation', form_id, 'create', request.remote_addr))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Tax rate calculation saved successfully",
            "id": form_id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/public-notice', methods=['POST'])
def save_public_notice():
    """Save public notice"""
    try:
        data = request.json
        conn = get_conn()
        cursor = conn.cursor()

        form_id = insert_and_get_id(cursor, '''
            INSERT INTO public_notices (
                notice_type, form_number, taxing_unit, proposed_rate,
                no_new_revenue_rate, voter_approval_rate, meeting_date,
                meeting_time, meeting_location, notice_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('noticeType'), data.get('formNumber'), data.get('taxingUnit'),
            data.get('proposedRate'), data.get('noNewRevenueRate'),
            data.get('voterApprovalRate'), data.get('meetingDate'),
            data.get('meetingTime'), data.get('meetingLocation'),
            data.get('noticeText')
        ))

        cursor.execute(p('''
            INSERT INTO form_submissions_log (form_category, form_id, action, ip_address)
            VALUES (?, ?, ?, ?)
        '''), ('public_notice', form_id, 'create', request.remote_addr))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Public notice saved successfully",
            "id": form_id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/ballot-petition', methods=['POST'])
def save_ballot_petition():
    """Save ballot or petition"""
    try:
        data = request.json
        conn = get_conn()
        cursor = conn.cursor()

        form_id = insert_and_get_id(cursor, '''
            INSERT INTO ballots_petitions (
                ballot_type, form_number, taxing_unit, proposed_rate,
                election_date, language, ballot_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('ballotType'), data.get('formNumber'), data.get('taxingUnit'),
            data.get('proposedRate'), data.get('electionDate'),
            data.get('language'), data.get('ballotText')
        ))

        cursor.execute(p('''
            INSERT INTO form_submissions_log (form_category, form_id, action, ip_address)
            VALUES (?, ?, ?, ?)
        '''), ('ballot_petition', form_id, 'create', request.remote_addr))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Ballot/Petition saved successfully",
            "id": form_id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/school-district', methods=['POST'])
def save_school_district():
    """Save school district form"""
    try:
        data = request.json
        conn = get_conn()
        cursor = conn.cursor()

        form_id = insert_and_get_id(cursor, '''
            INSERT INTO school_district_forms (
                form_type, form_number, school_district, county, tax_year,
                current_value, mo_portion, debt_portion, total_rate, has_chapter_313
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('formType'), data.get('formNumber'), data.get('schoolDistrict'),
            data.get('county'), data.get('taxYear'), data.get('currentValue'),
            data.get('moPortion'), data.get('debtPortion'),
            data.get('totalRate'), data.get('hasChapter313')
        ))

        cursor.execute(p('''
            INSERT INTO form_submissions_log (form_category, form_id, action, ip_address)
            VALUES (?, ?, ?, ?)
        '''), ('school_district', form_id, 'create', request.remote_addr))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "School district form saved successfully",
            "id": form_id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/water-district', methods=['POST'])
def save_water_district():
    """Save water district form"""
    try:
        data = request.json
        conn = get_conn()
        cursor = conn.cursor()

        form_id = insert_and_get_id(cursor, '''
            INSERT INTO water_district_forms (
                district_type, form_number, district_name, county, tax_year,
                proposed_rate, hearing_date, hearing_time, hearing_location
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('districtType'), data.get('formNumber'), data.get('districtName'),
            data.get('county'), data.get('taxYear'), data.get('proposedRate'),
            data.get('hearingDate'), data.get('hearingTime'),
            data.get('hearingLocation')
        ))

        cursor.execute(p('''
            INSERT INTO form_submissions_log (form_category, form_id, action, ip_address)
            VALUES (?, ?, ?, ?)
        '''), ('water_district', form_id, 'create', request.remote_addr))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Water district form saved successfully",
            "id": form_id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/submissions', methods=['GET'])
def get_all_submissions():
    """Get all form submissions"""
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM tax_rate_calculations ORDER BY created_at DESC')
        tax_calcs = rows_to_dicts(cursor, cursor.fetchall())

        cursor.execute('SELECT * FROM public_notices ORDER BY created_at DESC')
        notices = rows_to_dicts(cursor, cursor.fetchall())

        cursor.execute('SELECT * FROM ballots_petitions ORDER BY created_at DESC')
        ballots = rows_to_dicts(cursor, cursor.fetchall())

        cursor.execute('SELECT * FROM school_district_forms ORDER BY created_at DESC')
        school = rows_to_dicts(cursor, cursor.fetchall())

        cursor.execute('SELECT * FROM water_district_forms ORDER BY created_at DESC')
        water = rows_to_dicts(cursor, cursor.fetchall())

        conn.close()

        return jsonify({
            "status": "success",
            "data": {
                "tax_rate_calculations": tax_calcs,
                "public_notices": notices,
                "ballots_petitions": ballots,
                "school_district_forms": school,
                "water_district_forms": water
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/submissions/<category>', methods=['GET'])
def get_submissions_by_category(category):
    """Get submissions by category"""
    try:
        conn = get_conn()
        cursor = conn.cursor()

        table_map = {
            'tax-rate': 'tax_rate_calculations',
            'notices': 'public_notices',
            'ballots': 'ballots_petitions',
            'school': 'school_district_forms',
            'water': 'water_district_forms'
        }

        table_name = table_map.get(category)
        if not table_name:
            return jsonify({"status": "error", "message": "Invalid category"}), 400

        cursor.execute(f'SELECT * FROM {table_name} ORDER BY created_at DESC')
        results = rows_to_dicts(cursor, cursor.fetchall())

        conn.close()

        return jsonify({
            "status": "success",
            "data": results
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/submission/<category>/<int:id>', methods=['GET'])
def get_submission_by_id(category, id):
    """Get a specific submission by ID"""
    try:
        conn = get_conn()
        cursor = conn.cursor()

        table_map = {
            'tax-rate': 'tax_rate_calculations',
            'notices': 'public_notices',
            'ballots': 'ballots_petitions',
            'school': 'school_district_forms',
            'water': 'water_district_forms'
        }

        table_name = table_map.get(category)
        if not table_name:
            return jsonify({"status": "error", "message": "Invalid category"}), 400

        cursor.execute(p(f'SELECT * FROM {table_name} WHERE id = ?'), (id,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return jsonify({
                "status": "success",
                "data": row_to_dict(cursor, result)
            }), 200
        else:
            return jsonify({"status": "error", "message": "Record not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/submission/<category>/<int:id>', methods=['DELETE'])
def delete_submission(category, id):
    """Delete a submission"""
    try:
        conn = get_conn()
        cursor = conn.cursor()

        table_map = {
            'tax-rate': 'tax_rate_calculations',
            'notices': 'public_notices',
            'ballots': 'ballots_petitions',
            'school': 'school_district_forms',
            'water': 'water_district_forms'
        }

        table_name = table_map.get(category)
        if not table_name:
            return jsonify({"status": "error", "message": "Invalid category"}), 400

        cursor.execute(p(f'DELETE FROM {table_name} WHERE id = ?'), (id,))

        cursor.execute(p('''
            INSERT INTO form_submissions_log (form_category, form_id, action, ip_address)
            VALUES (?, ?, ?, ?)
        '''), (category, id, 'delete', request.remote_addr))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Record deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get database statistics"""
    try:
        conn = get_conn()
        cursor = conn.cursor()

        stats = {}

        cursor.execute('SELECT COUNT(*) FROM tax_rate_calculations')
        stats['tax_rate_calculations'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM public_notices')
        stats['public_notices'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM ballots_petitions')
        stats['ballots_petitions'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM school_district_forms')
        stats['school_district_forms'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM water_district_forms')
        stats['water_district_forms'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM form_submissions_log')
        stats['total_submissions'] = cursor.fetchone()[0]

        conn.close()

        return jsonify({
            "status": "success",
            "data": stats
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Truth-in-Taxation API Server ({DB_MODE})...")
    print(f"Running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'true').lower() == 'true')
