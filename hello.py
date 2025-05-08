from preswald import text, plotly, connect, get_df, table, query
import pandas as pd
import plotly.express as px


text("# Students' Marksheet")
text("Dataset Source: https://www.kaggle.com/datasets/rohithmahadevan/students-marksheet-dataset")


#Step 1: Load the dataset
connect()
#Configed student_scores_csv in config
df = get_df('student_scores_csv')
df.columns = df.columns.str.strip().str.lower()


#Step 2: Query
#Query to see students that are failing at least one subject
sql = """SELECT * FROM student_scores_csv
       WHERE  science < 60
       OR  english < 60
       OR  history < 60
       OR  maths   < 60"""


filtered_df = query(sql, 'student_scores_csv')


#Step 2: Query
#Query for average
sql_avg = """SELECT section,
       AVG(science)  AS avg_science,
       AVG(english)  AS avg_english,
       AVG(history)  AS avg_history,
       AVG(maths)    AS avg_maths
       FROM   student_scores_csv
       GROUP  BY section
       ORDER  BY section"""


avg_df = query(sql_avg, "student_scores_csv")




#Step 3: Build an interactive UI
text("## The full dataset")
table(df)


text("### In this Dataset, I first wanted to see the number of students that are failing in at least one subject.")


table(filtered_df, title = "Filtered Data")
text("##### Judging from this data, it is safe to assume that this school has poor standards as 95.2% of the students are failing in at least one subject!")




text("### After seeing how poorly the students are doing, I wanted to see the average score of each subject grouped by sections.")
table(avg_df, title = "Average Data")


avg_df.columns = avg_df.columns.str.lower()


long_avg = avg_df.melt(
   id_vars="section",
   var_name="subject",
   value_name="average"
)


#Change column names to make it more pretty
pretty = {
   "avg_maths":    "Math Avg",
   "avg_science":  "Science Avg",
   "avg_english":  "English Avg",
   "avg_history":  "History Avg"
}
long_avg["subject_pretty"] = long_avg["subject"].map(pretty)


order = list(pretty.values())
long_avg["subject_pretty"] = pd.Categorical(
   long_avg["subject_pretty"], categories=order, ordered=True
)


#Step 4: Create a visualization
fig_bar = px.bar(
   long_avg,
   x="subject_pretty",
   y="average",
   color="section",
   barmode="group",
   labels={"subject_pretty": "", "average": "Average score"},
   title="Average score per subject and section",
   custom_data=["section", "subject_pretty", "average"]
)


#Custom hover
fig_bar.update_traces(
   hovertemplate=(
       "Section = %{customdata[0]}<br>"
       "%{customdata[1]} = %{customdata[2]:.1f}"
       "<extra></extra>"
   )
)


fig_bar.update_layout(template="plotly_white")
plotly(fig_bar)


text("##### This is one rough school")


text("### Finally, I wanted to see if the top students at STEM succeeded in humanities and vice versa.")


#Show pandas way (Step 2: "or manipulate the data")
df["stem_avg"]  = df[["maths", "science"]].mean(axis=1)
df["human_avg"] = df[["history", "english"]].mean(axis=1)


#Step 4: Create a visualization
fig_compare = px.scatter(
   df,
   x="stem_avg",
   y="human_avg",
   color="section",
   labels={
       "stem_avg":  "Math & Science (avg)",
       "human_avg": "History & English (avg)"
   },
   title="STEM vs Humanities averages",
   custom_data=["section", "name", "stem_avg", "human_avg"]
)


#Custom hover
fig_compare.update_traces(
   marker=dict(size=10),
   hovertemplate=(
       "Section = %{customdata[0]}<br>"
       "Name = %{customdata[1]}<br>"
       "Math & Science = %{customdata[2]:.1f}<br>"
       "History & English = %{customdata[3]:.1f}"
       "<extra></extra>"
   )
)


fig_compare.update_layout(template="plotly_white")
plotly(fig_compare)


text("##### After looking at the scatter plot, a student's mastery in STEM does not mean a mastery in humanities and vice versa.")
text("## Overall, after analyzing this dataset, I can confidently say this school is not the golden standard.")
