# Comparative Risk Recommendation Dashboard

A comprehensive, desktop-based financial risk management and portfolio analytics application built in Python. This system evaluates multi-client financial risk profiles, computes advanced risk metrics, and delivers automated, data-driven recommendations through an interactive graphical interface.

---

## 1. Executive Summary

The **Comparative Risk Recommendation Dashboard** is an advanced financial analytics and portfolio risk management application built in Python. Designed to bridge quantitative risk modeling with accessible desktop visualization, the system evaluates multi-client financial portfolios, computes critical risk parameters, and automatically formulates actionable advisory recommendations through an intuitive graphical interface.

---

## 2. Core Architecture & Modules

The application follows a modular architecture separating data processing, risk computation, UI interaction, and visualization layers:

| Module / Component | Technology / Libraries | Primary Responsibility |
| :--- | :--- | :--- |
| **Risk Engine** | Pandas, NumPy | Simulates portfolios and computes Value at Risk (VaR), CVaR, and Maximum Drawdown. |
| **User Interface** | Tkinter | Desktop GUI for managing client records, bank details, and interactive navigation. |
| **Visualization Layer** | Matplotlib, Seaborn | Renders dynamic charts displaying risk-reward trade-offs and comparative portfolio curves. |
| **Advisory Logic** | Python Rule-Based Engine | Generates automated textual financial advice and risk mitigation strategies. |

---

## 3. Key Financial Risk Metrics

* **Value at Risk (VaR) & Conditional Value at Risk (CVaR):** Quantifies potential financial losses over a given time horizon at specified confidence intervals, providing robust downside protection estimates across individual accounts.
* **Maximum Drawdown:** Measures the maximum observed peak-to-trough decline in portfolio value before a new peak is achieved, evaluating historical volatility severity.

---

## 4. Project Directory Structure

The repository is structured to maintain clean separation of concerns and ease of extensibility:

```text
Comparative-Risk-Recommendation-Dashboard/
│
├── data/               # Client financial records and portfolio datasets
├── src/                # Core application source code
│   ├── engine.py       # RiskEngine class for quantitative metrics
│   ├── ui.py           # Tkinter-based dashboard interface
│   └── visualization.py# Matplotlib & Seaborn plotting routines
│
├── requirements.txt    # Project dependencies
├── main.py             # Application entry point
└── README.md           # Project documentation

5. Getting Started & Usage
To run the application locally on your workstation, follow these setup steps:
Clone the Repository:
git clone [https://github.com/rishikeshjay/Comparative-Risk-Recommendation-Dashboard.git](https://github.com/rishikeshjay/Comparative-Risk-Recommendation-Dashboard.git)
cd Comparative-Risk-Recommendation-Dashboard

Set up Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install Dependencies:
pip install -r requirements.txt

Launch Application:
python main.py

License
This project is open-source and available under the MIT License.
