# 🏏 IPL Match Insights & Player Performance Analytics Dashboard

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/en/8/84/Indian_Premier_League_Official_Logo.svg" width="120" alt="IPL Logo"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python"/>
  <img src="https://img.shields.io/badge/Streamlit-1.29-red?style=flat-square&logo=streamlit"/>
  <img src="https://img.shields.io/badge/Pandas-2.1-green?style=flat-square&logo=pandas"/>
  <img src="https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square"/>
</p>

An end-to-end **Data Science project** that analyses 13 years of IPL cricket data (2008–2020)
to uncover team performances, top players, venue insights, and season-wise trends —
all presented in an interactive **Streamlit dashboard**.

---

## 📌 Project Overview

This project ingests two real-world CSV datasets (matches and ball-by-ball deliveries),
cleans and processes the data with **Pandas & NumPy**, generates 10+ visualisations using
**Matplotlib & Seaborn**, and exposes everything through a filterable **Streamlit** web dashboard.

The project is designed to be **beginner-friendly**, well-commented, and ready to showcase
in a Data Science internship portfolio.

---

## ✨ Features

| Category | Details |
|---|---|
| **Data Cleaning** | Missing value handling, deduplication, team name standardisation |
| **EDA** | 10+ analytical insights across teams, players, seasons, and venues |
| **Visualisations** | Bar charts, pie charts, line graphs, heatmaps, scatter plots |
| **Dashboard** | Streamlit app with sidebar filters (season, team, player) |
| **Player Spotlight** | Per-player batting stats and season-wise run trend |
| **Orange / Purple Cap** | Season-wise top scorers and wicket takers |
| **Head-to-Head** | Win/loss record between any two teams |
| **Dismissal Heatmap** | Wicket types per bowling team |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **Pandas** | Data loading, cleaning, and analysis |
| **NumPy** | Numerical operations |
| **Matplotlib** | Base charting library |
| **Seaborn** | Statistical visualisations |
| **Streamlit** | Interactive web dashboard |
| **Jupyter Notebook** | EDA exploration (`analysis.ipynb`) |

---

## 📂 Project Structure

```
ipl_dashboard/
│
├── app.py                  # 🚀 Main Streamlit dashboard
├── analysis.ipynb          # 📓 Jupyter EDA Notebook
├── requirements.txt        # 📦 Python dependencies
├── README.md               # 📖 You are here
│
├── datasets/               # 📁 Place CSV files here
│   ├── matches.csv
│   └── deliveries.csv
│
├── utils/                  # 🛠️ Helper modules
│   ├── __init__.py
│   ├── data_loader.py      # CSV loading & cleaning
│   ├── analysis.py         # All EDA functions
│   └── visualizations.py  # All chart functions
│
└── screenshots/            # 📸 Auto-saved chart images
```

---

## ⚙️ Installation Steps

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ipl-analytics-dashboard.git
cd ipl-analytics-dashboard
```

### 2. Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the dataset
Go to Kaggle and download the **IPL Complete Dataset (2008–2020)**:
👉 https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020

Place both files inside the `datasets/` folder:
```
datasets/
├── matches.csv
└── deliveries.csv
```

---

## ▶️ How to Run

### Option A — Streamlit Dashboard (Recommended)
```bash
streamlit run app.py
```
Then open your browser at **http://localhost:8501**

### Option B — Jupyter Notebook (EDA Only)
```bash
jupyter notebook analysis.ipynb
```

---

## 📊 Key Insights Discovered

- **Mumbai Indians** have the highest win count across all IPL seasons
- Toss advantage only converts to a match win ~51% of the time (barely above chance)
- **Virat Kohli** holds the record for most career runs in IPL history
- **SL Malinga** is the all-time leading wicket taker
- Teams generally prefer to **field first** after winning the toss
- Average match scores have increased over the seasons, reflecting more aggressive batting

---

## 📸 Screenshots

> Run the notebook to auto-generate charts in `screenshots/`

| Chart | Description |
|---|---|
| `01_matches_won.png` | Team win counts |
| `02_toss_impact.png` | Toss vs match result |
| `03_top_run_scorers.png` | Top 10 batsmen |
| `04_top_wicket_takers.png` | Top 10 bowlers |
| `05_season_trend.png` | Season-wise avg score |
| `06_dismissal_heatmap.png` | Wicket type heatmap |

---

## 🚀 Future Improvements

- [ ] Add a **Prediction Model** (who will win the next match?) using scikit-learn
- [ ] Integrate **live IPL data** via Cricbuzz / ESPNcricinfo API
- [ ] Add **fielding statistics** (catches, run-outs)
- [ ] Deploy on **Streamlit Cloud** for a public URL
- [ ] Add **bowling economy rate** and bowling average metrics
- [ ] Introduce a **"Fantasy XI" picker** based on top stats

---

## 🧠 Interview Prep

### "Explain your project"
> "I built an end-to-end Data Science project on IPL cricket data.
> I loaded and cleaned two large CSV datasets — one with match-level info and another
> with ball-by-ball delivery data. Then I performed EDA to find insights like top scorers,
> leading wicket takers, and which teams perform best. Finally, I built an interactive
> Streamlit dashboard where users can filter by season, team, or player and see charts update live."

### "What challenges did you face?"
> "My biggest challenge was data cleaning — team names had changed over the years (like
> 'Delhi Daredevils' becoming 'Delhi Capitals'), so I had to standardise them. I also had
> to handle run-outs carefully when counting bowler wickets, since run-outs shouldn't be
> credited to the bowler."

### "What did you learn?"
> "I learned how to write modular, reusable Python code by splitting data loading, analysis,
> and visualisation into separate files. I also learned that insights don't always match
> intuition — for example, winning the toss barely improves your chances of winning the match."

---

## 📄 Resume Bullet Points

- **Analysed 13 seasons of IPL cricket data** (76,000+ deliveries) using Pandas & NumPy to uncover team win rates, player strike rates, and toss-impact statistics
- **Built 10+ interactive visualisations** (bar charts, line graphs, heatmaps, scatter plots) using Matplotlib & Seaborn to communicate data-driven insights clearly
- **Developed a modular Streamlit dashboard** with sidebar filters for season, team, and player selection — enabling real-time, drill-down analysis of match and player performance
- **Performed end-to-end data wrangling** including missing value imputation, deduplication, and team name standardisation across two relational CSV datasets of 900+ matches

---

## 👤 Author

**Your Name**  
📧 your.email@example.com  
🔗 [LinkedIn](https://linkedin.com/in/your-profile)  
🐙 [GitHub](https://github.com/your-username)

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).
