import os
import sys
sys.path.insert(0, os.getcwd()[:-6] + r'/Dependencies/')
import pdfkit
import tkinter as tk
from tkinter import font

class MainApplication():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('ARG101 v1.0')

        self.root.resizable(width=tk.FALSE, height=tk.FALSE)
        self.root.geometry('{}x{}'.format(600,500))

        self.defaultText = ["Full directory of programs", "Screenshots' directory, leave this empty if no screenshots!", 
                            "Full path of problem statement file.txt", "Assignment number", "Your Name", 
                            "Your Enrollment ID", "Set starting page number", "Output directory"]

        self.form_data = [tk.StringVar(self.root,value = self.defaultText[i]) for i in range(8)]

        # Building GUI
        # ============
        self.Label1 = tk.Label(self.root, text="Programs: ")
        self.Label1.grid(row=0)

        self.Entry1 = tk.Entry(self.root, textvariable = self.form_data[0])
        self.Entry1.grid(row=0, column=1,columnspan=4,sticky="ew",padx=10)

        self.Label2 = tk.Label(self.root, text="Screenshots:")
        self.Label2.grid(row=1)

        self.Entry2 = tk.Entry(self.root, textvariable = self.form_data[1])
        self.Entry2.grid(row=1, column=1,columnspan=4,sticky="ew",padx=10)

        self.Label3 = tk.Label(self.root, text="Problems.txt: ")
        self.Label3.grid(row=2)

        self.Entry3 = tk.Entry(self.root, textvariable = self.form_data[2])
        self.Entry3.grid(row=2, column=1, columnspan=4,sticky="ew",padx=10) 

        self.Label4 = tk.Label(self.root, text="Assignment #: ")
        self.Label4.grid(row=3)

        self.Entry4 = tk.Entry(self.root, textvariable = self.form_data[3])
        self.Entry4.grid(row=3, column=1, columnspan=4,sticky="ew",padx=10)

        self.Label5 = tk.Label(self.root, text="Name: ")
        self.Label5.grid(row=4)

        self.Entry5 = tk.Entry(self.root, textvariable = self.form_data[4])
        self.Entry5.grid(row=4, column=1, columnspan=4,sticky="ew",padx=10)

        self.Label6 = tk.Label(self.root, text="Enrollment ID: ")
        self.Label6.grid(row=5)

        self.Entry6 = tk.Entry(self.root, textvariable = self.form_data[5])
        self.Entry6.grid(row=5, column=1, columnspan=4,sticky="ew",padx=10)

        self.Label7 = tk.Label(self.root, text="Starting page number: ")
        self.Label7.grid(row=6)

        self.Entry7 = tk.Entry(self.root, textvariable = self.form_data[6])
        self.Entry7.grid(row=6, column=1, columnspan=4,sticky="ew",padx=10)

        self.Label8 = tk.Label(self.root, text="Output File directory: ")
        self.Label8.grid(row=7)

        self.Entry8 = tk.Entry(self.root, textvariable = self.form_data[7])
        self.Entry8.grid(row=7, column=1, columnspan=4,sticky="ew",padx=10)
        
        # Setting the Entry fields to acquire more columns 
        self.root.grid_columnconfigure(0, weight=2, uniform="foo")
        for i in range(1,5):
                self.root.grid_columnconfigure(i, weight=1, uniform="foo")

        self.Button1 = tk.Button(self.root, text="generate pdf", command = self.generatePDF)
        self.Button1.grid(row=9,column=1)
        
        self.Button2 = tk.Button(self.root, text="Reset Form", command = self.resetForm)
        self.Button2.grid(row=9,column=2)

        self.root.grid_rowconfigure(10,weight=1)
        temp = font.Font(family="Verdana",size=9,weight="bold")
        self.TextArea = tk.Text(self.root,font=temp,bg="black",fg="#00ff00")
        self.TextArea.grid(rowspan=3, column=0,columnspan=5,sticky="ew",padx=(40,40),pady=(5,0))
        self.TextArea.insert(tk.END,"hey now brown cow")
        self.TextArea.insert(tk.END,"\n1\n2\n3\n4\n5\n6\n7\n8\n9\n0\n1\n2\n3\n4\n5\n6")
        tk.Label(text="\n  \t\u00a9 github.com/sidb101 | 2016").grid(column=0,columnspan=4,sticky="ew")



    def generatePDF(self):
        # Involves 3 steps
        # 1. Validating the data
        try:
        	self.validateForm()
        except Exception as error:
        	self.TextArea.insert(tk.END, str(error))
        	self.TextArea.see(tk.END)
        	return

        # 2. Structuring the equivalent HTML and stylizing it to look like a real assignmnent
        
        # 3. Converting it to pdf using PDFkit

        config = pdfkit.configuration(wkhtmltopdf=os.getcwd()[:-6]+"/Dependencies/wkhtmltopdf")
        pdfkit.from_file('try3.html','out1.pdf',configuration=config)

    def validateForm(self):
        form_is_valid, ERROR_MSG = True, ''

        if not os.path.isdir(self.form_data[0].get()):
            ERROR_MSG += '\nInvalid Directory for programs'
            form_is_valid = False

        if not os.path.isdir(self.form_data[1].get()):
            if self.form_data[1].get()!='':
                ERROR_MSG += '\nInvalid Screenshots directory'
                form_is_valid = False
            else:
                self.form_data[1].set(self.form_data[0].get())

        if not os.path.exists(self.form_data[2].get()):
            ERROR_MSG += '\nInvalid path to Problem statement File'
            form_is_valid = False

        temp = self.form_data[7].get()
        if not os.path.isdir(temp):
            ERROR_MSG += '\nInvalid directory to output PDF'
            form_is_valid = False
        if not temp[-1]=='/':
            self.form_data[7].set(temp+"/")
        
        if os.path.exists(temp + "REPORT_ARG101.pdf"):
            ERROR_MSG += '\nREPORT_ARG101.pdf already exists'
            form_is_valid = False
            
        if not form_is_valid:
            raise Exception(ERROR_MSG)

    
    def resetForm(self):
        for x in range(8):
            self.form_data[x].set(self.defaultText[x])
        self.TextArea.delete(1.0,tk.END)
        thx_Msg = "Thanks for using ARG101, please report bugs at our git repository\n" + \
                  "=================================================================\n\n "
        self.TextArea.insert(tk.END,thx_Msg)
        self.TextArea.see(tk.END)

    

if __name__ == "__main__":
    app = MainApplication()
    app.root.mainloop()
