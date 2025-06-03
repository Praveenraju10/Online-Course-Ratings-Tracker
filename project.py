import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for seaborn
sns.set(style="whitegrid")

# --- Generate synthetic dataset ---
np.random.seed(42)

# Sample data
courses = ['Python Basics', 'Data Science 101', 'Web Development', 'Machine Learning', 'AI Fundamentals']
num_entries = 300

data = {
    "course_name": np.random.choice(courses, num_entries),
    "rating": np.random.randint(1, 6, num_entries),  # Ratings from 1 to 5
    "feedback_score": np.round(np.random.normal(3.5, 1.0, num_entries), 2),  # Avg around 3.5
    "date": pd.date_range(start='2023-01-01', periods=num_entries).to_series().sample(frac=1).values
}

df = pd.DataFrame(data)

# Clean feedback score (keep within 1 to 5)
df["feedback_score"] = df["feedback_score"].clip(1, 5)

# Save dataset
df.to_csv("course_ratings.csv", index=False)
print("✅ Dataset saved as 'course_ratings.csv'")

# --- Visualizations ---

# 1. Bar Plot: Average Rating by Course
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="course_name", y="rating", ci=None, palette="Blues_d")
plt.title("Average Rating by Course")
plt.ylabel("Average Rating")
plt.xlabel("Course Name")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# 2. Line Plot: Average Rating Over Time
df['date'] = pd.to_datetime(df['date'])
daily_avg = df.groupby(df['date'].dt.to_period('M')).rating.mean().reset_index()
daily_avg['date'] = daily_avg['date'].dt.to_timestamp()

plt.figure(figsize=(10, 5))
sns.lineplot(data=daily_avg, x="date", y="rating", marker="o")
plt.title("Average Rating Over Time")
plt.ylabel("Average Rating")
plt.xlabel("Date")
plt.tight_layout()
plt.show()

# 3. Box Plot: Feedback Score Distribution by Course
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="course_name", y="feedback_score", palette="Set2")
plt.title("Feedback Score Distribution by Course")
plt.ylabel("Feedback Score")
plt.xlabel("Course Name")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
