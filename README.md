# 🚀 Streamlit Demo - Knowledge Sharing Session

A simple Streamlit demo app covering core concepts for building interactive web applications with Python.

## ✨ What You'll Learn

- **🎯 Components**: Buttons, forms, inputs, and widgets
- **📊 Data Viz**: Charts, tables, and interactive plots  
- **🤖 ML Integration**: Model loading and predictions
- **⚡ Caching**: Performance optimization techniques

## 🏗️ Project Structure

```
streamlit-demo/
├── main.py              # Main landing page
├── pages/               # Demo sections
│   ├── 1_Introduction.py
│   ├── 2_Components.py  
│   ├── 3_Model_Inference.py
│   ├── 4_Data_Visualization.py
│   └── 5_Caching.py
├── services/            # Data & model services
└── utils/               # Helper functions
```

## 📋 Prerequisites

- **Python 3.13+**
- **uv** - A fast Python package manager (recommended)

### What is uv?
[uv](https://docs.astral.sh/uv/) is an extremely fast Python package and project manager written in Rust. It's a drop-in replacement for pip that's 10-100x faster and includes dependency resolution, virtual environment management, and more.

**Install uv:**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

## 🚀 Quick Start

1. **Install dependencies**
   ```bash
   # Using uv (recommended - faster)
   uv sync
   
   # Or using pip
   pip install streamlit pandas matplotlib plotly numpy
   ```

2. **Run the app**
   ```bash
   # With uv
   uv run streamlit run main.py
   
   # Or with regular Python
   streamlit run main.py
   ```

3. **Open browser**
   Go to `http://localhost:8501`


## 📚 Learn More

- [Streamlit Docs](https://docs.streamlit.io/)
- [Gallery](https://streamlit.io/gallery)
- [Community](https://discuss.streamlit.io/)

---

**Happy coding! 🎉**