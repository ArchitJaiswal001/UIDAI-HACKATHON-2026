# 🔍 Unlocking Societal Trends in Aadhaar: A Data-Driven Framework

![Event](https://img.shields.io/badge/Event-UIDAI_Hackathon_2026-orange?style=for-the-badge)
![Tech](https://img.shields.io/badge/Tech-Python_%7C_Pandas_%7C_Seaborn-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

## 📄 Executive Summary
**Team ID:** UIDAI_2200

This project was developed for the **Online Hackathon on Data-Driven Innovation on Aadhaar 2026**.

## Problem Statement
Efficient delivery of Aadhaar services requires early identification of districts experiencing high migratory inflow, low child biometric compliance, or abnormal transaction spikes. Manual detection of such patterns is operationally challenging at scale.

## Solution Overview
We leveraged anonymized Aadhaar transaction logs to identifying critical governance insights. By analyzing the delta between enrolment and update patterns, our framework detects **Migration Hubs**, **Compliance Gaps**, and **System Anomalies** with statistical precision.

---

## 💡 Key Innovations

### 1. 🏙️ Migration Mapping (The "Magnet" Effect)
Identifies districts acting as economic hubs by isolating high-volume address updates from natural population growth.
- **Metric:** `Migration Flux Ratio`
- **Finding:** Districts like **Pune** show massive inward migration, requiring dynamic ASK resource allocation.

### 2. 👶 Compliance Auditing (The "Gap" Index)
Pinpoints regions where children are enrolled but failing to perform mandatory biometric updates at ages 5 and 15.
- **Metric:** `Compliance Ratio`
- **Finding:** **Nellore** exhibits a critical gap (0% compliance in sample), signalling a need for school-integrated camps.

### 3. 🚨 The Vigilance Protocol (Anomaly Detection)
A real-time statistical tripwire for fraud prevention.
- **Technique:** Z-Score Analysis (> 3 Sigma).
- **Finding:** Detected a **9.6-Sigma** event in **Udaipur** (58k updates/day), flagging potential bulk-upload fraud.

---

## 📂 Repository Structure

```text
UIDAI-Hackathon-Submission/
├── src/
│   └── analysis_and_viz.py   # Core logic for ingestion & visualization
├── output/
│   ├── migration_magnets.png # Bar chart of high-migration districts
│   ├── compliance_gap.png    # Chart of districts needing intervention
│   └── anomaly_spike.png     # Time-series graph of fraud detection
├── requirements.txt          # Python dependencies
└── README.md                 # Project Documentation

```
---

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python Package Manager)

---

## 🔧 Installation

### Clone the Repository
```bash
git clone https://github.com/ArchitJaiswal001/UIDAI-HACKATHON-2026.git
cd UIDAI-HACKATHON-2026
```


### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📊 Dataset Setup

- Download the official OGD datasets as specified in the problem statement.
- Place all downloaded .zip files in the root directory of the project.
- Datasets are intentionally excluded from version control as per hackathon guidelines.

---

## ▶️ Running the Project
```bash
python src/analysis.py
```

All generated visualizations are automatically saved in the output/ directory.

---

## 📈 Outputs

- **Migration Magnets**: Identifies districts attracting high labor migration.
- **Compliance Gap Analysis**: Highlights regions requiring administrative intervention.
- **Anomaly Spike Detection**: Detects statistically significant single-day transaction spikes indicative of potential fraud or system anomalies.

---

## 📝 Notes

The project applies statistical monitoring techniques to analyze migration patterns and detect black swan anomaly events.
Designed for clarity, reproducibility, and evaluation under UIDAI Hackathon 2026 guidelines.

---

## 📜 License
This project is open-source and available under the **MIT** License.
