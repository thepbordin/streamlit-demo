import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from services.load_data import generate_mockup_sales_data, load_sample_data
from services.load_model import load_mock_model
from utils.side_bar import add_sidebar_info

# Page configuration
st.set_page_config(
    page_title="Caching Deep Dive - Streamlit Demo", page_icon="⚡", layout="centered"
)

add_sidebar_info()

st.title("⚡ Caching Deep Dive")
st.markdown("""
Learn how to optimize your Streamlit apps with powerful caching mechanisms for better performance and user experience.
Streamlit provides several caching decorators to help you cache expensive computations, data loading, and resources.
""")

# Initialize session state for tracking function calls
if "call_count" not in st.session_state:
    st.session_state.call_count = 0
if "cached_call_count" not in st.session_state:
    st.session_state.cached_call_count = 0

# Tabs for different caching topics
tab1, tab2, tab3 = st.tabs(
    [
        "🎯 Caching Basics",
        "📊 @st.cache_data",
        "🎨 @st.cache_resource",
    ]
)

with tab1:
    st.header("Caching Basics")
    st.markdown("""
    Caching in Streamlit helps avoid expensive computations by storing results and reusing them when inputs haven't changed.
    This dramatically improves app performance and user experience.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Why Cache?")
        st.markdown("""
        **Without caching:**
        - Functions run every time the app reruns
        - Expensive operations repeat unnecessarily
        - Poor user experience with long wait times
        - Higher computational costs
        
        **With caching:**
        - Results stored and reused when possible
        - Faster app responses
        - Better resource utilization
        - Improved user satisfaction
        """)

    with col2:
        st.subheader("When to Use Caching")
        st.markdown("""
        **Perfect for caching:**
        - Data loading from files/databases
        - API calls and web requests
        - Machine learning model training
        - Complex data transformations
        - Expensive computations
        
        **Avoid caching:**
        - Functions with side effects
        - Non-deterministic operations
        - Functions returning different results for same inputs
        """)

    st.subheader("Types of Caching in Streamlit")

    cache_info = {
        "Decorator": [
            "@st.cache_data",
            "@st.cache_resource",
        ],
        "Use Case": [
            "Data processing, DataFrames, serializable objects",
            "ML models, database connections, non-serializable objects",
        ],
        "Serializable": ["Yes", "No"],
        "Status": ["✅ Current", "✅ Current"],
    }

    st.table(pd.DataFrame(cache_info))

    with st.expander("💡 Basic Caching Example"):
        st.code("""
import streamlit as st
import time

# Without caching - runs every time
def slow_function_no_cache(n):
    time.sleep(2)  # Simulate expensive operation
    return sum(range(n))

# With caching - runs once per unique input
@st.cache_data
def slow_function_cached(n):
    time.sleep(2)  # Simulate expensive operation
    return sum(range(n))

# Usage
result = slow_function_cached(1000)  # First call: takes 2 seconds
result = slow_function_cached(1000)  # Subsequent calls: instant!
        """)

with tab2:
    st.header("@st.cache_data Deep Dive")
    st.markdown("""
    `@st.cache_data` is used for caching data transformations, DataFrames, and other serializable objects.
    It's the most commonly used caching decorator in Streamlit apps.
    """)

    # Example 1: Basic data caching
    st.subheader("1. Basic Data Processing")

    def expensive_data_processing_no_cache(size):
        st.session_state.call_count += 1
        time.sleep(1)  # Simulate expensive operation
        data = np.random.rand(size, 3)
        df = pd.DataFrame(data, columns=["A", "B", "C"])
        df["Sum"] = df.sum(axis=1)
        return df

    @st.cache_data
    def expensive_data_processing_cached(size):
        st.session_state.cached_call_count += 1
        time.sleep(1)  # Simulate expensive operation
        data = np.random.rand(size, 3)
        df = pd.DataFrame(data, columns=["A", "B", "C"])
        df["Sum"] = df.sum(axis=1)
        return df

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Without Caching:**")
        if st.button("Run Expensive Function (No Cache)", key="no_cache"):
            start_time = time.time()
            result = expensive_data_processing_no_cache(1000)
            end_time = time.time()
            st.write(f"⏱️ Execution time: {end_time - start_time:.2f} seconds")
            st.write(f"📞 Total function calls: {st.session_state.call_count}")
            st.dataframe(result.head())

    with col2:
        st.markdown("**With Caching:**")
        if st.button("Run Expensive Function (Cached)", key="cached"):
            start_time = time.time()
            result = expensive_data_processing_cached(1000)
            end_time = time.time()
            st.write(f"⏱️ Execution time: {end_time - start_time:.2f} seconds")
            st.write(
                f"📞 Total cached function calls: {st.session_state.cached_call_count}"
            )
            st.dataframe(result.head())

    with st.expander("💡 Code Example"):
        st.code("""
@st.cache_data
def expensive_data_processing(size):
    # This will only run once per unique 'size' value
    time.sleep(1)  # Simulate expensive operation
    data = np.random.rand(size, 3)
    df = pd.DataFrame(data, columns=['A', 'B', 'C'])
    df['Sum'] = df.sum(axis=1)
    return df

# First call with size=1000: takes ~1 second
df = expensive_data_processing(1000)

# Subsequent calls with size=1000: instant!
df = expensive_data_processing(1000)
        """)

    # Example 2: Data loading with parameters
    st.subheader("2. Parameterized Data Loading")

    st.markdown("""
    Using our actual data generation service with caching to demonstrate
    how service functions can be cached with different parameters.
    """)

    @st.cache_data
    def load_filtered_data(category_filter, min_sales):
        """Simulate loading and filtering data using our service"""
        time.sleep(0.5)  # Simulate database query
        df = generate_mockup_sales_data()
        filtered_df = df[
            (df["Category"] == category_filter) & (df["Sales"] >= min_sales)
        ]
        return filtered_df

    col1, col2 = st.columns(2)

    with col1:
        category = st.selectbox(
            "Category Filter",
            ["Electronics", "Office Supplies", "Furniture"],
            key="cache_category",
        )

    with col2:
        min_sales = st.slider("Minimum Sales", 0, 5000, 1000, key="cache_min_sales")

    # This will be cached based on the combination of parameters
    if st.button("Load Filtered Data"):
        start_time = time.time()
        filtered_data = load_filtered_data(category, min_sales)
        end_time = time.time()

        st.write(f"⏱️ Query time: {end_time - start_time:.3f} seconds")
        st.write(f"📊 Found {len(filtered_data)} records")
        st.dataframe(filtered_data)

    # Show direct service usage
    st.subheader("2.1. Direct Service Usage")

    if st.button("Generate Mockup Data (Direct Service)", key="direct_service"):
        start_time = time.time()
        # This uses the cached function from services directly
        mockup_data = generate_mockup_sales_data(num_records=100)
        end_time = time.time()

        st.write(f"⏱️ Generation time: {end_time - start_time:.3f} seconds")
        st.write(f"📊 Generated {len(mockup_data)} records")
        st.dataframe(mockup_data.head())

    with st.expander("💡 Code Example"):
        st.code("""
# Using service functions with additional caching layers
from services.load_data import generate_mockup_sales_data

@st.cache_data
def load_filtered_data(category_filter, min_sales):
    # Cache key includes both parameters
    time.sleep(0.5)  # Simulate database query
    # Use the already cached service function
    df = generate_mockup_sales_data()
    return df[(df['Category'] == category_filter) & (df['Sales'] >= min_sales)]

# Different parameter combinations create different cache entries
data1 = load_filtered_data("Electronics", 100)  # Cached separately
data2 = load_filtered_data("Electronics", 200)  # Different cache entry
data3 = load_filtered_data("Electronics", 100)  # Uses cached result from data1

# Direct service usage (already cached)
mockup_data = generate_mockup_sales_data(num_records=500)  # Cached by service
        """)

    # Example 3: Cache configuration options
    st.subheader("3. Cache Configuration")

    @st.cache_data(ttl=30, max_entries=5, show_spinner="Loading data...")
    def configurable_cache_example(data_type):
        time.sleep(1)
        if data_type == "random":
            return pd.DataFrame(np.random.rand(100, 3), columns=["X", "Y", "Z"])
        elif data_type == "sequential":
            return pd.DataFrame(
                {"X": range(100), "Y": range(100, 200), "Z": range(200, 300)}
            )
        else:
            return pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6], "Z": [7, 8, 9]})

    st.markdown("**Cache with TTL (Time To Live) and Entry Limits:**")

    data_type = st.selectbox(
        "Data Type", ["random", "sequential", "simple"], key="config_data_type"
    )

    if st.button("Load with Configured Cache"):
        result = configurable_cache_example(data_type)
        st.dataframe(result.head())
        st.info("This cache expires after 30 seconds and keeps max 5 entries")

    with st.expander("💡 Configuration Options"):
        st.code("""
@st.cache_data(
    ttl=300,                    # Cache expires after 5 minutes
    max_entries=10,             # Keep maximum 10 cache entries
    show_spinner="Loading...",  # Custom loading message
    persist="disk",             # Persist cache to disk (experimental)
    experimental_allow_widgets=True  # Allow widgets in cached functions
)
def my_cached_function(param):
    # Your expensive operation here
    return result
        """)

with tab3:
    st.header("@st.cache_resource Deep Dive")
    st.markdown("""
    `@st.cache_resource` is used for caching non-serializable objects like ML models, database connections,
    and other resources that shouldn't be recreated on every run.
    """)

    # Example 1: ML Model Caching
    st.subheader("1. Machine Learning Model Caching")

    st.markdown("""
    Using the actual model loading function from our services module to demonstrate 
    real-world caching scenarios.
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Load Model (First Time)", key="load_model_first"):
            with st.spinner(
                "Loading model... (this may take a few seconds on first load)"
            ):
                start_time = time.time()
                model = load_mock_model()
                end_time = time.time()

                st.success(f"✅ Model loaded in {end_time - start_time:.2f} seconds")
                st.json(model)

    with col2:
        if st.button("Load Model (Cached)", key="load_model_cached"):
            with st.spinner("Loading model..."):
                start_time = time.time()
                model = load_mock_model()
                end_time = time.time()

                st.success(f"⚡ Model retrieved in {end_time - start_time:.3f} seconds")
                st.json(model)

    # Example using data loading
    st.subheader("1.1. Data Loading Caching")

    st.markdown("""
    Demonstrating cached data loading from our services module.
    """)

    if st.button("Load Sample Data", key="load_sample_data"):
        with st.spinner("Loading data from external source..."):
            start_time = time.time()
            data = load_sample_data()
            end_time = time.time()

            st.success(f"📊 Data loaded in {end_time - start_time:.2f} seconds")
            st.write(f"📈 Dataset shape: {data.shape}")
            st.dataframe(data.head())

            # Show subsequent calls are instant
            if st.button("Reload Same Data (Should be instant)", key="reload_data"):
                start_time = time.time()
                data_cached = load_sample_data()
                end_time = time.time()
                st.info(
                    f"⚡ Cached data retrieved in {end_time - start_time:.3f} seconds"
                )

    with st.expander("💡 Code Example"):
        st.code("""
# Using the actual model loading service
from services.load_model import load_mock_model

# The @st.cache_resource decorator is already applied in the service
model = load_mock_model()  # First call: takes ~1 second
model = load_mock_model()  # Subsequent calls: instant!

# Using the data loading service  
from services.load_data import load_sample_data

# The @st.cache_data decorator is already applied in the service
data = load_sample_data()  # First call: takes ~5 seconds
data = load_sample_data()  # Subsequent calls: instant!
        """)

    # Example 2: Database Connection Caching
    st.subheader("2. Database Connection Simulation")

    class MockDatabase:
        def __init__(self, db_url):
            self.db_url = db_url
            self.connected = False
            self.connection_time = None
            time.sleep(1)  # Simulate connection time
            self.connect()

        def connect(self):
            self.connected = True
            self.connection_time = datetime.now()

        def query(self, sql):
            if not self.connected:
                raise ValueError("Database not connected!")
            # Simulate query execution
            time.sleep(0.1)
            return pd.DataFrame(
                {
                    "id": range(10),
                    "value": np.random.rand(10),
                    "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * 10,
                }
            )

        def close(self):
            self.connected = False

        def __str__(self):
            status = "Connected" if self.connected else "Disconnected"
            return f"Database: {self.db_url} ({status})"

    @st.cache_resource
    def get_database_connection(db_url):
        """Create and cache database connection"""
        return MockDatabase(db_url)

    db_url = st.text_input(
        "Database URL", value="postgresql://localhost:5432/mydb", key="db_url"
    )

    if st.button("Connect to Database"):
        start_time = time.time()
        db = get_database_connection(db_url)
        end_time = time.time()

        st.success(f"✅ Connected in {end_time - start_time:.2f} seconds")
        st.write(f"🔗 {db}")
        st.write(f"⏰ Connection established at: {db.connection_time}")

        if st.button("Run Query"):
            result = db.query("SELECT * FROM sample_table LIMIT 10")
            st.dataframe(result)

    with st.expander("💡 Code Example"):
        st.code("""
@st.cache_resource
def get_database_connection(connection_string):
    # Connection created once and reused
    conn = psycopg2.connect(connection_string)
    return conn

# Connection is established once
db = get_database_connection("postgresql://localhost/mydb")
result = db.execute("SELECT * FROM users")
        """)

    # Example 3: Cache Management
    st.subheader("3. Cache Management")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Clear All Caches"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("✅ All caches cleared!")

    with col2:
        if st.button("Clear Data Cache"):
            # Clear specific service caches
            load_sample_data.clear()
            st.cache_data.clear()
            st.success("✅ Data cache cleared!")

    with col3:
        if st.button("Clear Model Cache"):
            # Clear specific service caches
            load_mock_model.clear()
            st.cache_resource.clear()
            st.success("✅ Model cache cleared!")

    with st.expander("💡 Cache Management"):
        st.code("""
# Clear all cache types
st.cache_data.clear()     # Clear all @st.cache_data caches
st.cache_resource.clear() # Clear all @st.cache_resource caches

# Clear specific service function caches
from services.load_data import load_sample_data
from services.load_model import load_mock_model

load_sample_data.clear()  # Clear specific data loading cache
load_mock_model.clear()   # Clear specific model loading cache

# Programmatic cache invalidation
@st.cache_data
def get_user_data(user_id, _force_refresh=False):
    if _force_refresh:
        get_user_data.clear()  # Clear this function's cache
    return load_user_data(user_id)
        """)

# Best Practices section
st.header("📋 Caching Best Practices")

with st.expander("🎯 Do's and Don'ts"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### ✅ **DO:**
        
        **Use @st.cache_data for:**
        - DataFrames and data processing
        - API responses and file loading
        - Expensive computations
        - Serializable objects
        
        **Use @st.cache_resource for:**
        - ML models and database connections
        - Non-serializable objects
        - Global resources
        
        **Best Practices:**
        - Include all relevant parameters in function signature
        - Use TTL for time-sensitive data
        - Clear caches when data sources change
        - Monitor cache hit rates
        - Use service layers with built-in caching (like our services module)
        - Organize cached functions in dedicated service modules
        """)

    with col2:
        st.markdown("""
        ### ❌ **DON'T:**
        
        **Avoid caching:**
        - Functions with side effects
        - Non-deterministic functions
        - Functions that modify global state
        - User authentication functions
        
        **Common Mistakes:**
        - Caching functions that return different results for same inputs
        - Forgetting to include all parameters that affect output
        - Caching functions that depend on external state
        - Over-caching (everything doesn't need to be cached)
        - Not considering memory usage of cached objects
        """)

with st.expander("⚡ Performance Optimization Tips"):
    st.markdown("""
    ### 1. **Smart Cache Key Design**
    ```python
    # Good: Include all parameters that affect output
    @st.cache_data
    def process_data(data_path, filter_params, aggregation_level):
        return expensive_processing(data_path, filter_params, aggregation_level)
    
    # Good: Use service layers with caching
    from services.load_data import generate_mockup_sales_data
    # Already cached in the service - no need to add another layer
    
    # Bad: Missing parameters that affect output
    @st.cache_data
    def process_data(data_path):
        # filter_params and aggregation_level are global variables
        return expensive_processing(data_path, filter_params, aggregation_level)
    ```
    
    ### 2. **Service-based Architecture**
    ```python
    # Organize your cached functions in service modules
    # services/load_model.py
    @st.cache_resource
    def load_mock_model():
        return expensive_model_load()
    
    # services/load_data.py  
    @st.cache_data()
    def load_sample_data(file_name: str = "data.json"):
        return expensive_data_load(file_name)
    
    # pages/your_page.py
    from services.load_model import load_mock_model
    from services.load_data import load_sample_data
    
    model = load_mock_model()  # Cached automatically
    data = load_sample_data()  # Cached automatically
    ```
    
    ### 3. **Memory Management**
    ```python
    # Use TTL for large objects
    @st.cache_data(ttl=3600, max_entries=5)  # 1 hour TTL, max 5 entries
    def load_large_dataset(dataset_id):
        return pd.read_csv(f"large_dataset_{dataset_id}.csv")
    
    # Clear service caches programmatically when needed
    from services.load_data import load_sample_data
    if st.button("Refresh Data"):
        load_sample_data.clear()
        data = load_sample_data()
    ```
    
    ### 4. **Hierarchical Caching with Services**
    ```python
    # Cache at multiple levels for optimal performance
    # Level 1: Service layer (already cached)
    from services.load_data import generate_mockup_sales_data
    
    # Level 2: Application layer caching
    @st.cache_data
    def preprocess_sales_data(num_records, filter_type):
        raw_data = generate_mockup_sales_data(num_records)  # Service cached
        return expensive_preprocessing(raw_data, filter_type)
    
    # Level 3: View layer caching  
    @st.cache_data
    def analyze_sales_data(preprocessed_data_hash, analysis_params):
        return expensive_analysis(preprocessed_data_hash, analysis_params)
    ```
    
    ### 5. **Error Handling**
    ```python
    @st.cache_data
    def robust_data_loading(data_source):
        try:
            return load_data(data_source)
        except Exception as e:
            # Don't cache errors for retry capability
            st.error(f"Failed to load data: {e}")
            raise
    ```
    """)

st.success(
    "🎉 Congratulations! You've completed the Streamlit Demo App. You now have a comprehensive understanding of Streamlit's core features, from basic components to advanced caching strategies."
)
