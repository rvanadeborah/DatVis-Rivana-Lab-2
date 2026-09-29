import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ChaSis - Cha Analysis",
    page_icon="🍵",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"],
p, label, div, span {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background-color: #F8F1E5;
}

/* Main title */
h1 {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    color: #1B5E20;
}

/* Section titles */
h2, h3 {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: #2E7D32;
}

/* Normal text */
p {
    color: #4F5D4F;
}

/* Slider label */
.stSlider label {
    color: #2E5D34;
    font-weight: 500;
}

/* Slider */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #2E7D32;
    border-color: #2E7D32;
}

.stSlider [data-baseweb="slider"] > div > div {
    background-color: #81C784;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* Divider */
hr {
    border-color: #D7C9AE;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFDF8;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #E4D8C4;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER IMAGE
# =========================================================

st.image("tea.png", use_container_width=True)

# =========================================================
# TITLE
# =========================================================

st.title("ChaSis - Cha Analysis")

st.markdown(
    "This interactive dashboard presents tea sales performance. "
    )

st.divider()

# =========================================================
# TEA DATA
# =========================================================

tea_types = [
    "Jasmine Green Tea",
    "Da Hong Pao",
    "Tie Guan Yin",
    "Osmanthus Oolong",
    "Glutinous Green Tea",
    "White Peach Oolong",
    "Lapsang Souchong"
]

# Different starting values
default_sales = [
    800,
    450,
    650,
    300,
    550,
    700,
    200
]

# Green shades
colors = [
    "#1B5E20",
    "#2E7D32",
    "#388E3C",
    "#43A047",
    "#66BB6A",
    "#81C784",
    "#A5D6A7"
]

# =========================================================
# 1. ADJUST TEA SALES
# =========================================================

st.header("1. Adjust Tea Sales")

st.write(
    "Use the sliders below to adjust the sales value for each type of tea."
)

sales_values = []

col1, col2 = st.columns(2)

for i, tea in enumerate(tea_types):

    if i % 2 == 0:
        with col1:
            value = st.slider(
                tea,
                min_value=0,
                max_value=1000,
                value=default_sales[i],
                step=50,
                key=f"slider_{i}"
            )
    else:
        with col2:
            value = st.slider(
                tea,
                min_value=0,
                max_value=1000,
                value=default_sales[i],
                step=50,
                key=f"slider_{i}"
            )

    sales_values.append(value)

# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame({
    "Tea Type": tea_types,
    "Sales": sales_values
})

# =========================================================
# CALCULATIONS
# =========================================================

total_sales = df["Sales"].sum()
average_sales = df["Sales"].mean()

highest_sale = df["Sales"].max()
lowest_sale = df["Sales"].min()

highest_tea = df.loc[
    df["Sales"].idxmax(),
    "Tea Type"
]

lowest_tea = df.loc[
    df["Sales"].idxmin(),
    "Tea Type"
]

# =========================================================
# 2. SALES OVERVIEW
# =========================================================

st.header("2. Sales Overview")

