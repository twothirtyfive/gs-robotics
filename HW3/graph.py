import matplotlib.pyplot as plt
import sys, math
from string import split

R_DIM = (10,10) #example, robot that is 10cm x 10cm

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
            self.vertices.append([x+R_DIM[0], y+R_DIM[1]])
            self.vertices.append([x+R_DIM[0], y])
            self.vertices.append([x, y+R_DIM[1]])
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

            print i,": ",v
        print M
        self.convex_hull = v[0:M]
        print self.convex_hull
        print len(self.convex_hull)


    def draw_obstacles(self):
        #draw original obstacles
        temp_x = []
        temp_y = []
        for x,y in self.old_vertices:
            temp_x.append(x)
            temp_y.append(y)
        print temp_x
        print temp_y
        plt.plot(temp_x, temp_y, color='black', lw=1)
        plt.plot([temp_x[0], temp_x[-1]], [temp_y[0], temp_y[-1]], color='black', lw=1)

        #draw grown obstacles
    def draw_convex(self):
        temp_x = []
        temp_y = []
        for x,y in self.convex_hull:
            temp_x.append(x)
            temp_y.append(y)
        print temp_x
        print temp_y
        plt.plot(temp_x, temp_y, color='black', lw=1)
        plt.plot([temp_x[0], temp_x[-1]], [temp_y[0], temp_y[-1]], color='black', lw=1)


def setup_env(input_table):
    start_coord = input_table.pop(0)
    goal_coord = input_table.pop(0)
    env_coord = input_table.pop(0)
    plt.plot(start_coord[0], start_coord[1], marker='o', color='b')
    plt.text(start_coord[0], start_coord[1], 'start')
    plt.plot(goal_coord[0], goal_coord[1], marker='o', color ='r')
    plt.text(goal_coord[0], goal_coord[1], 'goal')
    plt.plot([0, env_coord[0], env_coord[0], 0], [0, 0, env_coord[1], env_coord[1]], color='g', lw=2)

def main():
    # test_obs = Obstacle(4, [[0,0], [0,10], [10,0], [10,10]], False)
    # test_obs.grow()
    # test_obs.sort()
    # test_obs.graham_scan()
    # test_obs.o_print()

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

    setup_env(input_table)

    num_of_obstacles = int(input_table[0][0])
    input_table.pop(0)

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
        print "\n\n\n"
        obstacle_table[a].graham_scan()
    temp_table = []
    print "\n\n\n"
    for a in range(0,len(obstacle_table)):
        obstacle_table[a].draw_obstacles()
        obstacle_table[a].draw_convex()

    # obstacle_table[0].o_print()
    plt.show()
    # obstacle_table[0].graham_scan()




if __name__ == '__main__':
    main()
