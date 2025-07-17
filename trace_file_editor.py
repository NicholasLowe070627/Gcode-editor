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
        self.root.geometry("800x800")
        self.root.rowconfigure(0, weight = 1)
        self.root.columnconfigure(0, weight = 1)
        self.style = "Arial 30"
       
        self.container = Frame(self.root)
        self.container.grid(sticky="news", row = 0, column = 0)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        
        self.number_bar = Canvas(self.container, width = 50)
        self.number_bar.grid(row = 0, column= 0, sticky="news")


        self.code_bar = Canvas(self.container, width = 400)
        self.code_bar.grid(row = 0, column = 1, sticky="nsew")
       
        self.scroll = Scrollbar(self.container, orient=VERTICAL, command=self.scroll_both)
        self.scroll.grid(row=0, column=2, sticky="ns")
        self.code_bar.configure(yscrollcommand=self.scroll.set)
        self.number_bar.configure(yscrollcommand=self.scroll.set)


        self.open_button = Button(self.container, text="Open File", command=self.open_file)
        self.open_button.grid(row = 0, column = 3)
       
        
        
    def scroll_both(self, *args):
        self.code_bar.yview(*args)
        self.number_bar.yview(*args)
        
    def open_file(self):
        self.file_path = filedialog.askopenfilename(
            title = "Select a file  ",
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        )
        if self.file_path:
            with open(self.file_path, "r") as file:
                self.file_content = file.read()
       
        y = 10  # initial y position
        for line in self.file_content.splitlines():
            self.code_bar.create_text(10, y, anchor="nw", text=line, font="Arial 12")
            y += 20  # move to next line


        y = 10  # initial y position
        for i in range(len(self.file_content.splitlines())):
            self.number_bar.create_text(10, y, anchor="nw", text=str(i + 1), font="Arial 12")
            y += 20  # move to next line    
            self.number_bar.create_line(49, 0,  49, i, fill = "black")

        # Update scroll region
        self.number_bar.configure(scrollregion=self.number_bar.bbox("all"))
        self.code_bar.configure(scrollregion=self.code_bar.bbox("all"))
           
    def run(self):
        self.root.mainloop()
       
if __name__ == "__main__":
    convert = trace_editor()
    convert.run()

