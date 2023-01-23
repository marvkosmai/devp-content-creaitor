import random
import tkinter as tk
import tkinter.messagebox as msg
import tkinter.ttk as ttk
import pandas as pd

from TitleDataloader import TitleDataloader

correct_answer = 3
asw_counter = 0
total_counter = 0
guessing_data = None
summary_data = None
score = 0

def window_setup(window: tk.Tk):
    window.geometry('1280x720')
    window.minsize(1000, 500)
    window.title("YouTube Title Guessing Game")
    frame = tk.Frame()
    frame.pack()
    frame.rowconfigure(tuple(range(3)), weight=1)
    frame.rowconfigure(3, weight=0)
    frame.columnconfigure(tuple(range(2)), weight=1)
    global asw1_stringvar
    global asw2_stringvar
    global summary_stringvar
    global score_stringvar
    summary_stringvar = tk.StringVar()
    asw1_stringvar = tk.StringVar()
    asw2_stringvar = tk.StringVar()
    asw1_stringvar.set('ASW1')
    asw2_stringvar.set('ASW2')
    score_stringvar = tk.StringVar()
    score_stringvar.set('0/0')
    summary_stringvar.set('Sum')
    button_style = ttk.Style()
    button_style.configure('my.TButton', font=('Arial', 15), justify=tk.CENTER,relief=tk.GROOVE)
    glabel_style = ttk.Style()
    glabel_style.configure('greeting.TLabel', font=('Arial', 45), justify=tk.CENTER)
    sglabel_style = ttk.Style()
    sglabel_style.configure('subgreeting.TLabel', font=('Arial', 20), justify=tk.CENTER)
    lbl_greeting = ttk.Label(master=frame, text='The YouTube Title guessing Game.', style='greeting.TLabel')
    lbl_subgreeting = ttk.Label(master=frame,
                                text="Select the answer you think was written by the video's original creator",
                                style='subgreeting.TLabel')
    lbl_summary = ttk.Label(master=frame,textvariable = summary_stringvar,wraplength=1000, justify=tk.CENTER,
                            font=('Arial', 15))
    lbl_score = ttk.Label(master=frame,textvariable = score_stringvar,wraplength=1000, justify=tk.CENTER,
                            font=('Arial', 25))

    #btn_answer1 = ttk.Button(master=frame, textvariable=asw1_stringvar, style='my.TButton',command=lambda: guess(1))
    btn_answer1 = tk.Button(master=frame, textvariable=asw1_stringvar,wraplength=200, font=('Arial', 15), justify=tk.CENTER,relief=tk.GROOVE,command=lambda: guess(1))
    #btn_answer2 = ttk.Button(master=frame, textvariable=asw2_stringvar, style='my.TButton',command=lambda: guess(2))
    btn_answer2 = tk.Button(master=frame, textvariable=asw2_stringvar,wraplength=200, font=('Arial', 15), justify=tk.CENTER,relief=tk.GROOVE,command=lambda: guess(2))
    btn_resetscore = tk.Button(master=frame, text='Reset Score',wraplength=200, font=('Arial', 15), justify=tk.CENTER,relief=tk.GROOVE,command=reset_score)
    lbl_greeting.grid(column=0, row=0, padx=5, pady=5, columnspan=2)
    lbl_subgreeting.grid(column=0, row=1, padx=5, pady=5, columnspan=2)
    lbl_summary.grid(column=0, row=2, padx=5, pady=15,columnspan=2)
    btn_answer1.grid(column=0, row=3, padx=5, pady=5, ipadx = 5,ipady = 5, sticky='NEWS')
    btn_answer2.grid(column=1, row=3, padx=5, pady=5, ipadx = 5,ipady = 5, sticky='NEWS')
    lbl_score.grid(column=0, row=4,columnspan=2, padx=5, pady=5, ipadx = 5,ipady = 5)
    btn_resetscore.grid(column=0, row=5,columnspan=2, padx=5, pady=5, ipadx = 5,ipady = 5)
    return window


def reset_score():
    global score
    global total_counter
    global score_stringvar
    score = 0
    total_counter  =1
    score_stringvar.set('0/0')

def answer_setup():
    global asw_counter
    global asw1_stringvar
    global asw2_stringvar
    global guessing_data
    global summary_stringvar
    global summary_data
    global total_counter
    global correct_answer
    #guessing_data = TitleDataloader(path="tom_scott_videos_t5_headline_vanilla_summarized_v2.csv").load()
    guessing_data = TitleDataloader(path="tom_scott_videos_trained.csv").load()
    summary_data = pd.read_csv("tom_scott_all_title_summary.csv", delimiter=',')
    #gen_title = guessing_data.iloc[asw_counter]['generated']
    summary = pd.Series()
    while(len(summary)==0):
        gen_title = guessing_data.iloc[asw_counter]['t0_3B_vanilla_title_summarized']
        orig_title = guessing_data.iloc[asw_counter]['title']
        summary = summary_data.loc[summary_data['title']==orig_title]['summary']
        asw_counter += 1
    summary = summary.values[0]
    if random.randint(1, 2) == 1:
        asw1_stringvar.set(gen_title)
        asw2_stringvar.set(orig_title)
        correct_answer = 2
    else:
        asw1_stringvar.set(orig_title)
        asw2_stringvar.set(gen_title)
        correct_answer = 1
    summary_stringvar.set(summary)
    total_counter+=1



def guess(answer: int):
    global asw_counter
    global asw1_stringvar
    global asw2_stringvar
    global correct_answer
    global guessing_data
    global summary_stringvar
    global score
    global total_counter
    global score_stringvar
    if answer == correct_answer:
        #print('You guessed correctly')
        score+=1
        if score >= 5:
            msg.showinfo(title='Win', message=f'You won.\n You got 5 correct answers :)\n {score}/{total_counter}')
            total_counter = 0
            score = 0
            score_stringvar.set(f'{score}/{total_counter}')
        else:
            msg.showinfo(title='Correct', message=f'You guessed correctly\n {score}/{total_counter}')
            score_stringvar.set(f'{score}/{total_counter}')
    else:

        print('You guessed wrong')
        if (total_counter-score) >= 10:
            msg.showinfo(title='Lose', message=f'You lost.\n You got 10 wrong answers :(\n {score}/{total_counter}')
            total_counter = 0
            score = 0
            score_stringvar.set(f'{score}/{total_counter}')
        else:
            msg.showinfo(title='Wrong', message=f'You guessed wrong\n {score}/{total_counter}')
            score_stringvar.set(f'{score}/{total_counter}')
    summary = pd.Series()
    while (len(summary) == 0):
        gen_title = guessing_data.iloc[asw_counter]['t0_3B_vanilla_title_summarized']
        orig_title = guessing_data.iloc[asw_counter]['title']
        summary = summary_data.loc[summary_data['title'] == orig_title]['summary']
        asw_counter += 1
    summary = summary.values[0]
    if random.randint(1, 2) == 1:
        asw1_stringvar.set(gen_title)
        asw2_stringvar.set(orig_title)
        correct_answer = 2
    else:
        asw1_stringvar.set(orig_title)
        asw2_stringvar.set(gen_title)
        correct_answer = 1
    summary_stringvar.set(summary)
    total_counter += 1


if __name__ == '__main__':
    window = tk.Tk()
    window_setup(window)
    answer_setup()


    window.mainloop()
