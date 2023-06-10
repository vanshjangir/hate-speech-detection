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

        self.geometry('1920x1080')
        self.title('Hate Speech Detection')

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.head = ctk.CTkLabel(self, text = "HateSpeechDetector", fg_color = "transparent")
        self.head.place(relx = 0.5, rely = 0.2, anchor = "center")
    
        self.BtnYoutube = ctk.CTkButton(self, text = "youtube", command = self.youtubecomments)
        self.BtnYoutube.place(relx = 0.5, rely = 0.3, anchor = "center")

        self.BtnText = ctk.CTkButton(self, text = "Text", command = self.textfrominput)
        self.BtnText.place(relx = 0.2, rely = 0.3, anchor = "center")
    
        self.BtnFile = ctk.CTkButton(self, text = "File", command = self.textfromfile)
        self.BtnFile.place(relx = 0.8, rely = 0.3, anchor = "center")

        self.TextBox = ctk.CTkTextbox(self, fg_color="transparent",border_width=2, corner_radius=4, bg_color="#2b2b2b")
        self.TextBox.bind('<Return>', lambda event: userinput(self, text = self.TextBox.get("0.0","end")))
    
        self.LinkEntry = ctk.CTkEntry(self, placeholder_text = "link")
        self.LinkEntry.bind('<Return>', lambda event: userinput(self, link = self.LinkEntry.get()))

    def textfromfile(self):
        '''
        takes a .txt file and returns a list of all the sentences
        '''
        filename = ctk.filedialog.askopenfilename(title = "Select a File", 
                                          filetypes = (("Text files", "*.txt*"),("all files","*.*")))

        file  = open(filename, 'r')
        data = ""
        with open(filename, 'r') as file:
            data = file.read().replace('\n','')

        userinput(root = self,text = data)

    def textfrominput(self):
        '''
        prompts user to give input in a testbox and returns a list of sentences
        '''
        self.TextBox.configure(width = self.winfo_width()*0.71, height = self.winfo_height()*0.3)
        try:
            self.LinkEntry.place_forget()
        except:
            pass

        self.TextBox.place(relx = 0.5, rely = 0.5, anchor = "center")
    
    def youtubecomments(self):
        '''
        returns list of comments on a youtube video 
        '''    
        self.LinkEntry.configure(width = self.winfo_width()*0.71)
        try:
            self.TextBox.place_forget()
        except:
            pass
        self.LinkEntry.place(relx = 0.5, rely = 0.4, anchor = "center")

    
def userinput(root, link = None, text = None):
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

    result(root,corpus[:-1])


def result(root,text):
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
            negative += (f"{num+1}. ")
            negative += str(text[i])
            negative += "\n\n";
            num += 1 

    if len(negative) == 0:
        negative = "This document does not contains any hate speech"

            
    ResultLabel = ctk.CTkTextbox(root, fg_color="transparent", activate_scrollbars = True)
    ResultLabel.configure(height = root.winfo_height()*0.3, width = root.winfo_width()*0.71)
    ResultLabel.insert("0.0", (f"Out of {len(text)}  no. of negatives are {num}\n\n"))
    ResultLabel.insert("end", negative)
    ResultLabel.configure(state = "disabled")
    ResultLabel.place(relx = 0.5, rely = 0.85, anchor = "center")

def main():
    App = APPwindow()
    App.mainloop()

if __name__ == "__main__":
    main()

