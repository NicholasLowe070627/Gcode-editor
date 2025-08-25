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
from tkinter import filedialog
from tkinter import messagebox

#Creates the editor in a class so it can be oppened from another file as a window
class drill_editor():
    def __init__(self, parent=None):
        #Creates GUI
        self.root = Toplevel(parent)
        self.root.title("drill file editor")
        self.root.geometry("800x800")
        self.root.rowconfigure(0, weight = 1)
        self.root.columnconfigure(0, weight = 1)
        self.style = "Arial 12"
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit) #when pressing close window calls the on exit function

        #makes a frame to hold all of the "sections"
        #adjusts the size and "priority" of each row and column
        self.container = Frame(self.root)
        self.container.grid(sticky="news", row = 0, column = 0)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(2, weight=17)
        self.container.columnconfigure(1, weight=3)
        self.container.columnconfigure(3, weight =2 )
        
        #Creates all of the sections in the frame
        self.title = Label(self.container, text = "Drill file editor", font = self.style)
        self.title.grid(row = 0, column= 1, columnspan = 4)
        self.spacer = Frame(self.container, bg = "black")
        self.spacer.grid(row =1 ,column=0, columnspan= 4, sticky= "news")
        self.number_bar = Canvas(self.container, width = 50)
        self.number_bar.grid(row = 2, column= 0, sticky="news")
        self.code_bar = Canvas(self.container, width = 300, bg = "white")
        self.code_bar.grid(row = 2, column = 1, sticky="nsew")
        self.scroll = Scrollbar(self.container, orient=VERTICAL, command=self.scroll_both)
        self.scroll.grid(row=2, column=2, sticky="ns")
       
        #sets the scroll bar and scroll wheel to scroll only the canvas and number bar
        self.code_bar.configure(yscrollcommand=self.scroll.set)
        self.number_bar.configure(yscrollcommand=self.scroll.set)
        self.code_bar.bind_all("<MouseWheel>", self.mouse_scroll)
        self.number_bar.bind_all("<MouseWheel>", self.mouse_scroll)

        #crates a sub frame to hold all of the buttons and entry boxes
        self.button_container = Frame(self.container)
        self.button_container.grid(row=2, column= 3, sticky="news")
        self.button_container.columnconfigure(0, weight= 1, pad = 10)
        self.button_container.columnconfigure(1, weight= 1, pad = 10)
       
        self.open_button = Button(self.button_container, text="Open File", command=self.open_file)
        self.open_button.grid(row = 0, column = 0, columnspan= 2)
       
        #a dictionary containing all the infomation for the entries and corrosponding button
        #the format of the dictionary, the key is used to create the entry and button attribute so it can be called eg self.retract
        #the first index is the text to be displayed on the button
        #the index position 2 is the command
        #the command calls the corrosponding function and passes in the entry value and the minimun, maximun and label and the "command"
        self.actions = {
           "retract": ["Set retraction height", lambda entry: self.has_feed("R", entry.get(), 2, 130.75, "Retraction height")],
           "RPM": ["Set Drill RPM", lambda entry: self.has_feed("S", entry.get(), 3000, 7000, "RPM")],
           "drill_depth": ["Set Drill Depth", lambda entry: self.has_feed("Z", entry.get(), -3,-1, "Drill Depth")],
            "drill_speed": ["Set Drill Speed", lambda entry: self.has_feed("F", entry.get(), 50, 250, "Drill Speed")],
        }
        #loops through the dictionary and creates each of the entries and buttons
        for line_no, (name, (text, command)) in enumerate(self.actions.items()):
            entry = Entry(self.button_container)
            entry.grid(row=line_no+1, column=0, sticky="news", padx=10, pady=5)
            #makes the entry something that can be called / infomation can be recived from it
            setattr(self, f"{name}_inp", entry)

            # Bind the command passing the current entry
            button = Button(
                self.button_container,
                text=text,
                #allows the command to be ran by taking in the entry as a variable and runs the command in the dictionary
                command=lambda e=entry, cmd=command: cmd(e)
            )
            button.grid(row=line_no+1, column=1, padx=10, pady=5, sticky="news")
            setattr(self, f"{name}_button", button)
 
        #Creates export button
        self.new_name = Label(self.button_container, text = "New file name", font = self.style)
        self.new_name.grid(row = 7, column= 0, sticky="news", padx=10, pady=5)
        self.new_name_inp = Entry(self.button_container)
        self.new_name_inp.grid(row= 8, column= 0, sticky="news", padx=10, pady=5)
        self.new_name_button = Button(self.button_container, text = "Export as new file", command = lambda: self.export(self.new_name_inp.get()))
        self.new_name_button.grid(row = 8, column= 1, sticky="news", padx=10, pady=5)
        #creates home button
        self.button_container.rowconfigure(9, weight=1)
        self.return_button = Button(self.button_container, text="Home", font=self.style, command=self.home, bg = "#FF6666")
        self.return_button.grid(row=10, column=1, sticky="se", padx=10, pady=10)     
        self.open_file()
        
    def home(self):
        #displays a message box to check if the uiser wants to return home
        if messagebox.askokcancel("Return to home page", "Are you sure you want to return home?"):    
            from homepage_V4 import home_page
            home_page()
            self.root.destroy()
        
    def on_exit(self):
        #asks the user are they sure they want to quit when the "X" button is clicked
        if messagebox.askokcancel("Quit", "Are you sure you want to exit?"):
            self.root.destroy()
       
    def mouse_scroll(self,event):
        #makes the canvas scroll by a consistant amount when the mouse wheel is scrolled
        if event.delta:
            self.code_bar.yview_scroll(int(-1 * (event.delta / 120)), "units")
            self.number_bar.yview_scroll(int(-1 * (event.delta / 120)), "units")
       
    def scroll_both(self, *args):
        #changes both the code bar and number bar when scrolling
        self.code_bar.yview(*args)
        self.number_bar.yview(*args)
       
    def open_file(self):
        #clares the canvases and asks the user to open a file
        self.code_bar.delete("all")
        self.number_bar.delete("all")
        #makes a file explore popup for the user to open the file      
        self.file_path = filedialog.askopenfilename(
            title = "Select a file  ",
            filetypes = [("All files", "*.*"),("Text files", "*.txt")]
        )
        #if a file is selected read the file and call the remove function
        if self.file_path:
            with open(self.file_path, "r") as file:
                self.file_content = file.read()
            self.lines = self.file_content.splitlines()
            self.remove()
        else:   #updates the canvas to show no file is open
            self.code_bar.create_text(5, 0, anchor = "nw", text = "No open file", font = "Arial 30")
       
    def display(self):   
        #displays/updates the lines of code 
        self.code_bar.delete("all")
        self.number_bar.delete("all")
        line_height = 20
        y = 0
        #writes each line of code from the list self.lines on a new line and numbers them
        for i, line in enumerate(self.lines):
            self.code_bar.create_text(5, y, anchor="nw", text=line, font="Arial 12")
            self.number_bar.create_text(5, y, anchor="nw", text=str(i + 1), font="Arial 12")
            y += line_height
        #Draw vertical separator line in number_bar
        self.number_bar.create_line(49, 0, 49, y, fill="black")

        # Update scroll region so scrollbars work correctly
        self.code_bar.configure(scrollregion=(0, 0, 400, y))
        self.number_bar.configure(scrollregion=(0, 0, 50, y))
   
    def remove(self):
        #removes all unnessicary lines from the file and rewrites in lines that are needed
        self.defult = ["G21", "G90", "G00 X0.0000 Y0.0000", "G01 Z0.0000 F254.00", "G00 Z2.5400"]
        remove_lines = ["G01", "G00 Z"]
        #loops though all lines and removes them untill the line M03
        for index, i in enumerate(self.lines):
            if i == "M03":
                self.lines = self.lines[index:]
                break
        #removes any lines starting with G01 F
        for index, i in enumerate(self.lines):
            if i[:5] == "G01 F":    
                self.lines[index] = ""
        #removes any lines in the remove lines list
        for index, i in enumerate(self.lines):
            if i.startswith(tuple(remove_lines)):
                self.lines[index] = ""
        #replaces the prefix for all lines that start with G00 to G82
        for index, i in enumerate(self.lines):
            if i.startswith("G00"):
                line_component = i.split()
                line_component[0] = "G82"
                self.lines[index] = " ".join(line_component)
        #writes in the lines in the defult list
        for i in self.defult[::-1]:
            self.lines.insert(0,i)
        #removes blank lines
        while "" in self.lines:
            self.lines.remove("")
        self.display()  
   
    def add(self, command, value, min, max, label):
        #function that adds the values
        #depending on  the given command asigns a index position as the position of each command matters
        if command == "R":
            command_index = 5
        elif command == "F":
            command_index = 4
        elif command == "Z":
            command_index = 3
            value = f"-{value}"
            
        checked_value = self.is_float(value, min, max, label)#calls the function to check if it is a valid input
        if checked_value is not None:
            for index, i in enumerate(self.lines):
                if i.startswith("G82") and command in ["R", "F", "Z"]: #for every line that starts with G82 add the corrosponding command and the value
                    words = i.split()
                    words.insert(command_index, f"{command}{checked_value}")
                    self.lines[index] = " ".join(words)
                    
                elif i.startswith("M03") and command not in ["R", "F", "Z"]: #for non M03 commands and the speed value
                    words = i.split()
                    words.insert(1, f"S{checked_value}")
                    self.lines[index] = " ".join(words)
            self.display()#calls the function to update canvas
        else:
            return None#as the checked value is returned as none if its invalid do nothing if this is true
        
    def has_feed(self, command, value, min, max, label):
        #removes exisiting commands if it is present
        if command in ["R", "F", "Z"]: #if the command is in the list set prefix to G82
            self.prefix = "G82"
        elif command == "S":#if command is S set prefix to M03
            self.prefix = "M03"
        for index, i in enumerate(self.lines):
            if i.startswith(self.prefix):
                words = i.split()    
                for index2, y in enumerate(words):#removes the commands starting with the command, does nothing if line dosent have the command
                    if y.startswith(command):
                        words.pop(index2)
                        self.lines[index] = " ".join(words)
        self.add(command, value, min, max, label)  #calls the add function to add new command
         
    def is_float(self, value, min, max, label):
        #validates the users inputs
        try:
            value = float(value)#ensures the input is a float and between the minimun and maximun values
            if value >= min and value <= max:
                value = round(value, 4)
                return value
            else:
                 #prints an error message if value is grater or less than min and max
                messagebox.showerror("Invalid Input", f"Invalid Input. {label} must be between {min} and {max}")
                return None
        except ValueError:
            #prints an error message if invalid input
            messagebox.showerror("Invalid Input", "Please enter a float")
            return None
        
    def export(self, default_name):
        #exports the file
        #opens file explorer short cut
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_name if default_name.endswith(".nc") else f"{default_name}.nc", #auto adds .nc to export as a nc file
            filetypes=[("All files", "*.*"),("Text files", "*.txt")])
        if file_path:#writes the lines to the file
            with open(file_path, "w") as file:
                file.write("\n".join(self.lines))
           
    def run(self):
        self.root.mainloop()
       
