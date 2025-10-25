# ==========================================================
# 🍏 APPLE GLOBAL SALES DASHBOARD 2024 — Power BI Style
# ==========================================================
 
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Apple Global Sales Dashboard",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Power BI-like styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f1f1f;
        font-weight: 700;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #0078D4;
    }
    .plot-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("apple_sales_dataset_1000.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.quarter
    return df

df = load_data()

# -----------------------------
# Sidebar Filters - Power BI Style
# -----------------------------
st.sidebar.markdown("### 🎛️ FILTERS")

# Region filter with select all option
st.sidebar.markdown("**Regions**")
all_regions = st.sidebar.checkbox("Select All Regions", value=True)
if all_regions:
    regions = st.sidebar.multiselect(
        "Select Region(s)",
        options=df['Region'].unique(),
        default=df['Region'].unique(),
        label_visibility="collapsed"
    )
else:
    regions = st.sidebar.multiselect(
        "Select Region(s)",
        options=df['Region'].unique(),
        label_visibility="collapsed"
    )

# Category filter
st.sidebar.markdown("**Categories**")
all_categories = st.sidebar.checkbox("Select All Categories", value=True)
if all_categories:
    categories = st.sidebar.multiselect(
        "Select Category(ies)",
        options=df['Category'].unique(),
        default=df['Category'].unique(),
        label_visibility="collapsed"
    )
else:
    categories = st.sidebar.multiselect(
        "Select Category(ies)",
        options=df['Category'].unique(),
        label_visibility="collapsed"
    )

# Customer Segment filter
st.sidebar.markdown("**Customer Segments**")
all_segments = st.sidebar.checkbox("Select All Segments", value=True)
if all_segments:
    segments = st.sidebar.multiselect(
        "Select Customer Segment(s)",
        options=df['CustomerSegment'].unique(),
        default=df['CustomerSegment'].unique(),
        label_visibility="collapsed"
    )
else:
    segments = st.sidebar.multiselect(
        "Select Customer Segment(s)",
        options=df['CustomerSegment'].unique(),
        label_visibility="collapsed"
    )

# Date Range Filter
st.sidebar.markdown("**Date Range**")
min_date = df['Date'].min()
max_date = df['Date'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    label_visibility="collapsed"
)

# Year and Quarter filters
st.sidebar.markdown("**Time Period**")
years = st.sidebar.multiselect(
    "Select Year(s)",
    options=sorted(df['Year'].unique()),
    default=sorted(df['Year'].unique())
)

quarters = st.sidebar.multiselect(
    "Select Quarter(s)",
    options=sorted(df['Quarter'].unique()),
    default=sorted(df['Quarter'].unique())
)

# -----------------------------
# Apply Filters
# -----------------------------
start_date = pd.to_datetime(date_range[0]) if len(date_range) > 0 else min_date
end_date = pd.to_datetime(date_range[1]) if len(date_range) > 1 else max_date

df_filtered = df[
    (df['Region'].isin(regions)) &
    (df['Category'].isin(categories)) &
    (df['CustomerSegment'].isin(segments)) &
    (df['Year'].isin(years)) &
    (df['Quarter'].isin(quarters)) &
    (df['Date'].between(start_date, end_date))
]

# -----------------------------
# Dashboard Header
# -----------------------------
st.markdown('<h1 class="main-header">🍎 APPLE GLOBAL SALES DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive Business Intelligence Dashboard | 2024 Performance Overview</p>', unsafe_allow_html=True)

# -----------------------------
# KPI Metrics - Power BI Style Cards
# -----------------------------
total_revenue = df_filtered['TotalRevenue'].sum()
total_orders = df_filtered['OrderID'].nunique()
avg_order_value = df_filtered['TotalRevenue'].mean()

# Check if we have any additional numeric columns for more KPIs
numeric_columns = df_filtered.select_dtypes(include=['number']).columns.tolist()
available_columns = df_filtered.columns.tolist()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("💰 TOTAL REVENUE", f"${total_revenue:,.0f}", delta=None)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🛍️ TOTAL ORDERS", f"{total_orders:,}", delta=None)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("📦 AVG ORDER VALUE", f"${avg_order_value:,.0f}", delta=None)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# First Row: Revenue Overview
# -----------------------------
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    # Monthly Trend with Region Breakdown
    monthly_region = df_filtered.groupby(['Month', 'Region'])['TotalRevenue'].sum().reset_index()
    fig_trend = px.line(
        monthly_region, x='Month', y='TotalRevenue', color='Region',
        title='📈 MONTHLY REVENUE TREND BY REGION',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_trend.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    fig_trend.update_traces(line=dict(width=3))
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    # Revenue by Category
    category_rev = df_filtered.groupby('Category', as_index=False)['TotalRevenue'].sum()
    fig_cat = px.pie(
        category_rev, names='Category', values='TotalRevenue',
        title='🧩 REVENUE BY CATEGORY',
        color_discrete_sequence=px.colors.qualitative.Vivid,
        hole=0.4
    )
    fig_cat.update_traces(textposition='inside', textinfo='percent+label')
    fig_cat.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Second Row: Performance Analysis
# -----------------------------
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    # Top Products
    top_products = (
        df_filtered.groupby('Product', as_index=False)['TotalRevenue']
        .sum()
        .sort_values(by='TotalRevenue', ascending=False)
        .head(10)
    )
    fig_prod = px.bar(
        top_products, x='TotalRevenue', y='Product', orientation='h',
        title='🏆 TOP 10 PRODUCTS BY REVENUE',
        color='TotalRevenue', color_continuous_scale='Sunset'
    )
    fig_prod.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title="Total Revenue ($)",
        yaxis_title=""
    )
    st.plotly_chart(fig_prod, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    # Customer Segment Breakdown
    segment_rev = df_filtered.groupby('CustomerSegment', as_index=False)['TotalRevenue'].sum()
    fig_segment = px.bar(
        segment_rev, x='CustomerSegment', y='TotalRevenue',
        title='🎯 REVENUE BY CUSTOMER SEGMENT',
        color='TotalRevenue', color_continuous_scale='Tealgrn'
    )
    fig_segment.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title="Customer Segment",
        yaxis_title="Total Revenue ($)"
    )
    st.plotly_chart(fig_segment, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Third Row: Additional Insights
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    # Payment Method Distribution
    payment_counts = df_filtered['PaymentMethod'].value_counts().reset_index()
    payment_counts.columns = ['PaymentMethod', 'Count']
    
    fig_payment = px.pie(
        payment_counts, names='PaymentMethod', values='Count',
        title='💳 PAYMENT METHOD DISTRIBUTION',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_payment.update_traces(textposition='inside', textinfo='percent+label')
    fig_payment.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    st.plotly_chart(fig_payment, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    # Top Stores
    store_rev = df_filtered.groupby('Store', as_index=False)['TotalRevenue'].sum().sort_values(by='TotalRevenue', ascending=False).head(10)
    fig_store = px.bar(
        store_rev, x='TotalRevenue', y='Store', orientation='h',
        title='🏢 TOP 10 STORES BY REVENUE',
        color='TotalRevenue', color_continuous_scale='Cividis'
    )
    fig_store.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title="Total Revenue ($)",
        yaxis_title=""
    )
    st.plotly_chart(fig_store, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])

with footer_col1:
    st.markdown("**📊 DATA SOURCE:** Apple Sales Dataset | **🔄 LAST UPDATED:** Current | **📈 DATA POINTS:** " + f"{len(df_filtered):,}")

with footer_col2:
    st.markdown("**👨‍💻 CREATED BY:** Bouyahia Yassine")

with footer_col3:
    st.markdown("**🔢 VERSION:** 1.0")