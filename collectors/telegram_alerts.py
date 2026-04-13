import requests
import config
import html

def send_telegram_alert(message):
    """Send alert message to Telegram"""
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("⚠️  Telegram credentials not configured")
        return False
    
    url = f'https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage'
    
    payload = {
        'chat_id': config.TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Telegram alert failed: {e}")
        return False

def send_threat_summary(stats, high_confidence_threats):
    """Send a summary of collected threats"""
    if not high_confidence_threats:
        return
    
    # Build alert message
    message = "🚨 <b>ThreatFeed Alert</b>\n\n"
    message += f"📊 Today's Statistics:\n"
    message += f"• Total threats: {stats.get('today', 0)}\n"
    message += f"• Phishing: {stats.get('by_type', {}).get('phishing', 0)}\n"
    message += f"• Malware: {stats.get('by_type', {}).get('malware', 0)}\n"
    message += f"• Malicious IPs: {stats.get('by_type', {}).get('malicious_ip', 0)}\n\n"
    
    message += f"⚠️ <b>High-Confidence Threats ({len(high_confidence_threats)}):</b>\n\n"
    
    # Show top threats
    for i, threat in enumerate(high_confidence_threats[:config.MAX_ALERTS_PER_RUN], 1):
        threat_type = threat.get('threat_type', 'unknown').replace('_', ' ').title()
        indicator = threat.get('indicator', '')[:50]  # Truncate long URLs
        indicator = html.escape(indicator)
        # Escape HTML characters in indicator
        indicator = html.escape(indicator)
        confidence = threat.get('confidence_score', 0)
        source = threat.get('source', '')
        
        message += f"{i}. <b>{threat_type}</b> ({confidence}% confidence)\n"
        message += f"   Source: {source}\n"
        message += f"   Indicator: <code>{indicator}</code>\n\n"
    
    if len(high_confidence_threats) > config.MAX_ALERTS_PER_RUN:
        message += f"... and {len(high_confidence_threats) - config.MAX_ALERTS_PER_RUN} more\n\n"
    
    message += "🔗 View full dashboard for details"
    
    send_telegram_alert(message)
    print(f"✅ Telegram alert sent ({len(high_confidence_threats)} threats)")
