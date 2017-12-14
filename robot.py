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

        # start state is a list of all legal states
        self.legal_locs = self.get_legal_locs()

        self.loc = tuple(maze.robotloc)
        self.correct_locs = [] # Testing only
        self.error_msgs = [] # Testing only

    # get all legal location
    def get_legal_locs(self):
        l = []
        for x in range(0, self.maze.width):
            for y in range(0, self.maze.height):
                if self.maze.is_floor(x, y):
                    l.append((x, y))
        return l

    # get sensor readings to be used in sensor_problem
    def make_readings(self):

        sensor_readings = []

        while self.timestep > 0:
            # get sensor readings
            sensor_readings.append(self.sense_color())

            # get correct locations (for testing purposes)
            self.correct_locs.append(self.loc)

            # get the next step
            self.loc = self.move()
            self.timestep -= 1

        return sensor_readings

    def sense_color(self):

        # pick a random number to be compared against threshold
        r = random.random()

        # real color
        real = self.maze.get_color(self.loc[0], self.loc[1])

        # list of wrong colors
        c = ["R", "G", "B", "Y"]
        c.remove(real)

        # if over the threshold, then return a random choice from the wrong colors
        if r > self.error_threshold:
            error_msg = "Wrong color sensed at ({}, {})".format(self.loc[0], self.loc[1])
            self.error_msgs.append(error_msg)
            return random.choice(c)

        # otherwise return the real color
        return real

    # returns new location of robot, chosen randomly
    def move(self):
        return random.choice(self.get_successors())

    # gets a list of legal successors
    def get_successors(self):

        # orientation of successors is "NSEW"
        succ = ["N", "S", "E", "W"]

        x = self.loc[0]
        y = self.loc[1]

        north_move = tuple((x, y + 1))
        south_move = tuple((x, y - 1))
        east_move = tuple((x + 1, y))
        west_move = tuple((x - 1, y))

        # if moving north is legal, then add northmove to successors
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

# test code
if __name__ == "__main__":
    test_maze = Maze("mazes/maze0.maz")
    robot = Robot(test_maze, 5)
    print(test_maze)

    sr = robot.make_readings()
    print(sr)
    print(robot.correct_locs)
