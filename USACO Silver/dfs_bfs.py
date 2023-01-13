def dfs(startnode, list_of_nbrs):
    stk = [startnode]
    component = set()
    while stk:
        node = stk.pop()
        component.add(node)
        for i in list_of_nbrs[node]:
            if i not in component:
                stk.append(i)
    return component

def bfs(startnode, list_of_nbrs):
    stk = [startnode]
    component = set()
    while stk:
        node = stk.pop(0)
        component.add(node)
        for i in list_of_nbrs[node]:
            if i not in component:
                stk.append(i)
    return component
