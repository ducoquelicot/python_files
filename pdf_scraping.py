from bs4 import BeautifulSoup
import os

cmd = 'pdftohtml -c -s /home/fabienne/Desktop/Python/Files/pdfs_2019_37.pdf  /home/fabienne/Desktop/Python/html/pdfs_2019_37'
os.system(cmd)

soup = BeautifulSoup('file:///home/fabienne/Desktop/Python/html/pdfs_2019_37-html.html', 'lxml')
print(soup)