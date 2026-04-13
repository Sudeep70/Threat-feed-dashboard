import requests
import config
from database import add_threat

def collect_abuseipdb():
    """Collect malicious IPs from AbuseIPDB"""
    if not config.ABUSEIPDB_API_KEY:
        print("⚠️  AbuseIPDB API key not configured")
        return []
    
    url = 'https://api.abuseipdb.com/api/v2/blacklist'
    
    headers = {
        'Accept': 'application/json',
        'Key': config.ABUSEIPDB_API_KEY
    }
    
    params = {
        'confidenceMinimum': 75,
        'limit': config.MAX_RESULTS_PER_SOURCE
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        threats = []
        
        if 'data' in data:
            for item in data['data']:
                ip = item.get('ipAddress', '')
                confidence = item.get('abuseConfidenceScore', 0)
                country = item.get('countryCode', '')
                
                threat_id = add_threat(
                    source='AbuseIPDB',
                    threat_type='malicious_ip',
                    indicator=ip,
                    description=f"Malicious IP with {confidence}% confidence",
                    confidence_score=confidence,
                    country=country,
                    tags='abuse,malicious_ip',
                    raw_data=str(item)
                )
                
                if threat_id:
                    threats.append({
                        'ip': ip,
                        'confidence': confidence,
                        'country': country
                    })
        
        print(f"✅ AbuseIPDB: Collected {len(threats)} malicious IPs")
        return threats
        
    except requests.exceptions.RequestException as e:
        print(f"❌ AbuseIPDB API error: {e}")
        return []
    except Exception as e:
        print(f"❌ AbuseIPDB processing error: {e}")
        return []
