# Sidra Ledger Transaction Monitor

This repository contains a Python-based transaction monitoring tool for SidraChain. It retrieves, analyzes, and visualizes blockchain transactions from the SidraChain ledger API.

## Features
- Fetch recent transactions from SidraChain API
- Monitor and analyze transaction activity
- Detect large transactions and trigger alerts
- Visualize top active addresses using Matplotlib
- Save transaction data for persistence

## Prerequisites
Ensure you have Python 3 installed along with the following dependencies:

```sh
pip install requests web3 matplotlib
```

## Usage

### 1. Verify Installations
Run the following script to ensure the required libraries are properly installed:

```python
import requests
import web3
print("Libraries imported successfully!")
```

### 2. Fetch Recent Transactions
This script fetches and prints the latest transactions from SidraChain.

```python
url = "https://ledger.sidrachain.com/api/v2/transactions?limit=50"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("Sample transaction:", data["items"][0])
else:
    print(f"API Error: {response.status_code}")
```

### 3. Monitor Transactions in Real-time
Run the following function to continuously check for new transactions at a set interval.

```python
poll_transactions(limit=10, interval=5)
```

### 4. Analyze and Visualize Transactions
#### Analyze Active Addresses
```python
total_val, addr_counts = analyze_transactions()
```

#### Plot Active Addresses
```python
import matplotlib.pyplot as plt
addresses = list(addr_counts.keys())[:10]
counts = [addr_counts[addr] for addr in addresses]
plt.bar(addresses, counts)
plt.xlabel("Addresses")
plt.ylabel("Tx Count")
plt.title("Top 10 Active Addresses")
plt.xticks(rotation=45)
plt.show()
```

### 5. Save and Persist Data
```python
save_to_file(test_data)
```

### 6. Monitor Sidra Ledger and Detect Large Transactions
```python
monitor_sidra_ledger(limit=10, interval=10, max_runs=5)
```

## License
This project is licensed under the MIT License.

## Contributions
Feel free to fork this repository and submit pull requests to improve the monitoring and analytics features.


