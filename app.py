#!/usr/bin/env python
# coding: utf-8

# # NETFLIX ANALYSIS

# #### This Netflix analysis is my first attempt and it materialised out of the aim and effort to take the first step as a Python developer.

# In[3]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#load dataset
df = pd.read_csv("https://raw.githubusercontent.com/Hakinleye/netflix-analysis/refs/heads/main/netflix_titles.csv")

#Display first 5 rows
df.head()


# ##### The labels and the first four records have been displayed. The next step is to have information about the dataset. 

# In[4]:


#check dataset information
df.info()


# ##### The information about the dataset is revealed and it is clear that the missing values for non-null counted are not the same. We need to discover the missing values count.

# In[5]:


#Count missing values
df.isnull().sum()


# ##### The result reveals that the missing values for director, cast and country are too high and critical. This will skew our analysis. We will remove them.

# In[7]:


#drop rows with missing crirical data
df.dropna(subset=["country", "cast", "director"], inplace=True)

#Replace missing ratings
df.fillna({"rating": "Not Rated"}, inplace=True)


# ##### Having removed the critical column, we still need to make a provision for missing values under the "rating" label, we used "Not rated".

# #### We can now move on with our analysis.

# In[16]:


plt.figure(figsize=(6, 4))
sns.countplot(x="type", data=df, hue="type", palette="coolwarm", legend=False)
plt.title("Distribution of Movies vs. TV Shows")
plt.show()


# # Insight: Discover whether Netflix has more movies or TV shows.

# In[19]:


df["date_added"] = pd.to_datetime(df["date_added"], format='mixed', errors='coerce')
df["year_added"] = df["date_added"].dt.year

plt.figure(figsize=(10, 5))
sns.histplot(df["year_added"].dropna(), bins=15, kde=True)
plt.title("Number of Titles Added per Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()


# # Insight: to know if Netflix has been adding more content over time.

# In[25]:


from collections import Counter

# Split genres and count occurrences
genre_list = ", ".join(df["listed_in"].dropna()).split(", ")
genre_counts = Counter(genre_list)

# Convert to DataFrame for visualization
genre_df = pd.DataFrame(genre_counts.items(), columns=["Genre", "Count"])
genre_df = genre_df.sort_values(by="Count", ascending=False)

plt.figure(figsize=(12, 5))
sns.barplot(x=genre_df["Genre"], y=genre_df["Count"], hue=genre_df["Genre"], palette="viridis", legend=False)
plt.xticks(rotation=45)
plt.title("Most Common Genres on Netflix")
plt.show()


# # Insight: Find the most popular genres on Netflix.

# In[26]:


plt.figure(figsize=(10, 5))
df["country"].value_counts().head(10).plot(kind="bar", colormap="plasma")
plt.title("Top 10 Content-Producing Countries on Netflix")
plt.ylabel("Number of Titles")
plt.show()


# # Insight: Discover which countries contribute the most.

# In[29]:


# Convert duration only for Movies
df.loc[df["type"] == "Movie", "duration"] = (
    df.loc[df["type"] == "Movie", "duration"]
    .str.replace(" min", "", regex=False)  # Remove ' min'
    .astype(float)  # Convert to float
)

# Plot only Movie durations
plt.figure(figsize=(8, 4))
sns.histplot(df[df["type"] == "Movie"]["duration"].dropna(), bins=30, kde=True)
plt.title("Distribution of Movie Durations")
plt.xlabel("Minutes")
plt.show()


# # Insight: Identify the average length of Netflix movies

# In[30]:


plt.figure(figsize=(10, 5))
df["director"].value_counts().head(10).plot(kind="bar", colormap="cividis")
plt.title("Top 10 Directors with Most Titles on Netflix")
plt.ylabel("Number of Titles")
plt.show()


# # Insight: Identify the most prolific Netflix directors

# ##### We assume that the above visuals are self explanatory. Therefore, there is no need for any extraordinary explanation.

# In[33]:


df.to_csv("cleaned_netflix_data.csv", index=False)


# In[ ]:


# Load Data
df = pd.read_csv("netflix_titles.csv")
df["date_added"] = pd.to_datetime(df["date_added"], format='mixed', errors='coerce')
df["year_added"] = df["date_added"].dt.year

# App Title
st.title("📊 Netflix Data Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Data")
content_type = st.sidebar.radio("Select Type", ["All", "Movie", "TV Show"])
year_range = st.sidebar.slider("Select Year Range", int(df["year_added"].min()), int(df["year_added"].max()), (2010, 2021))

# Apply Filters
filtered_df = df[(df["year_added"] >= year_range[0]) & (df["year_added"] <= year_range[1])]
if content_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == content_type]

