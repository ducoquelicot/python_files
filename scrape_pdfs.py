import fitz, glob, os, smtplib, urllib.request

def main():
    # pdf_list_2018 = glob.glob('/home/fabienne/Desktop/Python/PDF/pdfs_2018*.pdf')
    pdf_list_2019 = glob.glob('/home/fabienne/Desktop/Python/PDF/pdfs_2019*.pdf')
    
    for pdf in pdf_list_2019:
        pdf_converter(pdf)

    # for pdf in pdf_list_2018:
    #     pdf_converter2(pdf)

def pdf_converter(pdf_path):
    #creates basename pdf
    agenda = fitz.open(pdf_path) 
    filename = os.path.basename(pdf_path)[:-4]

    #gets lastpage and extracts links
    lastpage = agenda[range(len(agenda))[-1]]
    links = lastpage.getLinks()

    #gets links to letters
    letters = []

    for row in links:
        letters.append(row['uri'])

    #downloads links and turns pdf into text file
    for row in range(len(letters))[-2:]:
        try:
            urllib.request.urlretrieve(letters[row], os.path.expanduser('~/Desktop/Python/Letters/letters_' +filename +'_' +str(row) + '.pdf')) 
            lettertotext = 'pdftotext -layout ~/Desktop/Python/Letters/letters_' +filename +'_' +str(row) + '.pdf' 
            os.system(lettertotext)
        except:
            print('This is not a Letter to City Council')
            continue

# def pdf_converter2(pdf_path):
#     #creates basename pdf
#     agenda = fitz.open(pdf_path) 
#     filename = os.path.basename(pdf_path)[:-4]

#     #gets lastpage and extracts links
#     lastpage = agenda[range(len(agenda))[-1]]
#     links = lastpage.getLinks()

#     #gets links to letters
#     letters = []

#     for row in links:
#         letters.append(row['uri'])

#     #downloads links and turns pdf into text file
#     for row in range(len(letters))[-3:]:
#         try:
#             urllib.request.urlretrieve(letters[row], os.path.expanduser('~/Desktop/Python/Letters/letters_' +filename +'_' +str(row) + '.pdf')) 
#             lettertotext = 'pdftotext -layout ~/Desktop/Python/Letters/letters_' +filename +'_' +str(row) + '.pdf' 
#             os.system(lettertotext)
#         except:
#             print('This is not a Letter to City Council')
#             continue

if __name__ == '__main__':
    main()