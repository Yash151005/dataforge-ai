# ⚡ DataForge AI
### *Raw Data In → Model-Ready Out*

A production-grade AI Data Preparation Pipeline system built with Streamlit.

---

## 🚀 Quick Start

### Install
```bash
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```


## ✨ Features

### 🔐 Authentication
- Register & Login with SHA-256 hashed passwords
- Role-based access: `admin` / `user`
- Session management

### ⚡ Pipeline Builder (6 Stages)
| Stage | Description |
|-------|-------------|
| 📥 Ingestion | CSV, Excel (.xlsx), JSON upload |
| 🔍 Validation | Missing values, duplicates, outliers, cardinality |
| 🧹 Cleaning | 7 missing strategies, IQR outliers, text normalization |
| ⚙️ Feature Eng | Label/OHE encoding, 3 scalers, polynomial, log, interactions |
| ✂️ Splitting | Custom train/val/test ratios, stratified split |
| 📤 Export | Download split CSVs + JSON pipeline report |

### 📊 Data Explorer
- Interactive data preview with row control
- Statistics (numeric + categorical)
- Filter & search by column value
- Histogram & scatter plots

### 🕐 Run History
- Every pipeline run logged to SQLite
- Filter by status, search by name
- Export full history as CSV

### ⚙️ Saved Configs
- Save pipeline configurations by name
- Re-use across datasets
- Export configs as JSON

### 🛡️ Admin Panel
- View all registered users
- View all pipeline runs system-wide
- Export all history

---

## 📁 Project Structure

```
dataforge_ai/
├── app.py              # Full application (single file)
├── requirements.txt    # Dependencies
├── README.md           # This file
└── dataforge.db        # Auto-created SQLite database
```

---

## 🎨 Design

- **Theme:** Cyberpunk-Industrial dark UI
- **Fonts:** Orbitron (headers), Space Mono (code), Rajdhani (body)
- **Colors:** Neon cyan, purple, green, orange, pink
- **Fully responsive** Streamlit layout

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this folder to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set `app.py` as entry point
4. Deploy! (Free hosting)

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit + Custom CSS
- **Backend:** Python, Pandas, NumPy
- **Database:** SQLite (zero setup, fully local)
- **Auth:** SHA-256 password hashing
- **Export:** CSV + JSON

---

## 📝 License
MIT — Free to use and modify.
