import io
import pandas as pd
from utils.copilot import copilot
import streamlit as st
import plotly.express as px
from utils.analytics import (
    get_total_sales,
    get_total_profit,
    get_total_orders,
    get_average_order_value,
    get_sales_by_region,
    get_monthly_sales,
    get_top_products,

)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="InsightIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.main{
    background:#F5F7FA;
}

.block-container{
    padding-top:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

[data-testid="stSidebar"]{
    background:#13294B;
}

[data-testid="stSidebar"] *{
    color:white;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:16px;
    padding:18px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
    border:1px solid #ECECEC;
}

h1,h2,h3{
    color:#13294B;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📊 InsightIQ")

st.sidebar.markdown("---")

st.sidebar.header("Filters")

region = st.sidebar.selectbox(
    "Region",
    ["All","North","South","East","West","Central"]
)

category = st.sidebar.selectbox(
    "Category",
    ["All",
     "Electronics",
     "Furniture",
     "Sports",
     "Fashion",
     "Home Appliances"]
)

st.sidebar.markdown("---")

st.sidebar.info("""
## 🚀 InsightIQ v1.0

### AI-Powered Business Intelligence Platform

### 💻 Tech Stack

• Python

• SQL (SQLite)

• Streamlit

• Plotly

• Pandas

• AI Copilot

---

### ✨ Features

✅ Executive Dashboard

✅ Interactive KPIs

✅ Region & Category Filters

✅ Executive Excel Report

✅ AI Business Copilot

---

Built by **Arianna Vohra**
""")

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- HEADER ---------------- #

st.title("📊 InsightIQ")

st.markdown("""
### AI-Powered Business Intelligence Dashboard

Monitor KPIs, analyze trends, compare business performance,
and generate executive reports from one unified dashboard.
""")

st.divider()
st.markdown(f"""
### 📍 Current Dashboard View

<span style="background:#E3F2FD;padding:6px 12px;border-radius:20px;">
🌍 <b>{region}</b>
</span>

&nbsp;&nbsp;

<span style="background:#E8F5E9;padding:6px 12px;border-radius:20px;">
📦 <b>{category}</b>
</span>
""", unsafe_allow_html=True)

# ---------------- KPI ---------------- #

sales = get_total_sales(region, category)
profit = get_total_profit(region, category)
orders = get_total_orders(region, category)
aov = get_average_order_value(region, category)
kpi_df = pd.DataFrame({
    "Metric": [
        "Total Sales",
        "Total Profit",
        "Total Orders",
        "Average Order Value"
    ],
    "Value": [
        f"₹{sales/10000000:.2f} Cr",
        f"₹{profit/10000000:.2f} Cr",
        f"{orders:,}",
        f"₹{aov:,.0f}"
    ]
})

c1,c2,c3,c4=st.columns(4)

with c1:

    st.metric(
        "💰 Total Sales",
        f"₹{sales/10000000:.2f} Cr"
    )

with c2:

    st.metric(
        "📈 Total Profit",
        f"₹{profit/10000000:.2f} Cr"
    )

with c3:

    st.metric(
        "📦 Orders",
        f"{orders:,}"
    )

with c4:

    st.metric(
        "🛒 Avg Order Value",
        f"₹{aov:,.0f}"
    )

st.divider()

# ------------
# -------------------
# Load Data
# -------------------------------

region_df = get_sales_by_region(region, category)
monthly_df = get_monthly_sales(region, category)
top_products_df = get_top_products(region, category)


# -------------------------------
# Dashboard Charts
# -------------------------------

left, right = st.columns([1,1])

# ---------- Sales by Region ----------

with left:

    st.subheader("📊 Sales by Region")

    fig = px.bar(
        region_df,
        x="Region",
        y="Total_Sales",
        color="Total_Sales",
        color_continuous_scale="Blues",
        text_auto=".2s"
    )

    fig.update_layout(
        height=420,
        coloraxis_showscale=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10,r=10,t=30,b=10)
    )

    st.plotly_chart(fig, width="stretch")

# ---------- Monthly Sales ----------

with right:

    st.subheader("📈 Monthly Revenue Trend")

    fig = px.line(
        monthly_df,
        x="Month",
        y="Total_Sales",
        markers=True
    )

    fig.update_traces(line=dict(width=4))

    fig.update_layout(
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10,r=10,t=30,b=10)
    )

    st.plotly_chart(fig, width="stretch")

