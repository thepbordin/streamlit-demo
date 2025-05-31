import time
import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data()
def load_sample_data(file_name: str = "bike_rental_stats.json") -> pd.DataFrame:
    """Load sample sales data for demonstrations
    and cache it for performance.
    Docs: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data
    """
    time.sleep(5)
    url = f"http://raw.githubusercontent.com/streamlit/example-data/master/hello/v1/{file_name}"
    return pd.read_json(url)


@st.cache_data()
def generate_mockup_sales_data(num_records: int = 500) -> pd.DataFrame:
    """Generate mockup sales data for data visualization demonstrations.

    This function creates realistic business data with the following columns:
    - Product: Product names (Electronics, Office Supplies, Furniture items)
    - Category: Product categories (Electronics, Office Supplies, Furniture)
    - Sales: Sales amount in dollars
    - Profit: Profit amount in dollars
    - Quantity: Number of units sold
    - Region: Geographic regions (North, South, East, West)
    - Order_Date: Random dates in 2024
    - Customer_ID: Unique customer identifiers

    Args:
        num_records (int): Number of records to generate (default: 500)

    Returns:
        pd.DataFrame: Generated sales data with realistic business metrics
    """
    # Set random seed for reproducible results
    np.random.seed(42)

    # Define realistic product data
    products_data = {
        "Electronics": [
            "iPhone 15 Pro",
            "Samsung Galaxy S24",
            "MacBook Air M2",
            "Dell XPS 13",
            "iPad Pro",
            "Sony WH-1000XM5",
            "Apple Watch Series 9",
            "AirPods Pro",
            "Nintendo Switch",
            "PlayStation 5",
            "Xbox Series X",
            "LG OLED TV",
            "Canon EOS R5",
            "Sony A7R V",
            "DJI Mavic 3",
            "Tesla Model Y",
        ],
        "Office Supplies": [
            "Ergonomic Office Chair",
            "Standing Desk",
            "Wireless Mouse",
            "Mechanical Keyboard",
            "Monitor Stand",
            "Desk Lamp",
            "Paper Shredder",
            "Label Printer",
            "Whiteboard",
            "Office Organizer",
            "Stapler",
            "Hole Punch",
            "Calculator",
            "Pen Set",
            "Notebook Set",
            "File Cabinet",
        ],
        "Furniture": [
            "Executive Desk",
            "Conference Table",
            "Bookshelf",
            "Filing Cabinet",
            "Reception Desk",
            "Lounge Chair",
            "Coffee Table",
            "Storage Cabinet",
            "Dining Table",
            "Sofa Set",
            "Wardrobe",
            "Bed Frame",
            "Nightstand",
            "TV Stand",
            "Shoe Rack",
            "Kitchen Island",
        ],
    }

    # Define price ranges for each category (base prices)
    price_ranges = {
        "Electronics": (200, 3000),
        "Office Supplies": (25, 800),
        "Furniture": (150, 2500),
    }

    # Define profit margins for each category (percentage of sales)
    profit_margins = {
        "Electronics": (0.15, 0.35),  # 15-35% margin
        "Office Supplies": (0.25, 0.45),  # 25-45% margin
        "Furniture": (0.20, 0.40),  # 20-40% margin
    }

    regions = ["North", "South", "East", "West", "Central"]

    # Generate data
    data = []

    for _ in range(num_records):
        # Randomly select category
        category = np.random.choice(list(products_data.keys()))

        # Select product from category
        product = np.random.choice(products_data[category])

        # Generate sales amount based on category price range
        min_price, max_price = price_ranges[category]
        sales = np.random.uniform(min_price, max_price)

        # Add some realistic variation with log-normal distribution
        sales = sales * np.random.lognormal(0, 0.3)
        sales = round(sales, 2)

        # Generate quantity (typically 1-10 for most items, occasionally higher)
        if np.random.random() < 0.8:  # 80% of orders are small quantities
            quantity = np.random.randint(1, 6)
        else:  # 20% are bulk orders
            quantity = np.random.randint(5, 25)

        # Calculate profit based on category margin
        min_margin, max_margin = profit_margins[category]
        profit_margin = np.random.uniform(min_margin, max_margin)
        profit = sales * profit_margin * quantity
        profit = round(profit, 2)

        # Adjust sales based on quantity
        total_sales = sales * quantity

        # Generate other fields
        region = np.random.choice(regions)

        # Generate realistic dates in 2024
        start_date = pd.Timestamp("2024-01-01")
        end_date = pd.Timestamp("2024-12-31")
        random_date = start_date + pd.Timedelta(
            days=np.random.randint(0, (end_date - start_date).days)
        )

        # Generate customer ID
        customer_id = f"CUST-{np.random.randint(1000, 9999)}"

        data.append(
            {
                "Product": product,
                "Category": category,
                "Sales": round(total_sales, 2),
                "Profit": profit,
                "Quantity": quantity,
                "Region": region,
                "Order_Date": random_date,
                "Customer_ID": customer_id,
            }
        )

    # Create DataFrame
    df = pd.DataFrame(data)

    # Add some derived metrics for more interesting analysis
    df["Profit_Margin"] = (df["Profit"] / df["Sales"] * 100).round(2)
    df["Sales_Per_Unit"] = (df["Sales"] / df["Quantity"]).round(2)
    df["Month"] = df["Order_Date"].dt.month_name()
    df["Quarter"] = df["Order_Date"].dt.quarter
    df["Day_of_Week"] = df["Order_Date"].dt.day_name()

    # Sort by date for better visualization
    df = df.sort_values("Order_Date").reset_index(drop=True)

    return df


