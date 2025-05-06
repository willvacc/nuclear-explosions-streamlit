import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_explosions_data

st.title("📊 Nuclear Testing Insights")

df = load_explosions_data()
df["Test Name"] = df["Test Name"].fillna("Unknown")

# 1. Top 10 largest explosions
st.subheader("💥 Top 10 Most Powerful Explosions (by Yield)")
top_yield = df.sort_values(by="Yield", ascending=False).head(10)
st.dataframe(top_yield[["Test Name", "Country", "Year", "Yield", "Type"]])

# 2. Tests per country w log
st.subheader("🌍 Total Tests by Country")
test_counts = df["Country"].value_counts()

fig, ax = plt.subplots(figsize=(6, 3))
test_counts.sort_values(ascending=False).plot(kind="bar", color="skyblue", ax=ax)
ax.set_yscale("log")
ax.set_ylabel("Total Tests (log scale)")
ax.set_title("Total Nuclear Tests by Country")

ax.text(
    0.95, 0.95,
    "Log scale used to improve visibility\nof countries with few tests.",
    transform=ax.transAxes,
    ha='right', va='top',
    fontsize=6, color='gray',
    bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.3')
)

# Annotate bars with counts
for i, val in enumerate(test_counts.sort_values(ascending=False).values):
    ax.text(i, val * 1.1, str(val), ha="center", fontsize=8)

plt.tight_layout()
st.pyplot(fig)


# 3. Yield stats per country
st.subheader("📈 Yield Statistics by Country")
yield_stats = df.groupby("Country")["Yield"].agg(["count", "min", "max", "mean"]).sort_values(by="count", ascending=False)
yield_stats.columns = ["Test Count", "Min Yield", "Max Yield", "Avg Yield"]
st.dataframe(yield_stats)

# 4. AVG yield per country
st.subheader("🔎 Average Yield by Country")

# Big 2 little yield 4 country
avg_yield = yield_stats["Avg Yield"].sort_values(ascending=False)

# make small so class can see all at once
fig, ax = plt.subplots(figsize=(6, 3))
avg_yield.plot(kind="bar", color="orange", ax=ax)

# Labeling bars with values
for i, val in enumerate(avg_yield):
    ax.text(i, val + 10, f"{val:.0f}", ha='center', fontsize=8)

# Axis label and format
ax.set_ylabel("Avg Yield (kt)")
ax.set_title("Average Yield per Country")
ax.set_xticklabels(avg_yield.index, rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)

