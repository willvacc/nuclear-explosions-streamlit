import pandas as pd
import streamlit as st

@st.cache_data
def load_explosions_data(path="data/nuclear_explosions.xlsx"):
    # Load the Excel file
    df = pd.read_excel(path)

    # Normalize column names
    df.columns = [col.strip().upper() for col in df.columns]

    # Rename key columns for easier access
    df = df.rename(columns={
        'WEAPON SOURCE COUNTRY': 'Country',
        'LOCATION': 'Location',
        'LOCATION.CORDINATES.LATITUDE': 'Latitude',
        'LOCATION.CORDINATES.LONGITUDE': 'Longitude',
        'DATA.MAGNITUDE.BODY': 'Magnitude_Body',
        'DATA.MAGNITUDE.SURFACE': 'Magnitude_Surface',
        'LOCATION.CORDINATES.DEPTH': 'Depth',
        'DATA.YEILD.LOWER': 'Yield_Lower',
        'DATA.YEILD.UPPER': 'Yield',
        'DATA.PURPOSE': 'Purpose',
        'DATA.NAME': 'Test Name',
        'DATA.TYPE': 'Type',
        'DATE.DAY': 'Day',
        'DATE.MONTH': 'Month',
        'DATE.YEAR': 'Year'
    })

    # Create a datetime column
    df['Date'] = pd.to_datetime(dict(year=df['Year'], month=df['Month'], day=df['Day']), errors='coerce')

    # Drop rows missing key location or date info
    return df.dropna(subset=['Latitude', 'Longitude', 'Year'])
