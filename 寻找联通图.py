import collections
class day8_29_solve1:
    # dfs
    def canVisitAllRooms(self, rooms: list[list[int]]) -> bool:
        color = [0] * len(rooms)
        
        color[0] = 1
        def search(roomID:int):
            room = rooms[roomID]
            for key in room:
                if color[key] == 0:
                    color[key] = 1
                    search(key)
        
        search(0)
        return all(color)
    
class day8_29_solve2:
    def canVisitAllRooms(self, rooms: list[list[int]]) -> bool:
        vis = set()
        n = len(rooms)
        q = collections.deque([0])
        while q:
            x = q.popleft()
            vis.add(x)
            for key in rooms[x]:
                if key not in vis:
                    vis.add(key)
                    q.append(key)

        return len(vis) == n