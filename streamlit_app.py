# streamlit_app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from typing import Dict, Any
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "HuggingFaceH4/zephyr-7b-beta")

# Utility: call LLM

def call_llm(prompt: str, model: str = HF_MODEL) -> str:
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }
    json_data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 256,
            "temperature": 0.7
        }
    }
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers=headers,
        json=json_data
    )
    if resp.status_code != 200:
        logger.error(f"LLM call error {resp.status_code}: {resp.text}")
        return f"Error: {resp.status_code} {resp.text}"
    data = resp.json()
    if isinstance(data, list) and len(data) > 0 and 'generated_text' in data[0]:
        return data[0]['generated_text']
    return str(data)

# Modules / logic

class DataIngestor:
    @staticmethod
    def upload_csv(file) -> pd.DataFrame:
        try:
            df = pd.read_csv(file)
            return df
        except Exception as e:
            logger.error(f"CSV upload failed: {e}")
            st.error("Failed to parse CSV.")
            return pd.DataFrame()

class InsightGenerator:
    @staticmethod
    def generate_insights(df: pd.DataFrame, user_id: str) -> list:
        if df.empty:
            return ["No data uploaded. Please upload a valid CSV."]
        prompt = (
            f"User {user_id} uploaded dataset with {len(df)} rows and columns {list(df.columns)}.\n"
            "Generate a ranked list of three business insights and recommendations."
        )
        result = call_llm(prompt)
        return result.split("\n")

class ChatAgent:
    @staticmethod
    def chat(user_id: str, message: str) -> str:
        prompt = (
            f"You are an AI business analyst for user {user_id}. They say: {message}\n"
            "Provide a clear, actionable response."
        )
        return call_llm(prompt)

class DashboardAPI:
    @staticmethod
    def compute_metrics(df: pd.DataFrame) -> Dict[str, Any]:
        if df.empty:
            return {"info": "No data"}
        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "missing_values": df.isna().sum().to_dict(),
        }

# UI

def main():
    st.set_page_config(page_title="InsightEdge", layout="wide", page_icon="🧠")
    st.sidebar.title("InsightEdge")
    menu = st.sidebar.selectbox("Menu", ["Home", "Upload Data", "Chat", "Insights", "Dashboard", "Account"])

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if menu == "Account":
        user = st.text_input("Enter your name (for demo)")
        if st.button("Set User"):
            st.session_state.user_id = user.strip()
            st.success(f"Logged in as {st.session_state.user_id}")
        return

    if not st.session_state.user_id:
        st.warning("Please go to Account and set your user name to continue.")
        return

    user_id = st.session_state.user_id

    if menu == "Home":
        st.header("Welcome to InsightEdge")
        st.write("Upload your data, chat with the AI analyst, get insights and dashboards.")
        return

    if menu == "Upload Data":
        st.header("Upload CSV Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="upload")
        if uploaded_file:
            df = DataIngestor.upload_csv(uploaded_file)
            st.session_state.df = df
            st.success("Data uploaded.")
        return

    if menu == "Chat":
        st.header("💬 Chat with the AI Analyst")
        message = st.text_input("Your message:", key="chat_input")
        if st.button("Send", key="chat_send"):
            response = ChatAgent.chat(user_id, message)
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({"user": message, "ai": response})
        if "history" in st.session_state:
            for h in st.session_state.history:
                st.markdown(f"**You:** {h['user']}")
                st.markdown(f"**AI:** {h['ai']}")
        return

    if menu == "Insights":
        st.header("📈 Generate Insights")
        if "df" not in st.session_state:
            st.warning("No data uploaded yet.")
            return
        if st.button("Generate"):
            insights = InsightGenerator.generate_insights(st.session_state.df, user_id)
            for ins in insights:
                st.markdown(f"- {ins}")
        return

    if menu == "Dashboard":
        st.header("📊 Data Dashboard")
        if "df" not in st.session_state:
            st.warning("No data uploaded yet.")
            return
        if st.button("Show Metrics"):
            metrics = DashboardAPI.compute_metrics(st.session_state.df)
            st.json(metrics)
        if st.button("Download Data"):
            st.download_button("Download CSV", st.session_state.df.to_csv(index=False), file_name="exported_data.csv")
        return

if __name__ == "__main__":
    main()
