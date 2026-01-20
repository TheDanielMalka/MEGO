import pandas as pd
import numpy as np

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'London', 'Paris', 'Tokyo']
}

# df['Age'] = df['Age'] + 1
# print(df['Age'])
# print(df)

df = pd.read_csv('my_data.csv')
complex_mask = (df['Age'] > 28) & (df['City'] == 'London')
filtered_df = df[complex_mask]
print(filtered_df)
