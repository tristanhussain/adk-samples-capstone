import json
import pathlib

import dataset
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).parent
AGENTS_XLSX = BASE_DIR / "agents.xlsx"
OUTPUT_JSON = BASE_DIR / "output.json"
DB_PATH = BASE_DIR / "dashboard.db"

# ---------------------------------------------------------------------------
# Database bootstrap — clear and reload on every startup
# ---------------------------------------------------------------------------
@st.cache_resource
def init_db() -> dataset.Database:
    db = dataset.connect(f"sqlite:///{DB_PATH}")

    # --- agents table ---
    if "agents" in db:
        db["agents"].drop()
    agents_df = pd.read_excel(AGENTS_XLSX, engine="openpyxl")
    agents_df.columns = [str(c).strip() for c in agents_df.columns]
    # Replace NaN with None so dataset doesn't infer text columns as FLOAT
    agents_df = agents_df.astype(object).where(agents_df.notna(), None)
    db["agents"].insert_many(agents_df.to_dict(orient="records"))

    # --- extractions table ---
    if "extractions" in db:
        db["extractions"].drop()
    with open(OUTPUT_JSON, encoding="utf-8") as f:
        extractions = json.load(f)
    if isinstance(extractions, list):
        db["extractions"].insert_many(extractions)
    else:
        db["extractions"].insert(extractions)

    return db


def load_agents(db: dataset.Database) -> pd.DataFrame:
    rows = list(db["agents"].all())
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    # drop the auto-added 'id' column dataset inserts
    return df.drop(columns=["id"], errors="ignore")


def load_extractions(db: dataset.Database) -> pd.DataFrame:
    rows = list(db["extractions"].all())
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    return df.drop(columns=["id"], errors="ignore")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
st.set_page_config(page_title="ADK Agents Dashboard", layout="wide")
st.title("ADK Agents Dashboard")

db = init_db()
agents_df = load_agents(db)
extractions_df = load_extractions(db)

# Detect the status column name dynamically (case-insensitive)
status_col = next(
    (c for c in agents_df.columns if c.lower() == "status"),
    None,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Summary")
    st.metric("Total agents", len(agents_df))
    st.metric("Total extractions", len(extractions_df))

    if status_col and not agents_df.empty:
        st.subheader("Agents by status")
        status_counts = agents_df[status_col].value_counts()
        for status, count in status_counts.items():
            st.metric(str(status), count)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_agents, tab_extractions = st.tabs(["Agents", "Extractions"])

# ---- Agents tab ----
with tab_agents:
    st.subheader("Agents")

    if agents_df.empty:
        st.warning("No agent data found.")
    else:
        # Status filter
        STATUS_OPTIONS = ["All", "Merged", "Waiting for Review", "Reviewing"]
        selected_status = "All"

        if status_col:
            selected_status = st.selectbox(
                "Filter by status",
                options=STATUS_OPTIONS,
                index=0,
            )

        filtered = agents_df.copy()
        if status_col and selected_status != "All":
            filtered = filtered[filtered[status_col] == selected_status]

        st.caption(f"Showing {len(filtered)} of {len(agents_df)} agents")
        st.dataframe(filtered, use_container_width=True, hide_index=True)

# ---- Extractions tab ----
with tab_extractions:
    st.subheader("Extractions (auditor output)")

    if extractions_df.empty:
        st.warning("No extraction data found.")
    else:
        st.caption(f"{len(extractions_df)} records")
        st.dataframe(extractions_df, use_container_width=True, hide_index=True)
