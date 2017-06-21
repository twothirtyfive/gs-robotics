import matplotlib.pyplot as plt
import sys, math
from string import split

R_DIM = (23,23) #example, robot that is 10cm x 10cm
Starting_orientation = 90
orient_factor = math.cos(Starting_orientation)
orient_factor2 = math.sin(Starting_orientation)

class Obstacle:
    v_num = 0
    old_vertices = []
    vertices = []
    grown = False
    name = None

    def __init__(self, v_num, old_vertices, vertices, grown, name):
        self.v_num = v_num
        self.old_vertices = old_vertices
        self.vertices = vertices
        self.grown = False
        self.name = name

    def grow(self):
        for a in range(0, self.v_num):
            x,y = self.vertices[a]
            self.vertices.append([x+R_DIM[0], y])
            self.vertices.append([x, y+R_DIM[1]])
            self.vertices.append([x+R_DIM[0], y+R_DIM[1]])
        self.grown = True

    def sort(self):
        self.vertices = list(set(tuple(a) for a in self.vertices))
        self.vertices.sort(key=lambda x: (x[1], x[0]))
        self.vertices = (list(a) for a in self.vertices)

        ang_table = []
        temp_table = []
        v = list(self.vertices)
        for i in range(1,len(v)):
            ang = 0
            if v[i][0]-v[0][0] == 0:
                ang = -math.pi/2
            else:
                ang = math.atan(float(v[i][1]-v[0][1])/float(v[i][0]-v[0][0]))
            ang_table.append([ang, v[i]])
        temp_pos = []
        temp_neg = []
        # for a,b in ang_table:
        #     if
        for a,b in ang_table:
            if a>= 0:
                temp_pos.append([a,b])
            else:
                temp_neg.append([a,b])
        temp_pos.sort(key=lambda x: (x[0]))
        temp_neg.sort(key=lambda x: (x[0]))

        reversed(temp_neg)
        temp_pos.extend(temp_neg)

        temp_table.append(v[0])
        for a,b in temp_pos:
            temp_table.append(b)

        self.vertices = temp_table

    def o_print(self):
        for a in self.vertices:
            print a

    #ccw if >0, cw if <0, colinear if == 0
    def ccw(self, p1, p2, p3):
        return (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0])

    def graham_scan(self):
        temp_table = []
        v_num = len(self.vertices)
        v = list(self.vertices)
        last = v[-1]
        v.insert(0,last)
        M = 1
        for i in range(2,v_num+1):
            while self.ccw(v[M-1], v[M], v[i]) <= 0:
                if M > 1:
                    M -= 1
                    continue
                elif i is v_num:
                    break
                else:
                    i += 1
            M += 1
            tmp = v[M]
            v[M] = v[i]
            v[i] = tmp
            temp = v

            # print i,": ",v
        # print M
        self.convex_hull = v[0:M]
        # print self.convex_hull
        # print len(self.convex_hull)


    def draw_obstacles(self):
        #draw original obstacles
        temp_x = []
        temp_y = []
        for x,y in self.old_vertices:
            temp_x.append(x)
            temp_y.append(y)
        # print temp_x
        # print temp_y
        plt.plot(temp_x, temp_y, color='black', lw=1)
        plt.plot([temp_x[0], temp_x[-1]], [temp_y[0], temp_y[-1]], color='black', lw=1)

        #draw grown obstacles
    def draw_convex(self):
        temp_x = []
        temp_y = []
        for x,y in self.convex_hull:
            temp_x.append(x)
            temp_y.append(y)
        # print temp_x
        # print temp_y
        plt.plot(temp_x, temp_y, color='red', lw=1)
        plt.plot([temp_x[0], temp_x[-1]], [temp_y[0], temp_y[-1]], color='red', lw=1)

