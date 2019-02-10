import fitz, glob, os, smtplib, urllib.request
key_files = []

def main():
    pdf_list = glob.glob('/home/fabienne/Desktop/Python/PDF/*.pdf')
    text_list = glob.glob('/home/fabienne/Desktop/Python/Letters/*.txt')
    
    for pdf in pdf_list:
        try:
            pdf_converter(pdf)
        except:
            'This is not a relevant PDF. It might not be a PDF at all.'

    for text in text_list:
            keyword_search(text)

    # print(key_files)

    email = "you might want to take a look at the following {} files that contain the 'Hotel President' keyword:\n\n".format(len(key_files))

    for keyfile in key_files:
        filename = os.path.basename(keyfile)[:-4]
        row = "- {}\n".format(filename)
        email += row

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('fabienne.rosina.nicole@gmail.com', os.environ['dev_pass'])
    smtpObj.sendmail('fabienne.rosina.nicole@gmail.com', 'fmeijer@stanford.edu', 'Subject: Letters to City Council that mention Hotel President\nHi Fabienne, {}'.format(email))
    smtpObj.quit()

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

def keyword_search(text_path):
    #searches keyword and prints found/notfound
    filename = os.path.basename(text_path)[:-4]
    with open(text_path) as council_letters: 
        contents = council_letters.read()
        if 'Hotel President' in contents:
            key_files.append(text_path)
        else:
            print('Keyword not found in ' +filename)

if __name__ == '__main__':
    main()


    