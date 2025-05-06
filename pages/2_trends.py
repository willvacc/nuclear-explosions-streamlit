import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import load_explosions_data

st.title("📈 Trends in Nuclear Testing")

df = load_explosions_data()

# Sidebar filters
st.sidebar.subheader("Filter Options")
selected_countries = st.sidebar.multiselect(
    "Select countries", options=df['Country'].unique(), default=["USA", "USSR"]
)
year_range = st.sidebar.slider("Year Range", int(df['Year'].min()), int(df['Year'].max()), (1945, 1990))

# Filtered
filtered_df = df[
    (df['Country'].isin(selected_countries)) &
    (df['Year'].between(*year_range))
]

# Chart 1: Tests per year
st.subheader("Number of Tests Per Year")
year_counts = filtered_df['Year'].value_counts().sort_index()
fig1, ax1 = plt.subplots(figsize=(5, 2))
ax1.bar(year_counts.index, year_counts.values, color="orange")
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Tests")
ax1.set_title("Nuclear Tests Per Year")
st.pyplot(fig1)

# Chart 2: Average yield per year
st.subheader("Average Yield Per Year (kt)")
avg_yield = filtered_df.groupby('Year')['Yield'].mean()
fig2, ax2 = plt.subplots(figsize=(5, 2))
ax2.plot(avg_yield.index, avg_yield.values, color="red", marker="o", markersize=2, linewidth=.5)
ax2.set_xlabel("Year")
ax2.set_ylabel("Average Yield")
ax2.set_title("Average Yield Over Time")
st.pyplot(fig2)

# 3 Chart
st.subheader("Yield Distribution")
fig3, ax3 = plt.subplots(figsize=(5, 2))
sns.histplot(filtered_df['Yield'], bins=30, kde=True, ax=ax3, color="purple")
ax3.set_title("Distribution of Explosion Yields")
ax3.set_xlabel("Yield (kt)")
ax3.set_ylabel("Count")
ax3.set_xlim(0, 2000)
ax3.grid(True, linestyle="--", alpha=0.4)
st.pyplot(fig3)
st.markdown("""
<small>
This chart shows the distribution of nuclear explosion sizes based on yield (in kilotons).  
Most tests had small yields, while very high-yield explosions were much less common.
</large>
""", unsafe_allow_html=True)
