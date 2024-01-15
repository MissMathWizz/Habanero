import streamlit as st
import pandas as pd
import plost
from collections import defaultdict, namedtuple
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
from math import floor
from textblob import TextBlob
import altair as alt
import datetime
import functools
import re
import time
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
st.set_option('deprecation.showPyplotGlobalUse', False)

 # Useful functions for displaying stuff
df = pd.read_csv('/Users/yw/Downloads/output1_.csv')

COLOR_RED = "#FF4B4B"
COLOR_BLACK = "#000000"
COLOR_GREEN = "#008000"

def display_callout(title, color, icon, second_text):
        st.markdown(
            div(
                style=styles(
                    background_color=color,
                    padding=rem(1),
                    display="flex",
                    flex_direction="row",
                    border_radius=rem(0.5),
                    margin=(0, 0, rem(0.5), 0),
                )
            )(
                div(style=styles(font_size=rem(2), line_height=1))(icon),
                div(style=styles(padding=(rem(0.5), 0, rem(0.5), rem(1))))(title),
            ),
            unsafe_allow_html=True,
        )

def display_small_text(text):
        st.markdown(
            div(
                style=styles(
                    font_size=rem(0.8),
                    margin=(0, 0, rem(1), 0),
                )
            )(text),
            unsafe_allow_html=True,
        )

def display_dial(title, value, color):
        st.markdown(
            div(
                style=styles(
                    text_align="center",
                    color="sentiment_label",
                    padding=(rem(0.8), 0, rem(3), 0),
                )
            )(
                h2(style=styles(font_size=rem(0.8), font_weight=600, padding=0))(title),
                big(style=styles(font_size=rem(3), font_weight=800, line_height=1))(
                    value
                ),
            ),
            unsafe_allow_html=True,
        )

def display_dict(dict):
        for k, v in dict.items():
            a, b = st.columns([1, 4])
            a.write(f"**{k}:**")
            b.write(v)

def display_tweet(tweet):
        parsed_tweet = {
            "author": tweet.user.screen_name,
            "created_at": tweet.created_at,
            "url": get_tweet_url(tweet),
            "text": tweet.text,
        }
        display_dict(parsed_tweet)

def paginator(values, state_key, page_size):
        curr_page = getattr(st.session_state, state_key)

        a, b, c = st.columns(3)

        def decrement_page():
            curr_page = getattr(st.session_state, state_key)
            if curr_page > 0:
                setattr(st.session_state, state_key, curr_page - 1)

        def increment_page():
            curr_page = getattr(st.session_state, state_key)
            if curr_page + 1 < len(values) // page_size:
                setattr(st.session_state, state_key, curr_page + 1)

        def set_page(new_value):
            setattr(st.session_state, state_key, new_value - 1)

        a.write(" ")
        a.write(" ")
        a.button("Previous page", on_click=decrement_page)

        b.write(" ")
        b.write(" ")
        b.button("Next page", on_click=increment_page)

        c.selectbox(
            "Select a page",
            range(1, len(values) // page_size + 1),
            curr_page,
            on_change=set_page,
        )

        curr_page = getattr(st.session_state, state_key)

        page_start = curr_page * page_size
        page_end = page_start + page_size

        return values[page_start:page_end]

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
with st.sidebar:
    st.title('Xochitl Campaign Social Media stats')
    
    label_list = list(df.sentiment_label.unique())
    
    selected_year = st.selectbox('Select', label_list)
    df_selected= df[df.sentiment_label == selected_year]

st.sidebar.markdown('''
---
Created by [Habanero](https://www.linkedin.com/in/michiko-amemiya-9a930759/).
''')

# Row A  
count_pos = (df['sentiment_label'] == 'Positivo').sum()
count_neg =  (df['sentiment_label'] == 'Negativo').sum()


st.write("## Sentiment from the most recent ", len(df['text'])," tweets")


total_color = COLOR_BLACK


b, c = st.columns(2)

with b:
    display_dial(
        "POSITIVO", f"{count_pos}", "#008000"
    )
with c:
    display_dial(
        "NEGATIVO", f"{count_neg}", "#FF4B4B"
    )


st.write("")
#parse_dates=['date']
# Row B
c1, c2 = st.columns((7,3)) ## The first column takes 70%, the second column takes 30%



with c1:
    st.markdown('### Word cloud')
    # Combine all text from the 'tweets' column into a single string
    all_text = ' '.join(df_selected['text'].astype(str))

    # # Define a list of words to remove (customize as needed)
    words_to_remove = ['muy', 'para', 'se', 'XochitlGalvez', 'Gálvez','cómo', 'Xóchitl','https', 'la','los','que','y']

    # Remove specified words from the text
    for word in words_to_remove:
        all_text = all_text.replace(word, '')

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=STOPWORDS).generate(all_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    st.pyplot()

with c2:
    st.markdown('### Donut chart')
    Donut = df['sentiment_label'].value_counts().reset_index()
    Donut.columns = ['sentiment_label', 'Count']
    plost.donut_chart(
            theta = "Count", 
            data=Donut,
            color= 'sentiment_label',
            legend='bottom', 
            use_container_width=True)

# Row C

# Display the word cloud using matplotlib
st.markdown('### Tweets')
selected_col=['date','text', 'sentiment_score']
df_tweet = df_selected[selected_col]
st.table(df_tweet)
#st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)


# streamlit run streamlit_app.py


