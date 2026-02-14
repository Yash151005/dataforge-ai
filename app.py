import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import io
import time
import hashlib
import sqlite3
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS — Bright White Professional Theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --primary:   #4f46e5;
    --primary-light: #818cf8;
    --accent:    #0ea5e9;
    --green:     #16a34a;
    --orange:    #ea580c;
    --pink:      #db2777;
    --purple:    #7c3aed;
    --bg-main:   #f8fafc;
    --bg-panel:  #f1f5f9;
    --bg-card:   #ffffff;
    --bg-hover:  #e0e7ff;
    --border:    #e2e8f0;
    --border-accent: #c7d2fe;
    --text-dark: #0f172a;
    --text-mid:  #334155;
    --text-soft: #64748b;
    --text-muted:#94a3b8;
    --shadow:    0 1px 3px rgba(0,0,0,0.08), 0 4px 16px rgba(79,70,229,0.08);
    --shadow-md: 0 4px 24px rgba(79,70,229,0.14);
}

/* ── Global ── */
.stApp {
    background: var(--bg-main) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-dark) !important;
}

html, body, [class*="css"] {
    color: var(--text-dark) !important;
}

#MainMenu, footer, header {visibility: hidden;}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-panel); }
::-webkit-scrollbar-thumb { background: var(--primary-light); border-radius: 3px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 12px rgba(79,70,229,0.06) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-dark) !important;
}

/* ── Main content area ── */
[data-testid="stAppViewContainer"] > .main {
    background: var(--bg-main) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: #ffffff !important;
    color: var(--text-dark) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
    outline: none !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-dark) !important;
}

.stSelectbox > div > div > div {
    color: var(--text-dark) !important;
    background: #ffffff !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--purple)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(79,70,229,0.3) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #4338ca, #6d28d9) !important;
    box-shadow: 0 4px 16px rgba(79,70,229,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Labels ── */
.stTextInput > label, .stSelectbox > label, .stSlider > label,
.stNumberInput > label, .stTextArea > label, .stCheckbox > label,
.stRadio > label, label {
    color: var(--text-mid) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    box-shadow: var(--shadow) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-soft) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: var(--primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
}

/* ── Expander ── */
details {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    box-shadow: var(--shadow) !important;
}

summary {
    color: var(--primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-panel) !important;
    border-bottom: 2px solid var(--border) !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 0 8px !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-soft) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 18px !important;
    border-radius: 6px 6px 0 0 !important;
}

.stTabs [aria-selected="true"] {
    color: var(--primary) !important;
    background: #ffffff !important;
    border-bottom: 2px solid var(--primary) !important;
}

/* ── Checkbox ── */
.stCheckbox > div > label > div {
    border-color: var(--primary) !important;
    background: #ffffff !important;
}

/* ── Slider ── */
.stSlider > div > div > div > div {
    background: var(--primary) !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 10px !important;
    border-left: 4px solid var(--primary) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--green), #15803d) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(22,163,74,0.3) !important;
}

