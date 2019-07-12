from operator import itemgetter
import WebParser
import random


# Random Input Generator
def randInput():
    output = {}
    output['year'] = random.randrange(1960, 2000)  # 1960 ~ 1999
    output['month'] = random.randrange(1, 13)  # 1 ~ 12
    output['day'] = random.randrange(1, 30)  # 1 ~ 29
    output['time'] = random.randrange(0, 1440)  # 24시간 = 1440분
    output['lunar'] = random.randrange(0, 3)  # 양력/음력/윤달
    output['sex'] = random.randrange(0, 2)  # 남/여
    return output


def main():
    luckDict = {}

    for p in range(0, 1):
        personalData = randInput()
        # print(personalData)

        # 함수 리스트
        funcs = WebParser.parsingAll()
        for func in funcs:
            scripts = func(personalData)
            for script in scripts:
                for word in script.split(' '):
                    if word in luckDict:
                        luckDict[word] = luckDict[word] + 1
                    else:
                        luckDict[word] = 1

    luckList = list(luckDict.items())
    luckList = sorted(luckList, key=itemgetter(1), reverse=True)
    print(luckList)


if __name__ == "__main__":
    main()
