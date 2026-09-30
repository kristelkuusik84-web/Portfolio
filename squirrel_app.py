import streamlit as st
import pandas as pd
import plotly.express as px

# 1. VEEBILEHE SEADISTUS
st.set_page_config(page_title="Central Park Squirrel Tracker", layout="wide", page_icon="🐿️")

# KOHANDATUD STIIL (CSS) - Beež taust, oravapruun külgriba ja valged sisukaardid
st.markdown("""
    <style>
        /* Peamine taust (hele beež) */
        .stApp {
            background-color: #FDFBF7;
            color: #4A3B32;
        }
        /* Külgriba (oravapruun / šokolaadipruun) */
        section[data-testid="stSidebar"] {
            background-color: #5C4033 !important;
        }
        /* Külgriba tekstid valgeks */
        section[data-testid="stSidebar"] .css-17eq0hr, 
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p {
            color: #FFFFFF !important;
        }
        /* Külgriba pealkiri eraldi paksuks ja valgeks */
        div[data-testid="stSidebarHeader"] h2 {
            color: #FFFFFF !important;
        }
        /* Mõõdikute kastid (Metrics) ilusamaks ja loetavamaks */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #E8E2D9;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🐿️ Central Park Squirrel App")
st.markdown("Welcome to the squirrel observation data analysis app! Use the left panel to filter the data.")

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
    
    # ==========================================
    # KRIITILINE UUENDUS: FILTREERI "UNKNOWN" JA "?" VÄÄRTUSED
    # ==========================================
    # Määratleme vigased väärtused, mida soovime eemaldada
    invalid_values = ["Unknown", "?"]
    
    # Jätame alles ainult need read, mis EI SISALDA nimekirjas olevaid väärtusi
    full_df = full_df[
        (~full_df["Age"].astype(str).str.strip().isin(invalid_values)) &
        (~full_df["Primary_Fur_Color"].astype(str).str.strip().isin(invalid_values)) &
        (~full_df["Location"].astype(str).str.strip().isin(invalid_values))
    ]
    # ==========================================
    
    return full_df

df = load_clean_data()

# 3. KÜLGRIBA FILTRID (SIDEBAR)
st.sidebar.header("Filter Squirrels")

# Vanuse filter
age_options = ["All"] + list(df["Age"].dropna().unique())
selected_age = st.sidebar.selectbox("Select age:", age_options)

# Karva põhivärvuse filter
color_options = ["All"] + list(df["Primary_Fur_Color"].dropna().unique())
selected_color = st.sidebar.selectbox("Select fur color:", color_options)

# Päeva vahetuse filter (AM / PM)
shift_options = ["All"] + list(df["Shift"].dropna().unique())
selected_shift = st.sidebar.selectbox("Select day or night (AM/PM):", shift_options)

# FILTREERIMISE LOOGIKA
filtered_df = df.copy()
if selected_age != "All":
    filtered_df = filtered_df[filtered_df["Age"] == selected_age]
if selected_color != "All":
    filtered_df = filtered_df[filtered_df["Primary_Fur_Color"] == selected_color]
if selected_shift != "All":
    filtered_df = filtered_df[filtered_df["Shift"] == selected_shift]

# 4. PÕHILISED MÕÕDIKUD (METRICS)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total observations", len(filtered_df))
with col2:
    st.metric("Running squirrels", filtered_df["Running"].sum())
with col3:
    st.metric("Eating squirrels", filtered_df["Eating"].sum())
with col4:
    st.metric("Foraging squirrels", filtered_df["Foraging"].sum())

st.markdown("---")

# 5. INTERAKTIIVNE ASUKOHTADE KAART & GRAAFIKUD (KÕRVUTI)
chart_col, map_col = st.columns(2)

with chart_col:
    st.subheader("Primary squirrel activities")
    # Arvutame tegevuste summad filtreeritud andmetes
    activities = ["Running", "Chasing", "Climbing", "Eating", "Foraging"]
    activity_counts = filtered_df[activities].sum().reset_index()
    activity_counts.columns = ["Activity", "Count"]
    
    # ILUSAM GRAAFIK: Kohandatud oravatoonides värvipalett ja ümarad nurgad
    squirrel_colors = ["#8B5A2B", "#CD853F", "#E6A15C", "#D2B48C", "#BC8F8F"]
    
    fig_activity = px.bar(activity_counts, x="Activity", y="Count", 
                          color="Activity", 
                          color_discrete_sequence=squirrel_colors,
                          labels={"Count": "Number of squirrels", "Activity": "Activity"},
                          template="plotly_white")
    
    # Graafiku stiili peenhäälestus (taust läbipaistvaks, et ühtiks beežiga)
    fig_activity.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False  # Peidame legendi, kuna x-telg juba näitab tegevusi
    )
    st.plotly_chart(fig_activity, use_container_width=True)

with map_col:
    st.subheader("Squirrel locations in Central Park")
    # Streamlit vajab kaardi jaoks tulpasid nimega 'latitude' ja 'longitude'
    map_data = filtered_df[['Y', 'X']].dropna().rename(columns={'Y': 'latitude', 'X': 'longitude'})
    
    if not map_data.empty:
        st.map(map_data)
    else:
        st.warning("No location data found for the selected combination of filters.")

# 6. PUHASTATUD ANDMETABELI VAADE
st.markdown("---")
st.subheader("Cleaned data preview (Filtered results)")
st.dataframe(filtered_df[["Unique Squirrel ID", "Age", "Primary_Fur_Color", "Location", "Shift", "Running", "Eating"]].head(50))