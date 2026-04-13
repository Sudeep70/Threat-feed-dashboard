import requests
import config
from database import add_threat

def collect_urlhaus():
    """Collect malware URLs from URLhaus (abuse.ch)"""
    url = 'https://urlhaus.abuse.ch/downloads/csv_recent/'
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        lines = response.text.splitlines()

        threats = []

        # Skip header lines (first 9 lines are comments)
        for line in lines[9:9 + config.MAX_RESULTS_PER_SOURCE]:
            parts = line.split(',')

            if len(parts) < 3:
                continue

            malware_url = parts[2].strip('"')

            threat_id = add_threat(
                source='URLhaus',
                threat_type='malware',
                indicator=malware_url,
                description="Malware URL from URLhaus CSV feed",
                confidence_score=90,
                country='',
                tags='malware',
                raw_data=line
            )

            if threat_id:
                threats.append(malware_url)

        print(f"✅ URLhaus: Collected {len(threats)} malware URLs")
        return threats

    except Exception as e:
        print(f"❌ URLhaus error: {e}")
        return []