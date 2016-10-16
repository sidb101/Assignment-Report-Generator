import os
import sys
sys.path.insert(0, os.getcwd()[:-6] + r'/Dependencies/')
import pdfkit
from yattag import Doc
import tempfile
class Footer():
    def __init__(self, name, enroll):
        self.Name = name
        self.Enroll = enroll


class htmlGenerator():
    def __init__(self, formData):
        # formData is collected by MainApplication    
        self.programsDirectory	  = formData[0]
        self.screenshotsDirectory = formData[1]
        self.filePath			  = formData[2]
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
        with open("try44.html","w+") as ht:
            ht.write(main_html)

        
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as footer_html:
            self.pdf_options['footer-html'] = footer_html.name
            footer_html.write(self.processFooter().encode('utf-8'))

        config = pdfkit.configuration(wkhtmltopdf=os.getcwd()[:-6]+"/Dependencies/wkhtmltox/bin/wkhtmltopdf")
        pdfkit.from_string(main_html,'out.pdf',configuration=config, options=self.pdf_options)
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
        
if __name__=='__main__':
    testData = ['/home/siddharth/Desktop/BIS LAB/Programs',
    '/home/siddharth/Desktop/BIS LAB/Screenshots',
    '/home/siddharth/Desktop/BIS LAB/questions.txt',
    '1',
    'py',
    'Siddharth Bhatnagar',
    '0801IT141078',
    '/home/siddharth/Desktop/BIS LAB',
    '12']
    testObj = htmlGenerator(testData)
    testObj.processHTML()
