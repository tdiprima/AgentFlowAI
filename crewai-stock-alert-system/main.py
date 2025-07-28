from stock_tools import get_latest_stock_price, calculate_percent_change
from config import (
    STOCK_SYMBOLS,
    PRICE_CHANGE_THRESHOLD,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECEIVER,
)
import smtplib
from email.mime.text import MIMEText


# Tool: Email sender
def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())


# Agent 1: Researcher - Fetches and monitors stock prices
def researcher_agent():
    print("🔍 Researcher Agent: Fetching stock price data...")
    stock_data = {}
    for symbol in STOCK_SYMBOLS:
        prev, curr = get_latest_stock_price(symbol)
        if prev is not None and curr is not None:
            stock_data[symbol] = {"prev": prev, "current": curr}
            print(f"   Retrieved {symbol}: Prev=${prev:.2f}, Current=${curr:.2f}")
    return stock_data


# Agent 2: Analyst - Generates insights and triggers alerts
def analyst_agent(stock_data):
    print("📊 Analyst Agent: Analyzing price changes...")
    alerts = []
    insights = []
    for symbol, prices in stock_data.items():
        percent_change = calculate_percent_change(prices['prev'], prices['current'])
        insight = f"{symbol}: Prev Close=${prices['prev']:.2f}, Current=${prices['current']:.2f}, Change={percent_change:.2f}%"
        insights.append(insight)
        print(f"   {insight}")
        
        if abs(percent_change) >= PRICE_CHANGE_THRESHOLD:
            alert = f"{symbol} changed by {percent_change:.2f}% (Threshold: {PRICE_CHANGE_THRESHOLD}%)"
            alerts.append(alert)
            print(f"   ⚠️  ALERT: {alert}")
    return insights, alerts


def main():
    print("🚀 Starting Stock Alert System...")
    print("=" * 50)
    
    # Execute researcher agent
    stock_data = researcher_agent()
    
    if not stock_data:
        print("❌ No stock data retrieved. Exiting.")
        return
    
    print("\n" + "=" * 50)
    
    # Execute analyst agent
    insights, alerts = analyst_agent(stock_data)
    
    print("\n" + "=" * 50)
    print("📈 FINAL INSIGHTS:")
    for insight in insights:
        print(f"   {insight}")
    
    if alerts:
        print("\n🚨 ALERTS TRIGGERED:")
        for alert in alerts:
            print(f"   {alert}")
        
        alert_body = "\n".join(alerts)
        print(f"\n📧 Sending email alert...")
        # Uncomment to actually send email:
        # send_email_alert("Stock Alert: Significant Change Detected", alert_body)
        print("   Email alert prepared (currently disabled)")
    else:
        print("\n✅ No significant changes detected.")
    
    print("=" * 50)
    print("🏁 Stock Alert System completed.")


if __name__ == "__main__":
    main()
