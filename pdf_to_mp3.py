import pyttsx3,PyPDF2
from PyPDF2 import PdfReader

pdfreader = PdfReader("book.pdf") #You can also place "input("What is the path of the file with name.pdf ") in the name place so it would take file full path
page_num = len(pdfreader.pages)
engine = pyttsx3.init()
text = ""

for page_num in range(0, page_num):
    page = pdfreader.pages[page_num]
    text += page.extract_text((0, page_num)) + "\n"

print(text)  

engine.say(text)
engine.save_to_file(text, 'story.mp3')
engine.runAndWait()

engine.stop()
