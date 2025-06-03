import streamlit as st
from utils.side_bar import add_sidebar_info

# Page configuration
st.set_page_config(page_title="Core Components", page_icon="🎯", layout="wide")

add_sidebar_info()

st.title("🎯 Core Components Demo")

st.markdown("""
Streamlit provides a rich set of interactive components that make it easy to build user interfaces.
Let's explore the most commonly used ones!
""")

# Buttons Section
st.header("🔘 Buttons")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Simple Buttons")

    # Simple button
    if st.button("Click me! 🚀", key="simple_button"):
        st.success("Button clicked! 🎉")

    # Disabled button demo
    st.button("Disabled Button", disabled=True, help="This button is disabled")

    st.code(
        """
# Simple button
if st.button("Click me!"):
    st.success("Button clicked!")
    
# Disabled button
st.button("Disabled", disabled=True)
""",
        language="python",
    )

with col2:
    st.subheader("Download Button")

    # Sample data for download
    sample_csv = """Name,Age,City
John Doe,25,New York
Jane Smith,30,San Francisco
Bob Johnson,35,Chicago"""

    st.download_button(
        label="📥 Download Sample CSV",
        data=sample_csv,
        file_name="sample_data.csv",
        mime="text/csv",
    )

    # Download button with JSON data
    import json

    sample_json = {"users": [{"name": "John", "age": 25}, {"name": "Jane", "age": 30}]}

    st.download_button(
        label="📄 Download JSON",
        data=json.dumps(sample_json, indent=2),
        file_name="data.json",
        mime="application/json",
    )

    st.code(
        """
st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="data.csv",
    mime="text/csv"
)
""",
        language="python",
    )

# Forms Section
st.header("📝 Forms")

st.markdown("Forms allow you to group inputs and submit them together:")

with st.form("demo_form"):
    st.subheader("User Information Form")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
    with col2:
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
        city = st.selectbox("City", ["New York", "San Francisco", "Chicago", "Other"])

    message = st.text_area("Message (optional)")
    agree = st.checkbox("I agree to the terms and conditions")

    submitted = st.form_submit_button("Submit Form 🚀")

    if submitted:
        if name and email and agree:
            st.success(f"✅ Form submitted successfully!")
            st.json(
                {
                    "name": name,
                    "email": email,
                    "age": age,
                    "city": city,
                    "message": message,
                }
            )
        else:
            st.error("❌ Please fill in all required fields and agree to terms.")

st.code(
    """
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(f"Hello {name}, age {age}")
""",
    language="python",
)

# Input Widgets Section
st.header("📝 Input Widgets")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Text Inputs")

    # Text input
    single_line = st.text_input("Single line input:", placeholder="Type here...")
    if single_line:
        st.write(f"You typed: **{single_line}**")

    # Text area
    multi_line = st.text_area("Multi-line input:", placeholder="Type multiple lines...")
    if multi_line:
        st.write(
            f"Character count: {len(multi_line)} | Word count: {len(multi_line.split())}"
        )

with col2:
    st.subheader("Numeric Inputs")

    # Number input
    number = st.number_input(
        "Pick a number:", min_value=0, max_value=100, value=50, step=5
    )
    st.write(f"Selected: **{number}** | Squared: **{number**2}**")

    # Slider
    slider_value = st.slider("Slide me:", 0, 100, 25, step=5)
    st.progress(slider_value / 100)

    # Range slider
    range_values = st.slider("Select a range:", 0, 100, (25, 75))
    st.write(f"Range: {range_values[0]} - {range_values[1]}")

# Selection Widgets
st.header("🎛️ Selection Widgets")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Single Selection")

    # Select box
    option = st.selectbox("Choose an option:", ["Option A", "Option B", "Option C"])
    st.write(f"Selected: **{option}**")

    # Radio buttons
    radio_choice = st.radio("Pick one:", ["🍎 Apple", "🍌 Banana", "🍊 Orange"])
    st.write(f"You picked: {radio_choice}")

with col2:
    st.subheader("Multiple Selection")

    # Multiselect
    multi_options = st.multiselect(
        "Choose multiple:",
        ["Python", "JavaScript", "Java", "C++", "Go"],
        default=["Python"],
    )
    st.write(f"Selected {len(multi_options)} languages: {', '.join(multi_options)}")

    # Checkbox
    if st.checkbox("Enable notifications"):
        st.info("🔔 Notifications enabled!")

with col3:
    st.subheader("Date & Time")

    # Date input
    selected_date = st.date_input("Pick a date:")
    st.write(f"Date: {selected_date}")

    # Time input
    selected_time = st.time_input("Pick a time:")
    st.write(f"Time: {selected_time}")


# Advanced Widgets
st.header("🚀 Advanced Widgets")

col1, col2 = st.columns(2)

with col1:
    st.subheader("File Upload")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "txt", "json"],
        help="Upload a CSV, TXT, or JSON file",
    )

    if uploaded_file is not None:
        st.success(f"✅ File uploaded: **{uploaded_file.name}**")
        st.write(f"File size: {uploaded_file.size} bytes")

        if uploaded_file.type == "text/csv":
            import pandas as pd

            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head(), use_container_width=True)


# Interactive Examples
st.header("🎮 Interactive Examples")

st.subheader("Calculator Demo")

col1, col2, col3 = st.columns(3)

with col1:
    num1 = st.number_input("First number:", value=10.0)
with col2:
    operation = st.selectbox("Operation:", ["+", "-", "×", "÷"])
with col3:
    num2 = st.number_input("Second number:", value=5.0)

if st.button("Calculate 🧮"):
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "×":
        result = num1 * num2
    elif operation == "÷":
        result = num1 / num2 if num2 != 0 else "Error: Division by zero"

    st.success(f"Result: **{num1} {operation} {num2} = {result}**")

# Tips and Best Practices
st.header("💡 Tips & Best Practices")
st.markdown("""
### 🔄 Session State
- Use `st.session_state` to persist data across reruns
- Perfect for counters, user preferences, etc.

""")

# Session State Example
st.subheader("🔄 Session State Example")

if "counter" not in st.session_state:
    st.session_state.counter = 0

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Increment"):
        st.session_state.counter += 1

with col2:
    if st.button("➖ Decrement"):
        st.session_state.counter -= 1

with col3:
    if st.button("🔄 Reset"):
        st.session_state.counter = 0

st.metric("Counter Value", st.session_state.counter)

st.code(
    """
# Session state example
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment"):
    st.session_state.counter += 1

st.write(f"Counter: {st.session_state.counter}")
""",
    language="python",
)
