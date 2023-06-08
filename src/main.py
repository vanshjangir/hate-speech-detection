import model 
import youtube
import joblib
import gensim
import customtkinter as ctk 
import configparser

loadmodel = joblib.load("finalized_model.sav")
w2v_model = joblib.load("w2v_model.sav")

class APPwindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.geometry('800x500')
        self.title('Hate Speech Detection')

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.head = ctk.CTkLabel(self, text = "HateSpeechDetector", fg_color = "transparent")
        self.head.place(relx = 0.5, rely = 0.2, anchor = "center")
    
        self.BtnYoutube = ctk.CTkButton(self, text = "youtube", command = self.youtubecomments)
        self.BtnYoutube.place(relx = 0.5, rely = 0.3, anchor = "center")

        self.BtnText = ctk.CTkButton(self, text = "Text", command = self.textfrominput)
        self.BtnText.place(relx = 0.2, rely = 0.3, anchor = "center")
    
        self.BtnFile = ctk.CTkButton(self, text = "File", command = self.textfromfile())
        self.BtnFile.place(relx = 0.8, rely = 0.3, anchor = "center")

        self.TextBox = ctk.CTkTextbox(self, fg_color="transparent",border_width=1, corner_radius=1, bg_color="#2b2b2b")
        self.TextBox.configure(height = 200, width = 300)
        self.TextBox.bind('<Return>', lambda event: userinput(event, self, text = self.TextBox.get("0.0","end")))
    
        self.LinkEntry = ctk.CTkEntry(self, placeholder_text = "link", width = 600)
        self.LinkEntry.bind('<Return>', lambda event: userinput(event, self, link = self.LinkEntry.get()))

    def textfromfile(self):
        '''
        takes a .txt file and returns a list of all the sentences
        '''
        pass 

    def textfrominput(self):
        '''
        prompts user to give input in a testbox and returns a list of sentences
        '''
        try:
            self.LinkEntry.place_forget()
        except:
            pass 
        self.TextBox.place(relx = 0.5, rely = 0.7, anchor = "center")
    
    def youtubecomments(self):
        '''
        returns list of comments on a youtube video 
        '''    
        try:
            self.TextBox.place_forget()
        except:
            pass
        self.LinkEntry.place(relx = 0.5, rely = 0.6, anchor = "center")

    
def userinput(event, root, link = None, text = None):
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
        print("youtube comments:", len(comments))
        corpus = comments
    elif text != None:
        corpus = text.split(".")

    result(root,corpus)


def result(root,text):
    '''
    show the predictions of the model and print them in a label
    '''
    test = []
    for each in text:
        test.append(gensim.utils.simple_preprocess(each, deacc=False, min_len=2, max_len=50))

    test = model.makevector(w2v_model, test)
    score = loadmodel.predict(test)

    positive= 0 
    negative = 0 
    for i in score:
        if i == 1:
            negative += 1
        else:
            positive += 1

    ResultLabel = ctk.CTkLabel(root, fg_color="transparent", text = (f"no of positves are {positive} and negatives are {negative}"))
    ResultLabel.configure(height = 20, width = 100)
    ResultLabel.place(relx = 0.5, rely = 0.7,anchor = "center")

def main():
    App = APPwindow()
    App.mainloop()

if __name__ == "__main__":
    main()

