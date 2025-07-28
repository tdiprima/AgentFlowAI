from crewai import Agent, Task, Crew
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
def researcher_task():
    stock_data = {}
    for symbol in STOCK_SYMBOLS:
        prev, curr = get_latest_stock_price(symbol)
        if prev is not None and curr is not None:
            stock_data[symbol] = {"prev": prev, "current": curr}
    return stock_data

# Agent 2: Analyst - Generates insights and triggers alerts
def analyst_task(stock_data):
    alerts = []
    insights = []
    for symbol, prices in stock_data.items():
        percent_change = calculate_percent_change(prices['prev'], prices['current'])
        insights.append(
            f"{symbol}: Prev Close=${prices['prev']:.2f}, Current=${prices['current']:.2f}, Change={percent_change:.2f}%"
        )
        if abs(percent_change) >= PRICE_CHANGE_THRESHOLD:
            alerts.append(
                f"{symbol} changed by {percent_change:.2f}% (Threshold: {PRICE_CHANGE_THRESHOLD}%)"
            )
    return insights, alerts

# CrewAI Agents
researcher_agent = Agent(
    name="Researcher",
    description="Monitors and fetches current and previous stock prices.",
    goal="Get up-to-date stock price data for analysis.",
    role="researcher",
    task=researcher_task
)

analyst_agent = Agent(
    name="Analyst",
    description="Analyzes stock price changes and generates insights and alerts.",
    goal="Identify significant changes and trigger alerts.",
    role="analyst",
    task=analyst_task
)

# Task Chaining
def main():
    # Step 1: Researcher fetches stock data
    stock_data = researcher_agent.run()
    # Step 2: Analyst analyzes and triggers alerts
    insights, alerts = analyst_agent.run(stock_data)
    print("Insights:")
    for insight in insights:
        print(insight)
    if alerts:
        alert_body = "\n".join(alerts)
        print("Stock Alert: Significant Change Detected", alert_body)
        # send_email_alert("Stock Alert: Significant Change Detected", alert_body)
        # print("Alert sent!")
    else:
        print("No significant changes detected.")

if __name__ == "__main__":
    main()
