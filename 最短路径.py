# 颜色交替的最短路径

# 错误解法，为避免重复，应该判断是否重复搜索边而不是重复搜索节点
class Solution:
    def shortestAlternatingPaths(self, n: int, redEdges: list[list[int]], blueEdges: list[list[int]]) -> list[int]:
        rb = [{},{}]
        for x,y in redEdges:
            rb[0].setdefault(x,[]).append(y)
        for x,y in blueEdges:
            rb[1].setdefault(x,[]).append(y)
        step = [[-1,-1] for _ in range(n)] # step color
        step[0] = [0,0]
        def dps(color:int, node:int,deep:int):
            # color: 1: red, 0: blue
            deep += 1
            if node == 0:
                for item in rb[0].get(node,[]):
                    step[item][0] = 1
                    step[item][1] = 1
                    dps(1,item,deep)
                for item in rb[1].get(node,[]):
                    step[item][0] = 1
                    step[item][1] = 0
                    dps(0,item,deep)
            else:
                for item in rb[color].get(node,[]):
                    if step[item][1] == -1:
                        step[item][0] = deep
                        step[item][1] = 1 - color
                        dps(1-color,item,deep)
                    elif step[item][1] == 1 - color and item != 0:
                        dps(1-color,item,deep)
        dps(0,0,0)
        return [ x for x,y in step ]

if __name__ == "__main__":
    print(Solution().shortestAlternatingPaths(3,[[0,1],[0,2]],[[1,0]]))