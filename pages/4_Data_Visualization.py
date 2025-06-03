import streamlit as st
import pandas as pd
import plotly.express as px

import numpy as np
from services.load_data import generate_mockup_sales_data
from utils.side_bar import add_sidebar_info

# Page configuration
st.set_page_config(
    page_title="Data Visualization - Streamlit Demo", page_icon="📊", layout="wide"
)

add_sidebar_info()

st.title("📊 Data Visualization")
st.markdown("""
This page demonstrates Streamlit's powerful data visualization capabilities using various chart types,
interactive plots, and data display components.
""")

# Load sample data
df = generate_mockup_sales_data()

# Tabs for different visualization types
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Basic Charts",
        "🎨 Advanced Plots",
        "📋 Data Display",
        "🔄 Interactive Visualizations",
    ]
)

with tab1:
    st.header("Basic Charts")
    st.markdown(
        "Streamlit provides simple chart components for quick data visualization."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Line Chart")
        # Create time series data
        dates = pd.date_range("2023-01-01", periods=100)
        time_series = pd.DataFrame(
            {"date": dates, "value": np.cumsum(np.random.randn(100)) + 100}
        )
        st.line_chart(time_series.set_index("date"))

        with st.expander("💡 Code Example"):
            st.code("""
import streamlit as st
import pandas as pd
import numpy as np

dates = pd.date_range('2023-01-01', periods=100)
time_series = pd.DataFrame({
    'date': dates,
    'value': np.cumsum(np.random.randn(100)) + 100
})
st.line_chart(time_series.set_index('date'))
            """)

    with col2:
        st.subheader("Bar Chart")
        st.bar_chart(df.groupby("Category")["Sales"].sum())

        with st.expander("💡 Code Example"):
            st.code("""
# Assuming df is your DataFrame
st.bar_chart(df.groupby('Category')['Sales'].sum())
            """)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Area Chart")
        area_data = pd.DataFrame(
            {
                "Series A": np.random.randn(20).cumsum(),
                "Series B": np.random.randn(20).cumsum(),
                "Series C": np.random.randn(20).cumsum(),
            }
        )
        st.area_chart(area_data)

        with st.expander("💡 Code Example"):
            st.code("""
area_data = pd.DataFrame({
    'Series A': np.random.randn(20).cumsum(),
    'Series B': np.random.randn(20).cumsum(),
    'Series C': np.random.randn(20).cumsum()
})
st.area_chart(area_data)
            """)

    with col4:
        st.subheader("Scatter Chart")
        scatter_data = pd.DataFrame(
            {
                "x": np.random.randn(50),
                "y": np.random.randn(50),
                "size": np.random.randint(10, 100, 50),
            }
        )
        st.scatter_chart(scatter_data, x="x", y="y", size="size")

        with st.expander("💡 Code Example"):
            st.code("""
scatter_data = pd.DataFrame({
    'x': np.random.randn(50),
    'y': np.random.randn(50),
    'size': np.random.randint(10, 100, 50)
})
st.scatter_chart(scatter_data, x='x', y='y', size='size')
            """)

with tab2:
    st.header("Advanced Plots with Plotly")
    st.markdown("Using Plotly for more sophisticated and interactive visualizations.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Interactive Scatter Plot")
        fig_scatter = px.scatter(
            df,
            x="Sales",
            y="Profit",
            color="Category",
            size="Quantity",
            hover_data=["Product"],
            title="Sales vs Profit by Category",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        with st.expander("💡 Code Example"):
            st.code("""
import plotly.express as px

fig = px.scatter(
    df, 
    x='Sales', 
    y='Profit', 
    color='Category',
    size='Quantity',
    hover_data=['Product'],
    title="Sales vs Profit by Category"
)
st.plotly_chart(fig, use_container_width=True)
            """)

    with col2:
        st.subheader("Box Plot")
        fig_box = px.box(
            df, x="Category", y="Sales", title="Sales Distribution by Category"
        )
        st.plotly_chart(fig_box, use_container_width=True)

        with st.expander("💡 Code Example"):
            st.code("""
fig = px.box(
    df, 
    x='Category', 
    y='Sales',
    title="Sales Distribution by Category"
)
st.plotly_chart(fig, use_container_width=True)
            """)


with tab3:
    st.header("Data Display Components")
    st.markdown("Various ways to display and interact with tabular data.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Simple Table")
        st.table(df.head())

        with st.expander("💡 Code Example"):
            st.code("""
# Static table display
st.table(df.head())
            """)

    with col2:
        st.subheader("Interactive DataFrame")
        st.dataframe(df, use_container_width=True)

        with st.expander("💡 Code Example"):
            st.code("""
# Interactive dataframe with sorting, filtering
st.dataframe(df, use_container_width=True)
            """)

    st.subheader("Data Editor")
    st.markdown("Allow users to edit data directly in the interface:")

    # Create a smaller editable dataset
    editable_df = df.head(5).copy()
    edited_df = st.data_editor(
        editable_df,
        use_container_width=True,
        num_rows="dynamic",  # Allow adding/removing rows
    )

    if st.button("Show Edited Data"):
        st.write("Edited DataFrame:")
        st.json(edited_df.to_dict())

    with st.expander("💡 Code Example"):
        st.code("""
# Editable data interface
edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic"  # Allow adding/removing rows
)
        """)

    st.subheader("Metrics Display")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Sales",
            value=f"${df['Sales'].sum():,.0f}",
            delta=f"{np.random.randint(-10, 10)}%",
        )

    with col2:
        st.metric(
            label="Avg Profit",
            value=f"${df['Profit'].mean():,.0f}",
            delta=f"{np.random.randint(-5, 15)}%",
        )

    with col3:
        st.metric(
            label="Total Products", value=len(df), delta=f"+{np.random.randint(1, 10)}"
        )

    with col4:
        st.metric(label="Categories", value=df["Category"].nunique(), delta=None)

    with st.expander("💡 Code Example"):
        st.code("""
st.metric(
    label="Total Sales",
    value=f"${df['Sales'].sum():,.0f}",
    delta=f"{change_percentage}%"
)
        """)

with tab4:
    st.header("Interactive Visualizations")
    st.markdown("Create dynamic charts that respond to user input.")

    # Interactive chart controls
    st.subheader("Customizable Chart")

    col1, col2, col3 = st.columns(3)

    with col1:
        chart_type = st.selectbox(
            "Chart Type", ["scatter", "bar", "line", "box", "histogram"]
        )

    with col2:
        x_axis = st.selectbox("X-Axis", ["Sales", "Profit", "Quantity", "Category"])

    with col3:
        y_axis = st.selectbox("Y-Axis", ["Profit", "Sales", "Quantity"], index=0)

    # Color option
    color_by = st.selectbox("Color By", [None, "Category", "Product"], index=1)

    # Create the chart based on selections
    if chart_type == "scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by, hover_data=["Product"])
    elif chart_type == "bar":
        if x_axis == "Category":
            agg_df = df.groupby("Category")[y_axis].sum().reset_index()
            fig = px.bar(agg_df, x="Category", y=y_axis)
        else:
            fig = px.bar(df.head(10), x="Product", y=y_axis, color=color_by)
    elif chart_type == "line":
        if x_axis in ["Sales", "Profit", "Quantity"]:
            # Sort by x_axis for line chart
            sorted_df = df.sort_values(x_axis)
            fig = px.line(sorted_df, x=x_axis, y=y_axis, color=color_by)
        else:
            fig = px.line(
                df.groupby("Category")[y_axis].sum().reset_index(),
                x="Category",
                y=y_axis,
            )
    elif chart_type == "box":
        fig = px.box(df, x="Category", y=y_axis)
    elif chart_type == "histogram":
        fig = px.histogram(df, x=y_axis, color=color_by)

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("💡 Code Example"):
        st.code("""
# Interactive chart with user controls
chart_type = st.selectbox("Chart Type", ["scatter", "bar", "line"])
x_axis = st.selectbox("X-Axis", df.columns)
y_axis = st.selectbox("Y-Axis", df.columns)

if chart_type == "scatter":
    fig = px.scatter(df, x=x_axis, y=y_axis)
elif chart_type == "bar":
    fig = px.bar(df, x=x_axis, y=y_axis)
# ... more chart types

st.plotly_chart(fig, use_container_width=True)
        """)
