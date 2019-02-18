import fda, opencalais, os, report

def main():
    try:
        os.makedirs(os.path.expanduser('~/Desktop/Python/Files'))
    except FileExistsError:
        print('This folder already exists.')
    fda.main()
    opencalais.main()
    report.main()

if __name__ == '__main__':
    main()