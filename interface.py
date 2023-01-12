from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.font import Font
import init


def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_code.delete("1.0", END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        txt_code.insert(END, text)
    window.title(f"Simple Text Editor - {filepath}")


def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_code.get("1.0", END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")

def stop():
    pass



window = Tk()
window.title("Simple Text Editor")
window.geometry('1000x1000')
window.configure(bg='white')

myFont = Font(family='Courier New', size=12)

window.rowconfigure(1, minsize=50, weight=1)
window.columnconfigure(1, minsize=50, weight=1)

def run():
    try:
        _input = txt_code.get(1.0, END)
        init.start_visitor(_input)
    except ValueError:
        pass
txt_code = Text(window, borderwidth=3)
txt_result = Text(window, borderwidth=3)
frm_buttons = Frame(window, relief=RAISED, bd=2, bg='white')
btn_run = Button(frm_buttons, text="Run", command=run, bg='green', font=myFont)
btn_stop = Button(frm_buttons, text="Stop", command=stop, bg='red', font=myFont)

text_input=Entry(frm_buttons,width=10, textvariable=txt_code)

btn_run.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_stop.grid(row=2, column=0, sticky="ew", padx=5)

frm_buttons.grid(row=1, column=0, sticky="ns")
txt_code.grid(row=1, column=1, sticky="nsew")
txt_result.grid(row=3,column=1, sticky="new")

menu = Menu(window, relief=RAISED, bd=2, bg='white')

window.config(menu=menu)
filemenu = Menu(frm_buttons, relief=RAISED, bd=2, bg='white',font=myFont, borderwidth=10)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New')
filemenu.add_command(label='Open', command=open_file)
filemenu.add_command(label='Save', command=save_file)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=window.quit)

window.mainloop()


