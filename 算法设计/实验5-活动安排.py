import time
import random
import string
import numpy as np
import matplotlib.pyplot as plt

define = 1

class plan:
    def __init__(self,start:list,end:list) -> None:
        self.activites = [(start[i],end[i],i) for i in range(len(start))]
        self.activites.sort(key=lambda x:x[1])

    def greedy(self):
        startTime = time.time()
        selected_activities = [self.activites[0]]
        last_activity = 0
        for i in range(1,len(self.activites)):
            if self.activites[i][0] >= self.activites[last_activity][1]:
                selected_activities.append(self.activites[i])
                last_activity = i
        endTime = time.time()
        TimeStamp = (endTime - startTime)*1000
        return [activity[2] for activity in selected_activities],TimeStamp
    
if define:
    Drange = 1000
    Drend = 40
    Dsize = 100
    xname = 'data_size'
    yname = 'cost_time/ms'
    y = []
    xlable = []
    for _ in range(6):
        start = [random.randint(0,Drange) for _ in range(Dsize)]
        end = [x + random.randint(0,Drend) for x in start]
        test = plan(start,end)
        selected,TimeStamp = test.greedy()
        xlable.append(str(Dsize))
        y.append(TimeStamp)
        Dsize += 100
        print(TimeStamp)
    x_pos = np.arange(len(xlable))
    plt.bar(x_pos,y,width=0.5)
    for i,value in enumerate(y):
        plt.text(i,value,f'{value:.5f}',ha='center',va = 'bottom')
    plt.xticks(x_pos,xlable)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.legend()
    plt.show()



    
    