import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_csv("employee_attrition_cleaned.csv")

# Streamlit Config
st.set_page_config(layout="wide", page_title="Employee Attrition Dashboard")

#color_palette
color_palette = [
       "#4A6369",
       "#AB5852",
       "#D49C47",
       "#838469",
       "#D2C38B"]

st.markdown("""
<style>
body {
    background-color: #121212;
    color: #f0f0f0;
}
h1, h2, h3, h4 {
    color: #708090;
}
.metric-card {
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #333;
    text-align: center;
}
thead, tbody, tfoot, tr, td, th {
    color: #708090;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>Employee Attrition Dashboard</h1>", unsafe_allow_html=True)
st.markdown("Interactive dashboard exploring attrition through various factors.")

# Sidebar Filters
st.sidebar.header("Filters")
gender = st.sidebar.selectbox("Gender", ["All"] + sorted(df["gender"].unique()))
job_role = st.sidebar.selectbox("Job Role", ["All"] + sorted(df["job_role"].unique()))
marital_status = st.sidebar.selectbox("Marital Status", ["All"] + sorted(df["marital_status"].unique()))
remote_work = st.sidebar.selectbox("Remote Work", ["All"] + sorted(df["remote_work"].unique()))
attrition = st.sidebar.selectbox("Attrition", ["All"] + sorted(df["attrition"].unique()))
min_income = int(df["monthly_income"].min())
max_income = int(df["monthly_income"].max())

income_range = st.sidebar.slider(
    "Monthly Income Range",
    min_value=min_income,
    max_value=max_income,
    value=(min_income, max_income),
    step=100)

# Apply filters
filtered_df = df.copy()
if gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == gender]
if job_role != "All":
    filtered_df = filtered_df[filtered_df["job_role"] == job_role]
if marital_status != "All":
    filtered_df = filtered_df[filtered_df["marital_status"] == marital_status]
if remote_work != "All":
    filtered_df = filtered_df[filtered_df["remote_work"] == remote_work]
if attrition != "All":
    filtered_df = filtered_df[filtered_df["attrition"] == attrition]
filtered_df = filtered_df[
    (filtered_df["monthly_income"] >= income_range[0]) &
    (filtered_df["monthly_income"] <= income_range[1])]

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><h5>Total Employees</h5><h2>{len(filtered_df):,}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h5>Avg Monthly Income</h5><h2>${filtered_df['monthly_income'].mean():,.0f}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h5>Avg Years at Company</h5><h2>{filtered_df['years_at_company'].mean():.1f}</h2></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><h5>Avg Distance from Home</h5><h2>{filtered_df['distance_from_home'].mean():.1f} km</h2></div>", unsafe_allow_html=True)

# Tabs Setup
tabs = st.tabs([
    "Demographics",
    "Job Details",
    "Compensation",
    "Education & Performance",
    "Work Habits",
    "Recognition & Retention"
])

# DEMOGRAPHICS TAB
with tabs[0]:
    st.header("Demographics")
    columns = ["gender", "marital_status","age", "number_of_dependents"]
    st.subheader(f"Summary Statistics for: {', '.join(columns)}")
    st.dataframe(filtered_df[columns].describe(include='all').transpose(), use_container_width=True)


    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Age Distribution")
        st.plotly_chart(px.histogram(
        filtered_df,x="age",color="attrition",nbins=30,barmode="group",color_discrete_sequence=color_palette),use_container_width=True)        
        st.subheader("Number of Dependents by Attrition")
        st.plotly_chart(px.box(filtered_df,x="attrition",y="number_of_dependents",color="attrition",color_discrete_sequence=color_palette),use_container_width=True)
    with col2:
        st.subheader("Gender Distribution")
        st.plotly_chart(px.pie(filtered_df, names="gender", hole=0.3, color_discrete_sequence=color_palette), use_container_width=True)
        st.subheader("Attrition by Marital Status")
        st.plotly_chart(px.bar(filtered_df, x="marital_status", color="attrition", barmode="group",color_discrete_sequence=color_palette), use_container_width=True)

# JOB DETAILS TAB
with tabs[1]:
    st.header("Job Details")
    columns = ["job_role", "job_level", "years_at_company"]
    st.subheader(f"Summary Statistics for: {', '.join(columns)}")
    st.dataframe(filtered_df[columns].describe(include='all').transpose(), use_container_width=True)


    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Years at Company")
        st.plotly_chart(px.histogram(filtered_df, x="years_at_company", nbins=20 ,color_discrete_sequence=[color_palette[4]]), use_container_width=True)
        st.subheader("Years at Company by Attrition")
        st.plotly_chart(
            px.box(filtered_df,x="attrition",y="years_at_company",color="attrition",color_discrete_sequence=color_palette),use_container_width=True) 
    with col2:
        st.subheader("Job Role Distribution")
        job_role_counts = filtered_df["job_role"].value_counts().reset_index()
        job_role_counts.columns = ["job_role", "count"]

        st.plotly_chart(px.bar( job_role_counts,x="job_role", y="count",
                color="job_role",color_discrete_sequence=color_palette),use_container_width=True)
        st.subheader("Job Level Distribution")
        st.plotly_chart(px.pie(filtered_df, names="job_level" ,color_discrete_sequence=color_palette), use_container_width=True)

# COMPENSATION TAB
with tabs[2]:
    st.header("Compensation")
    columns = [ "income_category","monthly_income"]
    st.subheader(f"Summary Statistics for: {', '.join(columns)}")
    st.dataframe(filtered_df[columns].describe(include='all').transpose(), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Monthly Income Distribution")
        st.plotly_chart(px.histogram(filtered_df, x="monthly_income", nbins=50 ,color_discrete_sequence=[color_palette[2]]), use_container_width=True)
    with col2:
        st.subheader("Income Category Distribution")
        st.plotly_chart(px.pie(filtered_df, names="income_category", hole=0.4 ,color_discrete_sequence=color_palette), use_container_width=True)

# EDUCATION & PERFORMANCE TAB
with tabs[3]:
    st.header("Education & Performance")
    columns = ["education_level", "performance_rating", "job_satisfaction", "work-life_balance"]
    st.subheader(f"Summary Statistics for: {', '.join(columns)}")
    st.dataframe(filtered_df[columns].describe(include='all').transpose(), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Job Satisfaction by Attrition")
        st.plotly_chart(px.histogram(filtered_df,x="job_satisfaction",color="attrition",nbins=10,barmode="group",color_discrete_sequence=color_palette),use_container_width=True)
        st.subheader("Work-Life Balance by Attrition")
        st.plotly_chart(px.histogram(filtered_df, x="work-life_balance", color="attrition", barmode="group" ,color_discrete_sequence=color_palette), use_container_width=True)
        st.subheader("Performance Rating by Attrition")
        st.plotly_chart(px.histogram(
        filtered_df,x="performance_rating",color="attrition",barmode="group",color_discrete_sequence=color_palette),use_container_width=True)
    with col2:
        st.subheader("Education Level Distribution")
        st.plotly_chart(px.pie(filtered_df, names="education_level", hole=0.3 ,color_discrete_sequence=color_palette), use_container_width=True)
        st.subheader("Job Satisfaction")
        st.plotly_chart(px.histogram(filtered_df, x="job_satisfaction", nbins=10 ,color = "job_satisfaction" , color_discrete_sequence=color_palette), use_container_width=True)
        st.subheader("Performance Rating")
        performance_counts = filtered_df["performance_rating"].value_counts().reset_index()
        performance_counts.columns = ["performance_rating", "count"]
        st.plotly_chart(px.pie(performance_counts,names="performance_rating",values="count",color_discrete_sequence=color_palette,hole=0.3),use_container_width=True)

# WORK HABITS TAB
with tabs[4]:
    st.header("Work Habits")
    columns = ["overtime", "remote_work", "distance_from_home", "number_of_promotions"]
    st.subheader(f"Summary Statistics for: {', '.join(columns)}")
    st.dataframe(filtered_df[columns].describe(include='all').transpose(), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distance from Home by Attrition")
        st.plotly_chart(px.histogram(
                filtered_df,x="distance_from_home",color="attrition",nbins=20,barmode="group",color_discrete_sequence=color_palette),use_container_width=True) 
        st.subheader("Promotions by Job Level")
        st.plotly_chart(px.box(filtered_df, x="job_level", y="number_of_promotions", color="job_level" ,color_discrete_sequence=color_palette), use_container_width=True)
    with col2:
        st.subheader("Remote Work Distribution")
        st.plotly_chart(px.bar(filtered_df, x="remote_work", color="attrition", barmode="group",color_discrete_sequence=color_palette), use_container_width=True)
        st.subheader("Overtime and Attrition")
        st.plotly_chart(px.histogram(filtered_df, x="overtime", color="attrition", barmode="group" ,color_discrete_sequence=color_palette), use_container_width=True)

# RECOGNITION & RETENTION TAB
with tabs[5]:
    st.header("Recognition & Retention")
    columns = ["employee_recognition", "attrition", "hiring_year"]
    st.subheader(f"Summary Statistics for: {', '.join(columns)}")
    st.dataframe(filtered_df[columns].describe(include='all').transpose(), use_container_width=True)
    
    hires_by_year = filtered_df["hiring_year"].value_counts().reset_index().sort_values("index")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Recognition Distribution")
        st.plotly_chart(px.histogram(filtered_df, x="employee_recognition", color="attrition", barmode="group" ,color_discrete_sequence=color_palette), use_container_width=True)

        st.subheader("Hires by Year")
        hires_by_year = filtered_df["hiring_year"].value_counts().reset_index().sort_values("index")
        hires_by_year.columns = ["Year", "Count"]
        st.plotly_chart(px.bar(hires_by_year, x="Year", y="Count", text="Count",color_discrete_sequence=[color_palette[2]]), use_container_width=True)

    with col2:
        st.subheader("Attrition over Hiring Years")
        st.plotly_chart(px.histogram(filtered_df, x="hiring_year", color="attrition", barmode="group",color_discrete_sequence=color_palette), use_container_width=True)

        st.subheader("Attrition Distribution")
        attrition_counts = filtered_df["attrition"].value_counts().reset_index()
        attrition_counts.columns = ["attrition", "count"]
        st.plotly_chart(px.pie(attrition_counts,names="attrition",values="count",hole=0.4,color_discrete_sequence=color_palette),
            use_container_width=True)
