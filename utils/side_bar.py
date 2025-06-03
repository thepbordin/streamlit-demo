import streamlit as st


def add_sidebar_info():
    """Add common sidebar information to all pages"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔗 Useful Links")
    st.sidebar.markdown("""
    - [Streamlit Documentation](https://docs.streamlit.io)
    - [Streamlit Gallery](https://streamlit.io/gallery)
    - [API Reference](https://docs.streamlit.io/library/api-reference)
    """)