def dijkstra(vdict):
    x = 1
    vdict["s"].visited = True
    vdict["s"].distance = 0
    while x is 1:
        x = 0
        for vert in vdict.values():
            if vert.visited is True:
                # print "inside",vert.name
                for node,dist in vert.pairs:
                    # print "super",node
                    if vdict[node].visited is not True:
                        vdict[node].visited = True
                        vdict[node].distance = vert.distance + dist
                        vdict[node].prev = vert.name
                    elif((vert.distance + dist) < vdict[node].distance):
                        vdict[node].distance = vert.distance + dist
                        vdict[node].prev = vert.name
            else:
                x = 1
    dij_edges = []
    # print "\n\n"
    # printDict(vdict)
    for vert in vdict.values():
        # print "test",vert.name
        if vert.distance is 0:
            continue
        vert.prev_index = vert.neighbors.index(vert.prev)
    dij_edges.append(vdict["g"].edges[vdict["g"].prev_index])
    stt = vdict["g"].prev
    while vdict[stt].distance is not 0:
        dij_edges.insert(0,vdict[stt].edges[vdict[stt].prev_index])
        stt = vdict[stt].prev
    return dij_edges

def myccw( p1, p2, p3):
    temp = (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0])
    if temp == 0.0:
        return 0.0
    elif temp > 0.0:
        return 1.0
    else:
        return -1.0 

class Node:
    def __init__( self, nm ):
        # self.point = [x,y]
        self.name = nm
        self.visited = False
        self.distances = []
        self.neighbors = []
        self.edges = []
        self.pairs = []
        self.distance = -1
        self.prev = nm
        self.prev_index = -1

    def insert(self, node, edge):
        self.distances.append(edge.distance)
        self.edges.append(edge)
        self.neighbors.append(node)
        self.pairs.append([node,edge.distance])

def anything_equals(ax,bx):
    x = ax[0]
    x1 = ax[1]
    x2 = bx[0]
    x3 = bx[1]
    if ((x == x2) or (x == x3)) or ((x1 == x2) or (x1 == x3)):
        return True
    else:
        return False

class Edge:
    def __init__( self, ax,  ay,  bx,  by ):
        self.sx = ax
        self.sy = ay
        self.ex = bx
        self.ey = by
        self.x = [ax,bx]
        self.y = [ay,by]
        self.one = [ax,ay]
        self.two = [bx,by]
        #error-prone
        self.minx = min(self.x)-0.5
        self.maxx = max(self.x)+0.5
        self.miny = min(self.y)-0.5
        self.maxy = max(self.y)+0.5
        self.dx = ax-bx
        self.dy = ay-by
        self.num = ax*by - ay*bx
        self.distance = math.sqrt( pow(ax-bx,2.0) + pow(ay-by,2) )
        self.orientation = 0

    def orient(self):
        self.orientation = math.degrees(math.atan2(-1*self.dy,-1*self.dx))
        print "orientation: ",self.orientation

    def switch(self, premier):
        if self.sx == premier[0] and self.sy == premier[1]:
            self.orient()
            return
        else:
            self.ex = self.sx
            self.ey = self.sy
            self.sx = premier[0]
            self.sy = premier[1]
            temp = self.two
            self.two = self.one
            self.one = temp
            self.dx *= -1
            self.dy *= -1
            self.orient()


    def intersect(self, other):
        if self.sx==other.sx and self.sy==other.sy:
            return False
        if self.sx==other.ex and self.sy==other.ey:
            return False
        if self.ex==other.sx and self.ey==other.sy:
            return False
        if self.ex==other.ex and self.ey==other.ey:
            return False
        base = self.dx*other.dy - other.dx*self.dy
        if base == 0.0:
            if self.dx == 0.0 and other.dx==0.0:
                if self.sx != other.sx:
                    return False
                else:
                    return True
            if self.dy == 0.0 and other.dy==0.0:
                if self.sy != other.sy:
                    return False
                else:
                    return True
        px = (self.num*other.dx - self.dx*other.num)/base
        py = (self.num*other.dy - self.dy*other.num)/base
        
        if self.minx <= px:
            if px <= self.maxx:
                if self.miny <= py:
                    if py <= self.maxy:
                        if other.minx <= px:
                            if px <= other.maxx:
                                if other.miny <= py:
                                    if py <= other.maxy:
                                        # print "hi"
                                        # print "\np",px,",",py
                                        # print "self",self.one,",",self.two
                                        # print self.minx,",",self.maxx,",",self.miny,",",self.maxy
                                        # print "other",other.one,",",other.two
                                        # print other.minx,",",other.maxx,",",other.miny,",",other.maxy
                                        return True
        # print "\np",px,",",py
        # print "self",self.one,",",self.two
        # print self.minx,",",self.maxx,",",self.miny,",",self.maxy
        # print "other",other.one,",",other.two
        # print other.minx,",",other.maxx,",",other.miny,",",other.maxy
        # print "0",self.one,self.two,other.one,other.two
        return False

