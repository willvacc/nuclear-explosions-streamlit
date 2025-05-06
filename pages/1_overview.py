import streamlit as st
from utils.data_loader import load_explosions_data

st.set_page_config(page_title="Overview", layout="wide")

df = load_explosions_data()

# Top section layout
top_left, top_right = st.columns([2, 1])

with top_left:
    st.title("👨🏻‍🔬 Overview of Nuclear Testing 👨🏻‍🔬")
    st.markdown("Use the filters in the sidebar to explore nuclear test data by country and year.")

with top_right:
    with st.expander("💡 Little Boy Bomb – Historical Context", expanded=False):
        st.image("pages/Little_Boy_bomb.jpg", caption="Little Boy Bomb - 1945", width=350)
        st.markdown("""
        **💡 Did you know?**  
        *Little Boy* was the first atomic bomb ever used in warfare, dropped on Hiroshima on August 6, 1945. It used uranium-235 and had a blast yield of around 15 kilotons.
        """)

# Filters and data
st.sidebar.subheader("Filter Data")

countries = st.sidebar.multiselect("Select Countries", options=df['Country'].unique(), default=["USA", "USSR"])
year_range = st.sidebar.slider("Year Range", int(df['Year'].min()), int(df['Year'].max()), (1945, 1990))

filtered_df = df[
    (df['Country'].isin(countries)) &
    (df['Year'].between(*year_range))
]

st.metric("Total Tests", len(filtered_df))
st.metric("Average Yield (kt)", round(filtered_df['Yield'].mean(), 2))

st.dataframe(filtered_df[['Country', 'Test Name', 'Year', 'Yield', 'Type']].sort_values(by='Year'))
