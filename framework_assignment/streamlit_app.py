# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv('metadata.csv', low_memory=False)
    df = df[['title', 'abstract', 'publish_time', 'journal', 'source_x']].copy()
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))
    return df

df_clean = load_data()

# App layout
st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research metadata from the CORD-19 dataset.")

# Year range filter
year_range = st.slider("Select publication year range", 2019, 2022, (2020, 2021))
filtered = df_clean[df_clean['year'].between(year_range[0], year_range[1])]

# Show filtered data
st.subheader(f"Papers from {year_range[0]} to {year_range[1]}")
st.dataframe(filtered[['title', 'journal', 'year']].head(20))

# Publications by year
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values, color='orange')
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
ax.set_title("Publications Over Time")
st.pyplot(fig)

# Top journals
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
top_journals.plot(kind='barh', ax=ax2, color='green')
ax2.set_title("Top Journals Publishing COVID-19 Research")
st.pyplot(fig2)

# Word cloud of paper titles
st.subheader("Word Cloud of Paper Titles")
titles = ' '.join(filtered['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles)
fig_wc, ax_wc = plt.subplots()
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis('off')
st.pyplot(fig_wc)

# Distribution by source
st.subheader("Distribution by Source")
source_counts = filtered['source_x'].value_counts()
fig_src, ax_src = plt.subplots()
source_counts.plot(kind='bar', ax=ax_src, color='purple')
ax_src.set_title("Paper Counts by Source")
ax_src.set_xlabel("Source")
ax_src.set_ylabel("Number of Papers")
st.pyplot(fig_src)

# Optional: CSV download
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_clean = convert_df_to_csv(filtered)
st.download_button("Download filtered data as CSV", csv_clean, "cord19_filtered.csv", "text/csv")










