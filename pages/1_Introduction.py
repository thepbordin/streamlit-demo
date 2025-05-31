import streamlit as st
from utils.side_bar import add_sidebar_info

# Page configuration
st.set_page_config(page_title="Siigma", page_icon="👋🏻", layout="wide")

add_sidebar_info()

st.title("👋🏻 Hello, Welcome to streamlit")

st.markdown("""

### 🚀 Installation

Installing Streamlit is simple:

```bash
pip install streamlit
```


""")

st.subheader("🚀 Hello World Example")

st.markdown("Here's the simplest Streamlit app you can create:")

st.code(
    """
import streamlit as st

st.title("Hello World!")
st.write("This is your first Streamlit app!")

# Interactive element
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}! 👋🏻")
    st.balloons()
""",
    language="python",
)

name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}! 👋🏻")
    st.balloons()

st.subheader("🏃 Running Your App")

st.markdown("""
Save your code in a file (e.g., `app.py`) and run:

```bash
streamlit run app.py
```

Your app will open in your browser at `http://localhost:8501`
""")

st.subheader("🎯 Key Concepts")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🔄 Reactive Programming**
    - Your script runs from top to bottom
    - When users interact, the script reruns
    - Use caching for expensive operations
    
    **📊 Data-First Approach**
    - Built for data science workflows
    - Native support for pandas, numpy
    - Easy visualization with charts
    """)

with col2:
    st.markdown("""
    **🎨 Simple Layouts**
    - Columns, sidebars, containers
    - No CSS or HTML required
    - Responsive by default
    
    **⚡ Fast Prototyping**
    - From idea to web app in minutes
    - Perfect for demos and MVPs
    - Easy to share and deploy
    """)

st.subheader("📁 Project Structure")

st.markdown("""
A typical Streamlit project looks like this:

```
my_app/
├── app.py              # Main application entrypoint
├── pages/              # Additional pages (optional)
│   ├── 1_📊_Dashboard.py
│   └── 2_🔧_Settings.py
├── services/           # External services (e.g., APIs) 
├── data/               # Static Data files
├── utils/              # Helper functions

```
""")

st.info("💡 **Tip**: Use the pages/ directory to create multi-page apps automatically!")
