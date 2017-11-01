from numpy import matrix
from Maze import Maze

class sensor_problem:

    def __init__(self, maze, timestep):

        self.maze = maze
        self.path = self.path_sequence(timestep, True)

    def path_sequence(self, timestep, test):
        print('path sequence')

    def make_transition_matrix(self, maze):
        print('print')


if __name__ == "__main__":
    test_maze = Maze("mazes/maze0.maz")
    test_problem = sensor_problem(test_maze, 4)
    print(test_problem)