def setup_env(input_table):
    start_coord = input_table.pop(0)
    goal_coord = input_table.pop(0)
    env_coord = input_table.pop(0)
    plt.plot(start_coord[0], start_coord[1], marker='o', color='b')
    plt.text(start_coord[0], start_coord[1], 'start')
    plt.plot(goal_coord[0], goal_coord[1], marker='o', color ='r')
    plt.text(goal_coord[0], goal_coord[1], 'goal')
    plt.plot([0, env_coord[0], env_coord[0], 0], [0, 0, env_coord[1], env_coord[1]], color='g', lw=2)
    draw_rover(start_coord)
    return start_coord,goal_coord

def draw_rover(Starting_pos):
    temp_x = []
    temp_y = []
    temp_x.append(Starting_pos[0])
    temp_y.append(Starting_pos[1])
    temp_x.append(Starting_pos[0]-R_DIM[0])
    temp_y.append(Starting_pos[1])
    temp_x.append(Starting_pos[0]-R_DIM[0])
    temp_y.append(Starting_pos[1]-R_DIM[0])
    temp_x.append(Starting_pos[0])
    temp_y.append(Starting_pos[1]-R_DIM[1])
    plt.plot(temp_x, temp_y, color='black', lw=1)
    plt.plot([temp_x[0], temp_x[-1]], [temp_y[0], temp_y[-1]], color='black', lw=1)
    
def createEdges(points):
    c_edges = []
    for i in range(len(points)):
        pos = points[i]
        nex = points[i-1]
        # print "pos",pos
        # print "nex",nex
        ed = Edge( pos[0], pos[1], nex[0], nex[1] )
        c_edges.append(ed)
    return c_edges

def plotEdges(edges,col):
    colo = 'black'
    sz = 1
    if col is 1:
        colo = 'blue'
        sz = 4
    for i in edges:
        plt.plot([i.sx, i.ex], [i.sy, i.ey], color=colo, lw=sz)

