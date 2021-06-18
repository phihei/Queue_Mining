import random
import datetime


def main():
    f2 = open("delayPredictionTestCreationTemplateLog.xes", "r")
    f = open("delayPrediction-example1.xes", "w+")
    for i in range(15):
        f.write(f2.readline())
    customers = list()
    s1 = -1
    s2 = -1
    currentQueueLength = -1
    for i in range(7200):
        if random.randint(0, 99) == 0:
            customers.append([i])
        if s1 == 0:
            pass
        if s2 == 0:
            pass
        if s1 == -1 and currentQueueLength + 1 < len(customers):
            s1 = 300
            currentQueueLength = currentQueueLength + 1
            customers[currentQueueLength].append(i)
            if i < 6900:
                customers[currentQueueLength].append(i + 300)
        if s2 == -1 and currentQueueLength + 1 < len(customers):
            s2 = 300
            currentQueueLength = currentQueueLength + 1
            customers[currentQueueLength].append(i)
            if i < 6900:
                customers[currentQueueLength].append(i + 300)
        s1, s2 = max(-1, s1 - 1), max(-1, s2 - 1)
    j = 1
    for Customer in customers:
        f.write('\t<trace>\n\t\t<string key="concept:name" value="' + str(j) + '"/>\n')
        j = j + 1
        i = 0
        for event in Customer:
            f.write('\t\t<event>\n')
            if i == 0:
                f.write('\t\t\t<string key="concept:name" value="EnterQueue"/>\n')
            elif i == 1:
                f.write('\t\t\t<string key="concept:name" value="ServiceStart"/>\n')
            elif i == 2:
                f.write('\t\t\t<string key="concept:name" value="ServiceEnd"/>\n')

            i = i + 1

            time = datetime.datetime(2021, 6, 18, 8)
            time = time + datetime.timedelta(seconds=event)
            f.write('\t\t\t<date key="time:timestamp" value="' + str(time) + '"/>\n\t\t</event>\n')
        f.write('\t</trace>\n')
    f.write(f2.readline())
    f.flush()
    f.close()


if __name__ == '__main__':
    main()