st.write(
    "The following indicators summarize the current tea sales performance."
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(
        label="Total Sales",
        value=f"{total_sales:,.0f}"
    )

with metric2:
    st.metric(
        label="Average Sales",
        value=f"{average_sales:,.0f}"
    )

with metric3:
    st.metric(
        label="Highest Sale",
        value=f"{highest_sale:,.0f}"
    )

with metric4:
    st.metric(
        label="Lowest Sale",
        value=f"{lowest_sale:,.0f}"
    )

st.write("")

# =========================================================
# SALES TABLE
# =========================================================

st.subheader("Current Sales Data")

display_df = df.copy()

display_df["Sales"] = display_df["Sales"].map(
    lambda x: f"{x:,.0f}"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# 3. TEA SALES PERFORMANCE
# =========================================================

st.header("3. Tea Sales Performance")

st.write(
    "The vertical bar chart compares the sales performance of each tea type. "
    "The dashed line represents the average sales."
)

# Create figure
fig, ax = plt.subplots(figsize=(13, 6))

# Create bars
bars = ax.bar(
    df["Tea Type"],
    df["Sales"],
    color=colors,
    width=0.65
)

# Average line
ax.axhline(
    average_sales,
    color="#1B5E20",
    linestyle="--",
    linewidth=2,
    label=f"Average Sales: {average_sales:,.0f}"
)

# Title
ax.set_title(
    "Tea Sales Performance",
    fontsize=18,
    fontweight="bold",
    pad=20,
    color="#1B5E20"
)

# Axis labels
ax.set_xlabel(
    "Tea Type",
    fontsize=11,
    fontweight="bold"
)

ax.set_ylabel(
    "Sales",
    fontsize=11,
    fontweight="bold"
)

# Rotate labels
plt.xticks(
    rotation=20,
    ha="right"
)

# Add sales values above bars
for bar, value in zip(bars, df["Sales"]):

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 20,
        f"{value:,.0f}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color="#1B5E20"
    )

# Highlight highest
highest_index = df["Sales"].idxmax()

ax.text(
    highest_index,
    df.loc[highest_index, "Sales"] + 90,
    "Highest",
    ha="center",
    fontsize=10,
    fontweight="bold",
    color="#1B5E20"
)

# Highlight lowest
lowest_index = df["Sales"].idxmin()

ax.text(
    lowest_index,
    df.loc[lowest_index, "Sales"] + 90,
    "Lowest",
    ha="center",
    fontsize=10,
    fontweight="bold",
    color="#2E7D32"
)

# Grid
ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.25
)

# Remove unnecessary borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend
ax.legend()

# Layout
plt.tight_layout()

st.pyplot(fig)

# =========================================================
# HIGHEST & LOWEST INFORMATION
# =========================================================

info_col1, info_col2 = st.columns(2)

with info_col1:

    st.markdown(
        f"""
        **Highest Sales**

        {highest_tea}

        **Sales:** {highest_sale:,.0f}
        """
    )

with info_col2:

    st.markdown(
        f"""
        **Lowest Sales**

        {lowest_tea}

        **Sales:** {lowest_sale:,.0f}
        """
    )

# =========================================================
# RANKING
# =========================================================

st.subheader("Sales Ranking")

ranking_df = df.sort_values(
    by="Sales",
    ascending=False
).reset_index(drop=True)

ranking_df.insert(
    0,
    "Rank",
    range(1, len(ranking_df) + 1)
)

ranking_df["Sales"] = ranking_df["Sales"].map(
    lambda x: f"{x:,.0f}"
)

st.dataframe(
    ranking_df,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# 4. SALES DISTRIBUTION
# =========================================================

st.header("4. Sales Distribution")

st.write(
    "The pie chart shows the percentage contribution of each tea type "
    "to the total sales."
)

fig2, ax2 = plt.subplots(figsize=(8, 8))

ax2.pie(
    df["Sales"],
    labels=df["Tea Type"],
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    textprops={
        "fontsize": 9
    }
)

ax2.set_title(
    "Tea Sales Distribution",
    fontsize=17,
    fontweight="bold",
    color="#1B5E20",
    pad=20
)

plt.tight_layout()

st.pyplot(fig2)

# =========================================================
# 5. DETAILED ANALYSIS
# =========================================================

st.header("5. Detailed Analysis")

st.write(
    "This table provides a more detailed comparison of sales contribution "
    "and performance for each tea type."
)

analysis_df = df.copy()

analysis_df["Percentage"] = (
    analysis_df["Sales"] / total_sales * 100
)

analysis_df["Performance"] = analysis_df["Sales"].apply(
    lambda x:
    "Highest"
    if x == highest_sale
    else "Lowest"
    if x == lowest_sale
    else "Normal"
)

analysis_df["Sales"] = analysis_df["Sales"].map(
    lambda x: f"{x:,.0f}"
)

analysis_df["Percentage"] = analysis_df["Percentage"].map(
    lambda x: f"{x:.1f}%"
)

st.dataframe(
    analysis_df,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# SUMMARY
# =========================================================

st.subheader("Summary")

st.write(
    f"""
    Based on the current sales values, **{highest_tea}** has the highest
    sales with **{highest_sale:,.0f}**, while **{lowest_tea}** has the lowest
    sales with **{lowest_sale:,.0f}**.

    The average sales across all tea types is **{average_sales:,.0f}**,
    with a total sales value of **{total_sales:,.0f}**.
    """
)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Made By Rivana Deborah Satriani - 26010127"
)
