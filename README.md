# ML Trading Bot


# Automated Sentiment-Based Algorithmic Trading

This project combines advanced sentiment analysis with machine learning techniques to create a dynamic trading strategy. By analyzing sentiment from financial news headlines, the system makes data-driven trading decisions in real-time.

## Features

- Real-time sentiment analysis of financial news
- Dynamic trading strategy based on sentiment and risk management
- Advanced position sizing using Kelly Criterion, VaR, and CVaR
- Trade execution and backtesting using Alpaca API
![zbi](https://github.com/AdamHassouni/finbot/assets/122727246/480d9812-d520-4649-a55a-eff767778935)
![Backtest1](https://github.com/AdamHassouni/finbot/assets/122727246/8e91b606-fb2e-4dd9-b0ec-deb082aed578)
![backtest2](https://github.com/AdamHassouni/finbot/assets/122727246/5fd2c19c-af6e-42ba-9dd7-4adff83bd1fc)

## Installation

### Prerequisites

- Python 3.12
- An Alpaca account with API keys

### Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/your-username/finbot.git
    cd finbot
    ```

2. **Create a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure API Keys**

    Create a `config.py` file in the project directory with the following content:

    ```python
    API_KEY = "your_alpaca_api_key"
    API_SECRET = "your_alpaca_api_secret"
    BASE_URL = "https://paper-api.alpaca.markets"
    ```

## Usage

1. **Run the strategy**

    ```bash
    python main.py
    ```

2. **Monitor the logs**

    The strategy logs messages to the console to help you monitor its actions.

## Project Structure

- `main.py`: Entry point for running the trading strategy.
- `strategy.py`: Contains the MLTrader class with the trading logic.
- `utils.py`: Utility functions for risk management and sentiment analysis.
- `config.py`: Configuration file for storing API keys.




