import pandas as pd
from datetime import datetime

# Sample ERP PO Creation Register
po_data = {
    "PO_Number": ["PO-2026-9041", "PO-2026-9042", "PO-2026-9043", "PO-2026-9044", "PO-2026-9045"],
    "PO_Date": ["2026-08-01", "2026-08-01", "2026-08-02", "2026-08-03", "2026-08-04"],
    "Vendor_Name": ["Tata Tiscon", "UltraTech Cement", "Supreme Pipes", "Schneider Electric", "Asian Paints"],
    "Material_Category": ["TMT Steel Fe550D", "Ready-Mix Concrete M30", "CPVC Plumbing Fittings", "Electrical DB Panels", "Exterior Emulsion"],
    "PO_Quantity": [100, 250, 500, 15, 80],
    "Unit_Price": [56500, 4800, 450, 12500, 3200],
    "Estimated_Baseline_Price": [57500, 4750, 480, 12000, 3300]
}
df_po = pd.DataFrame(po_data)
df_po.to_csv("data/raw/erp_po_register.csv", index=False)

# Sample Site GRN Receiving Register
grn_data = {
    "PO_Number": ["PO-2026-9041", "PO-2026-9042", "PO-2026-9043", "PO-2026-9044", "PO-2026-9045"],
    "GRN_Number": ["GRN-8801", "GRN-8802", "GRN-8803", "GRN-8804", "GRN-8805"],
    "GRN_Date": ["2026-08-08", "2026-08-06", "2026-08-14", "2026-08-11", "2026-08-10"],
    "Site_Location": ["Site #14 Hinjawadi", "Site #08 Kharadi", "Site #22 PCMC", "Site #03 Balewadi", "Site #19 Wagholi"],
    "Received_Quantity": [100, 250, 480, 15, 80]
}
df_grn = pd.DataFrame(grn_data)
df_grn.to_csv("data/raw/site_grn_register.csv", index=False)

print("Sample ERP & GRN CSV data files successfully generated in data/raw/")