import streamlit as st
import time


@st.cache_resource
def load_mock_model():
    """Simulate loading an ML model"""
    time.sleep(3)  # Simulate loading time
    return {"model_name": "Sentiment Analyzer", "version": "1.0", "accuracy": 0.87}
