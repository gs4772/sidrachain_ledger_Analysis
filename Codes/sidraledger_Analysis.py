# Verify installations
import requests
import web3
print("Libraries imported successfully!")

# Test API connection
url = "https://ledger.sidrachain.com/api/v2/transactions?limit=50"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Sample transaction:", data["items"][0])  # Print first transaction
else:
    print(f"API Error: {response.status_code}")

import requests
import time

def poll_transactions(limit=10, interval=5):
    url = f"https://ledger.sidrachain.com/api/v2/transactions?limit={limit}"
    headers = {"User-Agent": "LedgerAnalysis/1.0"}
    last_tx_hash = None

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            transactions = data.get("items", [])  # Adjust key if different
            for tx in transactions:
                tx_hash = tx["hash"]
                if tx_hash != last_tx_hash:
                    print(f"New Tx: {tx_hash}, From: {tx['from']['hash']}, Value: {tx['value']}")
                    last_tx_hash = tx_hash
        else:
            print(f"Error {response.status_code}: {response.text}")
        time.sleep(interval)

# Test briefly (interrupt with Jupyter’s stop button)
poll_transactions(limit=10, interval=5)

from collections import defaultdict

def analyze_transactions(limit=10, iterations=5):
    url = f"https://ledger.sidrachain.com/api/v2/transactions?limit={limit}"
    headers = {"User-Agent": "LedgerAnalysis/1.0"}
    last_tx_hash = None
    address_counts = defaultdict(int)
    total_value = 0

    for _ in range(iterations):  # Limited for testing
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            transactions = response.json().get("items", [])
            for tx in transactions:
                tx_hash = tx["hash"]
                if tx_hash != last_tx_hash:
                    value = int(tx["value"]) / 1e18  # Adjust for decimals (check token unit)
                    total_value += value
                    address_counts[tx["from"]["hash"]] += 1
                    last_tx_hash = tx_hash
            print(f"Total Value: {total_value:.4f}, Active Addresses: {len(address_counts)}")
        time.sleep(5)
    return total_value, address_counts

total_val, addr_counts = analyze_transactions()

import matplotlib.pyplot as plt
%matplotlib inline

addresses = list(addr_counts.keys())[:10]  # Top 10
counts = [addr_counts[addr] for addr in addresses]

plt.bar(addresses, counts)
plt.xlabel("Addresses")
plt.ylabel("Tx Count")
plt.title("Top 10 Active Addresses")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(f"Total Transaction Value: {total_val:.4f}")

with open("sidra_ledger_v2.txt", "w") as f:
    f.write(f"Total Value: {total_val:.4f}\n")
    f.write("Address Counts:\n")
    for addr, count in addr_counts.items():
        f.write(f"{addr}: {count}\n")
print("Saved to sidra_ledger_v2.txt")

import requests
import time
import json
from collections import defaultdict

def save_to_file(data, filename="sidra_ledger_data.json"):
    try:
        # Load existing data if file exists
        with open(filename, "r") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {"value_history": [], "address_counts": {}}

    # Update with new data
    existing_data["value_history"].extend(data.get("value_history", []))
    for addr, count in data.get("address_counts", {}).items():
        existing_data["address_counts"][addr] = existing_data["address_counts"].get(addr, 0) + count

    # Save back to file
    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=2)
    print(f"Data saved to {filename}")

# Test persistence (example data)
test_data = {
    "value_history": [10.5, 20.3],
    "address_counts": {"0x123": 2, "0x456": 1}
}
save_to_file(test_data)

def check_alerts(transactions, value_threshold=1000):
    alerts = []
    for tx in transactions:
        value = int(tx["value"]) / 1e18  # Adjust for token decimals
        if value > value_threshold:
            alert = f"ALERT: Large Tx {tx['hash']} - Value: {value:.4f} from {tx['from']['hash']}"
            alerts.append(alert)
    return alerts

# Test alerts with sample data
sample_txs = [
    {"hash": "0xabc", "value": "2000000000000000000000", "from": {"hash": "0x123"}},  # 2000 units
    {"hash": "0xdef", "value": "50000000000000000000", "from": {"hash": "0x456"}}    # 50 units
]
alerts = check_alerts(sample_txs)
for alert in alerts:
    print(alert)

def monitor_sidra_ledger(limit=10, interval=10, max_runs=5, value_threshold=1000):
    url = f"https://ledger.sidrachain.com/api/v2/transactions?limit={limit}"
    headers = {"User-Agent": "LedgerAnalysis/1.0"}
    last_tx_hash = None
    address_counts = defaultdict(int)
    value_history = []
    run_count = 0

    while run_count < max_runs:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                transactions = data.get("items", [])
                if not transactions:
                    print("No new transactions.")
                    time.sleep(interval)
                    continue

                new_total_value = 0
                alerts = check_alerts(transactions, value_threshold)
                for tx in transactions:
                    tx_hash = tx["hash"]
                    if tx_hash != last_tx_hash:
                        value = int(tx["value"]) / 1e18
                        new_total_value += value
                        address_counts[tx["from"]["hash"]] += 1
                        last_tx_hash = tx_hash

                value_history.append(new_total_value)
                print(f"Run {run_count}: Total Value: {sum(value_history):.4f}, Active Addresses: {len(address_counts)}")
                for alert in alerts:
                    print(alert)

                # Save data
                save_to_file({
                    "value_history": [new_total_value],
                    "address_counts": dict(address_counts)
                })
            else:
                print(f"API Error {response.status_code}: {response.text}")
                time.sleep(interval * 2)
        except Exception as e:
            print(f"Exception: {e}")
            time.sleep(interval * 2)
        run_count += 1
        time.sleep(interval)

    return value_history, address_counts

# monitor
value_history, addr_counts = monitor_sidra_ledger(limit=10, interval=10, max_runs=5)
