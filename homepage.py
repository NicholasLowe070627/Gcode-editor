from tkinter import *
from tkinter import filedialog

class home_page():
    def __init__(self):
        self.root = Tk()
        self.root.title("G Code editor Home page")
        self.root.geometry("800x800")
        self.root.rowconfigure(0, weight = 1)
        self.root.rowconfigure(1, weight = 1)
        self.root.rowconfigure(2, weight = 5)
        self.root.rowconfigure(3, weight= 2)
        self.root.columnconfigure(0, weight = 1)
        self.root.columnconfigure(1, weight = 1)
        
        self.title = Label(self.root, text = "G code editor for the roland CNC machine", font = "Arial 30")
        self.title.grid(row = 0, column= 0, columnspan= 2, sticky="news")
        
        self.subtitle = Label(self.root, text = "Which file would you like to edit", font = "Arial 20")
        self.subtitle.grid(row = 1, column= 0, columnspan= 2, sticky="news")
        
        self.trace_button = Button(self.root, text = "Trace File")
        self.trace_button.grid(row = 2, column= 0, sticky="ew")
        
        self.drill_button = Button(self.root, text = "Drill File")
        self.drill_button.grid(row = 2, column=1, sticky="ew")
        
        self.quit_button = Button(self.root, text = "Quit", bg = "red")
        self.quit_button.grid(row = 3, column= 0, columnspan= 2)
    def run(self):
        self.root.mainloop()
       
if __name__ == "__main__":
    convert = home_page()
    convert.run()