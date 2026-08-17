import sys
import os
import pandas as pd
from datetime import datetime

# Import local modules
sys.path.append(os.path.abspath("src"))
from engine import run_procurement_engine
from graph_extractor import load_config, get_graph_token, fetch_po_sent_timestamp

def run_pipeline():
    print("\n" + "="*70)
    print(f"ENTERPRISE LEAD-TIME PIPELINE INITIATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    # 1. Check Azure Connectivity
    config = load_config()
    token = get_graph_token(config)

    if token:
        print("[M365 STATUS] Active OAuth 2.0 Session Established via Microsoft Graph API.")
    else:
        print("[M365 STATUS] Running in Local Offline Engine Mode (Sample Fallback Mode).")

    # 2. Execute Calculation and Database Write
    run_procurement_engine()

if __name__ == "__main__":
    run_pipeline()