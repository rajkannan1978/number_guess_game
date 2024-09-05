import tkinter as tk
import tkinter.ttk as ttk
import sys
import random
import json

global PLAYER_NAME, NUMBER, LEVEL, MAX_ATTEMPTS, ATTEMPTS
WIDTH, HEIGHT = 800, 600


def create_hints():
    hints = dict()
    if NUMBER % 2 == 0:
        hints[1] = 'The number is Even.'
    else:
        hints[1] = 'The number is Odd.'

    hints[2] = f'The sum of digits of the number is {sum_of_digits(NUMBER)}.'
    if is_prime(NUMBER):
        hints[3] = 'The number is Prime.'
    else:
        hints[3] = 'The number is not Prime.'
    return hints


def give_hint(hints):
    percentage = (ATTEMPTS / MAX_ATTEMPTS) * 100
    hint = ''
    if 20 < percentage < 50:
        hint = hints[1]
        hints[1] = ''
    if 50 < percentage < 70:
        hint = hints[2]
        hints[2] = ''
    if percentage > 70:
        hint = hints[3]
        hints[3] = ''
    return hint


def is_prime(num):
    flag = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            flag = False
            break
    return flag


def sum_of_digits(num):
    sum_digits = 0
    while num:
        sum_digits += (num % 10)
        num = num // 10
    return sum_digits


def cmd_check(txt_widget, listbox, hints):
    global ATTEMPTS
    if not txt_widget.get().isdigit():
        txt_widget.delete(0, tk.END)
        listbox.insert(tk.END, 'Enter any number')
        txt_widget.focus()
        return

    guess = int((txt_widget.get()))
    ATTEMPTS += 1
    display_msg = ''

    if guess == NUMBER:
        score = int(((MAX_ATTEMPTS - ATTEMPTS + 1) / MAX_ATTEMPTS) * 100)
        write_fame(PLAYER_NAME, score, LEVEL)
        game_won(ATTEMPTS, score)

    elif guess > NUMBER:
        display_msg = f'Your guess {guess} is too high.'
    else:
        display_msg = f'Your guess {guess} is too low.'

    if MAX_ATTEMPTS - ATTEMPTS == 1:
        listbox.insert(tk.END, f'{display_msg} (You have {MAX_ATTEMPTS-ATTEMPTS} attempt left with.)')
    else:
        listbox.insert(tk.END, f'{display_msg} (You have {MAX_ATTEMPTS - ATTEMPTS} attempts left with.)')

    hint = give_hint(hints)
    if hint != '':
        listbox.insert(tk.END, f'*** Hint : {hint}')

    if ATTEMPTS == MAX_ATTEMPTS:
        game_lost(ATTEMPTS, NUMBER)

    listbox.yview(tk.END)


def cmd_exit(*agrs):
    window.destroy()
    sys.exit()


def cmd_get_name(*args):
    canvas.delete(3, 4, 5)
    window.unbind('<Alt_L><e>')
    window.unbind('<Alt_L><x>')
    lbl_name = tk.Label(window, text='Enter your Name', font=('Times new roman bold', 20), fg='white', bg='blue')
    canvas.create_window(WIDTH/2, 150, window=lbl_name)

    txt_entry = tk.Entry(window, width=20, font=('Times new roman bold', 20))
    txt_entry.focus()
    txt_entry.bind('<Key>', lambda e: keypress(e, txt_entry, 20))
    txt_entry.bind('<Return>', lambda _: cmd_ok(txt_entry))
    canvas.create_window(WIDTH/2, 200, window=txt_entry)

    btn_ok = tk.Button(window, text='OK', width=6, height=2, font=('Times new roman bold', 18),
                       command=lambda: cmd_ok(txt_entry))
    canvas.create_window(WIDTH/2, 280, window=btn_ok)


