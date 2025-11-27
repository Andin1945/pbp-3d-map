import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(page_title="3D Subsurface Visualization", layout="wide")

st.title("3D Subsurface Visualization (GOC & WOC)")
st.markdown("Upload your CSV or Excel file to visualize GOC and WOC surfaces in 3D.")

# Sidebar for controls
st.sidebar.header("Data Settings")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload Data (CSV/Excel)", type=["csv", "xlsx"])

def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        st.sidebar.success("File uploaded successfully!")
        
        # Column mapping
        st.sidebar.subheader("Map Columns")
        columns = df.columns.tolist()
        
        col_x = st.sidebar.selectbox("X Coordinate", columns, index=0 if len(columns) > 0 else 0)
        col_y = st.sidebar.selectbox("Y Coordinate", columns, index=1 if len(columns) > 1 else 0)
        col_z = st.sidebar.selectbox("Z Coordinate (Depth)", columns, index=2 if len(columns) > 2 else 0)
        col_surface = st.sidebar.selectbox("Surface Type (GOC/WOC)", columns, index=3 if len(columns) > 3 else 0)
        
        # Filter options
        st.sidebar.subheader("Visualization Options")
        show_goc = st.sidebar.checkbox("Show GOC", value=True)
        show_woc = st.sidebar.checkbox("Show WOC", value=True)
        
        # Process data
        fig = go.Figure()
        
        unique_surfaces = df[col_surface].unique()
        
        for surface_name in unique_surfaces:
            # Determine visibility based on checkbox
            is_visible = False
            color = 'gray'
            
            if "GOC" in str(surface_name).upper():
                is_visible = show_goc
                color = 'red'
            elif "WOC" in str(surface_name).upper():
                is_visible = show_woc
                color = 'blue'
            else:
                # Default for other layers if any
                is_visible = True
                color = 'green'
            
            if is_visible:
                subset = df[df[col_surface] == surface_name]
                
                if not subset.empty:
                    # Create mesh3d plot
                    fig.add_trace(go.Mesh3d(
                        x=subset[col_x],
                        y=subset[col_y],
                        z=subset[col_z],
                        opacity=0.5,
                        color=color,
                        name=str(surface_name),
                        showscale=False
                    ))
                    
                    # Add scatter points for better visibility of data points
                    fig.add_trace(go.Scatter3d(
                        x=subset[col_x],
                        y=subset[col_y],
                        z=subset[col_z],
                        mode='markers',
                        marker=dict(size=4, color=color),
                        name=f"{surface_name} (Points)",
                        showlegend=False
                    ))

        # Layout settings
        fig.update_layout(
            scene=dict(
                xaxis_title=col_x,
                yaxis_title=col_y,
                zaxis_title=col_z,
                aspectmode='data' # Maintain aspect ratio based on data
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=700
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show raw data
        with st.expander("Show Raw Data"):
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload a file to get started. You can use the `sample_data.csv` provided in the project folder.")
    
    # Optional: Load sample data automatically if no file uploaded, for demo purposes
    if st.button("Load Sample Data"):
        try:
            df = pd.read_csv("sample_data.csv")
            # ... (Logic to render sample data would go here, but keeping it simple for now)
            st.warning("Please upload 'sample_data.csv' manually to the sidebar to test.")
        except:
            st.error("Sample data not found.")