def main():
    input_table = []
    obstacle_table = []
    input_file = sys.argv[1]

    with open(input_file, 'r') as fp:
        parsed_input = fp.readlines()

    fp.close()

    parsed_input = [x.strip() for x in parsed_input]
    for x in parsed_input:
        x = map(float, x.split())
        input_table.append(x)

    convex_points = []
    start,goal = setup_env(input_table)

    num_of_obstacles = int(input_table[0][0])
    input_table.pop(0)
    convex_edges = []
    dj_edges = []
    cvx_edges = []


    for a in range(0, num_of_obstacles):
        temp_table = []
        num_of_vertices = int(input_table[0][0])
        input_table.pop(0)

        for b in range(0, num_of_vertices):
            temp = input_table.pop(0)
            temp_table.append(temp)
        obstacle_table.append(Obstacle(num_of_vertices, list(temp_table), temp_table, False, a))
        obstacle_table[a].grow()
        obstacle_table[a].sort()
        obstacle_table[a].graham_scan()
        obstacle_table[a].draw_obstacles()
        obstacle_table[a].draw_convex()
        convex_points.append(obstacle_table[a].convex_hull)
        cvx_edges.append(createEdges(obstacle_table[a].convex_hull))
        tmp = createEdges(obstacle_table[a].convex_hull)
        for i in tmp:
            convex_edges.append(i)
        # tmp = obstacle_table[a].convex_hull
        # for i in tmp:
        #     convex_points.append(i)

        
        
    node_dict = {}
    for i in range(num_of_obstacles):
        tmp = convex_points[i]
        eds = cvx_edges[i]
        for j in range(len(tmp)):
            nm = str(i)+str(j)
            nn = str(i)
            if j is 0:
                nn += str(len(tmp)-1)
            else:
                nn += str(j-1)
            if j is not (len(tmp)-1):
                node_dict[nm] = Node(nm)
            node_dict[nm].insert(nn,eds[j])
            if j is 0:
                node_dict[nn] = Node(nn)
            node_dict[nn].insert(nm,eds[j])
    # print "First"
    # printDict(node_dict)
    node_dict["s"] = Node("s")
    node_dict["g"] = Node("g")

    x = Edge(start[0],start[1],goal[0],goal[1])
    bl = True
    for y in convex_edges:
        if x.intersect(y):
            bl = False
            break
    if bl:
        dj_edges.append(x)
        node_dict["s"].insert("g",x)
        node_dict["g"].insert("s",x)

    convex_points.append([start,goal])
    for i in range(num_of_obstacles):
        tmp = convex_points[i]
        for j in range(i+1,num_of_obstacles+1):
            tp = convex_points[j]
            for on in range(len(tmp)):
                for tw in range(len(tp)):
                    one = tmp[on]
                    two = tp[tw]
                    # print "edge"
                    # print one
                    # print two
                    x = Edge(one[0],one[1],two[0],two[1])
                    bl = True
                    # won = False
                    # lose = False
                    for y in convex_edges:
                        mybl = x.intersect(y)
                        if mybl:
                            bl = False
                    if bl:
                        dj_edges.append(x)
                        str1 = str(i)+str(on)
                        str2 = ""
                        if j is num_of_obstacles:
                            if tw is 0:
                                str2 = "s"
                            else:
                                str2 = "g"
                        else:
                            str2 = str(j)+str(tw)
                        node_dict[str1].insert(str2,x)
                        node_dict[str2].insert(str1,x)
                        # print "x",x

    # print "obst",num_of_obstacles
    plotEdges(dj_edges,0)
    # print "\n\n\n\nSecond"
    # printDict(node_dict)
    fini = dijkstra(node_dict)
    
    pter = start
    for ed in fini:
        ed.switch(pter)
        pter = ed.two
    plotEdges(fini,1)
    plt.show()

    # obstacle_table[0].graham_scan()

def printDict(dict):
    for x in dict.values():
        print "name",x.name
        print "neighbors",x.neighbors
        print "prev",x.prev








if __name__ == '__main__':
    main()







    # if yn == i:
                        #     won = True
                        #     lose = False
                        # elif yn == j:
                        #     lose = True
                        #     won = False
                        # else:
                        # #     won = False
                        # #     lose = False
                        # yy = convex_edges[yn]
                        # for y in range(len(yy)):
                        #     # if won:
                        #     #     if y == on:
                        #     #         continue
                        #     #     if on == 0 and y == (len(tmp)-1):
                        #     #         continue
                        #     #     if y == on-1:
                        #     #         continue
                        #     # if lose:
                        #     #     if y == tw:
                        #     #         continue
                        #     #     if tw == 0 and y == (len(tp)-1):
                        #     #         continue
                        #     #     if y == tw-1:
                        #     #         continue
                        #     ye = yy[y]
                        #     mybl = x.intersect(ye)
                        #     if mybl:
                        #         bl = False
                        #         break