def cmd_level(level):
    global NUMBER, LEVEL, MAX_ATTEMPTS, ATTEMPTS
    LEVEL = level
    canvas.delete(9, 10, 11)
    high_range, MAX_ATTEMPTS = set_limits(LEVEL)
    NUMBER = random.randint(1, high_range)
    hints = create_hints()
    ATTEMPTS = 0
    print(NUMBER)
    lbl_name = tk.Label(window, text=PLAYER_NAME, font=('Times new roman bold', 30), fg='blue', bg='white')
    canvas.create_window(WIDTH/2, 120, window=lbl_name)

    lbl_number = tk.Label(window, text=f'Enter your guess (1-{high_range})',
                          font=('Times new roman bold', 20), fg='white', bg='blue')
    canvas.create_window(WIDTH/2, 180, window=lbl_number)

    txt_guess = tk.Entry(window, width=5, font=('Times new roman bold', 20))
    txt_guess.focus()
    txt_guess.bind('<Key>', lambda e: keypress(e, txt_guess, 4))
    txt_guess.bind('<Return>', lambda _: cmd_check(txt_guess, listbox, hints))
    canvas.create_window(WIDTH/2 - 30, 230, window=txt_guess)

    btn_check = tk.Button(window, text='OK', width=4, height=1, font=('Times new roman bold', 18),
                          command=lambda: cmd_check(txt_guess, listbox, hints))
    canvas.create_window(WIDTH/2 + 70, 230, window=btn_check)

    frame = tk.Frame(window, width=WIDTH//1.2, height=300)
    listbox = tk.Listbox(frame, width=60, height=10, font=('Helvetica', 15))
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    canvas.create_window(WIDTH/2, 380, window=frame)

    btn_exit = tk.Button(window, text='Exit', width=10, height=1, font=('Times new roman bold', 18),
                         command=cmd_exit)
    canvas.create_window(WIDTH/2, HEIGHT-70, window=btn_exit)


def cmd_ok(widget):
    global PLAYER_NAME
    canvas.delete(6, 7, 8)
    PLAYER_NAME = widget.get()

    lbl_frame = tk.Frame(window, bg='blue', bd=2, width=400, height=300, highlightbackground='white',
                         highlightcolor='white', highlightthickness=2)
    canvas.create_window(WIDTH/2, 300, window=lbl_frame)

    btn_level1 = tk.Button(window, text='Level 1', width=7, height=1, font=('Times new roman bold', 18),
                           command=lambda: cmd_level(1))
    btn_level2 = tk.Button(window, text='Level 2', width=7, height=1, font=('Times new roman bold', 18),
                           command=lambda: cmd_level(2))
    btn_level3 = tk.Button(window, text='Level 3', width=7, height=1, font=('Times new roman bold', 18),
                           command=lambda: cmd_level(3))

    canvas.create_window(WIDTH/2, 200, window=btn_level1)
    canvas.create_window(WIDTH / 2, 300, window=btn_level2)
    canvas.create_window(WIDTH / 2, 400, window=btn_level3)


def keypress(event, widget, length):
    text = widget.get()
    if len(text) >= length-1:
        widget.delete(length, tk.END)


def set_limits(lvl):
    if lvl == 1:
        high_range = 50
        no_attempts = 5
    elif lvl == 2:
        high_range = 100
        no_attempts = 10
    else:
        high_range = 1000
        no_attempts = 20
    return high_range, no_attempts


def game_won(attempts, score):
    canvas.delete(12, 13, 14, 15, 16, 17, 18)

    rect = canvas.create_rectangle(100, 100, WIDTH-100, HEIGHT-150, outline='white', fill='blue')

    lbl_greets = tk.Label(canvas, text='Congratulations!!!\n You guessed the number.!!!',
                          font=('Times new roman bold', 20))
    canvas.create_window(WIDTH/2, 200, window=lbl_greets)

    if attempts == 1:
        text_attempts = f'You took {attempts} attempt.'
    else:
        text_attempts = f'You took {attempts} attempts.'

    lbl_attempts = tk.Label(canvas, text=text_attempts, font=('Times new roman bold', 20))
    canvas.create_window(WIDTH/2, 300, window=lbl_attempts)

    lbl_score = tk.Label(canvas, text=f'Your score is {score}.', font=('Times new roman bold', 20))
    canvas.create_window(WIDTH/2, 400, window=lbl_score)

    btn_ok = tk.Button(window, text='OK', width=10, height=2,
                       font=('Times new roman bold', 18), command=leader_board)
    canvas.create_window(WIDTH/2, 500, window=btn_ok)


def game_lost(attempts, number):
    canvas.delete(12, 13, 14, 15, 16, 17, 18)

    rect = canvas.create_rectangle(100, 100, WIDTH-100, HEIGHT-150, outline='white', fill='blue')

    lbl_greets = tk.Label(canvas, text="Oops!!! You lost!!!\n You didn't guess the number.!!!",
                          font=('Times new roman bold', 20))
    canvas.create_window(WIDTH/2, 200, window=lbl_greets)

    lbl_attempts = tk.Label(canvas, text=f'You took {attempts} attempts.', font=('Times new roman bold', 20))
    canvas.create_window(WIDTH/2, 300, window=lbl_attempts)

    lbl_number = tk.Label(canvas, text=f'The number is {number}.', font=('Times new roman bold', 20))
    canvas.create_window(WIDTH/2, 400, window=lbl_number)

    btn_ok = tk.Button(window, text='OK', width=10, height=2,
                       font=('Times new roman bold', 18), command=leader_board)
    canvas.create_window(WIDTH/2, 500, window=btn_ok)


def leader_board():
    canvas.delete(19, 20, 21, 22, 23)
    history = read_fame()

    rect = canvas.create_rectangle(100, 100, WIDTH-100, HEIGHT-100, outline='white', fill='blue')
    lbl_leader = tk.Label(canvas, text='Leader Board', font=('Arial Bold', 20), fg='white', bg='blue')
    canvas.create_window(WIDTH/2, 130, window=lbl_leader)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview', rowheight=30)
    style.configure('Treeview.Heading', font=('Times New Roman bold', 20))
    style.configure('Treeview', font=('Times New Roman bold', 18))

    columns = ('Rank', 'Name', 'Score')
    frame = tk.Frame(canvas, width=WIDTH // 1.38, bg='blue')
    tree = ttk.Treeview(frame, column=columns, show="headings", height=10)
    tree.heading('Rank', text='Rank')
    tree.heading('Name', text='Name')
    tree.heading('Score', text='Score')
    tree.column('Rank', anchor=tk.CENTER, width=100)
    tree.column('Name', width=400)
    tree.column('Score', anchor=tk.CENTER, width=100)
    tree.pack(side=tk.BOTTOM)
    canvas.create_window(400, 340, window=frame)

    for name, score in history[str(LEVEL)]:
        tree.insert('', 'end', text="# 1", values=(str(score[1]), ' ' + name, str(score[0])))

    btn_exit_game = tk.Button(window, text='Exit', width=10, height=1,
                              font=('Times new roman bold', 18), command=cmd_exit)
    canvas.create_window(WIDTH/2, HEIGHT-50, window=btn_exit_game)


def read_fame():

    with open('fame.json') as f:
        hist_fame = json.load(f)
    for lvl in range(1, 4):
        if str(lvl) not in hist_fame:
            hist_fame[str(lvl)] = []
    return hist_fame


def write_fame(player_name, score, level):
    hist_fame = read_fame()
    hist_fame[str(level)].append([player_name, [score, 0]])
    sorted_data = sorted(hist_fame[str(level)], key=lambda x: x[1], reverse=True)[:10]
    fame = [[player, [scores[0], i+1]] for i, (player, scores) in enumerate(sorted_data)]
    hist_fame[str(level)] = fame
    json_object = json.dumps(hist_fame)

    with open("fame.json", "w") as outfile:
        outfile.write(json_object)


window = tk.Tk()
window.title("Welcome to Number Guess Game")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f'{str(WIDTH)}x{str(HEIGHT)}+{str((screen_width-WIDTH)//2)}+{str((screen_height-HEIGHT)//2)}')
icon = tk.PhotoImage(file='images/Icon_123.png')
window.iconphoto(True, icon)
window.resizable(0, 0)

canvas = tk.Canvas(window, width=screen_width-40, height=screen_height-20, bg='grey')
canvas.pack()

rectangle = canvas.create_rectangle(20, 20, WIDTH-20, HEIGHT-20, fill='blue')

lbl_Title = tk.Label(window, text='Welcome to Number Guess Game', font=('Arial Bold', 30))

instruction = """ Computer will generate a random number between 
1 to 50 for Level 1, 1 to 100 for Level 2, 1 to 1000 for Level 3.

You have to guess that number.
If your guess is correct, you WON the game!!!
if your guess is greater than the correct number, you will get 
"The guess is too high".
if your guess is less, then you will get 
"The guess is too low".
You guess again.
"""

lbl_instruction = tk.Label(window, text=instruction, font=('Times new roman', 20))

btn_enter = tk.Button(window, text='Enter', width=10, height=2, font=('Times new roman bold', 18), underline=0,
                      command=cmd_get_name)
btn_exit = tk.Button(window, text='Exit', width=10, height=2, font=('Times new roman bold', 18), underline=1,
                     command=cmd_exit)

window.bind('<Alt_L><e>', cmd_get_name)
window.bind('<Alt_L><x>', cmd_exit)

canvas.create_window(WIDTH/2, 50, window=lbl_Title)
canvas.create_window(WIDTH/2, 300, window=lbl_instruction)
canvas.create_window(WIDTH/2-180, HEIGHT-70, window=btn_enter)
canvas.create_window(WIDTH/2+180, HEIGHT-70, window=btn_exit)

window.mainloop()
