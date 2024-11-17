
# Well Log Visualization Dashboard

This project is a **Streamlit-based dashboard** designed for well log visualization and analysis. It includes dynamic plotting of well logs, computation of key parameters, and clustering based on provided data. Users can interact with the app to explore and analyze well logs with custom inputs.

## Features

- **Main Plots**:
  - Gamma Ray, SP Log, Bit Size, Caliper, and Rwa.
  - Porosity Logs: Density Porosity, Neutron Porosity, Average Porosity, and Resistivity Curves (RNML, RLML).
  - Saturation Logs: Sw, Sxo, BVW, and MHI.
  - Delta BVW analysis with dynamic scaling.

- **Customizable Inputs**:
  - Allows selection of wells and input of mandatory and optional data through an interactive sidebar.

- **Data Processing**:
  - Dynamic calculations such as **Rw**, **Rmf corrected**, **Saturation Logs**, and **Shale Volume**.

- **Clustering**:
  - KMeans clustering for specific parameters with interactive cluster selection.

## File Structure

- `app.py`: Main application file for Streamlit dashboard.
- `WellLogPlotter.py`: Class for plotting main well logs and porosity logs.
- `SecondWellLogPlotter.py`: Class for secondary log visualization (saturation, MHI, Delta BVW).
- `Calculations.py`: Data processing and calculation functions.
- `Work_data.xlsx`: Input well data.
- `Raster_logs_data.xlsx`: Input raster logs data for processing.

## Requirements

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   ```
2. Navigate to the project folder:
   ```bash
   cd <your-repo-name>
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select a well from the dropdown menu.
2. Input mandatory and optional parameters in the sidebar.
3. View dynamic plots and clustered scatter plots.
4. Analyze results and download processed data.

## Deployment

This app can be deployed for free using **Streamlit Community Cloud**:
1. Push your project to GitHub.
2. Deploy directly from [Streamlit Community Cloud](https://streamlit.io/cloud).