.stDownloadButton > button:hover {
    box-shadow: 0 4px 14px rgba(22,163,74,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 2px dashed var(--border-accent) !important;
    border-radius: 12px !important;
}

/* ── Select dropdown options ── */
[data-baseweb="popover"] li {
    color: var(--text-dark) !important;
    background: #ffffff !important;
}

[data-baseweb="popover"] li:hover {
    background: var(--bg-hover) !important;
}

/* ── All text visible ── */
p, span, div, h1, h2, h3, h4, h5, h6, li, td, th {
    color: var(--text-dark);
}

.stMarkdown p { color: var(--text-mid) !important; }

/* ── Streamlit info/success/warning ── */
.stSuccess { background: #f0fdf4 !important; color: #15803d !important; border-color: #86efac !important; }
.stError   { background: #fff1f2 !important; color: #be123c !important; border-color: #fda4af !important; }
.stWarning { background: #fffbeb !important; color: #b45309 !important; border-color: #fcd34d !important; }
.stInfo    { background: #eff6ff !important; color: #1d4ed8 !important; border-color: #93c5fd !important; }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HTML COMPONENTS
# ─────────────────────────────────────────────────────────────

def render_header():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #0ea5e9 100%);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(79,70,229,0.3);
    ">
        <div style="
            position:absolute; top:0; right:0; width:300px; height:100%;
            background: radial-gradient(ellipse at right, rgba(255,255,255,0.15) 0%, transparent 70%);
        "></div>
        <div style="position:absolute; bottom:-20px; right:40px; font-size:120px; opacity:0.07;">⚡</div>
        <div style="display:flex; align-items:center; gap:20px; position:relative;">
            <div style="
                background: rgba(255,255,255,0.2); border-radius:16px;
                width:64px; height:64px; display:flex; align-items:center; justify-content:center;
                font-size:36px; backdrop-filter:blur(10px);
            ">⚡</div>
            <div>
                <h1 style="
                    font-family:'Plus Jakarta Sans',sans-serif; font-size:30px; font-weight:800;
                    color:#ffffff; margin:0; letter-spacing:1px;
                ">DataForge AI</h1>
                <p style="
                    font-family:'Inter',sans-serif; color:rgba(255,255,255,0.8); font-size:13px;
                    margin:4px 0 0 0; letter-spacing:1px; font-weight:500;
                ">Raw Data In → Model-Ready Out</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_step_badge(num, label, color):
    return f"""
    <div style="
        display:inline-flex; align-items:center; gap:10px;
        background: {color}12; border:1.5px solid {color}55;
        border-radius:10px; padding:8px 16px; margin:4px 0;
    ">
        <div style="
            width:28px; height:28px; border-radius:50%;
            background:{color}; color:#ffffff; font-weight:800;
            display:flex; align-items:center; justify-content:center;
            font-family:'Plus Jakarta Sans',sans-serif; font-size:13px;
        ">{num}</div>
        <span style="font-family:'Plus Jakarta Sans',sans-serif; font-size:13px; color:{color}; font-weight:700;">
            {label}
        </span>
    </div>"""

def render_stat_card(icon, value, label, color):
    return f"""
    <div style="
        background: #ffffff;
        border: 1px solid {color}33;
        border-top: 4px solid {color};
        border-radius: 12px; padding: 18px 16px;
        text-align:center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    ">
        <div style="font-size:26px; margin-bottom:6px;">{icon}</div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:24px; color:{color}; font-weight:800; line-height:1;">{value}</div>
        <div style="font-family:'Inter',sans-serif; color:#64748b; font-size:12px; font-weight:500; margin-top:4px; letter-spacing:0.3px;">{label}</div>
    </div>"""

def render_section_title(icon, title, color="#4f46e5"):
    st.markdown(f"""
    <div style="
        display:flex; align-items:center; gap:10px;
        border-bottom: 2px solid {color}22;
        padding-bottom: 10px; margin: 24px 0 16px 0;
    ">
        <div style="
            background:{color}15; border-radius:8px;
            width:34px; height:34px; display:flex; align-items:center; justify-content:center;
            font-size:18px;
        ">{icon}</div>
        <span style="font-family:'Plus Jakarta Sans',sans-serif; font-size:15px; color:{color}; font-weight:800; letter-spacing:0.3px;">
            {title}
        </span>
    </div>
    """, unsafe_allow_html=True)

def render_tag(text, color):
    return f'<span style="background:{color}15; border:1.5px solid {color}44; color:{color}; border-radius:6px; padding:3px 10px; font-family:\'Inter\',sans-serif; font-size:11px; font-weight:600; margin:2px; display:inline-block;">{text}</span>'

# ─────────────────────────────────────────────────────────────
# DATABASE (SQLite — all free, no cloud)
# ─────────────────────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect("dataforge.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        created_at TEXT,
        role TEXT DEFAULT 'user'
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS pipeline_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        pipeline_name TEXT,
        dataset_name TEXT,
        rows_in INTEGER,
        rows_out INTEGER,
        columns_in INTEGER,
        columns_out INTEGER,
        steps_applied TEXT,
        created_at TEXT,
        status TEXT,
        notes TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS saved_configs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        config_name TEXT,
        config_json TEXT,
        created_at TEXT
    )""")
    # Seed demo admin
    admin_pw = hashlib.sha256("admin123".encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username, password, email, created_at, role) VALUES (?,?,?,?,?)",
                  ("admin", admin_pw, "admin@dataforge.ai", datetime.now().isoformat(), "admin"))
    except:
        pass
    conn.commit()
    conn.close()

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, password, email):
    conn = sqlite3.connect("dataforge.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, email, created_at) VALUES (?,?,?,?)",
                  (username, hash_pw(password), email, datetime.now().isoformat()))
        conn.commit()
        return True, "Account created!"
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("dataforge.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_pw(password)))
    user = c.fetchone()
    conn.close()
    return user

def save_pipeline_run(username, name, dataset, r_in, r_out, c_in, c_out, steps, status, notes=""):
    conn = sqlite3.connect("dataforge.db")
    c = conn.cursor()
    c.execute("""INSERT INTO pipeline_history
        (username, pipeline_name, dataset_name, rows_in, rows_out, columns_in, columns_out, steps_applied, created_at, status, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (username, name, dataset, r_in, r_out, c_in, c_out, json.dumps(steps),
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status, notes))
    conn.commit()
    conn.close()

def get_user_history(username):
    conn = sqlite3.connect("dataforge.db")
    df = pd.read_sql_query(
        "SELECT * FROM pipeline_history WHERE username=? ORDER BY created_at DESC",
        conn, params=(username,))
    conn.close()
    return df

def save_config(username, config_name, config_dict):
    conn = sqlite3.connect("dataforge.db")
    c = conn.cursor()
    c.execute("INSERT INTO saved_configs (username, config_name, config_json, created_at) VALUES (?,?,?,?)",
              (username, config_name, json.dumps(config_dict), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_user_configs(username):
    conn = sqlite3.connect("dataforge.db")
    df = pd.read_sql_query(
        "SELECT * FROM saved_configs WHERE username=? ORDER BY created_at DESC",
        conn, params=(username,))
    conn.close()
    return df

def get_all_users():
    conn = sqlite3.connect("dataforge.db")
    df = pd.read_sql_query("SELECT id,username,email,created_at,role FROM users", conn)
    conn.close()
    return df

def get_all_history():
    conn = sqlite3.connect("dataforge.db")
    df = pd.read_sql_query("SELECT * FROM pipeline_history ORDER BY created_at DESC", conn)
    conn.close()
    return df

# ─────────────────────────────────────────────────────────────
# AUTH PAGE
# ─────────────────────────────────────────────────────────────

def auth_page():
    render_header()
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("""
        <div style="
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 20px; padding: 40px 36px;
            box-shadow: 0 8px 40px rgba(79,70,229,0.12);
        ">
        <div style="text-align:center; margin-bottom:28px;">
            <div style="font-size:48px; margin-bottom:8px;">⚡</div>
            <h2 style="font-family:'Plus Jakarta Sans',sans-serif; font-size:22px; font-weight:800;
                color:#0f172a; margin:0;">Welcome to DataForge AI</h2>
            <p style="font-family:'Inter',sans-serif; color:#64748b; font-size:13px; margin:6px 0 0;">
                Sign in to your pipeline workspace
            </p>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["⚡  LOGIN", "🔮  REGISTER"])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username", key="l_user", placeholder="your_username")
            password = st.text_input("Password", type="password", key="l_pass", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In →", key="login_btn", use_container_width=True):
                if username and password:
                    user = login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = user[1]
                        st.session_state.role = user[5]
                        st.session_state.email = user[3]
                        st.success(f"Welcome back, {user[1]}!")
                        time.sleep(0.8)
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.warning("Please enter your credentials.")
            st.markdown("""
            <div style="text-align:center; margin-top:16px;
                background:#f8fafc; border-radius:8px; padding:10px;">
                <span style="font-family:'Space Mono',monospace; color:#64748b; font-size:11px;">
              
                </span>
            </div>""", unsafe_allow_html=True)

        with tab_register:
            st.markdown("<br>", unsafe_allow_html=True)
            r_user = st.text_input("Choose Username", key="r_user", placeholder="forge_user_01")
            r_email = st.text_input("Email", key="r_email", placeholder="you@domain.com")
            r_pass = st.text_input("Password", type="password", key="r_pass", placeholder="••••••••")
            r_pass2 = st.text_input("Confirm Password", type="password", key="r_pass2", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account →", key="reg_btn", use_container_width=True):
                if r_pass != r_pass2:
                    st.error("Passwords do not match.")
                elif len(r_pass) < 6:
                    st.error("Password too short (min 6 chars).")
                elif r_user and r_email and r_pass:
                    ok, msg = register_user(r_user, r_pass, r_email)
                    if ok:
                        st.success(msg + " Please login.")
                    else:
                        st.error(msg)
                else:
                    st.warning("Fill all fields.")

        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PIPELINE CORE FUNCTIONS
# ─────────────────────────────────────────────────────────────

def run_validation(df):
    report = {}
    report["total_rows"] = len(df)
    report["total_cols"] = len(df.columns)
    report["missing"] = df.isnull().sum().to_dict()
    report["missing_pct"] = (df.isnull().mean() * 100).round(2).to_dict()
    report["dtypes"] = df.dtypes.astype(str).to_dict()
    report["duplicates"] = int(df.duplicated().sum())
    report["duplicate_pct"] = round(df.duplicated().mean() * 100, 2)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outlier_report = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        n_out = int(((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum())
        outlier_report[col] = n_out
    report["outliers"] = outlier_report
    report["cardinality"] = {c: int(df[c].nunique()) for c in df.columns}
    return report

def clean_data(df, opts):
    steps = []
    original_rows = len(df)

    if opts.get("drop_duplicates"):
        before = len(df)
        df = df.drop_duplicates()
        steps.append(f"Removed {before - len(df)} duplicate rows")

    if opts.get("handle_missing") == "Drop rows":
        before = len(df)
        df = df.dropna()
        steps.append(f"Dropped {before - len(df)} rows with missing values")
    elif opts.get("handle_missing") == "Mean (numeric)":
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            n = df[col].isnull().sum()
            if n > 0:
                df[col] = df[col].fillna(df[col].mean())
                steps.append(f"Filled '{col}' missing ({n}) with mean={df[col].mean():.3f}")
    elif opts.get("handle_missing") == "Median (numeric)":
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            n = df[col].isnull().sum()
            if n > 0:
                df[col] = df[col].fillna(df[col].median())
                steps.append(f"Filled '{col}' missing ({n}) with median={df[col].median():.3f}")
    elif opts.get("handle_missing") == "Mode (categorical)":
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        for col in cat_cols:
            n = df[col].isnull().sum()
            if n > 0:
                df[col] = df[col].fillna(df[col].mode()[0])
                steps.append(f"Filled '{col}' missing ({n}) with mode")
    elif opts.get("handle_missing") == "Fill with 0":
        df = df.fillna(0)
        steps.append("Filled all missing values with 0")
    elif opts.get("handle_missing") == "Forward Fill":
        df = df.ffill()
        steps.append("Forward-filled all missing values")
    elif opts.get("handle_missing") == "Backward Fill":
        df = df.bfill()
        steps.append("Backward-filled all missing values")

    if opts.get("remove_outliers"):
        num_cols = df.select_dtypes(include=[np.number]).columns
        before = len(df)
        for col in num_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR))]
        steps.append(f"Removed {before - len(df)} outlier rows (IQR method)")

    if opts.get("strip_text"):
        cat_cols = df.select_dtypes(include=["object"]).columns
        for col in cat_cols:
            df[col] = df[col].astype(str).str.strip().str.lower()
        if len(cat_cols) > 0:
            steps.append(f"Normalized text in {len(cat_cols)} columns (strip + lowercase)")

    if opts.get("drop_cols"):
        cols_to_drop = [c.strip() for c in opts["drop_cols"].split(",") if c.strip() in df.columns]
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
            steps.append(f"Dropped columns: {cols_to_drop}")

    return df, steps

def engineer_features(df, opts):
    steps = []

    if opts.get("encoding") and opts.get("encoding") != "None":
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        if opts["encoding"] == "Label Encoding":
            for col in cat_cols:
                unique_vals = df[col].unique()
                mapping = {v: i for i, v in enumerate(unique_vals)}
                df[col] = df[col].map(mapping)
            if cat_cols:
                steps.append(f"Label encoded: {cat_cols}")
        elif opts["encoding"] == "One-Hot Encoding":
            try:
                df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
                steps.append(f"One-hot encoded: {cat_cols}")
            except:
                steps.append("One-hot encoding skipped (type issues)")

    if opts.get("scaling") and opts.get("scaling") != "None":
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if opts["scaling"] == "Standard Scaler":
            for col in num_cols:
                mean, std = df[col].mean(), df[col].std()
                if std != 0:
                    df[col] = (df[col] - mean) / std
            if num_cols:
                steps.append(f"StandardScaler applied to: {num_cols[:3]}{'...' if len(num_cols)>3 else ''}")
        elif opts["scaling"] == "Min-Max Scaler":
            for col in num_cols:
                mn, mx = df[col].min(), df[col].max()
                if mx != mn:
                    df[col] = (df[col] - mn) / (mx - mn)
            if num_cols:
                steps.append(f"MinMaxScaler applied to: {num_cols[:3]}{'...' if len(num_cols)>3 else ''}")
        elif opts["scaling"] == "Robust Scaler":
            for col in num_cols:
                med = df[col].median()
                iqr = df[col].quantile(0.75) - df[col].quantile(0.25)
                if iqr != 0:
                    df[col] = (df[col] - med) / iqr
            if num_cols:
                steps.append(f"RobustScaler applied to: {num_cols[:3]}{'...' if len(num_cols)>3 else ''}")

    if opts.get("add_polynomial") and opts.get("poly_cols"):
        poly_cols = [c.strip() for c in opts["poly_cols"].split(",") if c.strip() in df.columns]
        degree = opts.get("poly_degree", 2)
        for col in poly_cols:
            for d in range(2, degree + 1):
                df[f"{col}_pow{d}"] = df[col] ** d
        if poly_cols:
            steps.append(f"Added polynomial features (deg {degree}) for: {poly_cols}")

    if opts.get("add_log") and opts.get("log_cols"):
        log_cols = [c.strip() for c in opts["log_cols"].split(",") if c.strip() in df.columns]
        for col in log_cols:
            df[f"{col}_log"] = np.log1p(np.abs(df[col]))
        if log_cols:
            steps.append(f"Added log1p features for: {log_cols}")

    if opts.get("add_interaction") and opts.get("int_col1") and opts.get("int_col2"):
        c1, c2 = opts["int_col1"], opts["int_col2"]
        if c1 in df.columns and c2 in df.columns:
            df[f"{c1}_x_{c2}"] = df[c1] * df[c2]
            steps.append(f"Added interaction feature: {c1} × {c2}")

    return df, steps

def split_data(df, target_col, test_size, val_size, stratify):
    steps = []
    n = len(df)
    if target_col and target_col in df.columns:
        X = df.drop(columns=[target_col])
        y = df[target_col]
    else:
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

    # Manual stratified split
    n_test = int(n * test_size)
    n_val = int(n * val_size)
    n_train = n - n_test - n_val

    idx = np.random.permutation(n)
    if stratify and len(y.unique()) < 20:
        # Simple stratified
        classes = y.unique()
        train_idx, val_idx, test_idx = [], [], []
        for cls in classes:
            cls_idx = np.where(y.values == cls)[0]
            np.random.shuffle(cls_idx)
            n_cls = len(cls_idx)
            n_t = max(1, int(n_cls * test_size))
            n_v = max(1, int(n_cls * val_size))
            test_idx.extend(cls_idx[:n_t])
            val_idx.extend(cls_idx[n_t:n_t+n_v])
            train_idx.extend(cls_idx[n_t+n_v:])
        steps.append("Stratified split applied")
    else:
        train_idx = idx[:n_train]
        val_idx = idx[n_train:n_train+n_val]
        test_idx = idx[n_train+n_val:]

    X_train = X.iloc[train_idx]
    y_train = y.iloc[train_idx]
    X_val = X.iloc[val_idx]
    y_val = y.iloc[val_idx]
    X_test = X.iloc[test_idx]
    y_test = y.iloc[test_idx]

    steps.append(f"Train: {len(X_train)} rows | Val: {len(X_val)} rows | Test: {len(X_test)} rows")
    return X_train, y_train, X_val, y_val, X_test, y_test, steps

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:20px 0 12px;">
            <div style="
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                width:52px; height:52px; border-radius:14px;
                display:flex; align-items:center; justify-content:center;
                font-size:26px; margin:0 auto 10px;
                box-shadow: 0 4px 14px rgba(79,70,229,0.35);
            ">⚡</div>
            <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:17px; font-weight:800;
                color:#0f172a; letter-spacing:0.5px;">DataForge AI</div>
            <div style="font-family:'Inter',sans-serif; font-size:11px; color:#94a3b8; margin-top:2px;">Pipeline System</div>
        </div>
        <hr style="border:none; border-top:1px solid #e2e8f0; margin:0 0 12px;">
        """, unsafe_allow_html=True)

        # User info
        role_badge = "🔴 Admin" if st.session_state.get('role') == 'admin' else "🟢 User"
        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0;
            border-radius:10px; padding:12px 14px; margin-bottom:14px;">
            <div style="font-family:'Inter',sans-serif; font-size:11px; color:#94a3b8; font-weight:500;">SIGNED IN AS</div>
            <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:15px; color:#0f172a; font-weight:700; margin-top:2px;">
                {st.session_state.get('username','USER')}
            </div>
            <div style="font-family:'Inter',sans-serif; font-size:11px; color:#7c3aed; font-weight:600; margin-top:2px;">
                {role_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

        pages = ["🏠 Dashboard", "⚡ Pipeline Builder", "📊 Data Explorer",
                 "🕐 Run History", "⚙️ Saved Configs", "📖 Documentation"]
        if st.session_state.get("role") == "admin":
            pages.append("🛡️ Admin Panel")

        page = st.selectbox("NAVIGATE", pages, label_visibility="collapsed")

        st.markdown("<hr style='border-color:rgba(0,245,255,0.15);'>", unsafe_allow_html=True)

        # Quick stats
        hist = get_user_history(st.session_state.get("username", ""))
        total_runs = len(hist)
        success_runs = len(hist[hist["status"] == "Success"]) if total_runs > 0 else 0

        st.markdown(f"""
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:14px;">
            <div style="background:#eff6ff; border:1px solid #bfdbfe;
                border-radius:8px; padding:10px; text-align:center;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:20px; color:#4f46e5; font-weight:800;">{total_runs}</div>
                <div style="font-family:'Inter',sans-serif; font-size:10px; color:#64748b; font-weight:500;">TOTAL RUNS</div>
            </div>
            <div style="background:#f0fdf4; border:1px solid #bbf7d0;
                border-radius:8px; padding:10px; text-align:center;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:20px; color:#16a34a; font-weight:800;">{success_runs}</div>
                <div style="font-family:'Inter',sans-serif; font-size:10px; color:#64748b; font-weight:500;">SUCCESS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border:none; border-top:1px solid #e2e8f0;'>", unsafe_allow_html=True)

        if st.button("⏻  Sign Out", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        return page

# ─────────────────────────────────────────────────────────────
# DASHBOARD PAGE
# ─────────────────────────────────────────────────────────────

def dashboard_page():
    render_header()
    render_section_title("📡", "SYSTEM OVERVIEW")

    hist = get_user_history(st.session_state.get("username", ""))
    total = len(hist)
    success = len(hist[hist["status"] == "Success"]) if total > 0 else 0
    total_rows_processed = hist["rows_in"].sum() if total > 0 else 0
    success_rate = round((success / total) * 100) if total > 0 else 0

    cols = st.columns(4)
    stats = [
        ("🧪", str(total), "PIPELINE RUNS", "#4f46e5"),
        ("✅", str(success), "SUCCESSFUL", "#16a34a"),
        ("📦", f"{total_rows_processed:,}", "ROWS PROCESSED", "#ea580c"),
        ("🎯", f"{success_rate}%", "SUCCESS RATE", "#7c3aed"),
    ]
    for i, (icon, val, label, color) in enumerate(stats):
        with cols[i]:
            st.markdown(render_stat_card(icon, val, label, color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.6, 1])

    with col1:
        render_section_title("🕐", "RECENT PIPELINE RUNS", "#16a34a")
        if total > 0:
            show_hist = hist.head(5)[["pipeline_name","dataset_name","rows_in","rows_out","status","created_at"]].copy()
            show_hist.columns = ["Pipeline","Dataset","Rows In","Rows Out","Status","When"]
            st.dataframe(show_hist, use_container_width=True, hide_index=True)
        else:
            st.info("No pipeline runs yet. Head to Pipeline Builder!")

    with col2:
        render_section_title("⚡", "QUICK START", "#ea580c")
        st.markdown("""
        <div style="background:linear-gradient(135deg,#eff6ff,#f5f3ff); border:1px solid #c7d2fe;
            border-radius:12px; padding:18px;">
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Inter',sans-serif; color:#334155; line-height:2.2; font-size:14px;">
        <b style="color:#4f46e5;">Step 1:</b> Upload your CSV<br>
        <b style="color:#16a34a;">Step 2:</b> Configure cleaning<br>
        <b style="color:#ea580c;">Step 3:</b> Engineer features<br>
        <b style="color:#7c3aed;">Step 4:</b> Split your data<br>
        <b style="color:#db2777;">Step 5:</b> Export &amp; download!
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        render_section_title("📋", "PIPELINE STAGES", "#7c3aed")
        stages = [
            ("1", "Ingestion",   "#4f46e5"),
            ("2", "Validation",  "#16a34a"),
            ("3", "Cleaning",    "#ea580c"),
            ("4", "Feature Eng", "#7c3aed"),
            ("5", "Splitting",   "#db2777"),
            ("6", "Export",      "#0ea5e9"),
        ]
        for num, label, color in stages:
            st.markdown(render_step_badge(num, label, color), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PIPELINE BUILDER PAGE
# ─────────────────────────────────────────────────────────────

def pipeline_builder_page():
    render_section_title("⚡", "PIPELINE BUILDER")

    # ── STAGE 1: INGESTION
    render_section_title("📥", "STAGE 1 — DATA INGESTION", "#4f46e5")
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Dataset (CSV, Excel, JSON)", 
            type=["csv", "xlsx", "xls", "json"],
            key="pipeline_upload"
        )
    with col2:
        pipeline_name = st.text_input("Pipeline Name", value=f"pipeline_{datetime.now().strftime('%H%M%S')}")
        separator = st.selectbox("CSV Separator", [",", ";", "\t", "|"], index=0)
        encoding = st.selectbox("Encoding", ["utf-8", "latin-1", "iso-8859-1"])

    if uploaded_file is None:
        st.markdown("""
        <div style="background:#f8fafc; border:2px dashed #c7d2fe;
            border-radius:16px; padding:48px; text-align:center; margin:16px 0;">
            <div style="font-size:52px; margin-bottom:12px;">📂</div>
            <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:15px; color:#334155; font-weight:700;">
                Upload a Dataset to Begin
            </div>
            <div style="font-family:'Inter',sans-serif; font-size:12px; color:#94a3b8; margin-top:6px;">
                Supports CSV · Excel · JSON
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Load data
    try:
        if uploaded_file.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded_file, sep=separator, encoding=encoding)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df_raw = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            df_raw = pd.read_json(uploaded_file)
        else:
            st.error("Unsupported format.")
            return
    except Exception as e:
        st.error(f"Failed to load file: {e}")
        return

    st.session_state["df_raw"] = df_raw.copy()
    rows_in = len(df_raw)
    cols_in = len(df_raw.columns)

    st.success(f"✅ Dataset loaded: **{uploaded_file.name}** — {rows_in:,} rows × {cols_in} columns")

    # ── STAGE 2: VALIDATION
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("🔍", "STAGE 2 — VALIDATION REPORT", "#16a34a")

    val_report = run_validation(df_raw)

    v1, v2, v3, v4 = st.columns(4)
    metrics = [
        ("Rows", f"{rows_in:,}", "#4f46e5"),
        ("Columns", str(cols_in), "#16a34a"),
        ("Duplicates", str(val_report["duplicates"]), "#ea580c"),
        ("Total Missing", str(sum(val_report["missing"].values())), "#7c3aed"),
    ]
    for (label, val, color), col in zip(metrics, [v1, v2, v3, v4]):
        with col:
            st.markdown(render_stat_card("", val, label, color), unsafe_allow_html=True)

    with st.expander("📊 Full Validation Report", expanded=False):
        tab_missing, tab_dtypes, tab_outliers, tab_card = st.tabs([
            "Missing Values", "Data Types", "Outliers", "Cardinality"
        ])
        with tab_missing:
            miss_df = pd.DataFrame({
                "Column": list(val_report["missing"].keys()),
                "Missing Count": list(val_report["missing"].values()),
                "Missing %": list(val_report["missing_pct"].values())
            })
            miss_df = miss_df[miss_df["Missing Count"] > 0].sort_values("Missing %", ascending=False)
            if len(miss_df) > 0:
                st.dataframe(miss_df, use_container_width=True, hide_index=True)
            else:
                st.success("No missing values detected!")
        with tab_dtypes:
            dtype_df = pd.DataFrame({"Column": list(val_report["dtypes"].keys()),
                                     "Data Type": list(val_report["dtypes"].values())})
            st.dataframe(dtype_df, use_container_width=True, hide_index=True)
        with tab_outliers:
            out_df = pd.DataFrame({"Column": list(val_report["outliers"].keys()),
                                   "Outlier Count": list(val_report["outliers"].values())})
            out_df = out_df[out_df["Outlier Count"] > 0].sort_values("Outlier Count", ascending=False)
            if len(out_df) > 0:
                st.dataframe(out_df, use_container_width=True, hide_index=True)
            else:
                st.success("No significant outliers detected!")
        with tab_card:
            card_df = pd.DataFrame({"Column": list(val_report["cardinality"].keys()),
                                    "Unique Values": list(val_report["cardinality"].values())})
            st.dataframe(card_df, use_container_width=True, hide_index=True)

    # ── STAGE 3: CLEANING
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("🧹", "STAGE 3 — DATA CLEANING", "#ea580c")

    col1, col2 = st.columns(2)
    with col1:
        handle_missing = st.selectbox(
            "Handle Missing Values",
            ["None", "Drop rows", "Mean (numeric)", "Median (numeric)",
             "Mode (categorical)", "Fill with 0", "Forward Fill", "Backward Fill"]
        )
        drop_duplicates = st.checkbox("Remove Duplicate Rows", value=True)
        remove_outliers = st.checkbox("Remove Outliers (IQR Method)")
    with col2:
        strip_text = st.checkbox("Normalize Text (strip + lowercase)", value=True)
        drop_cols_raw = st.text_input("Drop Columns (comma-separated)", placeholder="col1, col2, col3")

    clean_opts = {
        "handle_missing": handle_missing,
        "drop_duplicates": drop_duplicates,
        "remove_outliers": remove_outliers,
        "strip_text": strip_text,
        "drop_cols": drop_cols_raw,
    }

    # ── STAGE 4: FEATURE ENGINEERING
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("⚙️", "STAGE 4 — FEATURE ENGINEERING", "#7c3aed")

    col1, col2 = st.columns(2)
    with col1:
        encoding = st.selectbox("Categorical Encoding", ["None", "Label Encoding", "One-Hot Encoding"])
        scaling = st.selectbox("Numeric Scaling", ["None", "Standard Scaler", "Min-Max Scaler", "Robust Scaler"])
    with col2:
        add_poly = st.checkbox("Polynomial Features")
        add_log = st.checkbox("Log Transform Features")
        add_interaction = st.checkbox("Interaction Features")

    feat_opts = {"encoding": encoding, "scaling": scaling,
                 "add_polynomial": add_poly, "add_log": add_log, "add_interaction": add_interaction}

    if add_poly:
        c1, c2 = st.columns(2)
        with c1:
            feat_opts["poly_cols"] = st.text_input("Columns for Poly Features", placeholder="col1, col2")
        with c2:
            feat_opts["poly_degree"] = st.slider("Degree", 2, 4, 2)
    if add_log:
        feat_opts["log_cols"] = st.text_input("Columns for Log Transform", placeholder="col1, col2")
    if add_interaction:
        c1, c2 = st.columns(2)
        with c1:
            feat_opts["int_col1"] = st.selectbox("Feature 1", [""] + list(df_raw.select_dtypes(include=[np.number]).columns))
        with c2:
            feat_opts["int_col2"] = st.selectbox("Feature 2", [""] + list(df_raw.select_dtypes(include=[np.number]).columns))

    # ── STAGE 5: SPLITTING
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("✂️", "STAGE 5 — TRAIN/VAL/TEST SPLIT", "#db2777")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        target_col = st.selectbox("Target Column", ["(last column)"] + list(df_raw.columns))
        if target_col == "(last column)":
            target_col = df_raw.columns[-1]
    with col2:
        test_size = st.slider("Test Size %", 5, 40, 20) / 100
    with col3:
        val_size = st.slider("Val Size %", 5, 40, 10) / 100
    with col4:
        stratify = st.checkbox("Stratified Split", value=True)
        random_seed = st.number_input("Random Seed", value=42, step=1)

    np.random.seed(int(random_seed))

    # ── STAGE 6: PIPELINE CONFIG SAVE & RUN
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("💾", "STAGE 6 — SAVE CONFIG & EXECUTE", "#4f46e5")

    col1, col2 = st.columns([1, 2])
    with col1:
        config_name = st.text_input("Save Config As", placeholder="my_credit_risk_config")
        run_notes = st.text_area("Notes for this run", placeholder="e.g. First run on raw credit data...", height=80)
    with col2:
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0;
            border-radius:10px; padding:16px; height:100%;">
            <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:12px; color:#64748b; font-weight:700; letter-spacing:0.5px; margin-bottom:10px;">
                PIPELINE SUMMARY
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-family:'Inter',sans-serif; font-size:13px; color:#334155; line-height:2.2;">
        📂 Dataset: <span style="color:#4f46e5; font-weight:600;">{uploaded_file.name}</span><br>
        🧹 Missing: <span style="color:#ea580c; font-weight:600;">{handle_missing}</span><br>
        🔧 Encoding: <span style="color:#7c3aed; font-weight:600;">{encoding}</span><br>
        📏 Scaling: <span style="color:#db2777; font-weight:600;">{scaling}</span><br>
        🎯 Target: <span style="color:#16a34a; font-weight:600;">{target_col}</span><br>
        ✂️ Split: <span style="color:#0ea5e9; font-weight:600;">Train {int((1-test_size-val_size)*100)}% / Val {int(val_size*100)}% / Test {int(test_size*100)}%</span>
        </div>
        </div>
        """, unsafe_allow_html=True)

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        save_conf_btn = st.button("💾 SAVE CONFIG", use_container_width=True)
    with btn_col2:
        run_btn = st.button("⚡ RUN PIPELINE", use_container_width=True, type="primary")
    with btn_col3:
        preview_btn = st.button("👁 PREVIEW DATA", use_container_width=True)

    if save_conf_btn and config_name:
        full_config = {
            "clean": clean_opts, "features": feat_opts,
            "target": target_col, "test_size": test_size,
            "val_size": val_size, "stratify": stratify, "seed": int(random_seed)
        }
        save_config(st.session_state["username"], config_name, full_config)
        st.success(f"Config saved as '{config_name}'")

    if preview_btn:
        with st.expander("📋 Raw Data Preview", expanded=True):
            st.dataframe(df_raw.head(20), use_container_width=True)

    if run_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        render_section_title("🚀", "EXECUTING PIPELINE...", "#4f46e5")

        prog = st.progress(0)
        status_box = st.empty()
        all_steps = []

        try:
            status_box.info("⚡ Stage 1: Loading data...")
            prog.progress(15)
            time.sleep(0.3)
            df_work = df_raw.copy()

            status_box.info("🧹 Stage 2: Cleaning data...")
            prog.progress(30)
            df_work, clean_steps = clean_data(df_work, clean_opts)
            all_steps.extend(clean_steps)
            time.sleep(0.3)

            status_box.info("⚙️ Stage 3: Engineering features...")
            prog.progress(55)
            df_work, feat_steps = engineer_features(df_work, feat_opts)
            all_steps.extend(feat_steps)
            time.sleep(0.3)

            status_box.info("✂️ Stage 4: Splitting data...")
            prog.progress(75)
            X_train, y_train, X_val, y_val, X_test, y_test, split_steps = split_data(
                df_work, target_col, test_size, val_size, stratify
            )
            all_steps.extend(split_steps)
            time.sleep(0.3)

            prog.progress(100)
            status_box.success("✅ PIPELINE EXECUTION COMPLETE!")

            rows_out = len(df_work)
            cols_out = len(df_work.columns)

            # Save to history
            save_pipeline_run(
                st.session_state["username"], pipeline_name, uploaded_file.name,
                rows_in, rows_out, cols_in, cols_out, all_steps, "Success", run_notes
            )

            # Results
            st.markdown("<br>", unsafe_allow_html=True)
            render_section_title("📊", "PIPELINE RESULTS", "#16a34a")

            r1, r2, r3, r4 = st.columns(4)
            results = [
                ("Rows In", f"{rows_in:,}", "#4f46e5"),
                ("Rows Out", f"{rows_out:,}", "#16a34a"),
                ("Train Set", f"{len(X_train):,}", "#ea580c"),
                ("Test Set", f"{len(X_test):,}", "#7c3aed"),
            ]
            for (label, val, color), col in zip(results, [r1, r2, r3, r4]):
                with col:
                    st.markdown(render_stat_card("", val, label, color), unsafe_allow_html=True)

            with st.expander("📋 Applied Transformations Log", expanded=True):
                for i, step in enumerate(all_steps, 1):
                    st.markdown(f"""
                    <div style="font-family:'Inter',sans-serif; font-size:13px;
                        color:#334155; padding:6px 0; border-bottom:1px solid #f1f5f9; display:flex; gap:10px; align-items:center;">
                        <span style="background:#eff6ff; color:#4f46e5; border-radius:6px; padding:2px 8px; font-weight:700; font-size:11px; min-width:28px; text-align:center;">{i}</span>
                        {step}
                    </div>
                    """, unsafe_allow_html=True)

            # Downloads
            st.markdown("<br>", unsafe_allow_html=True)
            render_section_title("⬇️", "DOWNLOAD PROCESSED DATA", "#db2777")

            d1, d2, d3, d4 = st.columns(4)

            train_df = pd.concat([X_train, y_train], axis=1)
            val_df = pd.concat([X_val, y_val], axis=1)
            test_df = pd.concat([X_test, y_test], axis=1)

            with d1:
                st.download_button("⬇️ TRAIN SET",
                    train_df.to_csv(index=False).encode(),
                    "train.csv", "text/csv", use_container_width=True)
            with d2:
                st.download_button("⬇️ VAL SET",
                    val_df.to_csv(index=False).encode(),
                    "val.csv", "text/csv", use_container_width=True)
            with d3:
                st.download_button("⬇️ TEST SET",
                    test_df.to_csv(index=False).encode(),
                    "test.csv", "text/csv", use_container_width=True)
            with d4:
                st.download_button("⬇️ FULL CLEAN",
                    df_work.to_csv(index=False).encode(),
                    "full_clean.csv", "text/csv", use_container_width=True)

            # Pipeline report JSON
            report = {
                "pipeline_name": pipeline_name,
                "run_at": datetime.now().isoformat(),
                "dataset": uploaded_file.name,
                "rows_in": rows_in, "rows_out": rows_out,
                "cols_in": cols_in, "cols_out": cols_out,
                "steps": all_steps,
                "split": {"train": len(X_train), "val": len(X_val), "test": len(X_test)},
                "config": {"clean": clean_opts, "features": feat_opts}
            }
            st.download_button("📄 PIPELINE REPORT (JSON)",
                json.dumps(report, indent=2).encode(),
                "pipeline_report.json", "application/json", use_container_width=True)

            st.session_state["last_df"] = df_work
            st.session_state["last_splits"] = {
                "X_train": X_train, "y_train": y_train,
                "X_val": X_val, "y_val": y_val,
                "X_test": X_test, "y_test": y_test
            }

        except Exception as e:
            prog.progress(0)
            status_box.error(f"Pipeline failed: {e}")
            save_pipeline_run(
                st.session_state["username"], pipeline_name, uploaded_file.name,
                rows_in, 0, cols_in, 0, [], "Failed", str(e)
            )

# ─────────────────────────────────────────────────────────────
# DATA EXPLORER PAGE
# ─────────────────────────────────────────────────────────────

def data_explorer_page():
    render_section_title("📊", "DATA EXPLORER")

    uploaded = st.file_uploader("Load CSV to Explore", type=["csv", "xlsx"])
    df = None

    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        st.session_state["explorer_df"] = df

    if "explorer_df" in st.session_state:
        df = st.session_state["explorer_df"]
    elif "df_raw" in st.session_state:
        df = st.session_state["df_raw"]
        st.info("Showing dataset from Pipeline Builder.")

    if df is None:
        st.info("Upload a CSV file to explore your data.")
        return

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Preview", "📈 Statistics", "🔍 Filter & Search", "🎨 Visualize"])

    with tab1:
        n_rows = st.slider("Rows to display", 5, min(200, len(df)), 20)
        st.dataframe(df.head(n_rows), use_container_width=True)
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace; font-size:11px; color:#64748b; padding:8px;">
        Shape: <span style="color:#4f46e5;">{df.shape[0]:,} rows × {df.shape[1]} columns</span>
        | Memory: <span style="color:#16a34a;">{df.memory_usage(deep=True).sum() / 1024:.1f} KB</span>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        num_df = df.select_dtypes(include=[np.number])
        if len(num_df.columns) > 0:
            render_section_title("📐", "NUMERIC STATISTICS", "#4f46e5")
            st.dataframe(num_df.describe().round(4), use_container_width=True)
        cat_df = df.select_dtypes(include=["object"])
        if len(cat_df.columns) > 0:
            render_section_title("🏷️", "CATEGORICAL STATISTICS", "#7c3aed")
            st.dataframe(cat_df.describe(), use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            filter_col = st.selectbox("Filter by Column", ["(none)"] + list(df.columns))
        with col2:
            search_term = st.text_input("Search Value", placeholder="Enter search term...")
        if filter_col != "(none)" and search_term:
            filtered = df[df[filter_col].astype(str).str.contains(search_term, case=False, na=False)]
            st.dataframe(filtered, use_container_width=True)
            st.markdown(f"Found **{len(filtered):,}** rows matching.")
        else:
            st.dataframe(df, use_container_width=True)

    with tab4:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
        render_section_title("📊", "DISTRIBUTION PLOTS", "#ea580c")
        if num_cols:
            sel_col = st.selectbox("Select numeric column", num_cols)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Distribution — {sel_col}**")
                hist_data = df[sel_col].dropna()
                counts, bins = np.histogram(hist_data, bins=30)
                hist_df = pd.DataFrame({"bin": bins[:-1], "count": counts})
                st.bar_chart(hist_df.set_index("bin"))
            with col2:
                if len(num_cols) >= 2:
                    sel_col2 = st.selectbox("Scatter Y-axis", [c for c in num_cols if c != sel_col])
                    scatter_df = df[[sel_col, sel_col2]].dropna()
                    st.scatter_chart(scatter_df.sample(min(500, len(scatter_df))))

        if cat_cols:
            st.markdown("<br>", unsafe_allow_html=True)
            render_section_title("🏷️", "CATEGORY COUNTS", "#7c3aed")
            sel_cat = st.selectbox("Select categorical column", cat_cols)
            vc = df[sel_cat].value_counts().head(15)
            st.bar_chart(vc)

# ─────────────────────────────────────────────────────────────
# HISTORY PAGE
# ─────────────────────────────────────────────────────────────

def history_page():
    render_section_title("🕐", "PIPELINE RUN HISTORY")
    hist = get_user_history(st.session_state.get("username", ""))

    if len(hist) == 0:
        st.info("No runs yet. Execute a pipeline to see history here.")
        return

    # Summary stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(render_stat_card("🧪", str(len(hist)), "TOTAL RUNS", "#4f46e5"), unsafe_allow_html=True)
    with c2:
        success_n = len(hist[hist["status"]=="Success"])
        st.markdown(render_stat_card("✅", str(success_n), "SUCCESSFUL", "#16a34a"), unsafe_allow_html=True)
    with c3:
        fail_n = len(hist[hist["status"]=="Failed"])
        st.markdown(render_stat_card("❌", str(fail_n), "FAILED", "#db2777"), unsafe_allow_html=True)
    with c4:
        total_rows = hist["rows_in"].sum()
        st.markdown(render_stat_card("📦", f"{total_rows:,}", "ROWS PROCESSED", "#ea580c"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Success", "Failed"])
    with col2:
        search_pipeline = st.text_input("Search Pipeline Name", placeholder="pipeline_name...")

    filtered = hist.copy()
    if status_filter != "All":
        filtered = filtered[filtered["status"] == status_filter]
    if search_pipeline:
        filtered = filtered[filtered["pipeline_name"].str.contains(search_pipeline, case=False, na=False)]

    st.markdown("<br>", unsafe_allow_html=True)

    for _, row in filtered.iterrows():
        status_color = "#16a34a" if row["status"] == "Success" else "#db2777"
        steps_parsed = []
        try:
            steps_parsed = json.loads(row["steps_applied"])
        except:
            pass

        with st.expander(f"{'✅' if row['status']=='Success' else '❌'} {row['pipeline_name']} — {row['created_at']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div style="font-family:'Inter',sans-serif; font-size:13px; color:#334155; line-height:2.2;">
                📂 Dataset: <span style="color:#4f46e5; font-weight:600;">{row['dataset_name']}</span><br>
                📥 Rows In: <span style="color:#16a34a; font-weight:600;">{row['rows_in']:,}</span><br>
                📤 Rows Out: <span style="color:#ea580c; font-weight:600;">{row['rows_out']:,}</span>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="font-family:'Inter',sans-serif; font-size:13px; color:#334155; line-height:2.2;">
                🔲 Cols In: <span style="color:#4f46e5; font-weight:600;">{row['columns_in']}</span><br>
                🔲 Cols Out: <span style="color:#7c3aed; font-weight:600;">{row['columns_out']}</span><br>
                🕐 Time: <span style="color:#db2777; font-weight:600;">{row['created_at']}</span>
                </div>""", unsafe_allow_html=True)
            with col3:
                if row.get("notes"):
                    st.markdown(f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0;
                        border-radius:8px; padding:10px; font-family:'Inter',sans-serif; font-size:12px; color:#64748b;">
                        📝 {row['notes']}
                    </div>""", unsafe_allow_html=True)

            if steps_parsed:
                st.markdown("**Applied Steps:**")
                steps_html = " ".join([render_tag(s[:50]+"..." if len(s)>50 else s, "#4f46e5") for s in steps_parsed])
                st.markdown(steps_html, unsafe_allow_html=True)

    # Export history
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("⬇️ EXPORT FULL HISTORY (CSV)",
        hist.to_csv(index=False).encode(), "pipeline_history.csv", "text/csv")

# ─────────────────────────────────────────────────────────────
# SAVED CONFIGS PAGE
# ─────────────────────────────────────────────────────────────

def saved_configs_page():
    render_section_title("⚙️", "SAVED PIPELINE CONFIGS")
    configs = get_user_configs(st.session_state.get("username", ""))

    if len(configs) == 0:
        st.info("No saved configs yet. Save a pipeline config in Pipeline Builder.")
        return

    for _, row in configs.iterrows():
        try:
            conf_data = json.loads(row["config_json"])
        except:
            conf_data = {}

        with st.expander(f"⚙️ {row['config_name']} — saved {row['created_at'][:16]}"):
            col1, col2 = st.columns(2)
            with col1:
                render_section_title("🧹", "Cleaning Config", "#ea580c")
                clean = conf_data.get("clean", {})
                st.markdown(f"""
                <div style="font-family:'Inter',sans-serif; font-size:13px; color:#334155; line-height:2.2;">
                Missing: <span style="color:#ea580c; font-weight:600;">{clean.get('handle_missing','N/A')}</span><br>
                Drop Dupes: <span style="color:#4f46e5; font-weight:600;">{clean.get('drop_duplicates','N/A')}</span><br>
                Outliers: <span style="color:#7c3aed; font-weight:600;">{clean.get('remove_outliers','N/A')}</span>
                </div>""", unsafe_allow_html=True)
            with col2:
                render_section_title("⚙️", "Feature Config", "#7c3aed")
                feat = conf_data.get("features", {})
                st.markdown(f"""
                <div style="font-family:'Inter',sans-serif; font-size:13px; color:#334155; line-height:2.2;">
                Encoding: <span style="color:#ea580c; font-weight:600;">{feat.get('encoding','N/A')}</span><br>
                Scaling: <span style="color:#4f46e5; font-weight:600;">{feat.get('scaling','N/A')}</span><br>
                Target: <span style="color:#16a34a; font-weight:600;">{conf_data.get('target','N/A')}</span>
                </div>""", unsafe_allow_html=True)

            st.download_button(
                f"⬇️ Export JSON",
                json.dumps(conf_data, indent=2).encode(),
                f"{row['config_name']}.json", "application/json"
            )

# ─────────────────────────────────────────────────────────────
# DOCUMENTATION PAGE
# ─────────────────────────────────────────────────────────────

def documentation_page():
    render_section_title("📖", "DOCUMENTATION & GUIDE")

    tabs = st.tabs(["🚀 Quick Start", "⚡ Pipeline Stages", "🔧 Features", "🏗️ Architecture"])

    with tabs[0]:
        st.markdown("""
        <div style="font-family:'Inter',sans-serif; font-size:15px; color:#334155; line-height:2.2;">

        <h3 style="font-family:'Plus Jakarta Sans',sans-serif; color:#4f46e5; font-size:15px; font-weight:800;">GETTING STARTED</h3>

        <b style="color:#4f46e5;">1. Upload Data</b> — Support for CSV, Excel (.xlsx), and JSON formats<br>
        <b style="color:#16a34a;">2. Validate</b> — Automatic schema &amp; quality report generated<br>
        <b style="color:#ea580c;">3. Clean</b> — Handle missing values, duplicates, outliers<br>
        <b style="color:#7c3aed;">4. Engineer</b> — Encode, scale, create new features<br>
        <b style="color:#db2777;">5. Split</b> — Auto train/val/test with optional stratification<br>
        <b style="color:#0ea5e9;">6. Export</b> — Download CSVs + JSON pipeline report<br>

       </div>
        """, unsafe_allow_html=True)

    with tabs[1]:
        stages = [
            ("📥", "Data Ingestion",     "#4f46e5",
             "CSV, Excel, JSON file upload. Auto-detection of separator and encoding. Schema inference."),
            ("🔍", "Validation",         "#16a34a",
             "Missing value detection, duplicate scan, outlier flagging (IQR), cardinality analysis, dtype check."),
            ("🧹", "Cleaning",           "#ea580c",
             "7 missing-value strategies, duplicate removal, IQR outlier removal, text normalization, column dropping."),
            ("⚙️", "Feature Engineering","#7c3aed",
             "Label/One-Hot encoding, Standard/MinMax/Robust scaling, polynomial features, log transforms, interaction terms."),
            ("✂️", "Data Splitting",     "#db2777",
             "Train/Val/Test split with custom ratios, optional stratification, reproducible random seed."),
            ("📤", "Export",             "#0ea5e9",
             "Download train/val/test CSVs individually, full clean CSV, and JSON pipeline execution report."),
        ]
        for icon, name, color, desc in stages:
            st.markdown(f"""
            <div style="background:#ffffff; border:1px solid {color}22; border-left:4px solid {color};
                border-radius:10px; padding:16px; margin:8px 0; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:13px; color:{color}; font-weight:800; margin-bottom:4px;">
                    {icon} {name}
                </div>
                <div style="font-family:'Inter',sans-serif; color:#64748b; font-size:13px;">
                    {desc}
                </div>
            </div>""", unsafe_allow_html=True)

    with tabs[2]:
        features = {
            "🔐 Authentication": "Secure login/register system with SHA-256 password hashing. Role-based access (admin/user).",
            "🕐 Run History": "Every pipeline execution logged with timestamps, row counts, applied steps, and status.",
            "⚙️ Config Saving": "Save pipeline configurations by name and re-apply them or export as JSON.",
            "📊 Data Explorer": "Interactive data browser with filtering, search, statistics, and charting.",
            "🛡️ Admin Panel": "Admin users can view all users and pipeline runs system-wide.",
            "📥 Multi-format": "Import CSV (with separator options), Excel, and JSON. Export as CSV or JSON.",
            "📄 Reports": "Auto-generated JSON pipeline execution report with full audit trail.",
        }
        for feat, desc in features.items():
            st.markdown(f"""
            <div style="display:flex; gap:16px; padding:12px; border-bottom:1px solid #f1f5f9; align-items:flex-start;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:13px; color:#4f46e5; font-weight:700; min-width:200px;">{feat}</div>
                <div style="font-family:'Inter',sans-serif; color:#64748b; font-size:13px;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("""
        <div style="font-family:'Space Mono',monospace; font-size:12px; color:#334155; line-height:2.2;
            background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:24px;">
dataforge_ai/<br>
├── app.py              <span style="color:#94a3b8;"># Main Streamlit app (this file)</span><br>
├── dataforge.db        <span style="color:#94a3b8;"># SQLite: users, history, configs</span><br>
│<br>
├── Auth Layer          <span style="color:#4f46e5; font-weight:700;"># register_user(), login_user()</span><br>
├── DB Layer            <span style="color:#4f46e5; font-weight:700;"># save_pipeline_run(), get_user_history()</span><br>
├── Pipeline Core       <span style="color:#4f46e5; font-weight:700;"># run_validation(), clean_data()</span><br>
│                       <span style="color:#4f46e5; font-weight:700;"># engineer_features(), split_data()</span><br>
└── UI Layer            <span style="color:#4f46e5; font-weight:700;"># dashboard, builder, explorer,</span><br>
                        <span style="color:#4f46e5; font-weight:700;"># history, configs, docs, admin</span><br>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ADMIN PANEL
# ─────────────────────────────────────────────────────────────

def admin_panel():
    render_section_title("🛡️", "ADMIN PANEL", "#db2777")

    if st.session_state.get("role") != "admin":
        st.error("Access denied. Admin only.")
        return

    tab1, tab2 = st.tabs(["👥 All Users", "📊 All Pipeline Runs"])

    with tab1:
        users = get_all_users()
        a1, a2 = st.columns(2)
        with a1:
            st.markdown(render_stat_card("👥", str(len(users)), "TOTAL USERS", "#4f46e5"), unsafe_allow_html=True)
        with a2:
            admins = len(users[users["role"] == "admin"])
            st.markdown(render_stat_card("🛡️", str(admins), "ADMINS", "#db2777"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(users, use_container_width=True, hide_index=True)

    with tab2:
        all_hist = get_all_history()
        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(render_stat_card("🧪", str(len(all_hist)), "TOTAL RUNS", "#4f46e5"), unsafe_allow_html=True)
        with b2:
            success_all = len(all_hist[all_hist["status"] == "Success"]) if len(all_hist) > 0 else 0
            st.markdown(render_stat_card("✅", str(success_all), "SUCCESSFUL", "#16a34a"), unsafe_allow_html=True)
        with b3:
            total_rows_all = all_hist["rows_in"].sum() if len(all_hist) > 0 else 0
            st.markdown(render_stat_card("📦", f"{total_rows_all:,}", "ROWS PROCESSED", "#ea580c"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if len(all_hist) > 0:
            show = all_hist[["username","pipeline_name","dataset_name","rows_in","rows_out","status","created_at"]]
            st.dataframe(show, use_container_width=True, hide_index=True)
        st.download_button("⬇️ EXPORT ALL HISTORY", all_hist.to_csv(index=False).encode(),
                           "all_history.csv", "text/csv")

# ─────────────────────────────────────────────────────────────
# MAIN APP ENTRY
# ─────────────────────────────────────────────────────────────

def main():
    init_db()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        auth_page()
        return

    page = render_sidebar()

    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "⚡ Pipeline Builder":
        pipeline_builder_page()
    elif page == "📊 Data Explorer":
        data_explorer_page()
    elif page == "🕐 Run History":
        history_page()
    elif page == "⚙️ Saved Configs":
        saved_configs_page()
    elif page == "📖 Documentation":
        documentation_page()
    elif page == "🛡️ Admin Panel":
        admin_panel()

if __name__ == "__main__":
    main()