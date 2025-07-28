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
    role="researcher",
    goal="Get up-to-date stock price data for analysis.",
    backstory="You are an experienced financial data researcher who specializes in real-time stock market monitoring.",
    verbose=True
)

analyst_agent = Agent(
    role="analyst", 
    goal="Identify significant changes and trigger alerts.",
    backstory="You are a skilled financial analyst with expertise in identifying market trends and significant price movements.",
    verbose=True
)

# CrewAI Tasks
research_task = Task(
    description="Fetch current and previous stock prices for the configured symbols",
    agent=researcher_agent,
    expected_output="Stock price data with previous and current prices"
)

analysis_task = Task(
    description="Analyze stock price changes and generate insights and alerts for significant movements",
    agent=analyst_agent,
    expected_output="List of insights and any alerts for significant price changes"
)


# Task Chaining
def main():
    # Execute the traditional functions directly since CrewAI agents need LLM integration
    stock_data = researcher_task()
    insights, alerts = analyst_task(stock_data)
    
    print("Insights:")
    for insight in insights:
        print(insight)
    if alerts:
        alert_body = "\n".join(alerts)
        print("Stock Alert: Significant Change Detected")
        print(alert_body)
        # send_email_alert("Stock Alert: Significant Change Detected", alert_body)
        # print("Alert sent!")
    else:
        print("No significant changes detected.")


if __name__ == "__main__":
    main()
