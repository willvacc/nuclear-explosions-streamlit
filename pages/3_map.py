import streamlit as st
import pydeck as pdk
import numpy as np
from utils.data_loader import load_explosions_data

st.title("💣 Nuclear Explosions Map 💣")

df = load_explosions_data()

# Country color map
country_colors = {
    "USA": [0, 200, 255],
    "USSR": [255, 100, 100],
    "UK": [255, 255, 0],
    "CHINA": [255, 150, 50],
    "FRANCE": [150, 255, 150],
    "INDIA": [200, 0, 200],
    "PAKISTAN": [0, 255, 100],
}

# Sidebar filters
st.sidebar.subheader("Map Filters")
all_countries = df["Country"].unique().tolist()
selected_countries = st.sidebar.multiselect("Select countries", all_countries, default=["USA", "USSR"])
year_range = st.sidebar.slider("Select year range", int(df["Year"].min()), int(df["Year"].max()), (1945, 1990))

# Filter early
filtered = df[
    (df["Country"].isin(selected_countries)) &
    (df["Year"].between(*year_range))
].copy()

# Clean test names
filtered["Test Name"] = filtered["Test Name"].fillna("Unknown")
test_name_options = sorted(filtered["Test Name"].unique().tolist())
selected_test = st.sidebar.selectbox("Search specific test name", ["All"] + test_name_options)
if selected_test != "All":
    filtered = filtered[filtered["Test Name"] == selected_test]

if filtered.empty:
    st.warning("No data matches your filters.")
    st.stop()

def yield_to_alpha(yield_val):
    min_alpha = 50
    max_alpha = 255
    if np.isnan(yield_val) or yield_val <= 0:
        return min_alpha
    norm_yield = min(yield_val / df["Yield"].max(), 1.0)
    return int(min_alpha + (max_alpha - min_alpha) * norm_yield)

filtered["Alpha"] = filtered["Yield"].fillna(0).apply(yield_to_alpha)

# Assign color based on country
filtered["Color"] = filtered.apply(
    lambda row: country_colors.get(row["Country"].upper(), [200, 200, 200])[:3] + [row["Alpha"]],
    axis=1
)

# Country color legend
st.markdown("### 🗂️ Country Legend")
legend_items = []
for country in selected_countries:
    rgb = country_colors.get(country.upper(), [180, 180, 180])
    hex_color = '#%02x%02x%02x' % tuple(rgb)
    legend_items.append(f"<span style='background-color:{hex_color};padding:3px 10px;border-radius:5px;color:black'>{country}</span>")
st.markdown(" ".join(legend_items), unsafe_allow_html=True)

# Yield intensity key
st.markdown("### 💥 Yield Intensity Key")
st.markdown("""
- 🔴 **Light Dot** = Small explosion  
- 🔴 **Medium Dot** = Moderate explosion  
- 🔴 **Dark Dot** = Massive explosion  
""")

# Map view
view_state = pdk.ViewState(
    latitude=filtered["Latitude"].mean(),
    longitude=filtered["Longitude"].mean(),
    zoom=1.5,
    pitch=10
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered,
    get_position='[Longitude, Latitude]',
    get_radius=20000,
    get_fill_color="Color",
    get_line_color=[0, 0, 0],
    line_width_min_pixels=1,
    pickable=True,
    auto_highlight=True
)

tooltip = {
    "html": """
        <b>{Test Name}</b><br/>
        Country: {Country}<br/>
        Year: {Year}<br/>
        Yield: {Yield} kt<br/>
        Type: {Type}
    """,
    "style": {"backgroundColor": "black", "color": "white"}
}

st.markdown(f"**Showing {len(filtered)} explosions**")
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style="mapbox://styles/mapbox/dark-v10"
))
