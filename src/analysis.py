import pandas as pd
import glob
import os
import zipfile
import seaborn as sns
import matplotlib.pyplot as plt

# Set visual style for professional charts
sns.set_theme(style="whitegrid")

# -----------------------------------------------------------------------------
# 1. DATA INGESTION & UNZIPPING
#    Handles compressed datasets automatically to ensure reproducibility.
# -----------------------------------------------------------------------------
print("Step 1: Checking for zip files...")
search_path = '/content/'  # Default Colab directory

for item in os.listdir(search_path):
    if item.endswith('.zip'):
        file_path = os.path.join(search_path, item)
        print(f"--> Found zip: {item}. Extracting...")
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(search_path)
            print("    Extraction successful.")
        except zipfile.BadZipFile:
            print("    Error: Bad zip file.")

# -----------------------------------------------------------------------------
# 2. DATA LOADING & MERGING
#    Aggregates fragmented CSV files into cohesive dataframes.
# -----------------------------------------------------------------------------
def get_files(keyword):
    """Recursive search for CSVs containing the specific keyword."""
    return glob.glob(f"/content/**/*{keyword}*.csv", recursive=True)

def load_dataset(file_list):
    """Reads multiple CSVs and concatenates them into one DataFrame."""
    if not file_list: return pd.DataFrame()
    return pd.concat((pd.read_csv(f) for f in file_list), ignore_index=True)

print("\nStep 2: Loading Dataframes...")
df_enrol = load_dataset(get_files("enrolment"))
df_bio = load_dataset(get_files("biometric"))
df_demo = load_dataset(get_files("demographic"))

print(f"Loaded: {len(df_enrol)} Enrolment, {len(df_bio)} Biometric, {len(df_demo)} Demographic rows.")

# -----------------------------------------------------------------------------
# 3. PREPROCESSING & AGGREGATION
#    Standardizes dates and location names to enable accurate grouping.
# -----------------------------------------------------------------------------
print("\nStep 3: Cleaning and Aggregating...")

for df in [df_enrol, df_bio, df_demo]:
    if not df.empty:
        # Parse Dates
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
        # Create Month Period for trend analysis
        df['month'] = df['date'].dt.to_period('M')
        # Standardize Text (Title Case removes duplicates like "DELHI" vs "Delhi")
        df['state'] = df['state'].astype(str).str.title().str.strip()
        df['district'] = df['district'].astype(str).str.title().str.strip()

# Aggregate Daily Counts to Monthly District Totals
grp_enrol = df_enrol.groupby(['state', 'district', 'month'])[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
grp_bio = df_bio.groupby(['state', 'district', 'month'])[['bio_age_5_17', 'bio_age_17_']].sum().reset_index()
grp_demo = df_demo.groupby(['state', 'district', 'month'])[['demo_age_17_']].sum().reset_index()

# Merge into a single Master DataFrame for cross-metric analysis
master = pd.merge(grp_enrol, grp_bio, on=['state', 'district', 'month'], how='outer')
master = pd.merge(master, grp_demo, on=['state', 'district', 'month'], how='outer').fillna(0)

# -----------------------------------------------------------------------------
# 4. INSIGHT GENERATION & VISUALIZATION
# -----------------------------------------------------------------------------

# --- Insight A: Migration Magnets ---
# Logic: High volume of Address Updates vs. Low New Enrolments suggests inward migration.
# Metric: Adult Updates / (New Adult Enrolments + 1)
master['migration_ratio'] = master['demo_age_17_'] / (master['age_18_greater'] + 1)

# Filter for meaningful volume (>50 updates) to avoid statistical noise
mig_data = master[master['demo_age_17_'] > 50].copy()
top_migration = mig_data.sort_values('migration_ratio', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_migration, x='migration_ratio', y='district', hue='state', dodge=False, palette='viridis')
plt.title('Top 10 "Migration Magnets" (High Address Updates vs New Enrolments)')
plt.xlabel('Migration Flux Ratio')
plt.ylabel('District')
plt.tight_layout()
plt.show()

# --- Insight B: Compliance Gaps ---
# Logic: High Child Population vs. Low Biometric Updates indicates a compliance failure.
# Metric: Child Bio Updates / Total Child Population
master['child_pool'] = master['age_0_5'] + master['age_5_17']
kids_data = master[master['child_pool'] > 100].copy() # Ignore small districts
kids_data['compliance_ratio'] = kids_data['bio_age_5_17'] / kids_data['child_pool']

# Sort by LOWEST ratio (worst compliance)
lagging_districts = kids_data.sort_values('compliance_ratio', ascending=True).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=lagging_districts, x='compliance_ratio', y='district', hue='state', dodge=False, palette='Reds_r')
plt.title('Top 10 Districts with Critical Child Update Gaps')
plt.xlabel('Compliance Ratio (Updates per Child)')
plt.ylabel('District')
plt.tight_layout()
plt.show()

# --- Insight C: Anomaly Detection (Z-Score) ---
# Logic: Identify daily transaction spikes > 3 Standard Deviations from the mean (Potential Fraud).

if not df_demo.empty:
    # 1. Prepare Daily Data (Granular view required for spikes)
    daily_demo = df_demo.groupby(['date', 'district'])['demo_age_17_'].sum().reset_index()

    # 2. Calculate Statistical Baseline (Mean & Std Dev per District)
    stats = daily_demo.groupby('district')['demo_age_17_'].agg(['mean', 'std']).reset_index()
    daily_demo = daily_demo.merge(stats, on='district')

    # 3. Calculate Z-Score
    # Formula: (Daily Value - Mean) / (StdDev + epsilon)
    daily_demo['z_score'] = (daily_demo['demo_age_17_'] - daily_demo['mean']) / (daily_demo['std'] + 0.001)

    # 4. Identify the Top Anomaly
    anomalies = daily_demo.sort_values('z_score', ascending=False).head(1)

    if not anomalies.empty:
        top_district = anomalies.iloc[0]['district']
        
        # Filter time-series for the affected district
        subset = daily_demo[daily_demo['district'] == top_district].sort_values('date')

        plt.figure(figsize=(12, 5))
        sns.lineplot(data=subset, x='date', y='demo_age_17_', marker='o', color='red')
        
        # Add baseline reference
        plt.axhline(y=subset['mean'].mean(), color='green', linestyle='--', label='Normal Average')
        
        # Annotate the specific anomaly point
        spike_date = anomalies.iloc[0]['date']
        spike_val = anomalies.iloc[0]['demo_age_17_']
        plt.annotate(f'CRITICAL SPIKE: {int(spike_val)}', 
                     xy=(spike_date, spike_val), 
                     xytext=(spike_date, spike_val * 1.2),
                     arrowprops=dict(facecolor='black', shrink=0.05))

        plt.title(f'CRITICAL ALERT: Anomaly Detected in {top_district}')
        plt.ylabel('Daily Updates')
        plt.legend()
        plt.tight_layout()
        plt.show()

        print(f"ANOMALY FOUND: {top_district} had {spike_val} updates on {spike_date.date()}")