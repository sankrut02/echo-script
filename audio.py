import pdfplumber
import os
from gtts import gTTS


file = input("Enter the path of the PDF file: ")


if not os.path.exists(file):
    print("Error: File not found!")
    exit()


file_dest = input("Enter file name to be created with .mp3 extension: ")
dest_path = os.path.join("/Users/sankrut/Downloads", file_dest)


entire_text = ""
with pdfplumber.open(file) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            entire_text = entire_text + text + "\n"


audio =gTTS(text=entire_text, lang="en", slow=False)
audio.save(dest_path)

print(f"Audio file saved at {dest_path}")