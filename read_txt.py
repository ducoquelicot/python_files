import glob, os, smtplib
key_files = []

def main():
    text_list = glob.glob('/home/fabienne/Desktop/Python/Letters/*.txt')

    for text in text_list:
        keyword_search(text)

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

