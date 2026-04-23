import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="TCF Drawing Library", layout="wide")

st.title("📂 TCF Digital Library - Drawings & OneDrive Links")
st.markdown("Is dashboard ke zariye aap kisi bhi campus ki drawings aur unke OneDrive links dhoond sakte hain.")

# 1. Data Load karna
@st.cache_data
def load_data():
    # File name wahi rakhen jo aapne save ki hai
    df = pd.read_csv('fiinal_fixed_links.csv')
    return df

try:
    df = load_data()

    # 2. Sidebar Filters
    st.sidebar.header("Filter Options")
    
    # Campus Name Filter
    # Humein list mein se 'nan' hatane ke liye dropna() use karna hoga
    all_campuses = sorted(df['campus_name'].dropna().unique())
    selected_campus = st.sidebar.selectbox("Campus Select Karen:", ["All"] + list(all_campuses))

    # Discipline Filter
    all_disciplines = sorted(df['discipline'].dropna().unique())
    selected_discipline = st.sidebar.multiselect("Discipline Filter:", all_disciplines)

    # 3. Data Filtering Logic
    filtered_df = df.copy()
    
    if selected_campus != "All":
        filtered_df = filtered_df[filtered_df['campus_name'] == selected_campus]
    
    if selected_discipline:
        filtered_df = filtered_df[filtered_df['discipline'].isin(selected_discipline)]

    # 4. Display Results
    st.write(f"### Total Drawings Found: {len(filtered_df)}")

    # OneDrive link ko clickable banane ke liye formatting
    def make_clickable(link):
        if pd.isna(link) or link == "":
            return "No Link Available"
        return f'<a href="{link}" target="_blank">Open OneDrive Folder</a>'

    # Display Table
    # Hum sirf zaroori columns dikhayenge
    display_cols = ['campus_name', 'discipline', 'file_name', 'onedrive_link']
    
    # Clickable link apply karna
    display_df = filtered_df[display_cols].copy()
    display_df['onedrive_link'] = display_df['onedrive_link'].apply(make_clickable)

    # Table ko HTML mode mein dikhana taake links kaam karen
    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

except FileNotFoundError:
    st.error("Ghalti: 'final_fixed_links.csv' file nahi mili. Pehle file upload karen.")
