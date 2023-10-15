# 图,目的为将图中节点分为若干组，每组中的节点互相连通，但不同组中的节点不连通
# 输入方式，将图中各个节点导入，再导入图中节点间关系
class day8_28:
    def __init__(self) -> None:
        # 字典，key为子节点，value为父节点
        self.father = {}
    
    def add(self,x):
        if x not in self.father:
            self.father[x] = None
        # 将节点作为key导入字典，value为None，表示该节点为根节点

    def find(self,x):
        if x not in self.father:
            self.add(x)
        if self.father[x] == None:
            return x
        root = x
        while self.father[root] != None:
            root = self.father[root]

        # 路径压缩
        while x != root:
            original_father = self.father[x]
            self.father[x] = root
            x = original_father
        
        return root
    
    def merge(self,x,y):
        if x not in self.father:
            self.add(x)
        if y not in self.father:
            self.add(y)
        
        root_x,root_y = self.find(x),self.find(y)

        if root_x != root_y:
            self.father[root_x] = root_y
        #使用此函数为了将x，y和为一组

    def is_connected(self,x,y):
        return self.find(x) == self.find(y)