#!/usr/bin/env python3
"""
ThreatFeed Dashboard - Main Collection Script
Collects threats from multiple sources and sends alerts
"""
from collectors.urlhaus import collect_urlhaus
# collect_abuseipdb()
# collect_phishtank()
collect_urlhaus()

import sys
from datetime import datetime
from database import init_database, get_threat_stats, update_daily_stats, get_recent_threats
from collectors.abuseipdb import collect_abuseipdb
from collectors.urlhaus import collect_urlhaus
from collectors.phishtank import collect_phishtank
from telegram_alerts import send_threat_summary
import config

def collect_all_threats():
    """Run all collectors"""
    print("\n" + "="*60)
    print(f"🔍 ThreatFeed Collection Started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    # Initialize database
    init_database()
    
    # Collect from all sources
    collectors = [
        ("AbuseIPDB", collect_abuseipdb),
        ("URLhaus", collect_urlhaus),
        ("Phishtank", collect_phishtank),
    ]
    
    total_collected = 0
    
    for name, collector_func in collectors:
        print(f"\n📡 Collecting from {name}...")
        try:
            results = collector_func()
            total_collected += len(results)
        except Exception as e:
            print(f"❌ {name} failed: {e}")
    
    print(f"\n{'='*60}")
    print(f"✅ Collection complete: {total_collected} threats processed")
    print(f"{'='*60}\n")
    
    # Update statistics
    update_daily_stats()
    
    # Get stats and high-confidence threats
    stats = get_threat_stats()
    recent_threats = get_recent_threats(limit=100)
    
    # Filter high-confidence threats for alerts
    high_confidence = [
        t for t in recent_threats 
        if t.get('confidence_score', 0) >= config.CRITICAL_CONFIDENCE_THRESHOLD
    ]
    
    print(f"\n📊 Statistics:")
    print(f"   • Total threats in DB: {stats.get('total', 0)}")
    print(f"   • New today: {stats.get('today', 0)}")
    print(f"   • High confidence: {len(high_confidence)}")
    
    # Send Telegram alert
    if high_confidence:
        print(f"\n📱 Sending Telegram alert...")
        send_threat_summary(stats, high_confidence)
    else:
        print(f"\n✅ No high-confidence threats to alert")
    
    print(f"\n{'='*60}")
    print(f"🎉 ThreatFeed collection finished successfully!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    try:
        collect_all_threats()
    except KeyboardInterrupt:
        print("\n\n⚠️  Collection interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        sys.exit(1)
