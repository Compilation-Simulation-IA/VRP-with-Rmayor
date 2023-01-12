from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.font import Font
from my_parser import RmayorParser

class MyApp:

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Simple Text Editor")
        self.window.geometry('1000x1000')
        self.window.configure(bg='white')

        myFont = Font(family='Courier New', size=12)

        self.window.rowconfigure(1, minsize=50, weight=1)
        self.window.columnconfigure(1, minsize=50, weight=1)

        self.txt_code = Text(self.window, borderwidth=3)
        self.txt_result = Text(self.window, borderwidth=3)
        frm_buttons = Frame(self.window, relief=RAISED, bd=2, bg='white')
        btn_run = Button(frm_buttons, text="Run", command=self.run, bg='green', font=myFont)
        #btn_stop = Button(frm_buttons, text="Stop", command=self.stop, bg='red', font=myFont)

        self.text_input=Entry(frm_buttons,width=10, textvariable=self.txt_code)

        btn_run.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        #btn_stop.grid(row=2, column=0, sticky="ew", padx=5)

        frm_buttons.grid(row=1, column=0, sticky="ns")
        self.txt_code.grid(row=1, column=1, sticky="nsew")
        self.txt_result.grid(row=3,column=1, sticky="new")

        menu = Menu(self.window, relief=RAISED, bd=2, bg='white')

        self.window.config(menu=menu)
        filemenu = Menu(frm_buttons, relief=RAISED, bd=2, bg='white',font=myFont, borderwidth=10)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New')
        filemenu.add_command(label='Open', command=self.open_file)
        filemenu.add_command(label='Save', command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.window.quit)

        self.window.mainloop()

        

    def open_file(self):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        self.txt_code.delete("1.0", END)
        with open(filepath, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()
            self.txt_code.insert(END, text)
        self.window.title(f"Simple Text Editor - {filepath}")


    def save_file(self):
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, mode="w", encoding="utf-8") as output_file:
            text = self.txt_code.get("1.0", END)
            output_file.write(text)
        self.window.title(f"Simple Text Editor - {filepath}")

    def stop():
        pass

    def run(self):
        try:
            _input = self.text_input
            RmayorParser.parse(_input)
            with open('30_simulations.txt', mode="r", encoding="utf-8") as input_file:
                text = input_file.read()
                self.txt_result.insert(END, text)

        except ValueError:
            self.txt_result.delete("1.0", END)        
            self.txt_result.insert(END, ValueError)

MyApp()