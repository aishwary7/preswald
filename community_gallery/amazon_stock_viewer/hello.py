from preswald import table, plotly, slider
import pandas as pd
import plotly.express as px

# Load the CSV manually
df = pd.read_csv("data/amazon_stock.csv", parse_dates=["date"], dayfirst=False)
df = df.dropna(subset=["date"])  # Drop bad rows

# 📅 Ensure datetime formatting is clean
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.sort_values(by="date")  # Sort for better plots

# 🎚️ Year Selection Slider
min_year = int(df["date"].dt.year.min())
max_year = int(df["date"].dt.year.max())
selected_year = slider("📅 Select Year", min_val=min_year, max_val=max_year, default=max_year)

# 🔽 Fake dropdown using a slider (Select Stock Metric)
metric_options = ["close", "open", "high", "low"]
metric_index = slider("📊 Select Metric (0: Close, 1: Open, 2: High, 3: Low)", min_val=0, max_val=3, default=0)
metric = metric_options[metric_index]  # Convert slider value to actual metric

# 📈 Add Moving Average (7-day rolling window)
df["Moving_Avg"] = df.groupby(df["date"].dt.year)[metric].transform(lambda x: x.rolling(7, min_periods=1).mean())

# 📆 Filter Data for Selected Year
filtered_df = df[df["date"].dt.year == selected_year]

# 🎨 Stunning Plotly Line Chart
fig = px.line(
    filtered_df, x="date", y=metric,
    title=f"Amazon {metric.capitalize()} Price & 7-Day Moving Average ({selected_year})",
    labels={"date": "Date", metric: f"{metric.capitalize()} Price"},
    template="plotly_dark",  # 🔥 Dark mode for pro look
)

# 📈 Overlay Moving Average Line
fig.add_scatter(x=filtered_df["date"], y=filtered_df["Moving_Avg"], mode="lines", name="7-Day Moving Avg", line=dict(dash="dash", color="red"))

# 🔥 Display Interactive Chart & Table
plotly(fig)
table(filtered_df[["date", metric, "Moving_Avg", "volume"]], title=f"📊 Amazon {metric.capitalize()} Price Data ({selected_year})")