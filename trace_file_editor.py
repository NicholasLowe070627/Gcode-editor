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


        self.code_bar = Canvas(self.container, width = 400, bg = "white")
        self.code_bar.grid(row = 0, column = 1, sticky="nsew")
       
        self.scroll = Scrollbar(self.container, orient=VERTICAL, command=self.scroll_both)
        self.scroll.grid(row=0, column=2, sticky="ns")
        self.code_bar.configure(yscrollcommand=self.scroll.set)
        self.number_bar.configure(yscrollcommand=self.scroll.set)


        self.open_button = Button(self.container, text="Open File", command=self.open_file)
        self.open_button.grid(row = 0, column = 3)
       
        self.code_bar.bind_all("<MouseWheel>", self.mouse_scroll)
        self.number_bar.bind_all("<MouseWheel>", self.mouse_scroll)
        
    def mouse_scroll(self,event):
        if event.delta:
            self.code_bar.yview_scroll(int(-1 * (event.delta / 120)), "units")
            self.number_bar.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def scroll_both(self, *args):
        self.code_bar.yview(*args)
        self.number_bar.yview(*args)
        
    def open_file(self):
        self.code_bar.delete("all")
        self.number_bar.delete("all")
                
        self.file_path = filedialog.askopenfilename(
            title = "Select a file  ",
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        )
        if self.file_path:
            with open(self.file_path, "r") as file:
                self.file_content = file.read()
       
        
        self.lines = self.file_content.splitlines()
        line_height = 20
        y = 0

        for i, line in enumerate(self.lines):
            # Draw code line
            self.code_bar.create_text(5, y, anchor="nw", text=line, font="Arial 12")

            # Draw corresponding line number
            self.number_bar.create_text(5, y, anchor="nw", text=str(i + 1), font="Arial 12")

            y += line_height

        # Draw vertical separator line in number_bar
        self.number_bar.create_line(49, 0, 49, y, fill="black")

        # Update scroll region so scrollbars work correctly
        self.code_bar.configure(scrollregion=(0, 0, 400, y))
        self.number_bar.configure(scrollregion=(0, 0, 50, y))
           
    def run(self):
        self.root.mainloop()
       
if __name__ == "__main__":
    convert = trace_editor()
    convert.run()

