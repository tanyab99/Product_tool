import pandas as pd

def read_and_clean_data(file_path):
    data = pd.read_csv(file_path)
    data = data.dropna(subset=['our_price'])
    data['our_price'] = data['our_price'].apply(lambda x: str(x).replace('$', '') if isinstance(x, str) else x)
    data['our_price'] = pd.to_numeric(data['our_price'], errors='coerce')
    data['current_stock'] = data['current_stock'].apply(lambda x: 0 if x == 'out of stock' else x)
    return data

