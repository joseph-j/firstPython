if __name__ == '__main__':
    f = open('dataSample.txt')
    i = 0
    sampleList = [0] * 1600
    avgList = sampleList
    for item in f:
        sampleList[i] = item
        i = i + 1
        #print(item)
    for j in range(2, 890):
        rollingAvg = 0
        for k in range(0, 100):
            rollingAvgNext = int(sampleList[j+k])
            #print(type(rollingAvgNext))
            if isinstance(rollingAvgNext, int):
                    print(j, " ", rollingAvgNext)
                    rollingAvg = rollingAvg + rollingAvgNext
        avgList[j] = rollingAvg / 100

    g = open('dataOutput.csv', 'w')
    for item in avgList:
        g.write("%s\n" % item)
    g.close()