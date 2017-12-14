import numpy as numpy
from numpy import matrix
from Maze import Maze
from robot import Robot

class sensor_problem:

    def __init__(self, maze, timestep):

        self.maze = maze
        self.robot = Robot(self.maze, timestep)

        # array composed of colors SENSED by the robot (not necessarily accurate)
        # index of colors is the timestep
        self.path = self.robot.make_readings()
        self.timestep = timestep

        # represents what coordinates coorespond to what state
        self.index_to_color = []

        # maps an x-y coordinate to a state value
        # state is a single random variable X, where X_i can represent
        # the probabiliy the robot is at a given state
        self.state_map = self.make_state_map()

        # produce a transition matrix where T_(ij) = P(x_t = j | x_(t - 1) = i)
        self.transition_matrix = self.make_transition_matrix()

        # produce a dictionary of sensor matrices
        # key is a color which maps to a particular sensor matrix
        #   (since colors on the map do not change)
        # sensor matrix is a diagonal matrix O_t where P(e_t | x_t = i), i = state value
        self.sensor_matrices = self.make_sensor_matrices()

    def solve(self):

        # get a starting vector
        starting = self.starting_distribution()

        # feed starting vector to start filtering
        solution = self.filter(starting)
        self.render_solution(solution)

    def render_solution(self, solution):

        # statistics and paths that help with debugging
        print("sensed path: {}".format(str(self.path)))
        print("correct path: {}".format(str(self.robot.correct_locs)))

        if len(self.robot.error_msgs) == 0:
            print("no mistakes in sensors")
        else:
            print("mistakes: ")
            for msg in self.robot.error_msgs:
                print("     {}".format(msg))
        print("")

        # for each iteration of the solution, display probability values
        timestep = 0

        # solution is a list of vectors (where vector is a distribution of probabilities)
        for vector in solution:

            # convert the matrix back to a list for easier processing
            l = numpy.array(vector).tolist()[0]
            display = [] # displayed solution
            row = [] # each row of a solution
            row_element = 0 # index of a particular row element
            index = 0 # index of the solution vector

            # build display matrix
            for item in l:

                color = self.index_to_color[index]
                item_string = "|{}: ".format(color) + "{0:.5f}".format(item) + "|"
                row.append(item_string)

                # if reach the width, then start a new row
                row_element += 1
                if row_element > self.maze.width - 1:
                    row_element = 0
                    display.append(row)
                    row = []
                index += 1

            # reorder the display vector so (0, 0) is on bottom-left
            display.reverse()

            # title each timestep
            if timestep == 0:
                print(" t = 0 (starting values)")
            elif timestep == 1:
                print(" t = 1 (robot begins sensing)")
            else:
                print(" t = {}".format(timestep))

            index = self.maze.height - 1
            for row in display:

                # build y-axis on left
                print("{} ".format(index), end='')
                index -= 1
                for item in row:
                    print(item, end='')
                print("")

            # build x axis on bottom
            starting = "       0"
            for i in range(1, self.maze.width):
                starting += "           {}".format(i)
            print(starting)
            print("")
            timestep += 1

    def filter(self, starting):

        # initliaze an array with the starting vector
        distributions = [starting]

        # for as long as as there is still a timestep
        for t in range(self.timestep):

            # get color at particular time
            color = self.path[t]

            # get the previous solution vector
            prev = distributions[t]

            # multiply that solution vector by the transposed transition matrix
            intermediate = prev * self.transition_matrix

            # multiply that intermediate value with the appropriate sensor matrix
            result = intermediate * self.sensor_matrices[color]
            r = normalize(result)
            distributions.append(r)

        # return a distribution of vectors for each timestep
        return distributions

    # create the starting vector (where all appropriate states have equal probability)
    def starting_distribution(self):
        start = []

        # starting probability is 1/(number of legal states)
        starting_probability = float(1/(len(self.state_map) - self.maze.num_walls()))
        for coord in self.state_map:
            state = self.state_map[coord]

            # if the state value is a wall
            if state[1]:
                start.append(0)

            # otherwise append the correct probability
            else:
                start.append(starting_probability)

        # convert to a matrix
        s = matrix(start)
        return s

    def make_state_map(self):

        state_map = {}
        state = 0

        # each i, j coordinate represents a state value, where robot may be
        for j in range(self.maze.height):
            for i in range(self.maze.width):

                # link the state value to color (with index being state value)
                self.index_to_color.append(self.maze.get_color(i, j))

                # state_map maps coordinate to (state value, is_wall)
                if self.maze.is_floor(i, j):
                    state_map[tuple((i, j))] = (state, False)
                else:
                    state_map[tuple((i, j))] = (state, True)
                state += 1

        return state_map

    def make_transition_matrix(self):
        mat = self.initialize_matrix()

        # fill in matrix with transition probabilities
        for j in range(self.maze.height):
            for i in range(self.maze.width):
                state, wall_at_state = self.state_map[tuple((i, j))]

                # if there is no wall at state, then proceed
                # otherwise, state is automatically given a value of 0
                if not wall_at_state:

                    legal_moves = self.find_legal_moves(i, j)
                    num_legal_moves = len(legal_moves)

                    # probability of staying (explained in documentation)
                    mat[state][state] = float((5 - num_legal_moves)/4)
                    for move in legal_moves:
                        adj_state = self.state_map[move][0]
                        if adj_state != state:

                            # there is always a .25 chance
                            # of moving into a location
                            mat[state][adj_state] = .25

        # the transpose the transition matrix
        m = matrix(mat).getT()
        return m

    # produces the dictionary of sensor matrices
    # only needs to be run in beginning because colors do not change
    def make_sensor_matrices(self):

        # dictionary that maps color to the appropriate sensor matrix
        matrices = {}

        for color in self.maze.colors:

            mat = self.initialize_matrix()

            for j in range(self.maze.height):
                for i in range(self.maze.width):

                    state, wall_at_state = self.state_map[tuple((i, j))]

                    if not wall_at_state:

                        # the robot has an .88 chance of sensing the correct color
                        if self.maze.get_color(i, j) == color:
                            mat[state][state] = self.robot.error_threshold

                        # the remaining .12 is split between the other colors
                        else:
                            mat[state][state] = ((1 - self.robot.error_threshold)/
                                                 (len(self.maze.colors) - 1))

            m = matrix(mat)

            # map the color to the correct matrix
            matrices[color] = m

        return matrices

    # gets legal moves given a coordinate
    # there are up to 5 legal moves (NSEW and current location)
    # the robot can always be in the current location
    def find_legal_moves(self, x, y):
        legal_moves = []
        legal_moves.append(tuple((x, y)))

        # north
        if self.maze.is_floor(x, y + 1):
            legal_moves.append(tuple((x, y + 1)))

        # south
        if self.maze.is_floor(x, y - 1):
            legal_moves.append(tuple((x, y - 1)))

        # east
        if self.maze.is_floor(x + 1, y):
            legal_moves.append(tuple((x + 1, y)))

        # west
        if self.maze.is_floor(x - 1, y):
            legal_moves.append(tuple((x - 1, y)))

        return legal_moves

    # create an SxS 2d-list (where S is number of states)
    # fill all values with 0
    def initialize_matrix(self):

        mat = []

        # initialize maze
        for i in range(len(self.state_map)):
            row = []
            for j in range(len(self.state_map)):
                row.append(0)
            mat.append(row)

        return mat

# from https://stackoverflow.com/questions/21030391/how-to-normalize-array-numpy
def normalize(v):
    norm = numpy.linalg.norm(v)
    if norm == 0:
        return v
    return v/norm

if __name__ == "__main__":

    # load maze and problem
    test_maze = Maze("mazes/maze0.maz")
    test_problem = sensor_problem(test_maze, 5)

    # display maze for debugging
    print("Maze (robot labeled as 1):")
    print(test_problem.maze)

    test_problem.solve()
