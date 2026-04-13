#!/usr/bin/env python3
"""
ThreatFeed Dashboard - Web Interface
"""

from flask import Flask, render_template, jsonify
from database import get_recent_threats, get_threat_stats, get_threats_by_type, init_database
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Main dashboard page"""
    stats = get_threat_stats()
    recent = get_recent_threats(limit=20)
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         recent_threats=recent,
                         last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/threats')
def api_threats():
    """API endpoint for recent threats"""
    limit = request.args.get('limit', 100, type=int)
    threats = get_recent_threats(limit=limit)
    return jsonify(threats)

@app.route('/api/threats/<threat_type>')
def api_threats_by_type(threat_type):
    """API endpoint for threats by type"""
    limit = request.args.get('limit', 50, type=int)
    threats = get_threats_by_type(threat_type, limit=limit)
    return jsonify(threats)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    stats = get_threat_stats()
    return jsonify(stats)

@app.route('/phishing')
def phishing():
    """Phishing threats page"""
    threats = get_threats_by_type('phishing', limit=100)
    return render_template('dashboard.html', 
                         filter_type='phishing',
                         recent_threats=threats,
                         stats=get_threat_stats())

@app.route('/malware')
def malware():
    """Malware threats page"""
    threats = get_threats_by_type('malware', limit=100)
    return render_template('dashboard.html', 
                         filter_type='malware',
                         recent_threats=threats,
                         stats=get_threat_stats())

@app.route('/ips')
def malicious_ips():
    """Malicious IPs page"""
    threats = get_threats_by_type('malicious_ip', limit=100)
    return render_template('dashboard.html', 
                         filter_type='malicious_ip',
                         recent_threats=threats,
                         stats=get_threat_stats())

if __name__ == '__main__':
    init_database()
    print("\n" + "="*60)
    print("🌐 ThreatFeed Dashboard Starting...")
    print("="*60)
    print("\n🔗 Access the dashboard at: http://localhost:5000")
    print("💡 Press CTRL+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
