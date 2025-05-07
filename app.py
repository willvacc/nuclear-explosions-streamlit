# Name: Will Vaccari
# CS230: Section 1
# Data: Nuclear Explosions
# URL: https://nuclear-explosions-app-autotujh3tohqokkgdnz5k.streamlit.app
# Description: This program explores global nuclear test data from 1945–1998 using filters, maps, and charts.

import streamlit as st

st.set_page_config(page_title="Nuclear Explosions Explorer", page_icon="☢️", layout="wide")

# custom header and footer
st.markdown("""
    <style>
        .title {
            font-size: 48px;
            font-weight: bold;
            padding-top: 10px;
        }
        .subtitle {
            font-size: 20px;
            margin-top: -10px;
            color: #777;
        }
        .footer {
            margin-top: 80px;
            font-size: 16px;
            color: #888;
        }
    </style>
""", unsafe_allow_html=True)

# Main
emoji = "☢️"
title_html = f'<div class="title">{emoji} Nuclear Explosions Explorer {emoji}</div>'
st.markdown(title_html, unsafe_allow_html=True)
st.markdown('<div class="subtitle">⚛️Explore global nuclear test data from 1945–1998 with interactive maps and insights.⚛️</div>', unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.image("mushroom_cloud001.webp", width=400, caption="Castle Bravo Test - 1954")

with col2:
    st.markdown("""
    ### What You Can Do:
    🗺️ **Explore tests by country, year, and name**  
    📍 **Visualize locations and yields** on an interactive map  
    📊 **Analyze test trends and stats**  
    🔎 **Compare global nuclear activity**

    💡 **Did you know?** The largest nuclear test ever conducted was over 3,000 times more powerful than the Hiroshima bomb (The Tsar Bomb, detonated by the Soviet Union on October 30, 1961.)
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Exploring"):
        st.switch_page("pages/1_overview.py")

st.markdown('<div class="footer">Created by Will Vaccari • CS230 Final Project • Bentley University</div>', unsafe_allow_html=True)
