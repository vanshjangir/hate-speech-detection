import model 
import youtube
import joblib
import gensim
import tkinter as tk
import customtkinter as ctk 
import configparser

loadmodel = joblib.load("finalized_model.sav")
w2v_model = joblib.load("w2v_model.sav")


def textfromfile():
    '''
    takes a .txt file and returns a list of all the sentences
    '''
    pass 

def textfrominput():
    '''
    prompts user to give input in a testbox and returns a list of sentences
    '''
    pass 

def youtubecomments(root):
    '''
    returns list of comments on a youtube video 
    '''
    config = configparser.ConfigParser()
    config.read("config.ini")

    api_key = config['youtube']['api_key']
    video_id = ""
   
    LinkEntry = ctk.CTkEntry(root, placeholder_text = "link")
    LinkEntry.place(relx = 0.5, rely = 0.6, anchor = "center")
    
    link = "https://www.youtube.com/watch?v=6Zs8Kp8YULA&t=1s"
    
    for i in range(len(link)):
        if link[i] == "=": 
            video_id = link[i+1:i+12]
            break 

    comments = youtube.fetch_video_comments(video_id, api_key)
    print(len(comments))
    result(root,comments)


def result(root,text):
    '''
    Opens the entry box to type link and show the results
    by calling appropriate functions
    '''
    test = []
    target = []
    for each in text:
        test.append(gensim.utils.simple_preprocess(each, deacc=False, min_len=2, max_len=50))
        target.append(1)

    test = model.makevector(w2v_model, test)
    score = loadmodel.predict(test)

    positive= 0 
    negative = 0 
    for i in score:
        if i == 1:
            negative += 1
        else:
            positive += 1

    print(positive,negative)

def main():
    root = ctk.CTk()
    root.geometry('800x500')
    root.title('Hate Speech Detection')

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    head = ctk.CTkLabel(root, text = "HateSpeechDetector", fg_color = "transparent")
    head.place(relx = 0.5, rely = 0.2, anchor = "center")
    
    BtnYoutube = ctk.CTkButton(root, text = "youtube", state = "normal", command = lambda: youtubecomments(root))
    BtnYoutube.place(relx = 0.5, rely = 0.5, anchor = "center")

    root.mainloop()


if __name__ == "__main__":
    main()

