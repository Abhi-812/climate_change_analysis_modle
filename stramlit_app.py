import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit app title and description
st.title("Climate Change Analysis: Global Land-Ocean Temperature Index")
st.write("This app visualizes the global temperature anomalies from 1880 to the present using NASA's data.")

# Load the dataset
url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
data = pd.read_csv(url, skiprows=1)

# Clean up and process the data
data = data.dropna(how='all', axis=1)  # Remove any columns with all NaN values
data.columns = ['Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'J-D', 'D-N', 'DJF', 'MAM', 'JJA', 'SON']

# Filter out rows that contain any non-numeric data (like headers or empty cells)
data = data[pd.to_numeric(data['Year'], errors='coerce').notnull()]

# Remove any non-numeric data from the 'J-D' column and convert to numeric
data['J-D'] = pd.to_numeric(data['J-D'], errors='coerce')  # Invalid parsing will be set as NaN
data = data.dropna(subset=['J-D'])  # Drop rows where 'J-D' is NaN

# Convert 'Year' column to int
data['Year'] = data['Year'].astype(int)

# Display first few rows
st.subheader("First few rows of the dataset")
st.write(data.head())

# Plot the global temperature anomaly over time
st.subheader("Annual Temperature Anomaly (1880-Present)")
plt.figure(figsize=(10, 6))
plt.plot(data['Year'], data['J-D'], label='Annual Temperature Anomaly (°C)', color='r')
plt.xlabel('Year')
plt.ylabel('Temperature Anomaly (°C)')
plt.title('Global Land-Ocean Temperature Index (1880-Present)')
plt.grid(True)
plt.legend()
st.pyplot(plt)

# Calculate temperature anomaly trend per decade
data['Decade'] = (data['Year'] // 10) * 10
decade_avg = data.groupby('Decade')['J-D'].mean()

# Plot the decade-wise temperature anomaly trend
st.subheader("Decade-wise Global Temperature Anomalies")
plt.figure(figsize=(10, 6))
plt.plot(decade_avg.index, decade_avg.values, marker='o', color='b')
plt.xlabel('Decade')
plt.ylabel('Avg Temperature Anomaly (°C)')
plt.title('Decade-wise Global Temperature Anomalies')
plt.grid(True)
st.pyplot(plt)

# Further analysis: Temperature anomaly difference
data['Temp_Difference'] = data['J-D'].diff()

# Plot temperature difference over time
st.subheader("Yearly Temperature Anomaly Difference (1880-Present)")
plt.figure(figsize=(10, 6))
plt.bar(data['Year'], data['Temp_Difference'], color='purple')
plt.xlabel('Year')
plt.ylabel('Temperature Anomaly Difference (°C)')
plt.title('Yearly Temperature Anomaly Difference (1880-Present)')
plt.grid(True)
st.pyplot(plt)

# Show summary statistics
st.subheader("Summary Statistics")
st.write(data[['J-D', 'Decade']].describe())
