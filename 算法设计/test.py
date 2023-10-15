import time
import random
import matplotlib.pyplot as plt
import numpy as np

define = 1
xlable = []
ylable = []
class find:
    def __init__( self,data:list ) :
        self.data = data

    def find( self,x ) :
        startTime = time.time()
        left, right = 0, len(self.data) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if self.data[mid] == x:
                endTime = time.time()
                print(f"{(endTime - startTime)*1000:.6f}ms\n")
                return mid  # Element found, return its index
            elif self.data[mid] < x:
                left = mid + 1  # Search in the right half
            else:
                right = mid - 1  # Search in the left half
        endTime = time.time()
        ylable.append((endTime - startTime)*1000)
        print(f"this time is not find the solution {(endTime-startTime)*1000:.6f}ms\n")
        return -1  # Element not found
    

if define:
    start,end = 0,100
    xname = 'data_size'
    yname = 'cost_time/ms'
    for item in range(4):
        data = range(start,end)
        xlable.append(str(end))
        Find = find(data)
        Find.find(random.randint(start,end))
        Find.find(end+1)
        end *= 10
    plt.bar(xlable,ylable,width=0.5)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.show()
    