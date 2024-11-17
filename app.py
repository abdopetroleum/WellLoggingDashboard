import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from WellLogPlotter import WellLogPlotter  # Assuming the class is in a file named WellLogPlotter.py
from Calculations import process_well_data_optimized
from SecondWellLogPlotter import SecondWellLogPlotter

# Load data
file_path = 'Work_data.xlsx'  # Use the actual path to your file
df = pd.read_excel(file_path, sheet_name='All_Wells')
inputs_df= pd.read_excel('Raster_logs_data.xlsx')

# Sidebar: Well Selection
st.sidebar.header("Well Selection")
well_names = df['Well_Name'].unique()
selected_well = st.sidebar.selectbox('Select Well Name', well_names)

# Filter data based on selected well
filtered_df = df[df['Well_Name'] == selected_well]

# Sidebar: Mandatory Data Inputs
st.sidebar.header("Mandatory Data")
ssp = st.sidebar.slider('SSP', min_value=-110, max_value=-10, value=-100, step=1)
sp_baseline = st.sidebar.number_input('SP Baseline', value=0, format="%d")
shale_phid = st.sidebar.slider('Shale Density Porosity', min_value=0.0, max_value=0.5, value=0.2, step=0.01)
shale_phi_n = st.sidebar.slider('Shale Neutron Porosity', min_value=0.0, max_value=0.5, value=0.3, step=0.01)

# Sidebar: Optional Data Inputs
st.sidebar.header("Optional Data")
rw = st.sidebar.number_input('Rw', value=0.05, format="%.2f")
temp_rw = st.sidebar.number_input('Temp Rw', value=78, format="%d")
a = st.sidebar.slider('a', min_value=0.3, max_value=2.0, value=1.0, step=0.01)
m = st.sidebar.slider('m', min_value=1.0, max_value=3.0, value=2.0, step=0.01)
n = st.sidebar.slider('n', min_value=1.0, max_value=3.0, value=2.0, step=0.01)
maximum_gr = st.sidebar.number_input('Maximum GR', value=150, format="%d")
minimum_gr = st.sidebar.number_input('Minimum GR', value=15, format="%d")
sp_shift = st.sidebar.slider('SP Shift', min_value=-100, max_value=100, value=0, step=1)
rza = st.sidebar.number_input('Rza (Optional)', value=None, step=0.01, format="%.2f", key='rza_input') if st.sidebar.checkbox('Provide Rza') else None
invasion = st.sidebar.selectbox('Invasion (Optional)', [None, 'very deep', 'deep', 'average', 'shallow', 'very shallow'], index=0)
# Depth inputs for scatter plot
st.sidebar.header("Depth Range for BVW Scatter Plot")
depth_min = st.sidebar.number_input("Minimum depth for BVW Scatter plot", value=None, step=1, format="%d")
depth_max = st.sidebar.number_input("Maximum depth for BVW Scatter plot", value=None, step=1, format="%d")

# Sidebar: Clustering
st.sidebar.header("Clustering Options")
n_clusters = st.sidebar.slider('Number of Clusters', min_value=1, max_value=6, value=3, step=1)


# Main Area: Display Plot and Results
st.title('Well Log Visualization')
if not filtered_df.empty:
    # Call process_well_data_optimized with user inputs
    processed_df = process_well_data_optimized(
        filtered_df,
        inputs=inputs_df,
        ssp=ssp,
        sp_baseline=sp_baseline,
        shale_phid=shale_phid,
        shale_phi_n=shale_phi_n,
        sp_shift=sp_shift,
        Maximum_gr=maximum_gr,
        Minimum_gr=minimum_gr,
        rw=rw,
        Temp_rw=temp_rw,
        invasion=invasion,
        rza=rza,
        a=a,
        m=m,
        n=n
    )
    # Create and plot data using WellLogPlotter
    plotter = WellLogPlotter(processed_df, sp_shift=sp_shift)
    plotter.plot_all()
    st.pyplot(plotter.fig, use_container_width=False)
    # Create and plot data using WellLogPlotter

    plotter = SecondWellLogPlotter(processed_df,sp_shift)
    plotter.plot_all()
    st.pyplot(plotter.fig, use_container_width=False)
    # Display results below the plot
    st.subheader('Processed Data Results')
    st.dataframe(processed_df)

    # Scatter Plot with Clustering
    st.subheader("BVW Scatter Plot")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot lines y = k/x for k in 0.02, 0.04, ..., 0.14
    x = np.linspace(0.01, 0.4, 100)  # Avoid division by zero
    for k in np.arange(0.02, 0.16, 0.02):
        ax.plot(x, k / x, label=f'y={k:.2f}/x')

    # Filter scatter data by depth range
    scatter_df = processed_df
    if depth_min is not None:
        scatter_df = scatter_df[scatter_df['DEPTH'] >= depth_min]
    if depth_max is not None:
        scatter_df = scatter_df[scatter_df['DEPTH'] <= depth_max]

    # Scatter plot of phi_avg_calc vs Sw
    phi_values = scatter_df['phi_avg_calc'].values.reshape(-1, 1)
    sw_values = scatter_df['Sw'].values.reshape(-1, 1)
    scatter_data = np.hstack((phi_values, sw_values))

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    scatter_df['Cluster'] = kmeans.fit_predict(scatter_data)

    # Plot scatter points with cluster colors
    for cluster in range(n_clusters):
        cluster_data = scatter_df[scatter_df['Cluster'] == cluster]
        ax.scatter(cluster_data['phi_avg_calc'], cluster_data['Sw'], label=f'Cluster {cluster + 1}')

    # Plot cluster centers
    centers = kmeans.cluster_centers_
    ax.scatter(centers[:, 0], centers[:, 1], c='black', s=200, marker='X', label='Centers')

    ax.set_xlim(0, 0.4)
    ax.set_ylim(0, 1)
    ax.set_xlabel('Porosity (Phi)')
    ax.set_ylabel('Water Saturation (Sw)')
    ax.legend()
    st.pyplot(fig)
else:
    st.write('No data available for the selected well.')

