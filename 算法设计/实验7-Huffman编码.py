import time
import random
import string
import heapq
import binascii
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import deque

define = 1
try01 = 0   # code
try02 = 0   # tree

class node:
    def __init__(self) -> None:
        self.value = None
        self.child = []
    def __init__(self,value) -> None:
        self.value = None
        self.child = []
        if isinstance(value, tuple):
            for child in value:
                self.add_child(child)
        else:
            self.value = value
    def add_child(self, child_node):
        self.child.append(child_node)
    def __lt__(self, other):
        return len(self.child) < len(other.child)
    def __eq__(self, other):
        return len(self.child) == len(other.child)
        
    def pre_order_traversal(self):
        def order_traversal(node):
            if node:
                print(node.value)  # 访问当前节点
                for child in node.child:
                    order_traversal(child)
        order_traversal(self)
    def writeTree(self):
        # text = ''
        def order_traversal(node,text):
            text += '['
            # print(type(node.value))
            # text += str(node.value)
            if isinstance(node.value, str):
                text += '0'+''.join(chr(int(node.value, 2)))
            for child in reversed(node.child):
                text = order_traversal(child,text)
            text += ']'
            return text
        text = order_traversal(self,'')
        return text
    def printTree(self):
        # text = ''
        def order_traversal(node,text):
            text += '['
            # print(type(node.value))
            # text += str(node.value)
            if isinstance(node.value, str):
                print(node.value)
                text += '0'+''.join(chr(int(node.value, 2)))
            for child in node.child:
                text = order_traversal(child,text)
            text += ']'
            return text
        text = order_traversal(self,'')
        return text


class HuffmanCode:
    def __init__(self) -> None:
        self.freq = defaultdict(int)
        self.encode = ''
        self.huffman_tree = None
        self.binary_encoding = None
    
    def readFile(self,text:str):
        self.binary_encoding = text.encode('utf-8')
        for byte in self.binary_encoding:
            bit = ''.join(format(byte, '08b'))
            # print(bit)
            self.freq[bit] += 1
    
    def buildTree(self):
        priority_queue = [(freq, node(char)) for char,freq in self.freq.items()]
        heapq.heapify(priority_queue)
        while len(priority_queue) > 1:
            freq1, node1 = heapq.heappop(priority_queue)
            freq2, node2 = heapq.heappop(priority_queue)
            combined_freq = freq1 + freq2
            combined_node = node((node1,node2))
            heapq.heappush(priority_queue, (combined_freq, combined_node))
        self.huffman_tree = priority_queue[0][1]

    def buildCode(self):
        def recursion(node,code,value):
            if len(node.child) == 0:
                if node.value == value:
                    self.encode += code
                    return 1
                else :
                    return 0
            else:
                true = recursion(node.child[0],code+'0',value)
                if true == 0:
                    ture = recursion(node.child[1],code+'1',value)
                return true
        c = ''
        for byte in self.binary_encoding:
            bit = ''.join(format(byte, '08b'))
            c += bit
            recursion(self.huffman_tree,'',bit)
        if try01:
            print(c)
            pass
    
    def writeCode(self,text=''):
        i = 0
        # print(self.encode)
        # print(len(self.encode))
        while len(self.encode) % 8 != 0:
            self.encode += '0'
            i += 1
        a = [self.encode[i:i+8] for i in range(0,len(self.encode),8)]
        character = str(i) + ''.join([chr(int(byte, 2)) for byte in a])
        # print(character)
        with open(text+'code.txt', 'wb') as file:
            file.write(character.encode('utf-8'))
    
    def writeTree(self,text=''):
        with open(text+'tree.txt', 'w') as file:
            file.write(self.huffman_tree.writeTree())
        if try02:
            print('qqqqqq')
            print(self.huffman_tree.printTree())
            pass

    def test(self,text):
        self.readFile(text)
        self.buildTree()
        self.buildCode()
        # print(self.freq)
        self.writeCode()
        self.writeTree()
        

class HuffmanDecode:
    def __init__(self) -> None:
        self.decode = ''
        self.binary_dncoding = None
        self.huffman_tree = None
    
    def readCode(self,text=''):
        with open(text+'code.txt', 'rb') as file:
            code = file.read().decode('utf-8')
        i = int(code[0])
        binary_string = ''.join(format(ord(char), '08b') for char in code)
        if i == 0:
            self.binary_dncoding = binary_string[8:]
        else :
            self.binary_dncoding = binary_string[8:-i]
        # print(self.binary_dncoding)

    def readTree(self,text=''):
        with open(text+'tree.txt', 'r') as file:
            tree = file.read()
        stack1 = deque()
        stack2 = deque()
        last = 0
        now = 0
        i = 0
        while i < len(tree):
            if tree[i] == '[' :
                now += 1
            elif tree[i] == '0' :
                i += 1
                stack1.append(node(''.join(format(ord(tree[i]),'08b'))))
            elif tree[i] == ']' :
                last = now
                now -= 1
                stack2.append(last)
                if len(stack2) >= 2:
                    a = stack2.pop()
                    b = stack2.pop()
                    if a == b:
                        node1 = stack1.pop()
                        node2 = stack1.pop()
                        node3 = node((node1,node2))
                        stack1.append(node3)
                    else:
                        stack2.append(b)
                        stack2.append(a)
            i += 1
        self.huffman_tree = stack1.pop()
        if try02:
            print(self.huffman_tree.printTree())
            pass

    def Decode(self,title=''):
        node = self.huffman_tree
        for i in self.binary_dncoding:
            if i == '0':
                node = node.child[0]
            else:
                node = node.child[1]
            if len(node.child) == 0:
                self.decode += node.value
                node = self.huffman_tree
        if try01:
            print(self.decode)
            print(len(self.decode)%8)
            pass
        # Dtext = binascii.unhexlify(format(int(self.decode, 2), 'x'))
        Dtext = b''
        for i in range(0,len(self.decode),8):
            Dtext += int(self.decode[i:i+8],2).to_bytes(1,byteorder='big')
        text = Dtext.decode('utf-8')
        # print(Dtext.decode('utf-8'))
        with open(title+'decode.txt', 'w') as file:
            file.write(text)
                

# text = '啊this i.....s an example for huffman encoding'
if define:
    with open('a.txt', 'r') as file:
        text = file.read()
    huffman = HuffmanCode()
    huffman.test(text)
    q = HuffmanDecode()
    q.readTree()
    q.readCode()
    q.Decode()
    # print(''.join(format(ord('0'),'08b')))

