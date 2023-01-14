import random
import tkinter as tk
import tkinter.messagebox as msg
import tkinter.ttk as ttk

from TitleDataloader import TitleDataloader

correct_answer = 3
asw_counter = 0
guessing_data = None


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
    summary_stringvar = tk.StringVar()
    asw1_stringvar = tk.StringVar()
    asw2_stringvar = tk.StringVar()
    asw1_stringvar.set('ASW1')
    asw2_stringvar.set('ASW2')
    summary_stringvar.set('Sum')
    button_style = ttk.Style()
    button_style.configure('my.TButton', font=('Arial', 15), justify=tk.CENTER)
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

    lbl_answer1 = ttk.Label(master=frame, textvariable=asw1_stringvar, wraplength=300, justify=tk.CENTER,
                            font=('Arial', 15))
    lbl_answer2 = ttk.Label(master=frame, textvariable=asw2_stringvar, wraplength=300, justify=tk.CENTER,
                            font=('Arial', 15))
    btn_answer1 = ttk.Button(master=frame, text='Answer1', style='my.TButton',
                             command=lambda: guess(1))
    btn_answer2 = ttk.Button(master=frame, text='Answer2', style='my.TButton',
                             command=lambda: guess(2))
    lbl_greeting.grid(column=0, row=0, padx=5, pady=5, columnspan=2)
    lbl_subgreeting.grid(column=0, row=1, padx=5, pady=5, columnspan=2)
    lbl_summary.grid(column=0, row=2, padx=5, pady=15,columnspan=2)
    lbl_answer1.grid(column=0, row=3, padx=5, pady=15)
    lbl_answer2.grid(column=1, row=3, padx=5, pady=15)
    btn_answer1.grid(column=0, row=4, padx=5, pady=5, sticky='NEWS')
    btn_answer2.grid(column=1, row=4, padx=5, pady=5, sticky='NEWS')
    return window


def answer_setup():
    global asw_counter
    global asw1_stringvar
    global asw2_stringvar
    global guessing_data
    global summary_stringvar
    guessing_data = TitleDataloader(path="tom_scott_videos_t5_headline_vanilla_summarized_v2.csv").load()
    gen_title = guessing_data.iloc[asw_counter]['generated']
    orig_title = guessing_data.iloc[asw_counter]['title']
    summary = guessing_data.iloc[asw_counter]['summary']
    if random.randint(1, 2) == 1:
        asw1_stringvar.set(gen_title)
        asw2_stringvar.set(orig_title)
        correct_answer = 2
    else:
        asw1_stringvar.set(orig_title)
        asw2_stringvar.set(gen_title)
        correct_answer = 1
    summary_stringvar.set(summary)
    asw_counter += 1


def guess(answer: int):
    global asw_counter
    global asw1_stringvar
    global asw2_stringvar
    global correct_answer
    global guessing_data
    global summary_stringvar
    if answer == correct_answer:
        print('You guessed correctly')
        msg.showinfo(title='Correct', message='You guessed correctly')
    else:
        print('You guessed wrong')
        msg.showinfo(title='Wrong', message='You guessed wrong')
    gen_title = guessing_data.iloc[asw_counter]['generated']
    orig_title = guessing_data.iloc[asw_counter]['title']
    summary = guessing_data.iloc[asw_counter]['summary']
    if random.randint(1, 2) == 1:
        asw1_stringvar.set(gen_title)
        asw2_stringvar.set(orig_title)
        correct_answer = 2
    else:
        asw1_stringvar.set(orig_title)
        asw2_stringvar.set(gen_title)
        correct_answer = 1
    summary_stringvar.set(summary)
    asw_counter += 1


if __name__ == '__main__':
    window = tk.Tk()
    window_setup(window)
    answer_setup()


    window.mainloop()
