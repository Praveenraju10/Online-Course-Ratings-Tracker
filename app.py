import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="📊 Course Ratings Tracker", layout="wide")

st.title("🎓 Online Course Ratings Tracker")
st.write("Analyze student ratings and feedback to improve course quality.")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("course_ratings.csv", parse_dates=["date"])

df = load_data()

# Sidebar filters
st.sidebar.header("📂 Filters")
selected_courses = st.sidebar.multiselect(
    "Select Courses", options=df["course_name"].unique(),
    default=df["course_name"].unique()
)
filtered_df = df[df["course_name"].isin(selected_courses)]

# Plot 1: Bar Plot - Avg Rating by Course
st.subheader("📌 Average Rating by Course")
bar_fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=filtered_df, x="course_name", y="rating", ci=None, palette="Blues_d", ax=ax)
ax.set_title("Average Rating by Course")
ax.set_ylabel("Average Rating")
ax.set_xlabel("Course Name")
plt.xticks(rotation=30)
st.pyplot(bar_fig)

# Plot 2: Line Plot - Avg Rating Over Time
st.subheader("📈 Average Rating Over Time")
filtered_df['date'] = pd.to_datetime(filtered_df['date'])
monthly_avg = filtered_df.groupby(filtered_df['date'].dt.to_period('M')).rating.mean().reset_index()
monthly_avg['date'] = monthly_avg['date'].dt.to_timestamp()

line_fig, ax2 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=monthly_avg, x="date", y="rating", marker="o", ax=ax2)
ax2.set_title("Average Rating Over Time")
ax2.set_ylabel("Average Rating")
ax2.set_xlabel("Date")
st.pyplot(line_fig)

# Plot 3: Box Plot - Feedback Score Distribution
st.subheader("📊 Feedback Score Distribution by Course")
box_fig, ax3 = plt.subplots(figsize=(8, 5))
sns.boxplot(data=filtered_df, x="course_name", y="feedback_score", palette="Set2", ax=ax3)
ax3.set_title("Feedback Score Distribution")
ax3.set_ylabel("Feedback Score")
ax3.set_xlabel("Course Name")
plt.xticks(rotation=30)
st.pyplot(box_fig)

# Show raw data
with st.expander("🔍 Show Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True))
