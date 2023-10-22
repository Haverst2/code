import time
import random
import numpy as np
import matplotlib.pyplot as plt

define = 1

class MatrixConcatenation:
    def __init__(self,data:list) -> None:
        self.data = data 
    def matrix_chain_order(self):
        startTime = time.time()
        n = len(self.data) - 1
        m = [[0] * (n + 1) for _ in range(n + 1)]
        s = [[0] * (n + 1) for _ in range(n + 1)]

        for length in range(2, n + 1):
            for i in range(1, n - length + 2):
                j = i + length - 1
                m[i][j] = float('inf')
                for k in range(i, j):
                    cost = m[i][k] + m[k + 1][j] + self.data[i - 1] * self.data[k] * self.data[j]
                    if cost < m[i][j]:
                        m[i][j] = cost
                        s[i][j] = k
        endTime = time.time()
        TimeStamp = endTime - startTime
        mincost = m[1][len(self.data)-1]
        return mincost, s,TimeStamp

    def matrix_chain_order_recursion(self):
        startTime = time.time()
        s = [[0] * (len(self.data)) for _ in range(len(self.data))]
        def recursion(l,r):
            if r-l < 1:
                return 0
            mincost = float('inf')
            for k in range(l,r):
                cost = recursion(l,k) + recursion(k+1,r) + self.data[l-1] * self.data[k] * self.data[r]
                if cost < mincost:
                    mincost = cost
                    s[l][r] = k
            return mincost
        c = recursion(1,len(self.data)-1)
        endTime = time.time()
        TimeStamp = endTime - startTime
        return c,s,TimeStamp
    
    def matrix_chain_order_memorandum(self):
        memory = {}
        startTime = time.time()
        s = [[0] * (len(self.data)) for _ in range(len(self.data))]
        def recursion(l,r):
            if r-l < 1:
                return 0
            if (l,r) in memory:
                return memory[(l,r)]
            
            mincost = float('inf')
            for k in range(l,r):
                cost = recursion(l,k) + recursion(k+1,r) + self.data[l-1] * self.data[k] * self.data[r]
                if cost < mincost:
                    mincost = cost
                    s[l][r] = k
            memory[(l,r)] = mincost
            return mincost
        c = recursion(1,len(self.data)-1)
        endTime = time.time()
        TimeStamp = endTime - startTime
        return c,s,TimeStamp

def print_optimal_parens(s, i, j):
    if i == j:
        print("A" + str(i), end="")
    else:
        print("(", end="")
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j] + 1, j)
        print(")", end="")   
    

if define:
    Drange = 10
    Dend = 10000
    xname = 'data_size'
    yname = 'cost_time/ms'
    y1,y2,y3 = [],[],[]
    xlable = []
    for _ in range(4):
        data = [random.randint(1,Dend)for _ in range(Drange)]
        A = MatrixConcatenation(data)
        xlable.append(str(Drange))
        c1,s1,t1= A.matrix_chain_order()
        c2,s2,t2 = A.matrix_chain_order_recursion()
        c3,s3,t3 = A.matrix_chain_order_memorandum()
        # print_optimal_parens(s1,1,len(data)-1);print('\n')
        # print_optimal_parens(s2,1,len(data)-1);print('\n')
        # print_optimal_parens(s3,1,len(data)-1);print('\n')
        # print(f'{t1:.5},{t2:.5},{t3:.5}')
        y1.append(t1*1000)
        y2.append(t2*1000)
        y3.append(t3*1000)
        Drange += 2
    width = 0.4
    x_pos = np.arange(len(xlable))
    plt.bar(x_pos - width/2,y1,width=0.4,label='dynamic programming')
    plt.bar(x_pos + width/2,y2,width=0.2,label='recursion')
    # plt.bar(x_pos + width/2,y3,width=0.4,label='memorandum')
    for i,value in enumerate(y1):
        plt.text(i - width/2,value,f'{value:.5f}',ha='center',va = 'bottom')
    for i,value in enumerate(y2):
        plt.text(i,value,f'{value:.5f}',ha='left',va = 'bottom')
    # for i,value in enumerate(y3):
    #     plt.text(i + width/2,value,f'{value:.5f}',ha='center',va = 'bottom')
    plt.xticks(x_pos,xlable)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.title('dynamic programming compare recursion')
    plt.legend()
    plt.show()
