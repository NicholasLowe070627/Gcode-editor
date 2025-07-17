"""
G code editor
By Nicholas Lowe
a G code editor that takes G code from flatcam and allows the user to change it to compatible g code for the roland CNC machine
version 1
"""

from tkinter import *
from tkinter import filedialog

class trace_editor():
    def __init__(self):
        self.root = Tk()
        self.root.title("trace file editor")
        self.root.rowconfigure(0, weight = 1)
        self.root.columnconfigure(0, weight = 1)
        self.style = "Arial 30"
        
        self.container = Frame(self.root)
        self.container.grid(sticky="news", row = 0, column = 0)
        
        self.code_bar = Canvas(self.container)
        self.code_bar.grid(row = 0, column = 0, sticky="nsew")
        
        self.scroll = Scrollbar(self.container, orient=VERTICAL)
        self.scroll.grid(row = 0, column = 1, sticky="ns")
        self.code_bar.configure(yscrollcommand=self.scroll.set)
        
        self.open_button = Button(self.container, text="Open File", command=self.open_file)
        self.open_button.grid(row = 0, column = 2)
        
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
    def open_file(self):
        self.file_path = filedialog.askopenfilename(
            title = "Select a file  ",
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        )
        if self.file_path:
            with open(self.file_path, "r") as file:
                self.file_content = file.read()
        
        y = 10  # initial y position
        for line in self.file_content:
            self.code_bar.create_text(10, y, anchor="nw", text=line.strip(), font="Arial 12")
            y += 20  # move to next line

        # Update scroll region
        self.code_bar.configure(scrollregion=self.code_bar.bbox("all"))
            
    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    convert = trace_editor()
    convert.run()
