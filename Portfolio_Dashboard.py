import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

st.set_page_config(page_title="📊 Portfolio Optimization Dashboard", layout="wide")
st.title("📊 Portfolio Optimization Dashboard")

with open("portfolio_dashboard_data.pkl", "rb") as f:
    data = pickle.load(f)

assets = data["assets"]
portfolios = data["portfolios"]
stats_dict = data["stats"]
detailed_stats = data["detailed_stats"]
correlation_matrix = data["correlation_matrix"]
rolling_returns_10 = data["rolling_returns"]["10_year"]
rolling_returns_30 = data["rolling_returns"]["30_year"]
drawdowns = data["drawdowns"]
efficient_frontier = data["efficient_frontier"]
insights = data["insights"]

with st.sidebar:
    st.header("📘 Overview")
    st.markdown("""
    This dashboard showcases:
    - Portfolio strategies (P1 to P6)
    - Rolling returns & drawdowns
    - Correlation heatmaps
    - Efficient frontier
    - Performance insights
    """)

st.subheader("📈 Portfolio Growth Over Time")
st.line_chart(portfolios)

st.subheader("📊 Summary Stats (All Portfolios)")
summary_df = pd.DataFrame(stats_dict).T
st.dataframe(summary_df.style.format("{:.2%}"))

st.subheader("📉 Drawdowns")
st.line_chart(drawdowns)

st.subheader("🔗 Correlation Matrix")
fig1, ax1 = plt.subplots()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax1)
st.pyplot(fig1)

st.subheader("🌀 Efficient Frontier")
fig2, ax2 = plt.subplots()
sns.lineplot(x=efficient_frontier["sigma"], y=efficient_frontier["mu"], ax=ax2)
ax2.set_xlabel("Volatility")
ax2.set_ylabel("Expected Return")
st.pyplot(fig2)

st.subheader("📆 Rolling Returns")
tab1, tab2 = st.tabs(["10-Year", "30-Year"])
with tab1:
    st.line_chart(rolling_returns_10)
with tab2:
    st.line_chart(rolling_returns_30)

st.subheader("📌 Detailed Portfolio Stats")
tabs = st.tabs([f"Portfolio P{i}" for i in range(1, 7)])
for i, tab in enumerate(tabs, start=1):
    port = f"P{i}"
    with tab:
        st.markdown(f"**Stats for {port}:**")
        st.dataframe(detailed_stats[port]["stats"].style.format("{:.2%}"))
        st.markdown(f"**Returns for {port}:**")
        st.line_chart(detailed_stats[port]["returns"])

st.subheader("💡 Key Insights")
st.success(insights.get("summary", ""))
for line in insights.get("commentary", []):
    st.markdown(f"- {line}")
