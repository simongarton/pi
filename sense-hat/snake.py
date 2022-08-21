from time import sleep
from random import randint

from sense_emu import SenseHat
# from sense_hat import SenseHat


# Snake demo. Borrowed someone's Astar code and it doesn't work properly but at least it doesn't crash any more.
#
# Simon Garton
# simon.garton@gmail.com
# November / December 2020

sense = SenseHat()
sense.clear()


class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # this algorithm is buggy : open_list can grow indefinitely
        if len(open_list) > 100:
            break

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        # Adjacent squares
        # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            # Get node position
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


class Snake:

    def __init__(self):
        self.x = 4
        self.y = 4
        self.dir = 1
        self.tail = [(4, 3)]
        pass

    def move(self):
        for i in range(len(self.tail)-2, -1, -1):
            self.tail[i + 1] = self.tail[i]
        self.tail[0] = (self.x, self.y)
        tuple = self.directions.get(self.dir, (0, 0))
        self.x = (self.x + tuple[0] + 8) % 8
        self.y = (self.y + tuple[1] + 8) % 8

    def get_tail(self):
        return self.tail

    def grow(self):
        self.tail.append(self.tail[-1])

    def change_dir(self):
        if (self.dir == 1 or self.dir == 3):
            if (randint(0, 1) == 0):
                self.dir = 2
            else:
                self.dir = 0
        else:
            if (randint(0, 1) == 0):
                self.dir = 1
            else:
                self.dir = 3

    head = (200, 0, 0)
    food = (0, 200, 0)
    black = (0, 0, 0)
    body = (100, 100, 50)

    directions = {
        0: (0, -1),
        1: (1, 0),
        2: (0, 1),
        3: (-1, 0),
    }

    def find(self, food):

        maze = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        for i in range(len(self.tail)-2, -1, -1):
            x = self.tail[i][0]
            y = self.tail[i][1]
            maze[x][y] = 1

        start = (self.x, self.y)
        end = food

        path = astar(maze, start, end)
        if path and len(path) > 1:
            for i in range(len(self.tail)-2, -1, -1):
                self.tail[i + 1] = self.tail[i]
            self.tail[0] = (self.x, self.y)

            self.x = path[1][0]
            self.y = path[1][1]
            return True
        return False


def random_food():
    while(True):
        x = randint(0, 7)
        y = randint(0, 7)
        rgb = sense.get_pixel(x, y)
        if rgb[0] == 0:
            sense.set_pixel(x, y, Snake.food)
            return (x, y)


def run():
    snake = Snake()
    sense.clear()
    food = random_food()
    while(True):
        c = snake.get_tail()[-1]
        sense.set_pixel(c[0], c[1], Snake.black)
        if not snake.find(food):
            print("lost")
            snake.move()
        ground = sense.get_pixel(snake.x, snake.y)
        if ground[1] == Snake.food[1]:
            print("grow")
            snake.grow()
            food = random_food()
        if ground[0] == 96:  # scaling of set/get pixels
            print("die")
            sleep(3)
            snake = Snake()
            sense.clear()
            food = random_food()

        sense.set_pixel(snake.x, snake.y, Snake.head)
        for c in snake.get_tail():
            sense.set_pixel(c[0], c[1], Snake.body)
        if (randint(0, 10) == 0):
            snake.change_dir()
        sleep(0.1)


run()
