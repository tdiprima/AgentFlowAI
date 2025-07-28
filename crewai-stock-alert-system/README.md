# CrewAI Stock Alert System

## Summary

This project is a simple multi-agent system built with [CrewAI](https://github.com/joaomdmoura/crewAI) that monitors stock prices, generates insights, and sends email alerts if stock price changes exceed a specified threshold (default: 5%). The system demonstrates task chaining and tool integration in an agentic workflow.

## How It Works

- **Agents**:
  - **Researcher**: Fetches the latest and previous closing prices for a list of stocks.
  - **Analyst**: Analyzes the price changes, generates insights, and triggers an email alert if any stock moves more than the threshold.

- **Task Chaining**:
  1. The Researcher agent gathers stock price data.
  2. The Analyst agent receives this data, calculates percent changes, generates insights, and checks for significant changes.
  3. If any stock changes exceed the threshold, an email alert is sent.

- **Tool Integration**:
  - Uses [yfinance](https://pypi.org/project/yfinance/) to fetch stock prices.
  - Uses Python's `smtplib` to send email alerts.

## What It's Doing

- The system starts by having the Researcher agent collect the latest and previous closing prices for a list of stocks (e.g., AAPL, GOOGL, MSFT).
- The Analyst agent receives this data, calculates the percent change for each stock, and generates human-readable insights.
- If any stock's price has changed (up or down) by more than the threshold (default 5%), the system sends an email alert summarizing the event.
- Otherwise, it simply prints the insights.

## Customization

- You can add or remove stock symbols in `config.py`.
- Adjust the `PRICE_CHANGE_THRESHOLD` to set your own alert level.
- Update email settings with your own credentials.

## Note

- For Gmail, you may need to use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) instead of your main password.
- This is a simple demo of agentic task chaining and tool integration using CrewAI.

---

## Note!

I removed the **CrewAI pattern** because it failed due to complex dependency conflicts between Pydantic v1/v2, LangChain versions, and CrewAI versions. The error was:

  ```
  PydanticUserError: The `__modify_schema__` method is not supported in Pydantic v2. Use
  `__get_pydantic_json_schema__` instead in class `SecretStr`.
  ```

  The proper CrewAI pattern would be:

  ```python
  from crewai import Agent, Task, Crew

  # Define agents
  researcher_agent = Agent(
      role="researcher",
      goal="Get up-to-date stock price data for analysis.",
      backstory="You are an experienced financial data researcher...",
      verbose=True
  )

  analyst_agent = Agent(
      role="analyst",
      goal="Identify significant changes and trigger alerts.",
      backstory="You are a skilled financial analyst...",
      verbose=True
  )

  # Define tasks
  research_task = Task(
      description="Fetch current and previous stock prices...",
      agent=researcher_agent,
      expected_output="Stock price data with previous and current prices"
  )

  analysis_task = Task(
      description="Analyze stock price changes...",
      agent=analyst_agent,
      expected_output="List of insights and alerts",
      context=[research_task]
  )

  # Create crew
  crew = Crew(
      agents=[researcher_agent, analyst_agent],
      tasks=[research_task, analysis_task],
      verbose=2
  )

  # Execute
  result = crew.kickoff()
  ```

But the dependency conflicts made this impossible to run, so I created a functional equivalent that mimics the CrewAI workflow without the framework.

<br>
