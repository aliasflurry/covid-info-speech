import random

from tkinter import *
from tkinter import messagebox as tkMessageBox
import tkinter as tki
from tkinter import filedialog as th1
import re
import time
from config import config as cfg
from model.Data import Data
from service.SpeechRecognition import SpeechRecognizer
import tkinter as tk
API_KEY = cfg.credential['API_KEY']
PROJECT_TOKEN = cfg.credential['PROJECT_TOKEN']
RUN_TOKEN= cfg.credential['RUN_TOKEN']

data = Data(API_KEY, PROJECT_TOKEN)
country_list = data.get_list_of_countries()

TOTAL_PATTERNS = {
				re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
				re.compile("[\w\s]+ total cases"): data.get_total_cases,
				re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
				re.compile("[\w\s]+ total deaths"): data.get_total_deaths
				}

COUNTRY_PATTERNS = {
				re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
				re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
				}


recognizer = SpeechRecognizer(TOTAL_PATTERNS, COUNTRY_PATTERNS, country_list, data)
recognizer.start()

class App(object):

    def __init__(self,root):
        self.root = root

    # create a Frame for the Text and Scrollbar
        txt_frm = tki.Frame(self.root, width=900, height=900)
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)

    # create first Text label, widget and scrollbar
        self.lbl1 = tki.Label(txt_frm, text="Covid-19 cases in countries", font=("Courrier", 44))
        self.lbl1.grid(row=0,column=0,padx=2,pady=2)

        self.recognized_text = StringVar()
        self.txt1 = tki.Text(txt_frm, borderwidth=3, relief="sunken", height=100,width=55,)
        self.txt1.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt1.grid(row=25, column=0, sticky="nsew", padx=2, pady=2)
        root.after(100, self.update_recognized_text)

    def update_recognized_text(self):
        self.txt1.delete(0.0, END)
        self.txt1.insert(0.0, recognizer.recognized_text)
        root.after(100, self.update_recognized_text)

    def clearBox(self):
        if a == "clear":
            self.txt1.delete('1.0', 'end')

root = tki.Tk()
app = App(root)
root.mainloop()