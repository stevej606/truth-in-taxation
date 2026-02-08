#!/usr/bin/env python3
"""
Test script for Truth-in-Taxation database operations
"""

import sqlite3
import json
from datetime import datetime

import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'truth_in_taxation.db')

def test_insert_tax_calculation():
    """Test inserting a tax rate calculation"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    test_data = {
        'form_type': 'standard',
        'taxing_unit': 'Test City',
        'county': 'Test County',
        'tax_year': '2025',
        'last_year_levy': 1000000.00,
        'last_year_mo_rate': 0.450000,
        'last_year_debt_rate': 0.150000,
        'current_total_value': 250000000.00,
        'new_property_value': 5000000.00,
        'lost_property_levy': 10000.00,
        'proposed_mo_rate': 0.460000,
        'proposed_debt_rate': 0.150000,
        'total_debt': 15000000.00,
        'tax_increments': 0.00,
        'is_disaster_area': False,
        'no_new_revenue_rate': 0.404082,
        'voter_approval_rate': 0.568265,
        'de_minimis_rate': 0.586408,
        'proposed_rate': 0.610000
    }
    
    cursor.execute('''
        INSERT INTO tax_rate_calculations (
            form_type, taxing_unit, county, tax_year, last_year_levy,
            last_year_mo_rate, last_year_debt_rate, current_total_value,
            new_property_value, lost_property_levy, proposed_mo_rate,
            proposed_debt_rate, total_debt, tax_increments, is_disaster_area,
            no_new_revenue_rate, voter_approval_rate, de_minimis_rate, proposed_rate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(test_data.values()))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return record_id

def test_insert_public_notice():
    """Test inserting a public notice"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO public_notices (
            notice_type, form_number, taxing_unit, proposed_rate,
            no_new_revenue_rate, voter_approval_rate, meeting_date,
            meeting_time, meeting_location
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'exceeds-both',
        '50-873',
        'Test City',
        0.610000,
        0.404082,
        0.568265,
        '2025-08-15',
        '18:00',
        '123 Main St, City Hall'
    ))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return record_id

def view_all_records():
    """View all records in the database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("DATABASE CONTENTS")
    print("="*80)
    
    # Tax Rate Calculations
    cursor.execute('SELECT * FROM tax_rate_calculations')
    tax_calcs = cursor.fetchall()
    print(f"\nðŸ“Š Tax Rate Calculations ({len(tax_calcs)} records):")
    for record in tax_calcs:
        print(f"  ID: {record['id']}")
        print(f"  Taxing Unit: {record['taxing_unit']}")
        print(f"  County: {record['county']}")
        print(f"  Tax Year: {record['tax_year']}")
        print(f"  Proposed Rate: ${record['proposed_rate']:.6f}")
        print(f"  Created: {record['created_at']}")
        print()
    
    # Public Notices
    cursor.execute('SELECT * FROM public_notices')
    notices = cursor.fetchall()
    print(f"ðŸ“¢ Public Notices ({len(notices)} records):")
    for record in notices:
        print(f"  ID: {record['id']}")
        print(f"  Taxing Unit: {record['taxing_unit']}")
        print(f"  Form: {record['form_number']}")
        print(f"  Meeting: {record['meeting_date']} at {record['meeting_time']}")
        print(f"  Created: {record['created_at']}")
        print()
    
    # Submission Log
    cursor.execute('SELECT * FROM form_submissions_log')
    logs = cursor.fetchall()
    print(f"ðŸ“ Submission Log ({len(logs)} entries):")
    for log in logs:
        print(f"  {log['submitted_at']}: {log['action']} - {log['form_category']} (ID: {log['form_id']})")
    
    conn.close()

def get_statistics():
    """Get database statistics"""
    conn = sqlite3.connect(DB_PATH)
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
    
    print("\n" + "="*80)
    print("DATABASE STATISTICS")
    print("="*80)
    for key, value in stats.items():
        print(f"{key}: {value}")
    print()

if __name__ == '__main__':
    print("Testing Truth-in-Taxation Database Operations")
    print("="*80)
    
    # Test inserting records
    print("\n1ï¸âƒ£ Inserting test tax rate calculation...")
    tax_id = test_insert_tax_calculation()
    print(f"âœ… Created tax rate calculation with ID: {tax_id}")
    
    print("\n2ï¸âƒ£ Inserting test public notice...")
    notice_id = test_insert_public_notice()
    print(f"âœ… Created public notice with ID: {notice_id}")
    
    # View statistics
    print("\n3ï¸âƒ£ Getting database statistics...")
    get_statistics()
    
    # View all records
    print("\n4ï¸âƒ£ Viewing all records...")
    view_all_records()
    
    print("\n" + "="*80)
    print("âœ… All tests completed successfully!")
    print("="*80)
