import os
import sys
import tkinter
sys.path.insert(0, os.getcwd()[:-6] + r'/Dependencies/')
import pdfkit

def generatePDF():
    pdf_options = {'page-size': 'Letter'}
    config = pdfkit.configuration(wkhtmltopdf=os.getcwd()[:-6]+"Dependencies/wkhtmltox/bin/wkhtmltopdf")
    pdfkit.from_file('measure.html','out1.pdf',configuration=config,options=pdf_options)
generatePDF()