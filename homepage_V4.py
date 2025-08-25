"""
G code editor
By Nicholas Lowe
a G code editor that takes G code from flatcam and allows the user to change it to compatible g code for the roland CNC machine
version 4
linked to the home page so the user can navigate thoughout the entire system. 
has a confirmation to exit upon pressing close or the home button
validates inputs to ensure the user input will function the machine and only allows floats and strings to be enetered
"""
#imports nessicary libraies
from tkinter import *

#Creates the editor in a class so it can be oppened from another file as a window
class HomePage():
    def __init__(self):
        #Creates GUI
        self.root = Tk()
        self.root.title("G Code editor Home page")
        self.root.geometry("700x300")
        self.root.rowconfigure(0, weight = 1)
        self.root.rowconfigure(1, weight = 1)
        self.root.rowconfigure(2, weight = 1)
        self.root.columnconfigure(0, weight = 1)
        self.root.columnconfigure(1, weight = 1)
        
        self.title = Label(self.root, text = "G code editor for the roland SRM-20 CNC machine",
                           font = "Arial 22")
        self.title.grid(row = 0, column= 0, columnspan= 2, sticky="news")
        
        self.subtitle = Label(self.root, text = "Which file would you like to edit", font = "Arial 20")
        self.subtitle.grid(row = 1, column= 0, columnspan= 2, sticky="news")
        #buttons that allow the user to navigate to each of the editors
        self.trace_button = Button(self.root, text = "Trace File", bg = "#d9d9d9",
                                   font = "Arial 15", command = lambda: self.open_editor("trace"))
        self.trace_button.grid(row = 2, column= 0, sticky="news", padx = 60, pady= 40)
        self.drill_button = Button(self.root, text = "Drill File", bg = "#d9d9d9",
                                   font = "Arial 15", command = lambda: self.open_editor("drill"))
        self.drill_button.grid(row = 2, column=1, sticky="news", padx = 60, pady= 40)
    
    def open_editor(self, file_type):
        #function that opens each editor
        from trace_file_editor_V4 import TraceEditor
        from drill_editor_v4 import DrillEditor
        self.root.withdraw() #withdraw the root as the program ends when root is destoryed
        if file_type == "trace":#opens trace editor
            TraceEditor() 
        elif file_type == "drill":#opens drill editor
            DrillEditor() 
        
        
    def run(self):
        self.root.mainloop()
       
if __name__ == "__main__":
    convert = HomePage()
    convert.run()