@st.cache_data()
def generate_time_series_data(
    start_date: str = "2024-01-01",
    periods: int = 365,
    freq: str = "D",
    metrics: list = None,
) -> pd.DataFrame:
    """Generate time series data for trend analysis and time-based visualizations.

    Args:
        start_date (str): Start date in YYYY-MM-DD format
        periods (int): Number of time periods to generate
        freq (str): Frequency ('D' for daily, 'W' for weekly, 'M' for monthly)
        metrics (list): List of metric names to generate

    Returns:
        pd.DataFrame: Time series data with realistic trends and seasonality
    """
    if metrics is None:
        metrics = ["Revenue", "Orders", "Website_Visits", "Customer_Satisfaction"]

    # Generate date range
    dates = pd.date_range(start=start_date, periods=periods, freq=freq)

    # Set random seed for reproducible results
    np.random.seed(42)

    data = {"Date": dates}

    for metric in metrics:
        if metric == "Revenue":
            # Revenue with weekly seasonality and growth trend
            base_value = 10000
            trend = np.linspace(0, base_value * 0.5, periods)  # 50% growth over period
            seasonal = 2000 * np.sin(
                2 * np.pi * np.arange(periods) / 7
            )  # Weekly pattern
            noise = np.random.normal(0, 1000, periods)
            values = base_value + trend + seasonal + noise
            values = np.maximum(values, base_value * 0.3)  # Minimum threshold

        elif metric == "Orders":
            # Orders correlated with revenue but different pattern
            base_value = 150
            trend = np.linspace(0, base_value * 0.3, periods)
            seasonal = 30 * np.sin(2 * np.pi * np.arange(periods) / 7 + np.pi / 4)
            noise = np.random.normal(0, 20, periods)
            values = base_value + trend + seasonal + noise
            values = np.maximum(values, 50)  # Minimum orders

        elif metric == "Website_Visits":
            # Website visits with more volatility
            base_value = 5000
            trend = np.linspace(0, base_value * 0.4, periods)
            seasonal = 1000 * np.sin(2 * np.pi * np.arange(periods) / 7)
            weekend_boost = 500 * ((np.arange(periods) % 7) >= 5)  # Weekend boost
            noise = np.random.normal(0, 500, periods)
            values = base_value + trend + seasonal + weekend_boost + noise
            values = np.maximum(values, 2000)

        elif metric == "Customer_Satisfaction":
            # Customer satisfaction (0-5 scale) with slower changes
            base_value = 4.2
            trend = np.linspace(0, 0.3, periods)  # Slight improvement over time
            seasonal = 0.2 * np.sin(
                2 * np.pi * np.arange(periods) / 30
            )  # Monthly cycle
            noise = np.random.normal(0, 0.1, periods)
            values = base_value + trend + seasonal + noise
            values = np.clip(values, 1, 5)  # Keep in valid range

        else:
            # Generic metric with random walk
            base_value = 1000
            noise = np.random.normal(0, 100, periods)
            values = base_value + np.cumsum(noise)
            values = np.maximum(values, base_value * 0.1)

        data[metric] = np.round(values, 2)

    return pd.DataFrame(data)


@st.cache_data()
def generate_customer_segments_data(num_customers: int = 200) -> pd.DataFrame:
    """Generate customer segmentation data for advanced analytics demonstrations.

    Args:
        num_customers (int): Number of customers to generate

    Returns:
        pd.DataFrame: Customer data with segmentation features
    """
    np.random.seed(42)

    # Define customer segments
    segments = {
        "Premium": {"prob": 0.15, "avg_value": 5000, "frequency": 12},
        "Regular": {"prob": 0.50, "avg_value": 1500, "frequency": 6},
        "Occasional": {"prob": 0.25, "avg_value": 500, "frequency": 2},
        "New": {"prob": 0.10, "avg_value": 300, "frequency": 1},
    }

    data = []

    for i in range(num_customers):
        # Assign segment based on probabilities
        segment = np.random.choice(
            list(segments.keys()), p=[segments[s]["prob"] for s in segments.keys()]
        )

        seg_info = segments[segment]

        # Generate customer data based on segment
        total_spent = np.random.normal(
            seg_info["avg_value"], seg_info["avg_value"] * 0.3
        )
        total_spent = max(total_spent, 50)  # Minimum spending

        purchase_frequency = np.random.poisson(seg_info["frequency"]) + 1

        avg_order_value = total_spent / purchase_frequency

        # Customer demographics
        age = np.random.normal(40, 15)
        age = int(np.clip(age, 18, 80))

        # Generate satisfaction score (correlated with segment)
        base_satisfaction = {
            "Premium": 4.5,
            "Regular": 4.0,
            "Occasional": 3.5,
            "New": 3.8,
        }
        satisfaction = np.random.normal(base_satisfaction[segment], 0.3)
        satisfaction = np.clip(satisfaction, 1, 5)

        data.append(
            {
                "Customer_ID": f"CUST-{i + 1000:04d}",
                "Segment": segment,
                "Age": age,
                "Total_Spent": round(total_spent, 2),
                "Purchase_Frequency": purchase_frequency,
                "Avg_Order_Value": round(avg_order_value, 2),
                "Customer_Satisfaction": round(satisfaction, 2),
                "Months_Active": np.random.randint(1, 36),
                "Last_Purchase_Days_Ago": np.random.randint(1, 365),
            }
        )

    df = pd.DataFrame(data)

    # Add derived metrics
    df["Customer_Lifetime_Value"] = (
        df["Avg_Order_Value"] * df["Purchase_Frequency"] * (df["Months_Active"] / 12)
    ).round(2)

    df["Churn_Risk"] = np.where(
        df["Last_Purchase_Days_Ago"] > 180,
        "High",
        np.where(df["Last_Purchase_Days_Ago"] > 90, "Medium", "Low"),
    )

    return df
