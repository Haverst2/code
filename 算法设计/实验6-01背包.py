import time
import random
import heapq
import string
import numpy as np
import matplotlib.pyplot as plt

define = 1

class bag:
    def __init__(self,value:list,wight:list) -> None:
        self.object = [(value[i],wight[i],i) for i in range(len(value))]
        self.object.sort(key = lambda x:x[0]/x[1],reverse=True)

    def greedy(self,MaxWight):
        startTime = time.time()
        selected_object = []
        selectWight = 0
        for i in range(len(self.object)):
            if selectWight + self.object[i][1] <= MaxWight:
                selected_object.append(self.object[i])
                selectWight += self.object[i][1]
        endTime = time.time()
        TimeStamp = (endTime - startTime)*1000
        return selected_object,TimeStamp
    
    def backtrack(self,MaxWight):
        startTime = time.time()
        n = len(self.object)
        def recursion(i, current_weight, current_value,select_items):
            if i == n or current_weight == MaxWight:
                return current_value,select_items
            without_item = recursion(i+1,current_weight,current_value,select_items.copy())
            if current_weight + self.object[i][1] <= MaxWight:
                select_items[i] = 1
                with_item = recursion(i+1,current_weight + self.object[i][1],current_value + self.object[i][0],select_items.copy())
                if with_item[0] > without_item[0]:
                    return with_item
            return without_item
        select_items = [0] * n
        result = recursion(0,0,0,select_items)
        endTime = time.time()
        TimeStamp = (endTime - startTime)*1000
        return result,TimeStamp

def knapsack_branch_and_bound(values, weights, capacity):
    startTime = time.time()
    n = len(values)
    class Node:
        def __init__(self, level, profit, weight, include):
            self.level = level
            self.profit = profit
            self.weight = weight
            self.include = include
        def __lt__(self, other):
            return self.profit > other.profit  # 优先级队列按照利润降序排列
    max_profit = 0
    best_set = [0] * n
    current_set = [0] * n
    root = Node(-1, 0, 0, current_set)
    priority_queue = []
    heapq.heappush(priority_queue, root)
    while priority_queue:
        current_node = heapq.heappop(priority_queue)
        if current_node.level == n - 1:
            if current_node.profit > max_profit:
                max_profit = current_node.profit
                best_set = current_node.include
        else:
            next_level = current_node.level + 1
            without_item = Node(next_level, current_node.profit, current_node.weight, current_node.include.copy())
            heapq.heappush(priority_queue, without_item)
            if current_node.weight + weights[next_level] <= capacity:
                with_item = Node(next_level, current_node.profit + values[next_level],
                                 current_node.weight + weights[next_level],
                                 current_node.include.copy())
                with_item.include[next_level] = 1
                with_item_bound = bound(with_item, values, weights, capacity, n)
                if with_item_bound > max_profit:
                    heapq.heappush(priority_queue, with_item)
    endTime = time.time()
    TimeStamp = (endTime - startTime)*1000
    return max_profit, best_set,TimeStamp

def bound(node, values, weights, capacity, n):
    if node.weight >= capacity:
        return 0   
    bound_value = node.profit
    total_weight = node.weight
    level = node.level + 1
    while level < n and total_weight + weights[level] <= capacity:
        bound_value += values[level]
        total_weight += weights[level]
        level += 1
    if level < n:
        bound_value += (capacity - total_weight) * (values[level] / weights[level])
    return bound_value
        
if define:
    Drange = 1000
    Drend = 40
    Dsize = 100
    xname = 'data_size'
    yname = 'cost_time/ms'
    xlable = []
    y1,y2,y3 = [],[],[]
    for _ in range(5):
        value = [random.randint(1,Drange) for _ in range(Dsize)]
        weight = [random.randint(1,Drend) for _ in range(Dsize)]
        maxWight = Drend * 0.35 * Dsize
        test = bag(value,weight)
        selected,TimeStamp = test.greedy(maxWight)
        # max_value, t2 = test.backtrack(maxWight)
        # max_profit, best_set,t3 = knapsack_branch_and_bound(value, weight, maxWight)
        xlable.append(str(Dsize))
        y1.append(TimeStamp)
        # y2.append(t2)
        Dsize += 100
        # print(t3)
    width = 0.4
    x_pos = np.arange(len(xlable))
    plt.bar(x_pos - width/2,y1,width=0.4,label='greedy')
    # plt.bar(x_pos + width/2,y2,width=0.4,label='backtrack')
    for i,value in enumerate(y1):
        plt.text(i - width/2,value,f'{value:.5f}',ha='center',va = 'bottom')
    # for i,value in enumerate(y2):
    #     plt.text(i + width/2,value,f'{value:.5f}',ha='center',va = 'bottom')
    plt.xticks(x_pos,xlable)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.legend()
    plt.show()

