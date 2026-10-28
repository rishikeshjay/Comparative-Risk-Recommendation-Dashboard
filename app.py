"""
Web-Based Comparative Risk & Recommendation Dashboard
Core Focus: Data Visualization, Recommendations, and Backend Logic (Flask + Pandas)
"""

import io
import base64
from flask import Flask, render_template_string, request, redirect, url_for
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Required for headless server rendering
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# ==========================================
# 1. CORE OOP & 7-PERSON DATABASE
# ==========================================
class ClientProfile:
    def __init__(self, client_id, name, age, capital, risk_profile, equity_weight):
        self.client_id = client_id
        self.name = name
        self.age = int(age)
        self.capital = float(capital)
        self.risk_profile = risk_profile
        self.equity_weight = float(equity_weight)

# Pre-loading the 7 distinct individuals
db = {
    "C1": ClientProfile("C1", "Arun", 28, 10000, "Aggressive", 0.8),
    "C2": ClientProfile("C2", "Priya", 45, 50000, "Moderate", 0.6),
    "C3": ClientProfile("C3", "Rohan", 60, 120000, "Conservative", 0.3),
    "C4": ClientProfile("C4", "Sneha", 32, 25000, "Aggressive", 0.75),
    "C5": ClientProfile("C5", "Karan", 50, 80000, "Moderate", 0.5),
    "C6": ClientProfile("C6", "Aditi", 25, 15000, "Aggressive", 0.9),
    "C7": ClientProfile("C7", "Vikram", 41, 60000, "Conservative", 0.4)
}

# ==========================================
# 2. ANALYTICS & RECOMMENDATION ENGINE
# ==========================================
def process_client_analytics():
    """Generates the Pandas DataFrame and calculates comparative risk metrics."""
    data = [vars(client) for client in db.values()]
    df = pd.DataFrame(data)
    
    if df.empty:
        return df, ""
        
    equity_return, equity_vol = 0.12, 0.20
    debt_return, debt_vol = 0.06, 0.05
    
    # Calculate Expected Return & Volatility
    df["Exp_Return"] = (df["equity_weight"] * equity_return) + ((1 - df["equity_weight"]) * debt_return)
    df["Volatility"] = np.sqrt((df["equity_weight"] * equity_vol)**2 + ((1 - df["equity_weight"]) * debt_vol)**2)
    
    # Calculate 95% Value at Risk (VaR)
    df["VaR_Dollar"] = abs((df["Exp_Return"] - (1.645 * df["Volatility"])) * df["capital"])
    
    # Generate Automated Recommendations
    advice_log = []
    for _, row in df.iterrows():
        if row["age"] > 55 and row["risk_profile"] == "Aggressive":
            advice_log.append(f"⚠️ {row['name']} (Age {row['age']}): High risk near retirement. Reduce equity below {row['equity_weight']*100}%.")
        elif (row["VaR_Dollar"] / row["capital"]) > 0.15 and row["risk_profile"] == "Conservative":
            advice_log.append(f"🚨 {row['name']}: VaR (${row['VaR_Dollar']:,.0f}) exceeds conservative threshold. Rebalance to debt.")
        elif row["age"] < 30 and row["risk_profile"] == "Conservative":
            advice_log.append(f"💡 {row['name']} (Age {row['age']}): Young investor. Consider increasing equity for growth.")
        else:
            advice_log.append(f"✅ {row['name']}: Portfolio aligned with {row['risk_profile']} profile.")
            
    return df, advice_log

def generate_visualizations(df):
    """Generates Seaborn/Matplotlib charts and encodes them for the web."""
    if df.empty: return None
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.tight_layout(pad=4.0)
    
    # Chart 1: Risk vs Reward Scatter Plot
    axes[0].set_title("Client Risk vs. Expected Return", fontweight="bold")
    sns.scatterplot(data=df, x="Volatility", y="Exp_Return", hue="risk_profile", 
                    size="capital", sizes=(100, 600), ax=axes[0], palette="deep", alpha=0.8)
    for i in range(len(df)):
        axes[0].text(df.Volatility[i] + 0.002, df.Exp_Return[i], df.name[i], fontsize=9)
    axes[0].set_xlabel("Portfolio Volatility (Risk)")
    axes[0].set_ylabel("Expected Annual Return")
    
    # Chart 2: Value at Risk Bar Chart
    axes[1].set_title("Maximum Expected Loss (95% VaR)", fontweight="bold")
    sns.barplot(data=df, x="name", y="VaR_Dollar", hue="risk_profile", ax=axes[1], dodge=False)
    axes[1].set_xlabel("Client Name")
    axes[1].set_ylabel("Capital at Risk ($)")

    # Convert plot to Base64 image to embed in HTML
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode('utf8')

