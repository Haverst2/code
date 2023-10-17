import time
import random
import string
import numpy as np
import matplotlib.pyplot as plt

define = 1

class LongestCommonSubsequence:
    def __init__(self,x,y) -> None:
        self.X = x
        self.Y = y
    
    def longest_common_subsequence(self):
        m = len(self.X)
        n = len(self.Y)

        # 创建一个(m+1) x (n+1)的二维数组，用于存储中间结果
        dp = [[0] * (n+1) for _ in range(m+1)]

        startTime = time.time()
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.X[i - 1] == self.Y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        # 从dp表格中回溯以构造最长公共子序列
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if self.X[i - 1] == self.Y[j - 1]:
                lcs.append(self.X[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        # 最长公共子序列是逆序的，所以需要翻转
        lcs.reverse()
        endTime = time.time()
        TimeStamp = (endTime - startTime)*1000
        return dp[m][n],"".join(lcs),TimeStamp

    def longest_common_subsequence_recursion(self):
        startTime = time.time()
        def recursion(i,j):
            lec = []
            l = 0
            if i-1 >= 0 and j-1 >= 0:
                if self.X[i] == self.Y[j]:
                    l,k = recursion(i-1,j-1)
                    lec.extend(k)
                    lec.append(self.X[i])
                    l += 1
                else:
                    l1, k1 = recursion(i - 1, j)
                    l2, k2 = recursion(i, j - 1)
                    if l1 >= l2:
                        l, k = l1, k1
                    else:
                        l, k = l2, k2
                    lec.extend(k)
            elif i-1<0 and j-1<0:
                if self.X[i] == self.Y[i]:
                    lec.append(self.X[i])
                    l = 1
                else :
                    l = 0
            elif i-1<0 :
                if self.X[i] == self.Y[j]:
                    lec.append(self.X[i])
                    l += 1
                else:
                    l,k = recursion(i,j-1)
                    lec.extend(k)
            elif j-1<0 :
                if self.X[i] == self.Y[j]:
                    lec.append(self.X[i])
                    l += 1
                else:
                    l,k = recursion(i-1,j)
                    lec.extend(k)
            return l,lec
        l,k = recursion(len(self.X)-1,len(self.Y)-1)
        endTime = time.time()
        TimeStamp = (endTime - startTime)*1000
        return l,"".join(k),TimeStamp

    def longest_common_subsequence_memorandum(self):
        startTime = time.time()
        mem = [[-1] * (len(self.Y)) for _ in range(len(self.X))]
        def recursion(i,j):
            if mem[i][j] != -1:
                return mem[i][j]
            l = 0
            if i-1 >= 0 and j-1 >= 0:
                if self.X[i] == self.Y[j]:
                    l = recursion(i-1,j-1)
                    l += 1
                else:
                    l = max(recursion(i-1,j),recursion(i,j-1))
            elif i-1<0 and j-1<0:
                if self.X[i] == self.Y[i]:
                    l = 1
                else :
                    l = 0
            elif i-1<0 :
                if self.X[i] == self.Y[j]:
                    l += 1
                else:
                    l = recursion(i,j-1)
            elif j-1<0 :
                if self.X[i] == self.Y[j]:
                    l += 1
                else:
                    l = recursion(i-1,j)
            mem[i][j]=l
            return l
        l = recursion(len(self.X)-1,len(self.Y)-1)
        lcs = []
        i, j = len(self.X)-1, len(self.Y)-1
        while i >= 0 and j >= 0:
            if X[i] == Y[j]:
                lcs.append(X[i])
                i -= 1
                j -= 1
            elif mem[i - 1][j] > mem[i][j - 1]:
                i -= 1
            else:
                j -= 1
        lcs.reverse()
        endTime = time.time()
        TimeStamp = (endTime - startTime)*1000
        return l,"".join(lcs),TimeStamp
        

def generate_random_uppercase_string(length):
    letters = "ABCDEFGH"  # 获取大写英文字母
    result = ''.join(random.choice(letters) for _ in range(length))
    return result

if define:
    xname = 'data_size'
    yname = 'cost_time/ms'
    Dgrade = 5
    UPgrade = 10
    y1,y2,y3 = [],[],[]
    xlable = []
    for _ in range(5):
        X = generate_random_uppercase_string(random.randint(Dgrade,UPgrade))
        Y = generate_random_uppercase_string(random.randint(Dgrade,UPgrade))
        test = LongestCommonSubsequence(X,Y)
        l1,k1,t1 = test.longest_common_subsequence()
        l2,k2,t2 = test.longest_common_subsequence_recursion()
        # l3,k3,t3 = test.longest_common_subsequence_memorandum()
        # print(l1)
        # print(k1)
        # print(t1,t2,t3)
        y1.append(t1)
        y2.append(t2)
        # y3.append(t3)
        xlable.append([Dgrade,UPgrade])
        Dgrade+=1;UPgrade+=1
    width = 0.4
    x_pos = np.arange(len(xlable))
    plt.bar(x_pos - width/2,y1,width=0.4,label='dynamic programming')
    plt.bar(x_pos + width/2,y2,width=0.2,label='recursion')
    # plt.bar(x_pos + width/2,y3,width=0.4,label='memorandum')
    for i,value in enumerate(y1):
        plt.text(i - width/2,value,f'{value:.5f}',ha='center',va = 'bottom')
    for i,value in enumerate(y2):
        plt.text(i + width/2,value,f'{value:.5f}',ha='center',va = 'bottom')
    # for i,value in enumerate(y3):
    #     plt.text(i + width/2,value,f'{value:.5f}',ha='center',va = 'bottom')
    plt.xticks(x_pos,xlable)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.legend()
    plt.show()


