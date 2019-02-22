import fda, opencalais, os, report

def main():
    os.makedirs(os.path.expanduser('~/Desktop/Python/Files'), exist_ok=True)
    fda.main()
    opencalais.main()
    report.main()

if __name__ == '__main__':
    main()