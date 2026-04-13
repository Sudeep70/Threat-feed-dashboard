import requests
import config
from database import add_threat

def collect_phishtank():
    """Collect phishing URLs from Phishtank"""
    url = 'http://data.phishtank.com/data/online-valid.json'
    
    try:
        headers = {
            'User-Agent': 'ThreatFeed-Dashboard/1.0'
        }
        
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        threats = []
        phishing_data = data[:config.MAX_RESULTS_PER_SOURCE]
        
        for item in phishing_data:
            phish_url = item.get('url', '')
            phish_id = item.get('phish_id', '')
            target = item.get('target', 'unknown')
            verified = item.get('verified', 'no')
            
            confidence = 95 if verified == 'yes' else 75
            
            threat_id = add_threat(
                source='Phishtank',
                threat_type='phishing',
                indicator=phish_url,
                description=f"Phishing site targeting {target}",
                confidence_score=confidence,
                country='',
                tags=f'phishing,{target}',
                raw_data=str(item)
            )
            
            if threat_id:
                threats.append({
                    'url': phish_url,
                    'target': target,
                    'verified': verified,
                    'phish_id': phish_id
                })
        
        print(f"✅ Phishtank: Collected {len(threats)} phishing URLs")
        return threats
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Phishtank API error: {e}")
        return []
    except Exception as e:
        print(f"❌ Phishtank processing error: {e}")
        return []