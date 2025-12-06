import pandas as pd

# 1. Load the Excel workbook
phase_file = pd.ExcelFile('phase_data.xlsx')
sheet_names = phase_file.sheet_names
all_phases_data = []

# Define the clean, final column names for all 6 relevant columns
CLEAN_COLUMN_NAMES = [
    'Sl_No',                       # 0
    'State',                       # 1
    'Constituency',                # 2 (Renamed from 'PC Name')
    'Total_Electorate_Count',      # 3 (Renamed from 'Count of Elector*')
    'Poll_Percent',                # 4 (Renamed from '**Poll (%)')
    'Total_Votes_Polled'           # 5 (Renamed from 'Count of Votes***' - the column that caused the KeyError)
]

# 2. Loop through each sheet, apply forced rename, and combine
for sheet in sheet_names:
    df_phase = pd.read_excel(phase_file, sheet_name=sheet)
    
    # 🌟 ROBUST FIX: Directly assign new column names by position
    if len(df_phase.columns) >= 6:
        # Assuming the first 6 columns are the ones we care about
        df_phase.columns = CLEAN_COLUMN_NAMES + list(df_phase.columns[6:])
    else:
         print(f"Warning: Sheet {sheet} has unexpected column count.")
         continue

    # Extract the number from the sheet name (e.g., 'Phase1' -> 1)
    df_phase['Phase_Number'] = int(sheet.replace('Phase', ''))

    # Select the columns using the guaranteed clean names
    all_phases_data.append(df_phase[[
        'Phase_Number', 
        'State', 
        'Constituency', 
        'Total_Electorate_Count', 
        'Poll_Percent', 
        'Total_Votes_Polled'
    ]])

# 3. Concatenate all dataframes into one
df_dim_phase = pd.concat(all_phases_data, ignore_index=True)
df_dim_phase.drop_duplicates(subset=['State', 'Constituency'], keep='first', inplace=True)
print(f"✅ Dim_Phase created successfully with {len(df_dim_phase)} unique PCs.")

# --- Start of the next section ---

# 🛑 FIX APPLIED HERE: Added encoding='latin1' to handle the UnicodeDecodeError
try:
    df_eci_data = pd.read_csv('eci_data_2024.csv', encoding='latin1')
except UnicodeDecodeError:
    # If latin1 fails, try cp1252, which is also common for Windows files
    df_eci_data = pd.read_csv('eci_data_2024.csv', encoding='cp1252')


df_counted_polled = pd.read_excel('GE India 2024.xlsx', sheet_name='Counted vs polled')
df_final_results = pd.read_excel('GE India 2024.xlsx', sheet_name='Final Result')

# --- 1. Prepare ECI Data (Base Fact Table) ---
df_fact = df_eci_data.rename(columns={'Constituency': 'Constituency_Name'})

# --- 2. Prepare PC Dimension Table ---
# Select and clean columns for the PC Dimension
df_dim_pc = df_counted_polled[[
    'PC Name', 'State', 'EVM Votes Counted', 'EVM Votes Polled', 
    'Difference', 'Margin'
]].rename(columns={'PC Name': 'Constituency_Name'})

df_dim_pc.drop_duplicates(subset=['State', 'Constituency_Name'], keep='first', inplace=True)

# --- 3. Enrich Fact Table with Victory Margin ---
df_final_margin = df_final_results[['Constituency', 'Victory Margin']].rename(columns={'Constituency': 'Constituency_Name'})

df_fact = pd.merge(
    df_fact, 
    df_final_margin, 
    on='Constituency_Name', 
    how='left'
)

# --- 4. Prepare for Power BI Export ---
df_fact.fillna(
    {'Victory Margin': 0}, # Fill NA in Victory Margin with 0 for losers
    inplace=True
) 

# Export the clean tables
df_fact.to_csv('clean_fact_results.csv', index=False, encoding='utf-8') # Ensure output is standard UTF-8
df_dim_pc.to_csv('clean_dim_pc.csv', index=False, encoding='utf-8')
df_dim_phase.to_csv('clean_dim_phase.csv', index=False, encoding='utf-8')

print("Data cleaning and preparation complete. Ready to load into Power BI.")