from collections import deque
import networkx as nx 
import matplotlib.pyplot as plt

graph = {
    'MIT/X11': ['2-BSD', '3-BSD'],
    'ZPL v2.0': ['Apache v2.0'],
    'Zlib/libpng': ['Apache v2.0'],
    '2-BSD': ['3-BSD'],
    '3-BSD': ['EPL v1.0','EPL v2.0',"MPL v1.1","MPL v2.0"],
    'Mulan PSL v2': ['Apache v2.0'],
    "Apache v2.0":["LGPL v3 or LGPL v3+"],
    "EPL v1.0":[],
    "EPL v2.0":[],
    "MPL v1.1":[],
    "MPL v2.0":["LGPL v2.1+"],
    "LGPL v2.1":["GPL v2"],
    "LGPL v2.1+":["LGPL v2.1","LGPL v3 or LGPL v3+"],
    "LGPL v3 or LGPL v3+":["GPL v3 or GPL v3+","Mulan PubL v2"],
    "GPL v2":[],
    "GPL v2.1+":["GPL v3 or GPL v3+"],
    "GPL v3 or GPL v3+":["AGPL v3 or AGPL v3+"],
    "Mulan PubL v2":["AGPL v3 or AGPL v3+"],
    "AGPL v1.0+":["AGPL v3 or AGPL v3+"],
    "AGPL v3 or AGPL v3+":[]
}


def find_path(graph, start, end, path=[]):
    path = path + [start]  # 路径，每一次递归调用时，把当前结点加入已经访问的集合中去
    # print("path:%s" % path)
    if start == end:
        return path
    if start not in graph:  # 仅存在此节点 不作为弧头出现，仅作为弧尾[数据结构唐朔飞]
        return None  # 递归结束的条件
    # print("graph[{}]:{}".format(start, graph[start]))
    for node in graph[start]:  # 依次访问start的邻接顶点node
        if node not in path:  # 同一节点在返回的路径上不会出现多次
            # print("node:{}".format(node))
            newpath = find_path(graph, node, end, path)  # 递归调用时传入参数path
            # print("newpath:{}".format(newpath))
            # newpath=False
            if newpath:
                # print("if--newpath:{}".format(newpath))
                return newpath  # 找到一条路径便结束循环
    return None

def compatibility(license1, license2):
    tmp_graph = graph
    if license2 == "MPL v2.0":
        tmp_graph["Apache v2.0"].append("MPL v2.0")
        tmp_graph["MPL v1.1"].append("MPL v2.0")
    elif license2 == "EPL v2.0":
        tmp_graph["EPL v1.0"].append("EPL v2.0")
    
    return find_path(tmp_graph, license1, license2)

if __name__ == '__main__':
    print(compatibility("MPL v2.0", "GPL v2"))
    H = nx.DiGraph(graph) 
    nx.draw_circular(H, with_labels=True, font_weight='bold')
    plt.show()