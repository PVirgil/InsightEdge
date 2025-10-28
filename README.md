# 🧠 InsightEdge

**InsightEdge** is an AI-powered business intelligence tool that lets you upload structured data (CSV) and chat directly with it to uncover actionable insights, metrics, and visual summaries — all without writing code.

> “Upload your data. Ask smart questions. Get powerful answers.”

---

## 🚀 Live Demo

👉 [Launch the App](https://insightedge.streamlit.app)

---

## 📦 Features

- 💬 **AI Chat** — Ask business questions directly (e.g. “What drives churn?”)
- 📈 **Insight Generation** — Automated insights from raw data in seconds
- 📊 **Dashboard Metrics** — Real-time stats like row count, missing values, column overview
- 🧠 **Groq-powered LLM** — Uses ultra-fast open-source models via Groq Cloud API
- 🧰 **Fully Deployable** — Streamlit-ready with local and cloud support
- 🔐 **Environment Secure** — Secrets managed via `.env` or Streamlit Cloud

---

## 🧪 Local Usage

1. **Clone the repo and install dependencies**:

    ```bash
    git clone https://github.com/pvirgil/insightedge.git
    cd insightedge
    pip install -r requirements.txt
    ```

2. **Create a `.env` file in the root folder** with your Groq API key:

    ```env
    GROQ_API_KEY=your_actual_groq_api_key_here
    ```

3. **Run the app locally**:

    ```bash
    streamlit run streamlit_app.py
    ```

---

## ☁️ Deploy to Streamlit Cloud

1. Push to GitHub  
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) → Create New App  
3. Set your repository and branch  
4. Add your Groq API key in **Settings > Secrets**:

    ```toml
    GROQ_API_KEY = "your_actual_groq_api_key_here"
    ```

---

## 🧠 Supported Groq Models

Choose one of the following in your app code:

- `llama3-8b-8192`
- `llama3-70b-8192`
- `mixtral-8x7b-32768`

---

## 📁 File Structure

```
insightedge/
├── streamlit_app.py       # Main app UI + logic
├── requirements.txt       # Dependencies
└── .env                   # Local API key (not pushed)
```

---

## ✨ Built With

- [Streamlit](https://streamlit.io/)
- [Groq API](https://console.groq.com/)
- [Pandas](https://pandas.pydata.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---

> InsightEdge — turning your data into decisions, one prompt at a time.
