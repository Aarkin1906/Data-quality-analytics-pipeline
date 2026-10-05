import os
import duckdb
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Streamlit Page Setup
st.set_page_config(
    page_title="YouTube Executive Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "database/youtube_analytics.duckdb"

# Check Database Existence
if not os.path.exists(DB_PATH):
    st.error("⚠️ DuckDB Database file not found! Please run `python pipeline.py` first to generate data.")
    st.stop()

# Connect to DuckDB
@st.cache_resource
def get_connection():
    return duckdb.connect(DB_PATH, read_only=True)

conn = get_connection()

# Load Main Data
df = conn.execute("SELECT * FROM youtube_analytics").fetchdf()

# Detect Columns Dynamically
cat_col = 'category' if 'category' in df.columns else ('category_id' if 'category_id' in df.columns else None)
title_col = 'title' if 'title' in df.columns else 'video_id'

# -------------------------------------------------------------------
# SIDEBAR FILTERS (INTERACTIVE)
# -------------------------------------------------------------------
st.sidebar.header("🎯 Interactive Filters")

selected_category = "All"
if cat_col:
    categories = ["All"] + sorted(list(df[cat_col].unique()))
    selected_category = st.sidebar.selectbox("Filter by Category", categories)

# Apply Category Filter
if selected_category != "All":
    filtered_df = df[df[cat_col] == selected_category]
else:
    filtered_df = df.copy()

# Search Bar Filter
search_query = st.sidebar.text_input("🔍 Search Video Title", "")
if search_query:
    filtered_df = filtered_df[filtered_df[title_col].str.contains(search_query, case=False, na=False)]

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use the sidebar to filter data dynamically in real-time.")

# -------------------------------------------------------------------
# MAIN DASHBOARD HEADER
# -------------------------------------------------------------------
st.title("🎬 YouTube Content Analytics & Pipeline Dashboard")
st.markdown("Interactive performance overview powered by **DuckDB** and **Plotly**.")
st.divider()

# -------------------------------------------------------------------
# METRIC CARDS (KPIs)
# -------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_vids = len(filtered_df)
total_views = int(filtered_df['views'].sum()) if 'views' in filtered_df else 0
total_likes = int(filtered_df['likes'].sum()) if 'likes' in filtered_df else 0
avg_engagement = (total_likes / total_views * 100) if total_views > 0 else 0

col1.metric("Total Videos Analyzed", f"{total_vids:,}")
col2.metric("Total Views", f"{total_views:,}")
col3.metric("Total Likes", f"{total_likes:,}")
col4.metric("Avg Engagement Rate", f"{avg_engagement:.2f}%")

st.divider()

# -------------------------------------------------------------------
# INTERACTIVE CHARTS (ROW 1)
# -------------------------------------------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("🔥 Top Categories by Views")
    if cat_col:
        cat_agg = filtered_df.groupby(cat_col)['views'].sum().reset_index()
        cat_agg = cat_agg.sort_values(by='views', ascending=False)
        
        fig_bar = px.bar(
            cat_agg,
            x=cat_col,
            y='views',
            color='views',
            color_continuous_scale='Viridis',
            labels={cat_col: "Category", "views": "Total Views"},
            text_auto='.2s'
        )
        fig_bar.update_layout(xaxis_title="", yaxis_title="Views", showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    st.subheader("💡 Engagement Rate vs Views")
    if 'views' in filtered_df and 'likes' in filtered_df:
        filtered_df['engagement_pct'] = (filtered_df['likes'] / filtered_df['views']) * 100
        
        fig_scatter = px.scatter(
            filtered_df,
            x='views',
            y='engagement_pct',
            size='likes',
            color=cat_col if cat_col else None,
            hover_name=title_col,
            log_x=True,
            labels={"views": "Views (Log Scale)", "engagement_pct": "Engagement Rate (%)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# -------------------------------------------------------------------
# DYNAMIC DATA TABLE & TOP PERFORMERS (ROW 2)
# -------------------------------------------------------------------
st.subheader("🏆 Leaderboard: Top Performing Videos")

max_limit = len(filtered_df) if len(filtered_df) > 0 else 5
default_slider = min(5, max_limit)

top_n = st.slider("Select number of top videos to display:", min_value=1, max_value=max_value if (max_value := max(max_limit, 5)) else 5, value=default_slider)

display_df = filtered_df.sort_values(by='views', ascending=False).head(top_n)

# Format table display
show_cols = [title_col]
if cat_col and cat_col in display_df.columns:
    show_cols.append(cat_col)
show_cols.extend(['views', 'likes'])

if 'engagement_pct' in display_df.columns:
    show_cols.append('engagement_pct')

final_table = display_df[show_cols].rename(columns={
    title_col: "Video Title",
    cat_col: "Category",
    "views": "Views",
    "likes": "Likes",
    "engagement_pct": "Engagement (%)"
})

st.dataframe(
    final_table.style.format({
        "Views": "{:,}",
        "Likes": "{:,}",
        "Engagement (%)": "{:.2f}%"
    }),
    use_container_width=True
)

st.caption(f"Showing Top {min(top_n, len(filtered_df))} out of {len(filtered_df)} filtered videos.")