# -*- coding: utf-8 -*-

import re
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import tkinter as tk
from tkinter import *

def file_import(file_path):
    text =open(file_path, encoding="utf8")
    sent = text.read()
    return sent

def pre_tokenised(sent):
    pattern = re.compile(r"!|।|\.")
    print(pattern.split(sent))
    token = pattern.split(sent)
    return token
   
def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, ' ', data)

def preprocess(text):
      # for removing punctuation from sentencesc
    text = str(text)
#     text = re.sub(r'(\d+)', r'', text)
    
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\t', '')
    text = text.replace('\u200d', ' ')
    text=re.sub("(__+)", ' ', str(text)).lower()   #remove _ if it occors more than one time consecutively
    text=re.sub("(--+)", ' ', str(text)).lower()   #remove - if it occors more than one time consecutively
    text=re.sub("(~~+)", ' ', str(text)).lower()   #remove ~ if it occors more than one time consecutively
    text=re.sub("(\+\++)", ' ', str(text)).lower()   #remove + if it occors more than one time consecutively
    text=re.sub("(\.\.+)", ' ', str(text)).lower()   #remove . if it occors more than one time consecutively
    text=re.sub(r"[<>()|&©@#ø\[\]\'\",;:?.~*!]", '', str(text)).lower() #remove <>()|&©ø"',;?~*!
    text = re.sub(r"[‘’।:]", " ", str(text)) #removing other special characters
    text = re.sub("([a-zA-Z])",'',str(text)).lower()
    text = re.sub("(\s+)",' ',str(text)).lower()
    text = remove_emojis(text)
    return text

def post_tokenized(token):
    tokenised = []
    for i in token:
        tmp = []
        for j in i:
            tmp.append(preprocess(j))
        tmp.append('।')
        tokenised.append(''.join(tmp))
    return tokenised


def createfrequencytable(text_string, stopwords):
   stopWords = set(stopwords)
   words = word_tokenize(text_string)
   ps = PorterStemmer()
   
   freqTable = dict()
   for word in words:
      word=str(word)
      word = ps.stem(word)
      if word in stopWords:
         continue
      if word in freqTable:
         freqTable[word] += 1
      else:
         freqTable[word] = 1
   return freqTable

def score_sentences(sentences, freqTable):
    sentenceValue = dict()
    for sentence in sentences:
            word_count_in_sentence = (len(word_tokenize(sentence)))
            for wordValue in freqTable:
                if wordValue in sentence.lower():
                    if sentence[:10] in sentenceValue:
                        sentenceValue[sentence[:10]] += freqTable[wordValue]
                    else:
                        sentenceValue[sentence[:10]] = freqTable[wordValue]
    sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence
    return sentenceValue

def findaverage_score(sentenceValue):
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]
# Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))
    return average

def generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''
    for sentence in sentences:
            if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
                summary += " " + sentence
                sentence_count += 1
#     print(sentence_count)
    return summary


def close():
    root.destroy()

def openFile():
    global tokenised, sentence_val, thresh,sent

    tokenised=[]
    sentence_val = {}
    thresh=0
    summary_bt.config(state=DISABLED)
    filename_var.set("")
    text_box.config(state="normal")
    summary_box.config(state="normal")
    text_box.delete(1.0, END)
    summary_box.delete(1.0, END)
    filename = tk.filedialog.askopenfilename(initialdir="C:/Users", 
                                             title = "Select a File", 
                                             filetypes = (("text files", "*.txt"),))
    filename_var.set(filename)
    sent = file_import(r"{}".format(filename))
    
    token = pre_tokenised(sent)
    text_box.insert(END, sent)
    text_box.config(state="disabled")
    stop=open(r'E:\ML_PROJECTS\Text_summary_hindi\stopwords.txt', encoding="utf8")
    stopwords=[]
    for x in stop:
        stopwords.append(x)

    tokenised = post_tokenized(token)
    tokenised = list(filter(None, tokenised))

    ft=createfrequencytable(' '.join(tokenised), stopwords)
    print(ft)

    sentence_val=score_sentences(tokenised, ft)
    print(sentence_val)

    thresh=findaverage_score(sentence_val)
    
    summary_bt.config(state=NORMAL)
    
    
    
def summary():
    summary_box.config(state="normal")
    summary_box.delete(1.0, END)
    summary = generate_summary(tokenised, sentence_val, 1.5 * thresh)
    print(summary)
    print(len(sent.split()))
    print(len(summary.split()))
    summary_box.insert(END, summary)
    summary_box.config(state="disabled")

root = tk.Tk()
root.title("Hindi Text Summarizer")
root.geometry("1120x500")
filename_var=tk.StringVar()

top_frame = Frame(root)
top_frame.pack(side="top")

bottom_frame = Frame(root)
bottom_frame.pack(side="bottom")


title_frame = Frame(top_frame, width="1120")
title_frame.grid(row=0,column=0)

op_frame = Frame(bottom_frame)
op_frame.grid(row=1,column=0)

text_frame = Frame(bottom_frame)
text_frame.grid(row=2,column=0)

summary_frame = Frame(bottom_frame)
summary_frame.grid(row=2,column=1)

summary_op_frame = Frame(bottom_frame)
summary_op_frame.grid(row=3,column=1)

close_frame = Frame(bottom_frame)
close_frame.grid(row=3,column=0)

title = Label(title_frame, text = 'Hindi Text Summarizer', font = ('calibre',20,'bold'))
title.place(relx=0.5, rely=0.5,anchor="center")
title.pack(pady=20)


choose = Label(op_frame, text = 'Choose File', font = ('calibre',10,'bold'))
choose.grid(row=0,column=0,padx=5, pady=2)

file_name_path = Entry(op_frame,textvariable = filename_var,width=42, font=('calibre',10,'normal'))
file_name_path.grid(row=0,column=1,padx=5, pady=5)

file = Button(op_frame,text="Open",width=10, command=openFile)
file.grid(row=0,column=2,padx=5, pady=5)

text_box = Text(text_frame, width=60, height=20)
text_box.grid(row=0,column=0, padx=30)                                                

close = Button(close_frame, width=10, text="Close", command=close)
close.grid(row=0,column=0,padx=5, pady=5)

summary_box = Text(summary_frame, width=60, height=20)
summary_box.grid(row=0,column=0)     

summary_bt = Button(summary_op_frame, width=20, text="Generate Summary",state = DISABLED, command=summary)
summary_bt.grid(row=1,column=0,padx=5, pady=5)

# print(thresh)

root.mainloop()






