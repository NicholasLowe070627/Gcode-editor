from tkinter import *

class home_page():
    def __init__(self):
        self.root = Tk()
        self.root.title("G Code editor Home page")
        self.root.geometry("700x300")
        self.root.rowconfigure(0, weight = 1)
        self.root.rowconfigure(1, weight = 1)
        self.root.rowconfigure(2, weight = 1)
        self.root.columnconfigure(0, weight = 1)
        self.root.columnconfigure(1, weight = 1)
        
        self.title = Label(self.root, text = "G code editor for the roland SRM-20 CNC machine", font = "Arial 22")
        self.title.grid(row = 0, column= 0, columnspan= 2, sticky="news")
        
        self.subtitle = Label(self.root, text = "Which file would you like to edit", font = "Arial 20")
        self.subtitle.grid(row = 1, column= 0, columnspan= 2, sticky="news")
        
        self.trace_button = Button(self.root, text = "Trace File", bg = "#d9d9d9", font = "Arial 15", command = lambda: self.open_editor("trace"))
        self.trace_button.grid(row = 2, column= 0, sticky="news", padx = 60, pady= 40)
        
        self.drill_button = Button(self.root, text = "Drill File", bg = "#d9d9d9", font = "Arial 15", command = lambda: self.open_editor("drill"))
        self.drill_button.grid(row = 2, column=1, sticky="news", padx = 60, pady= 40)
    
    def open_editor(self, file_type):
        from trace_file_editor_V3 import trace_editor
        from drill_editor_v3 import drill_editor
        self.root.withdraw()
        if file_type == "trace":
            trace_editor() 
        elif file_type == "drill":
            drill_editor() 
        
        
    def run(self):
        self.root.mainloop()
       
if __name__ == "__main__":
    convert = home_page()
    convert.run()