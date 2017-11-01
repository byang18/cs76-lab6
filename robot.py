import random
from Maze import Maze

class Robot:

    # Given a sequence of sensor readings,
    # knowledge of the maze (where the walls are),
    # and the colors of each location of the maze
    def __init__(self, maze, timestep):
        self.maze = maze
        self.error_threshold = .88
        self.timestep = timestep

        l = []
        for x in range(0, self.maze.width):
            for y in range(0, self.maze.height):
                if maze.is_floor(x, y):
                    l.append((x, y))

        # start state is a list of all legal states
        self.legal_locs = tuple(l)

        self.loc = tuple(maze.robotloc)
        self.correct_locs = [] # Testing only

    def make_readings(self):

        sensor_readings = []

        while self.timestep > 0:
            sensor_readings.append(self.sense_color())
            self.correct_locs.append(self.loc)
            self.loc = self.move()
            self.timestep -= 1

        return sensor_readings

    def sense_color(self):
        r = random.random()
        real = self.maze.get_color(self.loc[0], self.loc[1])
        c = ["R", "G", "B", "Y"]
        c.remove(real)

        if r > self.error_threshold:
            return random.choice(c)
        return real

    # returns new location of robot
    def move(self):
        return random.choice(self.get_successors())

    def get_successors(self):

        succ = ["N", "S", "E", "W"]

        x = self.loc[0]
        y = self.loc[1]

        north_move = tuple((x, y + 1))
        south_move = tuple((x, y - 1))
        east_move = tuple((x + 1, y))
        west_move = tuple((x - 1, y))

        if north_move in self.legal_locs:
            succ[0] = north_move
        # Otherwise, reach a bump (wall or a boundary), if this happens leave
        # the pair into next robot successor state
        else:
            succ[0] = self.loc

        # Analogous
        if south_move in self.legal_locs:
            succ[1] = south_move
        else:
            succ[1] = self.loc

        if east_move in self.legal_locs:
            succ[2] = east_move
        else:
            succ[2] = self.loc

        if west_move in self.legal_locs:
            succ[3] = west_move
        else:
            succ[3] = self.loc

        return succ

if __name__ == "__main__":
    test_maze = Maze("mazes/maze0.maz")
    robot = Robot(test_maze, 5)
    print(test_maze)
    # print("successors are" + str(robot.get_successors()))
    sr = robot.make_readings()
    print(sr)
    print(robot.correct_locs)
