import json
import pandas as pd
import numpy as np
import streamlit as st
import requests
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
# nltk.download("punkt")
# nltk.download("stopwords")
from pprint import pprint
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

api_key_dict = main_functions.read_from_file("JSON_Files/api_keys.json")
api_key = api_key_dict["my_key"]
st.title("COP4813 - Web Application Programming")

st.title("Project 1")

st.header('Part A - Top Stories API')

st.write("I - Topic Select")

st.subheader('This app uses the Top Stories API to display the most '
             'common words used in the top current articles based on a specified topic selected by the user. '
             'The data is displayed as a line chart and as a wordcloud image')

name = st.text_input("Please enter your name")

st.write("Your name is", name)

option = st.selectbox(
    'Select a topic',
    ['', 'arts', 'automobiles', 'books', 'business', 'fashion',
     'food', 'health', 'home', 'insider', 'magazine', 'movies', 'nyregion', 'obituaries',
     'opinion', 'politics', 'realestate', 'science', 'sports', 'sundayreview', 'technology',
     'theater', 't-magazine', 'travel', 'upshot', 'us', 'world']
)
if option != '':
    st.write("Hi", name, "you selected the", option, "topic.")
    st.header('II - Frequency Distribution')

    url = "https://api.nytimes.com/svc/topstories/v2/" + option + ".json?api-key=" + api_key

    response = requests.get(url).json()

    main_functions.save_to_file(response, "JSON_Files/response.json")

    my_articles = main_functions.read_from_file("JSON_Files/response.json")

    str1 = ""

    for i in my_articles["results"]:
        str1 = str1 + i["abstract"]

    words = word_tokenize(str1)

    fdist = FreqDist(words)

    words_no_punc = []

    for w in words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    fdist2 = FreqDist(words_no_punc)

    pprint(fdist2.most_common((10)))

    stopwords1 = stopwords.words("english")

    clean_words = []
    fdist3 = FreqDist(clean_words)
    for w in words_no_punc:
        if w not in stopwords1:
            clean_words.append(w)

    print(len(clean_words))
    if st.checkbox("Click here to generate frequency distribution"):
        fdist4 = FreqDist(clean_words).most_common(10)
        # top10 = fdist4.most_common(10)
        freqdata = pd.DataFrame(fdist4, columns=["Word", "Frequency"])
        #st.line_chart(freqdata)
        fig = px.line(freqdata, x='Word', y ='Frequency',title ="Most Common words used")
        st.plotly_chart(fig)


        #remove one and behind
        #st.write(freqdata)
        #

        # st.write(top10words)
        # st.write(top10)
    st.header('III - Word Cloud')
    if st.checkbox("Click here to create a word cloud"):
        fdist4 = FreqDist(clean_words)
        fdist4words = ' '.join([str(elem) for elem in fdist4])
        wordcloud = WordCloud().generate(fdist4words)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        st.pyplot()
st.header('Part B - Most Popular Articles API')

st.write("Select if you want to see the most shared,emailed, or viewed articles")
option2 = st.selectbox(
    'Select the set of articles',
    ['', 'shared', 'emailed', 'viewed'])
days = st.selectbox(
        'Select the period of time(last days)',
        ['', '1', '7', '30'])
if option2 and days:
    url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + option2 + "/" + days + ".json?api-key=" + api_key

    mostpop = requests.get(url2).json()

    main_functions.save_to_file(mostpop, "JSON_Files/mostpop.json")

    my_articles = main_functions.read_from_file("JSON_Files/mostpop.json")

    str1 = ""

    for i in my_articles["results"]:
        str1 = str1 + i["abstract"]

    words = word_tokenize(str1)

    fdist = FreqDist(words)

    words_no_punc = []

    for w in words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    fdist2 = FreqDist(words_no_punc)

    pprint(fdist2.most_common((10)))

    stopwords2 = stopwords.words("english")

    clean_words = []
    fdist3 = FreqDist(clean_words)
    for w in words_no_punc:
        if w not in stopwords2:
            clean_words.append(w)
    words2 = ' '.join([str(elem) for elem in clean_words])
    wordcloud = WordCloud().generate(words2)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    st.pyplot()