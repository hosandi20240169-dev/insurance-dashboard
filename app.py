import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Insurance Analytics Dashboard",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_insurance.csv")

df = load_data()

# =====================================
# DASHBOARD TITLE
# =====================================

st.title("Insurance Website Analytics Dashboard")

st.write(
    """
    This dashboard provides insights into insurance website performance,
    marketing channels, customer engagement, policy purchases and revenue.
    """
)

# =====================================
# SIDEBAR FILTERS
# =====================================

st.sidebar.header("Filters")

selected_channels = st.sidebar.multiselect(
    "Select Marketing Channel",
    options=df["Marketing_Channel"].unique(),
    default=df["Marketing_Channel"].unique()
)

selected_devices = st.sidebar.multiselect(
    "Select Device Category",
    options=df["Device_Category"].unique(),
    default=df["Device_Category"].unique()
)

filtered_df = df[
    (df["Marketing_Channel"].isin(selected_channels)) &
    (df["Device_Category"].isin(selected_devices))
]

# =====================================
# KPI SECTION
# =====================================

st.subheader("Key Performance Indicators")

total_users = int(filtered_df["Users"].sum())
total_revenue = filtered_df["Revenue"].sum()
total_quotes = int(filtered_df["Insurance_Quotes"].sum())
total_policies = int(filtered_df["Policies_Purchased"].sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Users", f"{total_users:,}")
col2.metric("Total Revenue (£)", f"{total_revenue:,.2f}")
col3.metric("Insurance Quotes", f"{total_quotes:,}")
col4.metric("Policies Purchased", f"{total_policies:,}")

st.markdown("---")

# =====================================
# BAR CHART
# USERS BY MARKETING CHANNEL
# =====================================

st.subheader("Users by Marketing Channel")

channel_users = (
    filtered_df.groupby("Marketing_Channel")["Users"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    channel_users,
    x="Marketing_Channel",
    y="Users",
    title="Users by Marketing Channel"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================
# PIE CHART
# DEVICE DISTRIBUTION
# =====================================

st.subheader("User Distribution by Device Category")

device_distribution = (
    filtered_df.groupby("Device_Category")["Users"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    device_distribution,
    values="Users",
    names="Device_Category",
    title="User Distribution by Device Category"
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================
# SCATTER PLOT
# QUOTES VS PURCHASES
# =====================================

st.subheader("Insurance Quotes vs Policies Purchased")

fig3 = px.scatter(
    filtered_df,
    x="Insurance_Quotes",
    y="Policies_Purchased",
    color="Marketing_Channel",
    title="Insurance Quotes vs Policies Purchased"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================
# BOX PLOT
# SESSION DURATION
# =====================================

st.subheader("Average Session Duration by Marketing Channel")

fig4 = px.box(
    filtered_df,
    x="Marketing_Channel",
    y="Avg_Session_Duration",
    title="Average Session Duration by Marketing Channel"
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================
# HISTOGRAM
# REVENUE DISTRIBUTION
# =====================================

st.subheader("Revenue Distribution")

fig5 = px.histogram(
    filtered_df,
    x="Revenue",
    nbins=20,
    title="Revenue Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# =====================================
# DATA TABLE
# =====================================

st.subheader("Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================================
# DOWNLOAD FILTERED DATA
# =====================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_insurance_data.csv",
    mime="text/csv"
)

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.write("Business Data Analytics Dashboard")