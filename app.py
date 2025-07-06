import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Setting up the Streamlit page configuration
st.set_page_config(page_title="Financial Data Dashboard", layout="wide")

# Loading and cleaning the financial data
@st.cache_data
def load_data():
    df = pd.read_csv("data/financial.csv")
    
    # Cleaning data: Convert numeric columns and handle missing values
    numeric_columns = [
        'Age', 'Annual_Income', 'Monthly_Expenses', 'Savings_Rate',
        'Debt_to_Income_Ratio', 'Current_Investments_Value', 'Total_Loan_Amount',
        'Avg_Credit_Score', 'Inflation_Rate', 'Interest_Rate', 'Years_of_Employment',
        'Job_Stability_Score', 'Emergency_Fund_Value', 'Retirement_Fund_Contribution',
        'Future_Balance'
    ]
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Filling missing values with median for numeric columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
    
    # Ensuring categorical column is properly handled
    df['Customer_Segment'] = df['Customer_Segment'].fillna('Unknown')
    
    return df

# Loading the data
df = load_data()

# Creating the main title and sidebar
st.title("Financial Data Analysis Dashboard")
st.sidebar.header("Filter Options")

# Adding filters in the sidebar
age_range = st.sidebar.slider("Age Range", 
                             int(df['Age'].min()), 
                             int(df['Age'].max()), 
                             (int(df['Age'].min()), int(df['Age'].max())))
customer_segment = st.sidebar.multiselect("Customer Segment", 
                                        options=df['Customer_Segment'].unique(), 
                                        default=df['Customer_Segment'].unique())

# Filtering data based on user input
filtered_df = df[
    (df['Age'] >= age_range[0]) & 
    (df['Age'] <= age_range[1]) & 
    (df['Customer_Segment'].isin(customer_segment))
]

# Displaying summary statistics
st.header("Summary Statistics")
st.write(filtered_df.describe())

# Creating layout for visualizations
col1, col2 = st.columns(2)

# Plotting Income vs Expenses Scatter Plot
with col1:
    st.subheader("Annual Income vs Monthly Expenses")
    fig1 = px.scatter(filtered_df, 
                     x='Annual_Income', 
                     y='Monthly_Expenses', 
                     color='Customer_Segment',
                     size='Savings_Rate',
                     hover_data=['Age', 'Avg_Credit_Score'],
                     title="Income vs Expenses by Customer Segment")
    st.plotly_chart(fig1, use_container_width=True)

# Plotting Savings Rate Distribution by Segment
with col2:
    st.subheader("Savings Rate Distribution by Segment")
    fig2 = px.box(filtered_df, 
                  x='Customer_Segment', 
                  y='Savings_Rate',
                  title="Savings Rate by Customer Segment")
    st.plotly_chart(fig2, use_container_width=True)

# Plotting Debt-to-Income Ratio Histogram
st.subheader("Debt-to-Income Ratio Distribution")
fig3 = px.histogram(filtered_df, 
                   x='Debt_to_Income_Ratio',
                   nbins=30,
                   title="Distribution of Debt-to-Income Ratio",
                   color='Customer_Segment')
st.plotly_chart(fig3, use_container_width=True)

# Interesting Insight
st.header("Interesting Insight")
st.markdown("""
An interesting observation from the data: Customers in the **Gold** segment tend to have higher **Annual_Income** and **Current_Investments_Value** but show a wide range of **Debt_to_Income_Ratio**, indicating varied financial management practices. This could suggest opportunities for targeted financial advisory services for high-income individuals with higher debt ratios.
""")

# Displaying raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(filtered_df)


import os
print("Current working directory:", os.getcwd())
