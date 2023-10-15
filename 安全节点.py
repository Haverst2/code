# 有向图，无对外边的节点为终端节点，所有对外边最终仅指向终端节点的节点为安全节点（包括终端节点）
import collections
class day8_28_solve1:
    def __init__(self) -> None:
        self.graph = list[list[int]]()

    def deep_search(self):
        # i use 3 color to mark the node
        # 0: not visited
        # 1: visiting，and it's not safe
        # 2: visited，and it's safe
        color = [0] * len(self.graph)

        def dfs(node:int) -> bool:
            if color[node] > 0:
                return color[node] == 2
            color[node] = 1
            for x in self.graph[node]:
                if not dfs(x):
                    return False
            color[node] = 2
            return True
        
        return [i for i in range(len(self.graph)) if dfs(i)]


class day8_28_solve2:
    def __init__(self) -> None:
        self.graph = list[list[int]]()

    def topology(self) ->bool:
        # I hope to reverse the directed graph and use topology to solve the problem
        rg = [[] for _ in self.graph]
        for x,ys in enumerate(self.graph):
            for y in ys:
                rg[y].append(x)
        in_degrees = [len(ys) for ys in self.graph]

        q = collections.deque([i for i,d in enumerate(in_degrees) if d == 0])
        while q:
            y = q.popleft()
            for x in rg[y]:
                in_degrees[x] -= 1
                if in_degrees[x] == 0:
                    q.append(x)
        
        return [i for i,d in enumerate(in_degrees) if d == 0]
    

            

