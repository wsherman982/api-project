import sqlite3
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request

app = Flask(__name__)
DB = "api_data.db"

def query_db(query):
    conn = sqlite3.connect(DB)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

@app.route("/")
def home():
    df = query_db("SELECT * FROM requests LIMIT 20")
    return df.to_html()

@app.route("/search")
def search():
    keyword = request.args.get("q", "")

    if keyword:
        df = query_db(f"""
            SELECT * FROM requests
            WHERE endpoint LIKE '%{keyword}%'
            LIMIT 200
        """)
    else:
        df = query_db("SELECT * FROM requests LIMIT 200")

    return render_template(
        "index.html",
        data=df.to_dict(orient="records")
    )

@app.route("/dashboard")
def dashboard():
    df = query_db("SELECT * FROM requests")

    df["error_type"] = df["error_type"].fillna("No Error").astype(str)
    df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")

    summary = {
        "total_requests": int(len(df)),
        "error_count": int(df["error_type"].isna().sum()),
        "avg_latency": float(df["latency_ms"].mean())
    }

    error_counts = df["error_type"].value_counts().reset_index()
    error_counts.columns = ["error_type", "count"]
    error_counts["count"] = error_counts["count"].astype(int)

    fig = px.bar(
        error_counts,
        x="error_type",
        y="count",
        title="Error Type Distribution"
    )

    chart = fig.to_html(full_html=False)

    return render_template(
        "dashboard.html",
        summary=summary,
        chart=chart
    )
if __name__ == "__main__":
    app.run()