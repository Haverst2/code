import time
import random
import matplotlib.pyplot as plt

define = 1

xlable = []
y_quick = []
y_merge = []

class Sort:
    def __init__(self,data:list) -> None:
        self.data = data

    def MergeSort(self):
        startTime = time.time()
        def Merge(data:list):
            if len(data) <= 1 :
                return data
            mid = len(data)//2
            left = data[:mid]
            right = data[mid:]
            i,j = len(left),len(right)
            left = Merge(left)
            right = Merge(right)
            back = []
            i,j = 0,0 
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    back.append(left[i])
                    i += 1
                else:
                    back.append(right[j])
                    j += 1
            back.extend(left[i:])
            back.extend(right[j:])
            return back
        back = Merge(self.data)
        endTime = time.time()
        y_merge.append((endTime - startTime)*1000)
        print(f"Merge sort cost time is {(endTime-startTime)*1000:.6f}ms" )
        return back
    
    def QuickSort(self):
        startTime = time.time()
        data = self.data
        def Quick(data: list):
            if len(data) <= 1:
                return data

            pivot = data[0]  # 选择第一个元素作为基准点
            left = []
            right = []

            for element in data[1:]:
                if element <= pivot:
                    left.append(element)
                else:
                    right.append(element)

            left = Quick(left)
            right = Quick(right)

            return left + [pivot] + right
        back = Quick(data)
        endTime = time.time()
        y_quick.append((endTime - startTime)*1000)
        print(f"Quick sort cost time is {(endTime-startTime)*1000:.6f}ms" )
        return back 

        
def partition(arr, low, high):
    pivot = arr[high]  # 选择最后一个元素作为主元素
    i = low - 1  # 初始化较小元素的索引

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def linear_time_select(arr, low, high, k):
    if low == high:
        return arr[low]

    # 获取主元素的位置
    pivot_index = partition(arr, low, high)

    # 计算主元素在有序数组中的位置
    rank = pivot_index - low + 1

    if k == rank:
        return arr[pivot_index]
    elif k < rank:
        return linear_time_select(arr, low, pivot_index - 1, k)
    else:
        return linear_time_select(arr, pivot_index + 1, high, k - rank)
    
def qsort(q, l, r):
    x = q[(l + r) // 2]
    i, j = l - 1, r + 1
    while True:
        i += 1
        while q[i] < x:
            i += 1
        j -= 1
        while q[j] > x:
            j -= 1
        if i < j:
            q[i], q[j] = q[j], q[i]
        else:
            return i if i == j else j
        
def kth_smallest(q, l, r, k):
    index = qsort(q, l, r)
    if index == k - 1:
        return q[index]
    elif index > k - 1:
        return kth_smallest(q, l, index, k)
    else:
        return kth_smallest(q, index + 1, r, k)
    

if define:
    Drange = 30
    Dend = 10000
    xname = 'data_size'
    yname = 'cost_time/ms'
    for _ in range(5):
        data = [random.randint(1,Dend)for _ in range(Drange)]
        # print(data)
        # print(sorted(data))
        test = Sort(data)
        xlable.append(str(Drange))
        test.MergeSort()
        test.QuickSort()
        startTime = time.time()
        result = linear_time_select(data,0,len(data)-1,3)
        endTime = time.time()
        print(f"Linear time select cost time is {(endTime-startTime)*1000:.6f}ms" )
        # print(test.MergeSort())
        # print(test.QuickSort()) 
        Drange *= 10
    x_long = range(len(xlable))
    width = 0.5
    x2 = [i+width for i in x_long]
    plt.bar(x_long,y_quick,color = 'b',width=0.5,label='QuickSort')
    plt.bar(x2,y_merge,color = 'r',width=0.5,label='MergeSort')
    for i,value in enumerate(y_merge):
        plt.text(i,value,f'{value:.5f}',ha='left',va = 'bottom')
    for i,value in enumerate(y_quick):
        plt.text(i,value,f'{value:.5f}',ha='right',va = 'bottom')
    plt.xticks([i+width/2 for i in x_long],xlable)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.legend()
    plt.show()

        
