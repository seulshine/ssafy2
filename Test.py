from WebParser import _crawl_unse
from WordCollector import randInput


def main():

    # info = randInput()
    info = '1974/12/11/15:00/양력/남'
    listUnse = _crawl_unse(info)
    print(listUnse)
    # for unse in listUnse:
    # print(listUnse.split('.'))


if __name__ == "__main__":
    main()