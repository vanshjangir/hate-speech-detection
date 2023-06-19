# Hate Speech Detection

A Python based Machine Learning model that filters hate comments in a text corpus.

## Requirments

1. pandas
2. tweet_preprocessor
3. gensim
4. numpy
5. joblib
6. sklearn
7. configparser
8. googleapiclient
9. flask
10. customtkinter

## Model

The model is a binary classifier that uses support vector machines to classify hate speech and non-hate speech vectors. First the text in the merged dataset is converted in vector using word2vec feature extraction technique.

## Application

The tkinterGUI.py file open customtkinter window that accepts text, youtube video link and .txt file as input and then it show which sentences or comments can be flaged as hate speech. This uses youtube data api to fetch comments under a video using video_id.

The web.py uses flask as a backend to the templates/index.html file.
The bridge.py acts as a bridge that connects the the web application and the model.
