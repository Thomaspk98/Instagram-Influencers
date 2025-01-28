import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def convert_abbreviated_number(value):
    if isinstance(value, str):
        if 'k' in value:
            return float(value.replace('k', '')) * 1e3
        elif 'm' in value:
            return float(value.replace('m', '')) * 1e6
        elif 'b' in value:
            return float(value.replace('b', '')) * 1e9
        else:
            return float(value)
    return value


st.set_page_config(page_title="Instagram Influencers Analysis", layout="wide")
st.title("Instagram Influencers Analysis")


@st.cache_data  # Cache the dataset for faster loading
def load_data():
    df = pd.read_csv("insta_influencers_data.csv")
    columns_to_convert = ["posts","followers", "avg_likes", "new_post_avg_like", "total_likes"]
    for column in columns_to_convert:
        df[column] = df[column].apply(convert_abbreviated_number)
    return df

df = load_data()
set_X_rotation = 45


st.sidebar.header("Choose Analysis")
analysis_option = st.sidebar.selectbox(
    "",
    [
        "Correlation Analysis",
        "Frequency Distribution",
        "Top Countries by Influencers",
        "Top 10 Influencers",
        "Relationship Analysis",
    ],
)

# 1. Correlation Analysis
if analysis_option == "Correlation Analysis":
    st.header("Correlation Analysis")
    
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    print(numeric_df)
    st.write("Correlation matrix for numerical features:")
    corr_matrix = numeric_df.corr()
    st.dataframe(corr_matrix)

    st.write("Heatmap of Correlation Matrix:")
    plt.figure(figsize=(10, 6))
    g=sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    g.set_xticklabels(g.get_xticklabels(), rotation=set_X_rotation)
    st.pyplot(plt)

# 2. Frequency Distribution
elif analysis_option == "Frequency Distribution":
    st.header("Frequency Distribution")
    feature = st.selectbox(
        "Select Feature for Distribution",
        ["influence_score", "followers", "posts"],
    )
    st.write(f"Frequency Distribution of {feature}:")
    plt.figure(figsize=(8, 6))
    sns.histplot(df[feature], bins=30, kde=True)
    st.pyplot(plt)

# 3. Top Countries by Influencers
elif analysis_option == "Top Countries by Influencers":
    st.header("Top Countries by Influencers")
    country_counts = df["country"].value_counts()
    st.write("Number of Influencers by Country:")
    st.bar_chart(country_counts)

# 4. Top 10 Influencers
elif analysis_option == "Top 10 Influencers":
    st.header("Top 10 Influencers")
    top_option = st.selectbox(
        "Select Metric for Top 10 Influencers",
        ["followers", "avg_likes", "total_likes"],
    )
    st.write(f"Top 10 Influencers by {top_option}:")
    top_influencers = df.sort_values(by=top_option, ascending=False).head(10)
    st.dataframe(top_influencers.filter(['channel_info', f'{top_option}']))

# 5. Relationship Analysis
elif analysis_option == "Relationship Analysis":
    st.header("Relationship Analysis")
    pair = st.selectbox(
        "Select Pair of Features",
        [
            "Followers vs Total Likes",
            "Followers vs Influence Score",
            "Posts vs Average Likes",
            "Posts vs Influence Score",
        ],
    )
    st.write(f"Scatter Plot for {pair}:")

    # Group data based on the selected pair
    if pair == "Followers vs Total Likes":
        grouped_data = df.groupby(pd.cut(df["followers"], bins=10)).agg(
            {"total_likes": "mean"}
        ).reset_index()
        plt.figure(figsize=(8, 6))
        g=sns.lineplot(x=grouped_data["followers"].apply(lambda x: x.mid), y=grouped_data["total_likes"])
        g.set_xticklabels(g.get_xticklabels(), rotation=set_X_rotation)
        plt.xlabel("Followers (Binned, in 100 millions)")
        plt.ylabel("Average Total Likes (in 10 billions)")

    elif pair == "Followers vs Influence Score":
        grouped_data = df.groupby(pd.cut(df["followers"], bins=10)).agg(
            {"influence_score": "mean"}
        ).reset_index()
        plt.figure(figsize=(8, 6))
        g=sns.lineplot(x=grouped_data["followers"].apply(lambda x: x.mid), y=grouped_data["influence_score"])
        g.set_xticklabels(g.get_xticklabels(), rotation=set_X_rotation)
        plt.xlabel("Followers (Binned, in 100 millions)")
        plt.ylabel("Average Influence Score")

    elif pair == "Posts vs Average Likes":
        grouped_data = df.groupby(pd.cut(df["posts"], bins=10)).agg(
            {"avg_likes": "mean"}
        ).reset_index()
        plt.figure(figsize=(8, 6))
        g=sns.lineplot(x=grouped_data["posts"].apply(lambda x: x.mid), y=grouped_data["avg_likes"])
        g.set_xticklabels(g.get_xticklabels(), rotation=set_X_rotation)
        plt.xlabel("Posts (Binned)")
        plt.ylabel("Average Likes (in millions)")

    elif pair == "Posts vs Influence Score":
        grouped_data = df.groupby(pd.cut(df["posts"], bins=10)).agg(
            {"influence_score": "mean"}
        ).reset_index()
        plt.figure(figsize=(8, 6))
        g=sns.lineplot(x=grouped_data["posts"].apply(lambda x: x.mid), y=grouped_data["influence_score"])
        g.set_xticklabels(g.get_xticklabels(), rotation=set_X_rotation)
        plt.xlabel("Posts (Binned)")
        plt.ylabel("Average Influence Score")

    st.pyplot(plt)