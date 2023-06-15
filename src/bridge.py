import model 
import youtube
import joblib
import gensim
import configparser

loadmodel = joblib.load("finalized_model.sav")
w2v_model = joblib.load("w2v_model.sav")

def userinput(link = None, text = None):
    '''
    takes a link from entrybox or string from textbox and shows the results
    '''
    corpus = []

    if link != None:
        config = configparser.ConfigParser()
        config.read("config.ini")

        api_key = config['youtube']['api_key']
        video_id = ""
        
        for i in range(len(link)):
            if link[i] == "=": 
                video_id = link[i+1:i+12]
                break 

        comments = youtube.fetch_video_comments(video_id, api_key)
        if comments == "ERROR 1: input not a link":
            return comments 
        print("youtube comments:", len(comments))
        corpus = comments

    elif text != None:
        corpus = text.split(".")

    return result(corpus[:-1])


def result(text):
    '''
    show the predictions of the model and print them in a label
    '''
    test = []
    for each in text:
        test.append(gensim.utils.simple_preprocess(each, deacc=False, min_len=2, max_len=50))

    test = model.makevector(w2v_model, test)
    score = loadmodel.predict(test)

    negative = ""
    num = 0 
    for i in range(len(text)):
        if score[i] == 1:
            negative += f"{num+1}. "
            negative += text[i]
            negative += "\n\n"
            num += 1 

    negative = f"{num} hate comments<br>" + negative

    if len(negative) == 0:
        negative = "This document does not contains any hate speech"

    return negative 

