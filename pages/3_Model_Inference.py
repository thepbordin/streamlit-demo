import streamlit as st
import pandas as pd
import numpy as np
import time
from utils.side_bar import add_sidebar_info
from services.load_model import load_mock_model
from services.load_data import load_sample_data

# Page configuration
st.set_page_config(page_title="Data Input/Output & ML", page_icon="🤖", layout="wide")

add_sidebar_info()

st.title("🤖 Data Input/Output & Model Inferencing")

st.markdown("""
This section demonstrates how to handle data input/output and integrate machine learning models in Streamlit.
Perfect for building data science applications and ML demos!
""")

# File Upload Section
st.header("📤 File Upload Demo")

st.markdown("""
File upload is one of the most powerful features in Streamlit. Let's explore different file types and processing options.
""")

tab1 = st.tabs(["📊 CSV Files"])[0]

with tab1:
    st.subheader("CSV File Processing")

    uploaded_csv = st.file_uploader(
        "Upload a CSV file",
        type="csv",
        help="Upload a CSV file to see data analysis features",
    )

    if uploaded_csv is not None:
        try:
            df = pd.read_csv(uploaded_csv)
            st.success(f"✅ File uploaded successfully: **{uploaded_csv.name}**")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", f"{df.shape[0]:,}")
            with col2:
                st.metric("Columns", f"{df.shape[1]:,}")
            with col3:
                st.metric("Size", f"{uploaded_csv.size:,} bytes")

            # Data preview
            st.subheader("📊 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            # Data analysis
            if st.checkbox("Show Data Analysis"):
                st.subheader("📈 Quick Analysis")

                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Data Types:**")
                    st.dataframe(df.dtypes.to_frame("Type"), use_container_width=True)

                with col2:
                    st.write("**Missing Values:**")
                    missing = df.isnull().sum()
                    st.dataframe(missing.to_frame("Missing"), use_container_width=True)

                # Numeric columns analysis
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    st.write("**Numeric Columns Summary:**")
                    st.dataframe(df[numeric_cols].describe(), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")
    else:
        # Sample data for demo
        st.info("💡 **No file uploaded yet.** Here's a sample dataset:")
        sample_data = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie", "Diana"],
                "Age": [25, 30, 35, 28],
                "City": ["New York", "London", "Tokyo", "Paris"],
                "Salary": [50000, 60000, 70000, 55000],
            }
        )
        st.dataframe(sample_data, use_container_width=True)

# Machine Learning Demo Section
st.header("🤖 Mock ML Model Demo")

st.markdown("""
This section demonstrates how to integrate machine learning models with Streamlit for real-time predictions.
""")

# Text Analysis Section - Using functions from services
st.subheader("Sentiment Analysis")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("**Enter text to analyze:**")
    user_text = st.text_area(
        "Text input:",
        value="Streamlit is amazing for building data apps!",
        height=100,
    )

    confidence_threshold = st.slider("Confidence Threshold:", 0.5, 1.0, 0.8)

    if st.button("🔍 Analyze Sentiment"):
        if user_text.strip():
            with st.spinner("Analyzing sentiment..."):
                time.sleep(1)  # Simulate processing time

                # Mock sentiment analysis
                sentiment_score = np.random.uniform(-1, 1)
                confidence = np.random.uniform(0.7, 0.95)

                # Store results in session state
                st.session_state.sentiment_results = {
                    "text": user_text,
                    "score": sentiment_score,
                    "confidence": confidence,
                    "threshold": confidence_threshold,
                }

with col2:
    if "sentiment_results" in st.session_state:
        results = st.session_state.sentiment_results

        st.write("**Analysis Results:**")

        # Determine sentiment
        if results["score"] > 0.1:
            sentiment = "Positive 😊"
            color = "green"
        elif results["score"] < -0.1:
            sentiment = "Negative 😞"
            color = "red"
        else:
            sentiment = "Neutral 😐"
            color = "orange"

        st.markdown(f"**Sentiment:** :{color}[{sentiment}]")
        st.metric("Confidence Score", f"{results['confidence']:.2%}")

        # Progress bar
        st.progress(results["confidence"])

st.divider()
# Sample Data Loading Section - Using functions from services
st.header("📊 Sample Data Loading")
st.markdown("Demonstrating data loading using functions from the services module.")

if st.button("Load Sample Data"):
    with st.spinner("Loading sample data..."):
        try:
            sample_df = load_sample_data()
            st.success("✅ Sample data loaded successfully!")
            st.write(
                f"**Dataset shape:** {sample_df.shape[0]} rows × {sample_df.shape[1]} columns"
            )
            st.dataframe(sample_df.head(10), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")

st.divider()
# Model Management Section
st.header("🧠 Model Management")

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚡ Cached Model Loading")

    # Use the load_mock_model function from services
    if st.button("Load Mock Model"):
        with st.spinner("Loading model..."):
            model_info = load_mock_model()
            st.success("✅ Model loaded successfully!")
            st.json(model_info)

    st.code(
        """
        @st.cache_resource
        def load_model():
            # Load your actual model here
            model = joblib.load('model.pkl')
            return model

        model = load_model()
        prediction = model.predict(input_data)
    """,
        language="python",
    )


# Best Practices
st.header("💡 Best Practices")

st.markdown("""
### 🚀 Performance Tips

1. **Use Caching**: Cache expensive model loading and data processing or operations with `@st.cache_resource` and `@st.cache_data`
2. **Error Handling**: Always handle file upload errors gracefully
3. **Progress Bars**: Use `st.spinner()` for long-running operations

""")
