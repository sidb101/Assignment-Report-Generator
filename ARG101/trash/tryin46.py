import os
import sys
sys.path.insert(0, os.getcwd()[:-6] + r'/Dependencies/')
import pdfkit
from tkinter import font
from tkinter import *
from tkinter import filedialog
from idlelib.WidgetRedirector import WidgetRedirector
from yattag import Doc
import tempfile

class Footer():
    def __init__(self, name, enroll):
        self.Name = name
        self.Enroll = enroll


class htmlGenerator():
    def __init__(self, formData):
        # formData is collected by MainApplication    
        self.programsDirectory    = formData[0]
        self.screenshotsDirectory = formData[1]
        self.filePath             = formData[2]
        self.assignmentNumber     = formData[3]
        self.programmingLanguage  = formData[4]
        self.studentName          = formData[5]
        self.enrollmentId         = formData[6]
        self.outputDirectory      = formData[7]
        self.startingPageNumber   = formData[8]

        self.pdf_options = {'page-size': 'Letter', 'margin-bottom':'0.50in','margin-top':'0.50in', 'margin-left':'0.50in', 'margin-right':'0.50in'}

    def processHTML(self):
        allProblems = self.recordProblemsFile()
        doc, tag, text = Doc().tagtext()
        numberOfProblems = len(allProblems)
        with tag('html'):
            with tag('head'):
                with tag('title'):
                    text('generated from ARG-101')
                with tag('style'):
                    doc.asis(
                        '''
                        body {
                            padding-top:40px;
                            text-align: justify;
                            max-width: 1600px;
                            word-wrap: break-word;
                            font-family: 'Times';
                            font-size: 18px;
                        }
                        h1 {
                            font-family: 'Times';
                            font-size: 27px;
                            font-weight: bold;
                            text-decoration: underline;
                            margin-top: 0px;
                            margin-bottom: 0px;
                            text-align: center;
                        }
                        p.question{
                            font-weight: bold;
                           text-align: left;
                        }
                        div.image {
                            margin-top: 18px;
                            max-height:100%;
                            max-width:100%;
                            height:72px;
                            margin-bottom: 18px;
                            align-content: left;
                        }

                        '''
                        )

            with tag('body'):
                with tag('h1'):
                    text("Assignment {}".format(self.assignmentNumber))
                doc.stag('br')
                problem_count, line_count = 0, 0
                for problemo in allProblems:
                    with tag('p', klass='question'):
                        text(problemo)
                        doc.stag('br')
                    program = self.recordProgramByPath("{}/{}.{}".format(self.programsDirectory,problem_count+1,self.programmingLanguage))
                    
                    for statement in program:
                        text(statement)
                        doc.stag('br')

                    with tag('div',klass="image"):
                        doc.stag('img', src="{}/{}.png".format(self.screenshotsDirectory,problem_count+1),style="height: 100%; width: 100%; object-fit: contain;")

        main_html = doc.getvalue()
        # with open("try44.html","w+") as ht:
        #     ht.write(main_html)

        
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as footer_html:
            self.pdf_options['footer-html'] = footer_html.name
            footer_html.write(self.processFooter().encode('utf-8'))

        config = pdfkit.configuration(wkhtmltopdf=os.getcwd()[:-6]+"/Dependencies/wkhtmltox/bin/wkhtmltopdf")
        pdfkit.from_string(main_html,'{}/out.pdf'.format(outputDirectory),configuration=config, options=self.pdf_options)
        os.remove(self.pdf_options['footer-html'])


    def processFooter(self):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('head'):
                with tag('title'):
                    text('footer html generates by ARG101')
                with tag('style'):
                    text('span{text-align: left;}')
            with tag('body'):
                doc.stag('hr')
                with tag('span'):
                    text("{} ({})".format(self.studentName,self.enrollmentId))
        return doc.getvalue()


    def recordProblemsFile(self):
        problems, recording = [], ""
        with open(self.filePath,"r") as openfileobject:
            for line in openfileobject:
                if '+-' in line:
                    problems.append(recording[:-1])
                    recording=""
                    pass
                else:
                    recording += line
        return problems

    def recordProgramByPath(self,path):
        recording = []
        with open(path,"r") as openfileobject:
            for line in openfileobject:
                recording.append(line) 
        return recording
        
