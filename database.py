import sqlite3
from datetime import datetime
import config

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Threats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            threat_type TEXT NOT NULL,
            indicator TEXT NOT NULL,
            description TEXT,
            confidence_score INTEGER,
            country TEXT,
            tags TEXT,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            raw_data TEXT,
            UNIQUE(source, indicator)
        )
    ''')
    
    # Daily statistics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE,
            total_threats INTEGER DEFAULT 0,
            phishing_count INTEGER DEFAULT 0,
            malware_count INTEGER DEFAULT 0,
            malicious_ip_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def add_threat(source, threat_type, indicator, description='', confidence_score=0, 
               country='', tags='', raw_data=''):
    """Add or update a threat in the database"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO threats (source, threat_type, indicator, description, 
                               confidence_score, country, tags, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source, indicator) DO UPDATE SET
                last_seen = CURRENT_TIMESTAMP,
                confidence_score = excluded.confidence_score,
                description = excluded.description
        ''', (source, threat_type, indicator, description, confidence_score, 
              country, tags, raw_data))
        
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"❌ Error adding threat: {e}")
        return None
    finally:
        conn.close()

def get_recent_threats(limit=100):
    """Get most recent threats"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM threats 
        ORDER BY last_seen DESC 
        LIMIT ?
    ''', (limit,))
    
    threats = cursor.fetchall()
    conn.close()
    return [dict(row) for row in threats]

def get_threats_by_type(threat_type, limit=50):
    """Get threats filtered by type"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM threats 
        WHERE threat_type = ?
        ORDER BY last_seen DESC 
        LIMIT ?
    ''', (threat_type, limit))
    
    threats = cursor.fetchall()
    conn.close()
    return [dict(row) for row in threats]

def get_threat_stats():
    """Get overall statistics"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    stats = {}
    
    # Total threats
    cursor.execute('SELECT COUNT(*) FROM threats')
    stats['total'] = cursor.fetchone()[0]
    
    # By type
    cursor.execute('''
        SELECT threat_type, COUNT(*) as count 
        FROM threats 
        GROUP BY threat_type
    ''')
    stats['by_type'] = dict(cursor.fetchall())
    
    # Today's threats
    cursor.execute('''
        SELECT COUNT(*) FROM threats 
        WHERE DATE(last_seen) = DATE('now')
    ''')
    stats['today'] = cursor.fetchone()[0]
    
    # Top countries
    cursor.execute('''
        SELECT country, COUNT(*) as count 
        FROM threats 
        WHERE country != ''
        GROUP BY country 
        ORDER BY count DESC 
        LIMIT 10
    ''')
    stats['top_countries'] = dict(cursor.fetchall())
    
    conn.close()
    return stats

def update_daily_stats():
    """Update daily statistics"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    today = datetime.now().date()
    
    # Count today's threats
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN threat_type = 'phishing' THEN 1 ELSE 0 END) as phishing,
            SUM(CASE WHEN threat_type = 'malware' THEN 1 ELSE 0 END) as malware,
            SUM(CASE WHEN threat_type = 'malicious_ip' THEN 1 ELSE 0 END) as malicious_ip
        FROM threats
        WHERE DATE(last_seen) = ?
    ''', (today,))
    
    result = cursor.fetchone()
    
    cursor.execute('''
        INSERT INTO daily_stats (date, total_threats, phishing_count, 
                                malware_count, malicious_ip_count)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            total_threats = excluded.total_threats,
            phishing_count = excluded.phishing_count,
            malware_count = excluded.malware_count,
            malicious_ip_count = excluded.malicious_ip_count
    ''', (today, result[0], result[1], result[2], result[3]))
    
    conn.commit()
    conn.close()