# Visualization: Movies vs. TV Shows
st.subheader("Movies vs. TV Shows")
fig, ax = plt.subplots()
sns.countplot(x="type", data=df, hue="type", palette="coolwarm", ax=ax)
st.pyplot(fig)

# Visualization: Yearly Growth
st.subheader("Number of Titles Added Over Time")
fig, ax = plt.subplots()
sns.histplot(df["year_added"].dropna(), bins=15, kde=True, ax=ax)
plt.xlabel("Year")
plt.ylabel("Count")
st.pyplot(fig)

# Show Data Table
st.subheader("Filtered Netflix Data")
st.write(filtered_df)

# Run the App: streamlit run app.py



st.sidebar.image("netflix_logo.png", width=200)



st.subheader("🎭 Top 10 Genres")

# Filter by type
content_type_filter = st.radio("Select Content Type", ["All", "Movies", "TV Shows"])

# Process genres
from collections import Counter
genre_list = ", ".join(df["listed_in"].dropna()).split(", ")
genre_counts = Counter(genre_list)
genre_df = pd.DataFrame(genre_counts.items(), columns=["Genre", "Count"]).sort_values(by="Count", ascending=False).head(10)

# Plot
fig, ax = plt.subplots()
sns.barplot(y=genre_df["Genre"], x=genre_df["Count"], palette="rocket", ax=ax)
plt.xlabel("Number of Titles")
st.pyplot(fig)



st.subheader("🔍 Search Netflix Titles")

search_query = st.text_input("Enter Movie or TV Show Name")

if search_query:
    search_results = df[df["title"].str.contains(search_query, case=False, na=False)]
    st.write(search_results[["title", "type", "release_year", "country", "rating"]])
else:
    st.write("Type a title in the search box above.")




import pydeck as pdk

st.subheader("🌍 Netflix Content by Country")

# Get top 10 countries
top_countries = df["country"].value_counts().reset_index().rename(columns={"index": "Country", "country": "Count"}).head(10)

# Hardcoded latitude & longitude for visualization
country_locations = {
    "United States": [37.0902, -95.7129],
    "India": [20.5937, 78.9629],
    "United Kingdom": [55.3781, -3.4360],
    "Canada": [56.1304, -106.3468],
    "France": [46.6034, 1.8883],
    "Germany": [51.1657, 10.4515],
    "Japan": [36.2048, 138.2529],
    "South Korea": [35.9078, 127.7669],
    "Spain": [40.4637, -3.7492],
    "Mexico": [23.6345, -102.5528],
}

# Create a DataFrame with lat/lon data
top_countries["lat"] = top_countries["Country"].map(lambda x: country_locations.get(x, [0, 0])[0])
top_countries["lon"] = top_countries["Country"].map(lambda x: country_locations.get(x, [0, 0])[1])

# Create the map
map_layer = pdk.Layer(
    "ScatterplotLayer",
    data=top_countries,
    get_position=["lon", "lat"],
    get_radius="Count * 20000",
    get_fill_color=[200, 30, 0, 140],
    pickable=True,
)

# Display map
map_view = pdk.ViewState(latitude=20, longitude=0, zoom=1.5)
st.pydeck_chart(pdk.Deck(layers=[map_layer], initial_view_state=map_view))

