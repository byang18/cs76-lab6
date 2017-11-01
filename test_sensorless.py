# You write this:
from SensorlessProblem import SensorlessProblem
from Maze import Maze

# Sample Maze 2
# test_maze2 = Maze("mazes/maze2.maz")
# test_sl = SensorlessProblem(test_maze2)

# Sample Maze 3
test_maze3 = Maze("mazes/maze0.maz")
test_sl = SensorlessProblem(test_maze3)

print(test_sl.maze)

# Sample Maze 4
# test_maze4 = Maze("mazes/maze4.maz")
# test_sl = SensorlessProblem(test_maze4)
#
# result = astar_search(test_sl, null_heuristic)
# print(result)
#
# result = astar_search(test_sl, test_sl.blind_heuristic)
# print(result)
# test_sl.animate_path(result.path)