class ReadOnlyText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.redirector = WidgetRedirector(self)
        self.insert = self.redirector.register("insert", lambda *args, **kw: "break")
        self.delete = self.redirector.register("delete", lambda *args, **kw: "break")

class MainApplication():

    def __init__(self):
        self.root=Tk()
        self.root.geometry('700x650')
        self.root.title('ARG-101 v1.0 release Sept 16, 2016')
        self.root.resizable(width=False, height=False)

        # form data
        self.en1Text, self.en2Text, self.en3Text, self.en7Text = StringVar(), StringVar(), StringVar(), StringVar()
        self.en4Text, self.en5Text, self.en6Text, self.en8Text = StringVar(), StringVar(), StringVar(), StringVar()
        self.en9Text, self.pl = StringVar(), StringVar()

        ## GUI
        ## ===
        Label(self.root, text = "Programs directory").grid(row=0,column=0,padx=10, pady=5)
        self.en1 =  Entry(self.root, width=40, textvariable=self.en1Text,state="disabled")
        self.en1.grid(row=0, column=1, pady=5, padx=5,sticky='we', columnspan=8)
        self.bt1 = Button(self.root,command=self.askdirectory1,text="...")
        self.bt1.grid(row=0,column=9,pady=2)

        Label(self.root, text = "Screenshots directory").grid(row=1,column=0,padx=10, pady=5)
        self.en2 =  Entry(self.root,width=40, textvariable=self.en2Text,state="disabled")
        self.en2.grid(row=1, column=1, pady=5, padx=5,sticky='we', columnspan=8)
        self.bt2 = Button(self.root,command=self.askdirectory2,text="...")
        self.bt2.grid(row=1,column=9,pady=2)

        Label(self.root, text = "Problems file").grid(row=2,column=0,padx=10, pady=10)
        self.en3 =  Entry(self.root,width=40, textvariable=self.en3Text,state="disabled")
        self.en3.grid(row=2, column=1, pady=5, padx=5,sticky='we', columnspan=8)
        self.bt3 = Button(self.root,command=self.askfile3,text="...")
        self.bt3.grid(row=2,column=9,pady=2)

        Label(self.root, text = "Assignment number").grid(row=3,column=0,padx=10, pady=5)
        self.en4 =  Entry(self.root,width=2, textvariable=self.en4Text)
        self.en4.grid(row=3, column=1, columnspan=1,pady=5, padx=5,sticky='we')

        Label(self.root, text="Language",width=10).grid(row=3,column=2,padx=10,pady=5,columnspan=1)
        
        Radiobutton(self.root,text="C/C++", var=self.pl,value="cpp").grid(row=3,column=4,padx=0,pady=5)
        Radiobutton(self.root,text="Java",  var=self.pl,value="java").grid(row=3,column=5,padx=0,pady=5)
        Radiobutton(self.root,text="Text",  var=self.pl,value="txt").grid(row=3,column=6,padx=0,pady=5)
        Radiobutton(self.root,text="Python",var=self.pl,value="py").grid(row=3,column=7,padx=0,pady=5)

        Label(self.root,text="Name").grid(row=4,column=0,padx=5,pady=5)
        self.en5 = Entry(self.root,width=4, textvariable=self.en5Text)
        self.en5.grid(row=4,column=1,pady=5,padx=5,sticky="we",columnspan=5)

        Label(self.root,text="Enrollment ID").grid(row=4,column=6,padx=5,pady=5)
        self.en6 = Entry(self.root,width=4, textvariable=self.en6Text)
        self.en6.grid(row=4,column=7,pady=5,padx=5,sticky="we",columnspan=3)

        Label(self.root,text = "Output folder").grid(row=5,column=0,padx=5,pady=5)
        self.en7 = Entry(self.root, textvariable=self.en7Text,state="disabled",bg="white",fg="black")
        self.en7.grid(row=5,column=1,columnspan=8,padx=5,pady=5,sticky="we")
        self.bt4 = Button(self.root,command=self.askdirectory7, text="...")
        self.bt4.grid(row=5,column=9)

        Label(self.root,text = "Starting page number").grid(row=6,column=0,padx=5,pady=5)
        self.en8 = Entry(self.root, textvariable=self.en8Text)#,width=4)
        self.en8.grid(row=6,column=1,columnspan=8,padx=5,pady=5,sticky="we")
        
        self.bt5 = Button(self.root,text="Generate pdf",width=10,fg="#000000",bg="#666666",command=self.generatePDF)
        self.bt5.grid(row=7,column=2,columnspan=1)

        self.bt6 = Button(self.root,text="Reset",width=10,fg="#000000",bg="#666666",command=self.formReset)
        self.bt6.grid(row=7,column=5,columnspan=1)

        temp = font.Font(family="Sans",size=10)
        self.TextArea = ReadOnlyText(self.root,font=temp,bg="white",fg="black",width=15,height=15,relief=RIDGE,
            borderwidth=5,padx=10,pady=10,spacing1=3)
        self.TextArea.grid(rowspan=3,column=0,padx=10,pady=10,columnspan=10,sticky="ew")
        self.TextArea.insert(END, "Preparing your report, please wait.\n")

        frame=Frame(bg="black",height=1)
        frame.grid(columnspan=10,padx=10,sticky="news",pady=10)

        Label(text="github.com/sidb101/Python-ARG101",width=20).grid(column=2,columnspan=4,sticky="ew",pady=0)  


    def generatePDF(self):
        # get Form
        try:
            Form = [str(self.en1Text.get()),
                    str(self.en2Text.get()),
                    str(self.en3Text.get()),
                    str(self.en4Text.get()),
                    str(self.pl.get()),
                    str(self.en5Text.get()),
                    str(self.en6Text.get()),
                    str(self.en7Text.get()),
                    str(self.en8Text.get())]
            # for x in Form:
            #     self.printLog(x)
            if not all(Form):
                raise Exception()
        except Exception:
            self.printLog("ERROR in form, one or more entries were invalid")

        # calling htmlGenerator
        html = htmlGenerator(Form)
        html.processHTML()

    def formReset(self):
        self.en1Text.set("")
        self.en2Text.set("")
        self.en3Text.set("")
        self.en4Text.set("")
        self.en5Text.set("")
        self.en6Text.set("")
        self.en7Text.set("")
        self.en8Text.set("")
        self.pl.set("py")
        self.printLog("\n\nImprove this project at github.com/sidb101/Python-ARG101")
        self.printLog("========================================================\n")
        self.printLog("All fields reloaded, fill again.\n")

    def setDirOptions(self,dialogTitle):
        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\' if os.name=='nt' else '/home/'
        options['mustexist'] = False
        options['parent'] = self.root
        options['title'] = dialogTitle

    def askdirectory1(self):
        self.setDirOptions("Select the directory containing programs")
        self.en1Text.set("{}".format(filedialog.askdirectory(**self.dir_opt)))

    def askdirectory2(self):
        self.setDirOptions("Select the directory containing screenshots")
        self.en2Text.set("{}".format(filedialog.askdirectory(**self.dir_opt)))

    def askfile3(self):
        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt')]
        options['initialdir'] = 'C:\\' if os.name=='nt' else '/home/'
        options['parent'] = self.root
        options['title'] = 'Select the .txt containing assignment problems'
        self.en3Text.set("{}".format(filedialog.askopenfilename(**self.file_opt)))

    def askdirectory7(self):
        self.setDirOptions("Select the directory for output PDF file")
        self.en7Text.set("{}".format(filedialog.askdirectory(**self.dir_opt)))

    def printLog(self,tx):
        self.TextArea.insert(END,"{}\n".format(tx))
        self.TextArea.see(END)
        #self.TextArea.configure(fg="yellow")
if __name__ == "__main__":  
    app = MainApplication()
    app.root.mainloop()
