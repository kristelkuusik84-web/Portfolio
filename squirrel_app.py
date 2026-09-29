import streamlit as st
import pandas as pd
import plotly.express as px

# 1. VEEBILEHE SEADISTUS
st.set_page_config(page_title="Central Park Squirrel Tracker", layout="wide", page_icon="🐿️")

st.title("🐿️ Central Park Squirrel App")
st.markdown("Tere tulemast oravate vaatlusandmete analüüsi rakendusse! Kasuta vasakpoolset paneeli andmete filtreerimiseks.")

# 2. ANDMETE LAADIMINE MÄLLU (Võetakse sinu loodud dim/fact mudel)
@st.cache_data
def load_clean_data():
    fact = pd.read_csv("fact_observations.csv")
    dim_sq = pd.read_csv("dim_squirrel.csv")
    dim_loc = pd.read_csv("dim_location.csv")
    dim_t = pd.read_csv("dim_time.csv")
    
    # Liidame dimensioonid faktitabeliga kokku, et filtreerimine ja graafikud töötaksid sujuvalt
    full_df = fact.merge(dim_sq, on="Squirrel_Profile_ID", how="left")
    full_df = full_df.merge(dim_loc, on="Location_ID", how="left")
    full_df = full_df.merge(dim_t, on="Time_ID", how="left")
    return full_df

df = load_clean_data()

# 3. KÜLGRIBA FILTRID (SIDEBAR)
st.sidebar.header("Filtreeri oravaid")

# Vanuse filter
age_options = ["Kõik"] + list(df["Age"].unique())
selected_age = st.sidebar.selectbox("Vali vanus:", age_options)

# Karva põhivärvuse filter
color_options = ["Kõik"] + list(df["Primary_Fur_Color"].unique())
selected_color = st.sidebar.selectbox("Vali karva põhivärv:", color_options)

# Päeva vahetuse filter (AM / PM)
shift_options = ["Kõik"] + list(df["Shift"].unique())
selected_shift = st.sidebar.selectbox("Vali päeva vahetus (AM/PM):", shift_options)

# FILTREERIMISE LOOGIKA
filtered_df = df.copy()
if selected_age != "Kõik":
    filtered_df = filtered_df[filtered_df["Age"] == selected_age]
if selected_color != "Kõik":
    filtered_df = filtered_df[filtered_df["Primary_Fur_Color"] == selected_color]
if selected_shift != "Kõik":
    filtered_df = filtered_df[filtered_df["Shift"] == selected_shift]

# 4. PÕHILISED MÕÕDIKUD (METRICS)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Vaatlusi kokku", len(filtered_df))
with col2:
    st.metric("Jooksvaid oravaid", filtered_df["Running"].sum())
with col3:
    st.metric("Söövaid oravaid", filtered_df["Eating"].sum())
with col4:
    st.metric("Toiduotsinguil (Foraging)", filtered_df["Foraging"].sum())

st.markdown("---")

# 5. INTERAKTIIVNE ASUKOHTADE KAART & GRAAFIKUD (KÕRVUTI)
chart_col, map_col = st.columns([1, 1])

with chart_col:
    st.subheader("Oravate peamised tegevused")
    # Arvutame tegevuste summad filtreeritud andmetes
    activities = ["Running", "Chasing", "Climbing", "Eating", "Foraging"]
    activity_counts = filtered_df[activities].sum().reset_index()
    activity_counts.columns = ["Tegevus", "Arv"]
    
    fig_activity = px.bar(activity_counts, x="Tegevus", y="Arv", 
                          color="Tegevus", labels={"Arv": "Oravate arv"},
                          template="plotly_white")
    st.plotly_chart(fig_activity, use_container_width=True)

with map_col:
    st.subheader("Oravate asukohad Central Parkis")
    # Streamlit vajab kaardi jaoks tulpasid nimega 'latitude' ja 'longitude'
    map_data = filtered_df[['Y', 'X']].dropna().rename(columns={'Y': 'latitude', 'X': 'longitude'})
    
    if not map_data.empty:
        st.map(map_data)
    else:
        st.warning("Valitud filtrite kombinatsiooniga asukohaandmeid ei leitud.")

# 6. PUHASTATUD ANDMETABELI VAADE
st.markdown("---")
st.subheader("Puhastatud andmete eelvaade (Filtreeritud tulemus)")
st.dataframe(filtered_df[["Unique Squirrel ID", "Age", "Primary_Fur_Color", "Location", "Shift", "Running", "Eating"]].head(50))