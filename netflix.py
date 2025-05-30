import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), errors='coerce')
    df['year_added'] = df['date_added'].dt.year.astype('Int64')
    df['month_added'] = df['date_added'].dt.month
    df['director'].fillna("Not Specified", inplace=True)
    df['cast'].fillna("Not Specified", inplace=True)
    df['country'].fillna("Not Specified", inplace=True)
    df['rating'].fillna("Not Rated", inplace=True)
    df['duration'].fillna("Unknown", inplace=True)
    return df

df = load_data()

# Sidebar
st.sidebar.title("🔍 Filter Options")
st.sidebar.markdown("Use the filters below to customize the data view.")

# Filters
year_options = sorted(df['year_added'].dropna().unique().astype(int))
year_filter = st.sidebar.multiselect("Year Added", year_options, default=year_options)
type_filter = st.sidebar.multiselect("Type", df['type'].unique(), default=list(df['type'].unique()))

# Filtered Data
filtered_df = df[df['year_added'].isin(year_filter) & df['type'].isin(type_filter)]

# Title and Summary
st.title("🎬 Netflix Content Dashboard")
st.markdown("""
An interactive dashboard to explore Netflix's catalogue by type, year, country, rating, and genre.
""")

st.markdown(f"### Displaying {len(filtered_df)} titles")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
col3.metric("TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

# Charts
st.subheader("📊 Overview Visualizations")

# 1. Type Distribution
col1, col2 = st.columns(2)
with col1:
    fig = px.pie(filtered_df, names='type', title='Distribution by Content Type')
    st.plotly_chart(fig, use_container_width=True)

# 2. Top 10 Countries
with col2:
    top_countries = filtered_df['country'].value_counts().head(10)
    fig = px.bar(top_countries, title='Top 10 Countries by Content', labels={'value':'Count', 'index':'Country'})
    st.plotly_chart(fig, use_container_width=True)

# 3. Ratings Distribution
col3, col4 = st.columns(2)
with col3:
    top_ratings = filtered_df['rating'].value_counts().head(10)
    fig = px.bar(top_ratings, title='Top Ratings', labels={'value':'Count', 'index':'Rating'})
    st.plotly_chart(fig, use_container_width=True)

# 4. Yearly Additions
with col4:
    yearly_counts = filtered_df['year_added'].value_counts().sort_index()
    fig = px.line(x=yearly_counts.index.astype(int), y=yearly_counts.values, title='Content Added Over Years', labels={'x':'Year', 'y':'Count'})
    st.plotly_chart(fig, use_container_width=True)

# 5. Genre Distribution
st.subheader("🎭 Top Genres")
genres = ",".join(filtered_df['listed_in'].dropna()).split(',')
genre_counts = Counter([genre.strip() for genre in genres])
top_genres = pd.Series(genre_counts).sort_values(ascending=False).head(10)
fig = px.bar(top_genres, title='Top Genres', labels={'value':'Count', 'index':'Genre'})
st.plotly_chart(fig, use_container_width=True)


