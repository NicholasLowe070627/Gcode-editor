"""
G code editor
By Nicholas Lowe
a G code editor that takes G code from flatcam and allows the user to change it to compatible g code for the roland CNC machine
version 1
only edits the drill file and has no validation
"""

from tkinter import *
from tkinter import filedialog

class drill_editor():
    def __init__(self, parent=None):
        self.root = Toplevel(parent)
        self.root.title("drill file editor")
        self.root.geometry("800x800")
        self.root.rowconfigure(0, weight = 1)
        self.root.columnconfigure(0, weight = 1)
        self.style = "Arial 12"
       
        self.container = Frame(self.root)
        self.container.grid(sticky="news", row = 0, column = 0)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(2, weight=17)
        self.container.columnconfigure(1, weight=3)
        self.container.columnconfigure(3, weight =2 )
       
        self.title = Label(self.container, text = "Trace file editor", font = self.style)
        self.title.grid(row = 0, column= 1, columnspan = 4)

        self.spacer = Frame(self.container, bg = "black")
        self.spacer.grid(row =1 ,column=0, columnspan= 4, sticky= "news")
       
        self.number_bar = Canvas(self.container, width = 50)
        self.number_bar.grid(row = 2, column= 0, sticky="news")
       
        self.code_bar = Canvas(self.container, width = 300, bg = "white")
        self.code_bar.grid(row = 2, column = 1, sticky="nsew")
       
        self.scroll = Scrollbar(self.container, orient=VERTICAL, command=self.scroll_both)
        self.scroll.grid(row=2, column=2, sticky="ns")
       
        self.code_bar.configure(yscrollcommand=self.scroll.set)
        self.number_bar.configure(yscrollcommand=self.scroll.set)
        self.code_bar.bind_all("<MouseWheel>", self.mouse_scroll)
        self.number_bar.bind_all("<MouseWheel>", self.mouse_scroll)

        self.button_container = Frame(self.container)
        self.button_container.grid(row=2, column= 3, sticky="news")
        self.button_container.columnconfigure(0, weight= 1, pad = 10)
        self.button_container.columnconfigure(1, weight= 1, pad = 10)
       
        self.open_button = Button(self.button_container, text="Open File", command=self.open_file)
        self.open_button.grid(row = 0, column = 0, columnspan= 2)
       
        self.redundant = Button(self.button_container, text = "remove redundant code", command=self.remove)
        self.redundant.grid(row = 1, column= 1, sticky="news", padx=10, pady=5)
       
        self.retract_inp = Entry(self.button_container)
        self.retract_inp.grid(row= 2, column= 0, sticky="news", padx=10, pady=5)
        self.retract_button = Button(self.button_container, text = "set retraction height", command = lambda: self.has_feed("R" ,self.retract_inp.get()))
        self.retract_button.grid(row = 2, column= 1, sticky="news", padx=10, pady=5)
       
        self.RPM_inp = Entry(self.button_container)
        self.RPM_inp.grid(row= 4, column= 0, sticky="news", padx=10, pady=5)
        self.RPM_button = Button(self.button_container, text = "set Drill RPM", command = lambda: self.add("M03", self.RPM_inp.get()))
        self.RPM_button.grid(row = 4, column= 1, sticky="news", padx=10, pady=5)
       
        self.drill_deph_inp = Entry(self.button_container)
        self.drill_deph_inp.grid(row= 4, column= 0, sticky="news", padx=10, pady=5)
        self.drill_deph_button = Button(self.button_container, text = "set Drill deph", command = lambda: self.has_feed("Z", f"-{self.drill_deph_inp.get()}"))
        self.drill_deph_button.grid(row = 4, column= 1, sticky="news", padx=10, pady=5)
       
        self.drill_speed_inp = Entry(self.button_container)
        self.drill_speed_inp.grid(row= 5, column= 0, sticky="news", padx=10, pady=5)
        self.drill_speed_button = Button(self.button_container, text = "set drill speed", command= lambda: self.has_feed("F",self.drill_speed_inp.get()))
        self.drill_speed_button.grid(row = 5, column= 1, sticky="news", padx=10, pady=5)

        self.new_name = Label(self.button_container, text = "New file name", font = self.style)
        self.new_name.grid(row = 7, column= 0, sticky="news", padx=10, pady=5)
        self.new_name_inp = Entry(self.button_container)
        self.new_name_inp.grid(row= 8, column= 0, sticky="news", padx=10, pady=5)
        self.new_name_button = Button(self.button_container, text = "Export as new file", command = lambda: self.export(self.new_name_inp.get()))
        self.new_name_button.grid(row = 8, column= 1, sticky="news", padx=10, pady=5)
       
       
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
        self.display()
       
    def display(self):    
        self.code_bar.delete("all")
        self.number_bar.delete("all")
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
   
    def remove(self):
        self.defult = ["G21", "G90", "G00 X0.0000 Y0.0000", "G01 Z0.0000 F254.00", "G00 Z2.5400"]
        remove_lines = ["G01", "G00 Z"]
        for index, i in enumerate(self.lines):
            if i == "M03":
                self.lines = self.lines[index:]
                break
           
        for index, i in enumerate(self.lines):
            if i[:5] == "G01 F":    
                self.lines[index] = ""

        for index, i in enumerate(self.lines):
            if i.startswith(tuple(remove_lines)):
                self.lines[index] = ""
       
        for index, i in enumerate(self.lines):
            if i.startswith("G00"):
                line_component = i.split()
                line_component[0] = "G82"
                self.lines[index] = " ".join(line_component)
               
        for i in self.defult[::-1]:
            self.lines.insert(0,i)
           
        while "" in self.lines:
            self.lines.remove("")
        self.display()  
   
    def add(self, command, value):
        if command == "R":
            command_index = 5
        elif command == "F":
            command_index = 4
        elif command == "Z":
            command_index = 3
       
        for index, i in enumerate(self.lines):
            if i.startswith("G82"):
                words = i.split()
                words.insert(command_index, f"{command}{value}")
                self.lines[index] = " ".join(words)
        self.display()
        
    def has_feed(self, command, value):
        self.prefix = "G82"
        for index, i in enumerate(self.lines):
            if i.startswith(self.prefix):
                words = i.split()    
                for index2, y in enumerate(words):
                    if y.startswith(command):
                        words.pop(index2)
                        self.lines[index] = " ".join(words)


        self.add(command, value)  
         
    def export(self, default_name):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_name if default_name.endswith(".txt") else f"{default_name}.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write("\n".join(self.lines))
           
    def run(self):
        self.root.mainloop()
       
if __name__ == "__main__":
    convert = drill_editor()
    convert.run()