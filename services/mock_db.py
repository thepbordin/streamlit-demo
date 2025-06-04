import time
from datetime import datetime
import pandas as pd
import numpy as np


class MockDatabase:
    def __init__(self, db_url):
        self.db_url = db_url
        self.connected = False
        self.connection_time = None
        time.sleep(1)  # Simulate connection time
        self.connect()

    def connect(self):
        if self.connected:
            raise ValueError("Database already connected!")
        time.sleep(0.7)
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