# ==========================================
# 3. WEB ROUTING & TAILWIND FRONTEND
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparative Risk Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-800 p-6 font-sans">
    <div class="max-w-7xl mx-auto space-y-6">
        
        <div class="bg-indigo-900 text-white p-6 rounded-lg shadow-md">
            <h1 class="text-3xl font-bold">Multi-Client Risk Comparison & Advisory Panel</h1>
            <p class="text-indigo-200 mt-2">Data Analytics, Visualization, and Automated Portfolio Suggestions</p>
        </div>

        <!-- Automated Recommendations -->
        <div class="bg-white p-6 rounded-lg shadow border-l-4 border-yellow-400">
            <h2 class="text-xl font-bold mb-4 text-gray-800">Automated Advisor Suggestions</h2>
            <ul class="space-y-2 text-sm">
                {% for advice in recommendations %}
                    <li class="bg-gray-50 p-3 rounded border">{{ advice }}</li>
                {% endfor %}
            </ul>
        </div>

        <!-- Data Visualizations -->
        {% if plot_url %}
        <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-bold mb-4 text-gray-800">Risk vs. Reward Visualizations</h2>
            <img src="data:image/png;base64,{{ plot_url }}" alt="Risk Analytics Charts" class="w-full rounded border">
        </div>
        {% endif %}

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Add/Update Client Form -->
            <div class="bg-white p-6 rounded-lg shadow lg:col-span-1">
                <h2 class="text-lg font-bold mb-4">Add or Update Client</h2>
                <form action="/update_client" method="POST" class="space-y-3">
                    <input type="text" name="client_id" placeholder="Client ID (e.g., C8)" required class="w-full p-2 border rounded">
                    <input type="text" name="name" placeholder="Name" required class="w-full p-2 border rounded">
                    <input type="number" name="age" placeholder="Age" required class="w-full p-2 border rounded">
                    <input type="number" name="capital" placeholder="Capital ($)" required class="w-full p-2 border rounded">
                    <select name="risk_profile" class="w-full p-2 border rounded">
                        <option value="Conservative">Conservative</option>
                        <option value="Moderate">Moderate</option>
                        <option value="Aggressive">Aggressive</option>
                    </select>
                    <input type="number" step="0.05" name="equity_weight" placeholder="Equity Weight (0.0 to 1.0)" required class="w-full p-2 border rounded">
                    <button type="submit" class="w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded hover:bg-indigo-700">Submit Record</button>
                </form>
            </div>

            <!-- Client Data Table -->
            <div class="bg-white p-6 rounded-lg shadow lg:col-span-2 overflow-x-auto">
                <h2 class="text-lg font-bold mb-4">Live Client Database</h2>
                {{ table_html | safe }}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    df, recommendations = process_client_analytics()
    plot_url = generate_visualizations(df)
    
    table_html = ""
    if not df.empty:
        # Format columns for display
        display_df = df.round({"Exp_Return": 3, "Volatility": 3, "VaR_Dollar": 0})
        table_html = display_df.to_html(classes="min-w-full text-sm text-left divide-y divide-gray-200", index=False)
        table_html = table_html.replace('<th>', '<th class="px-4 py-2 bg-gray-50 text-gray-700 font-semibold">')
        table_html = table_html.replace('<td>', '<td class="px-4 py-2 border-t">')

    return render_template_string(HTML_TEMPLATE, 
                                  recommendations=recommendations, 
                                  plot_url=plot_url, 
                                  table_html=table_html)

@app.route("/update_client", methods=["POST"])
def update_client():
    # Updates existing client or adds a new one
    cid = request.form.get("client_id")
    db[cid] = ClientProfile(
        client_id=cid,
        name=request.form.get("name"),
        age=request.form.get("age"),
        capital=request.form.get("capital"),
        risk_profile=request.form.get("risk_profile"),
        equity_weight=request.form.get("equity_weight")
    )
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
