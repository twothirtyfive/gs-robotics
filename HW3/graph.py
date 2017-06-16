import matplotlib.pyplot as plt
import sys, string

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
    start_coord = input_table.pop(0)
    goal_coord = input_table.pop(0)
    env_coord = input_table.pop(0)
    num_of_obstacles = int(input_table[0][0])
    input_table.pop(0)
    for x in range(0, num_of_obstacles):
        num_of_vertices = int(input_table[0][0])
        input_table.pop(0)
        for y in range(0, num_of_vertices):
            obstacle_table.append(input_table.pop(0))
            print obstacle_table[y]
            if len(obstacle_table) < 2:
                continue
            elif y == num_of_vertices-1:
                plt.plot(obstacle_table[y][0], obstacle_table[y][1], obstacle_table[y-1][0], obstacle_table[y-1][1], 'y-', lw = 5)
                # plt.plot(obstacle_table[y], )
            else:
                plt.plot(obstacle_table[y][0], obstacle_table[y][1], obstacle_table[y-1][0], obstacle_table[y-1][1], 'y-', lw = 1)
        plt.show()
        raw_input("button...")
        obstacle_table = []
    # plt.show()


if __name__ == '__main__':
    main()
