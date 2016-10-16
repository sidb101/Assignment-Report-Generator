import os
import sys
sys.path.insert(0, os.getcwd()[:-6] + r'/Dependencies/')
import pdfkit
config = pdfkit.configuration(wkhtmltopdf=os.getcwd()[:-6]+"/Dependencies/wkhtmltopdf")
pdfkit.from_file('try3.html','out1.pdf',configuration=config)
