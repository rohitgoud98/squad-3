import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Squad 3 Finance Dashboard",
    layout="wide"
)

st.title("💰 Squad 3 Finance Dashboard")

# ----------------------------------
# Load Data
# ----------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("Squad 3 Finances.xlsx")

df = load_data()

# ----------------------------------
# Sidebar Filters
# ----------------------------------
st.sidebar.header("Filters")

name_filter = st.sidebar.multiselect(
    "Select Member(s)",
    options=sorted(df["Name"].unique()),
    default=sorted(df["Name"].unique())
)

filtered_df = df[df["Name"].isin(name_filter)]

# ----------------------------------
# KPI Metrics
# ----------------------------------
st.subheader("Key Metrics")

total_members = filtered_df["Name"].nunique()
total_contribution = filtered_df["Contribution Available"].sum()
avg_contribution = filtered_df["Contribution Available"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("Total Members", total_members)
c2.metric("Total Contribution (₹)", f"{total_contribution:,.0f}")
c3.metric("Average Contribution (₹)", f"{avg_contribution:,.0f}")

# ----------------------------------
# Contribution by Member
# ----------------------------------
st.subheader("Contribution by Member")

fig = px.bar(
    filtered_df,
    x="Name",
    y="Contribution Available",
    text="Contribution Available",
    title="Member-wise Contribution",
    labels={"Contribution Available": "Amount (₹)"}
)

fig.update_traces(textposition="outside")
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Top Contributors
# ----------------------------------
st.subheader("Top Contributors")

top_df = (
    filtered_df
    .sort_values("Contribution Available", ascending=False)
    .head(5)
)

fig2 = px.bar(
    top_df,
    x="Contribution Available",
    y="Name",
    orientation="h",
    color="Contribution Available",
    title="Top 5 Contributors",
    labels={"Contribution Available": "Amount (₹)"}
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# Data Table
# ----------------------------------
with st.expander("📄 View Full Data"):
    st.dataframe(filtered_df)

# ----------------------------------
# Footer
# ----------------------------------
st.markdown("---")
st.caption("Squad 3 | Finance Dashboard | Built with Streamlit & Plotly")