# ---------- Top Products ----------

st.subheader("🏆 Top 10 Products")

fig = px.bar(
    top_products_df,
    y="Product_Name",
    x="Total_Sales",
    orientation="h",
    color="Total_Sales",
    color_continuous_scale="Viridis",
    text_auto=".2s"
)

fig.update_layout(

    height=500,

    coloraxis_showscale=False,

    yaxis=dict(categoryorder="total ascending"),

    plot_bgcolor="white",

    paper_bgcolor="white",

    margin=dict(l=10,r=10,t=30,b=10)

)

st.plotly_chart(fig, width="stretch")


st.divider()
st.divider()

st.subheader("📥 Export Dashboard")

st.caption(
    "Download a professional Excel report containing KPIs, regional performance, monthly trends, and top-selling products."
)
output = io.BytesIO()

with pd.ExcelWriter(output, engine="openpyxl") as writer:

    kpi_df.to_excel(
        writer,
        sheet_name="KPI Summary",
        index=False
    )

    region_df.to_excel(
        writer,
        sheet_name="Sales by Region",
        index=False
    )

    monthly_df.to_excel(
        writer,
        sheet_name="Monthly Sales",
        index=False
    )

    top_products_df.to_excel(
        writer,
        sheet_name="Top Products",
        index=False
    )

st.download_button(
    label="📥 Download Executive Report",
    data=output.getvalue(),
    file_name="InsightIQ_Executive_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
# ============================================
# AI BUSINESS CONSULTANT
# ============================================

st.divider()

st.subheader("🤖 InsightIQ AI Copilot")

st.caption(
    "Ask questions about your business, generate SQL queries, analyze performance, and receive executive recommendations."
)

# ----------------------------------------
# Chat History
# ----------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:

    st.info("""
# 👋 Welcome to InsightIQ Copilot

I'm your AI Business Analyst.

I can help you:

• 📊 Summarize dashboard performance

• 🌍 Compare regions

• 📈 Explain trends

• 📦 Analyze products

• 💰 Recommend business strategies

• 💬 Answer follow-up questions

### Try asking:

• Summarize the dashboard

• Which region needs attention?

• Compare North and South

• What should management focus on?
""")
    # ----------------------------------------
# Show Previous Messages
# ----------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ----------------------------------------
# Chat Input
# ----------------------------------------
prompt = st.chat_input("Ask anything about your business...")

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    dashboard_data = f"""
    Total Sales: ₹{sales/10000000:.2f} Cr
    Total Profit: ₹{profit/10000000:.2f} Cr
    Total Orders: {orders}
    Average Order Value: ₹{aov:,.0f}

    Sales by Region:
    {region_df.to_string(index=False)}

    Monthly Sales:
    {monthly_df.to_string(index=False)}

    Top Products:
    {top_products_df.to_string(index=False)}
    """

    with st.chat_message("assistant"):

        with st.spinner("🧠 InsightIQ Copilot is thinking..."):

            result = copilot(
                prompt,
                dashboard_data,
                st.session_state.messages
            )

            # Rest of your SQL/chat handling code...

            if result["type"] == "chat":

                st.markdown(result["response"])

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["response"]
                    }
                )

            elif result["type"] == "sql":

                st.markdown("### 📝 Generated SQL")

                st.code(result["sql"], language="sql")

                st.markdown("### 📊 Query Result")

                st.dataframe(
                    result["result"],
                    use_container_width=True
                )

                st.markdown("### 💡 AI Insight")

                st.markdown(result["insight"])

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["insight"]
                    }
                )

            elif result["type"] == "empty":

                st.warning(result["message"])

            elif result["type"] == "error":

                st.error(result["message"])