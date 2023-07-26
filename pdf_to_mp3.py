import pyttsx3,PyPDF2
from PyPDF2 import PdfReader

pdfreader = PdfReader("book.pdf")
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