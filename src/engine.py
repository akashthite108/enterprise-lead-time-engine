import pandas as pd
import numpy as np
import sqlite3
import os

def run_procurement_engine():
    # 1. Load Raw Registers
    po_path = "data/raw/erp_po_register.csv"
    grn_path = "data/raw/site_grn_register.csv"
    
    df_po = pd.read_csv(po_path)
    df_grn = pd.read_csv(grn_path)

    # 2. Date Conversions
    df_po['PO_Date'] = pd.to_datetime(df_po['PO_Date'])
    df_grn['GRN_Date'] = pd.to_datetime(df_grn['GRN_Date'])

    # 3. Simulate Extracted Microsoft Graph API Sent Timestamps
    # (In live deployment, this is populated directly via MS Graph API)
    email_dispatch_log = {
        "PO-2026-9041": "2026-08-02",  # 1 day lag
        "PO-2026-9042": "2026-08-04",  # 3 days lag (Internal approval delay)
        "PO-2026-9043": "2026-08-03",  # 1 day lag
        "PO-2026-9044": "2026-08-05",  # 2 days lag
        "PO-2026-9045": "2026-08-05"   # 1 day lag
    }
    df_po['PO_Sent_Date'] = pd.to_datetime(df_po['PO_Number'].map(email_dispatch_log))

    # 4. Merge ERP PO with Site GRN
    df_merged = pd.merge(df_po, df_grn, on="PO_Number", how="left")

    # 5. Dual Lead-Time Formulations (in Days)
    df_merged['Internal_Dispatch_Lag_Days'] = (df_merged['PO_Sent_Date'] - df_merged['PO_Date']).dt.days
    df_merged['Vendor_Transit_Lag_Days'] = (df_merged['GRN_Date'] - df_merged['PO_Sent_Date']).dt.days
    df_merged['Total_Lead_Time_Days'] = (df_merged['GRN_Date'] - df_merged['PO_Date']).dt.days

    # 6. Bottleneck Attribution Matrix (Where, Why & From Whom)
    conditions = [
        (df_merged['Internal_Dispatch_Lag_Days'] > 2),
        (df_merged['Vendor_Transit_Lag_Days'] > 6),
        (df_merged['Received_Quantity'] < df_merged['PO_Quantity'])
    ]
    choices_bottleneck = [
        "Internal Approval Delay",
        "Vendor Transit Breach",
        "Quantity Shortage at Gate"
    ]
    choices_attribution = [
        "Purchasing Approver",
        "Vendor Logistics",
        "Supplier Factory Dispatch"
    ]

    df_merged['Bottleneck_Category'] = np.select(conditions, choices_bottleneck, default="On Schedule")
    df_merged['Responsible_Party'] = np.select(conditions, choices_attribution, default="Standard Execution")

    # 7. Price Bounds & Margin Calculations
    df_merged['Cost_Variance_Pct'] = (
        (df_merged['Unit_Price'] - df_merged['Estimated_Baseline_Price']) / df_merged['Estimated_Baseline_Price']
    ) * 100
    df_merged['Total_PO_Value'] = df_merged['PO_Quantity'] * df_merged['Unit_Price']

    # 8. Store Output to Local SQLite Database & Processed CSV
    os.makedirs("data/processed", exist_ok=True)
    csv_output_path = "data/processed/procurement_master_analytics.csv"
    db_output_path = "data/processed/lead_time_engine.db"

    df_merged.to_csv(csv_output_path, index=False)

    conn = sqlite3.connect(db_output_path)
    df_merged.to_sql("procurement_analytics", conn, if_exists="replace", index=False)
    conn.close()

    print("\n" + "="*70)
    print("ENGINE EXECUTION SUCCESSFUL")
    print("="*70)
    print(f"• Output Database Generated: {db_output_path}")
    print(f"• Processed CSV Generated:   {csv_output_path}")
    print("="*70)
    
    # Display Preview in Terminal
    preview_cols = ['PO_Number', 'Material_Category', 'Internal_Dispatch_Lag_Days', 'Vendor_Transit_Lag_Days', 'Total_Lead_Time_Days', 'Bottleneck_Category', 'Responsible_Party']
    print(df_merged[preview_cols].to_string(index=False))
    print("="*70 + "\n")

if __name__ == "__main__":
    run_procurement_engine()