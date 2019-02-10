import glob, os, smtplib
key_files = []

def main():
    text_list = glob.glob('/home/fabienne/Desktop/Python/Letters/letters_pdfs_2019*.txt')

    for text in text_list:
        keyword = keyword_search(text)

    email = "you might want to take a look at the following {} files that contain the requested keyword {}:\n\n".format(len(key_files), keyword)

    for keyfile in key_files:
        filename = os.path.basename(keyfile)[:-4]
        row = "- {}\n".format(filename)
        email += row

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('fabienne.rosina.nicole@gmail.com', os.environ['dev_pass'])
    smtpObj.sendmail('fabienne.rosina.nicole@gmail.com', 'fmeijer@stanford.edu', 'Subject: {} Letters that mention {}\nHi Fabienne, {}'.format(len(key_files), keyword, email))
    smtpObj.quit()

def keyword_search(text_path):
    #searches keyword and prints found/notfound
    filename = os.path.basename(text_path)[:-4]
    with open(text_path) as council_letters: 
        contents = council_letters.read()
        keyword = 'President Hotel'
        if keyword in contents:
            key_files.append(text_path)
        else:
            print('Keyword not found in ' +filename)
    return keyword

if __name__ == '__main__':
    main()

