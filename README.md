# 🇮🇳 India 2024 General Election: Integrity, Competitiveness, & Turnout Analysis

This project is a detailed, end-to-end **Business Intelligence (BI)** solution for analyzing the results of the 2024 Indian General Election. Built entirely on **Power BI** and **Python (Pandas)**, the solution transforms complex, multi-source raw data into three strategic dashboards.

The goal was to move beyond simple vote tallies to perform **Integrity Checks** and **Competitiveness Analysis**.

---

## 🎯 Analytical Objectives

The project addresses three core analytical objectives:

1.  **Vote Integrity:** Quantify and visualize the discrepancy between EVM votes **Counted** vs. **Polled** by constituency.
2.  **Competitiveness:** Measure the distribution of **Victory Margins** and assess the potential impact of Postal Votes on final outcomes.
3.  **Voter Behavior:** Track **Polling Percentages** and **Electorate Counts** across the seven election phases and regions.

---

## 🧠 Data Processing & Modeling Approach

The core challenge involved cleaning highly inconsistent data from multiple file formats (`.csv`, multi-sheet `.xlsx`) into a reliable model.

1. **ETL & Data Cleaning (Python/Pandas)**
   - **Data Acquisition:** Sourced data from ECI reports (via the Kaggle dataset).
   - **Consolidation:** Wrote Python scripts to merge seven separate Phase sheets into one dimensional table.
   - **Quality Fixes:** Overcame persistent **Unicode Errors** (`latin1` encoding used) and implemented robust standardization (TRIM, CLEAN, UPPERCASE) on **Constituency** names to resolve data linking issues.

2. **Data Modeling (Power BI)**
   - Designed and enforced a **Star Schema** with one central **Fact Table** (candidate results, votes, margins) linked to two **Dimension Tables** (PC-level discrepancies, Phase-level turnout data).
   - Implemented advanced **DAX measures** for dynamic calculations such as `Total EVM Discrepancy` and `Postal_Vote_Impact_Count`.

---

## 📊 Key Dashboards & Insights

The final solution is structured into three interactive reports:

| Dashboard | Primary Title | Key Visuals |
| :--- | :--- | :--- |
| **1** | **Final Tally & Vote Integrity Review** | Party Seat Tallies, **EVM Discrepancy Matrix** (flagging integrity concerns). |
| **2** | **Competitiveness & Margin Analysis** | **Victory Margin Histogram** (identifying close contests), Map colored by Average Margin, **Postal Vote Impact Count**. |
| **3** | **Voter Participation Across Phases** | **Phase-by-Phase Line Chart** of Poll Percentage, State-wise turnout map. |

---

## 🛠 Tech Stack

* **Programming & ETL:** Python, Pandas
* **Visualization & Modeling:** Power BI Desktop
* **DAX:** Advanced Calculated Measures
* **Other Tools:** Jupyter Notebook

---

## 📂 Repository Structure

```text
india-election-analytics-2024/
├── data/                         # Cleaned CSV files used by Power BI
├── notebooks/                    # Python scripts for data prep
├── dashboards/                   # Final PBIX dashboard file
