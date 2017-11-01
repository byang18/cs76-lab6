from time import sleep
from Maze import Maze

class SensorlessProblem:

    def __init__(self, maze):
        self.maze = maze

        # start state is a list of all legal states
        l = []
        for x in range(0, self.maze.width):
            for y in range(0, self.maze.height):
                if maze.is_floor(x, y):
                    l.append((x, y))
        # convert start state to tuple so that it is hashable
        # (can be stored in a dictionary)
        self.start_state = tuple(l)

        self.visited = 0

    def __str__(self):
        string = "Blind robot problem: "
        return string

    # Blind_heuristic is length of possible remaining states - 1
    # As goal is to get less possible pairs
    def blind_heuristic(self, state):
        return len(state) - 1

    def reset_visited(self):
        self.visited = 0

    def increment_visited(self):
        self.visited += 1

    def get_visited(self):
        return self.visited

    def get_successors(self, state):
        succ = []
        list_state = list(state) # Make state a list instead of a tuple

        # Lists to store movements if all possible locations move up
        north = []
        south = []
        east = []
        west = []

        # state is a set of pairs
        for pair in list_state:

            # Empty integer types sneak in when state is converted to a list
            # If this happens, can skip
            if(type(pair)) is int:
                continue

            # coordinate right now
            x = pair[0]
            y = pair[1]

            north_move = tuple((x, y + 1))
            south_move = tuple((x, y - 1))
            east_move = tuple((x + 1, y))
            west_move = tuple((x - 1, y))

            # If the north is in the list of acceptable locations, add it to the north movements
            if north_move in self.start_state:
                north.append(north_move)
            # Otherwise, reach a bump (wall or a boundary), if this happens leave
            # the pair into next robot successor state
            elif tuple(pair) not in north:
                north.append(tuple(pair))

            # Analogous
            if south_move in self.start_state:
                south.append(south_move)
            elif tuple(pair) not in south:
                south.append(tuple(pair))

            if east_move in self.start_state:
                east.append(east_move)
            elif tuple(pair) not in east:
                east.append(tuple(pair))

            if west_move in self.start_state:
                west.append(west_move)
            elif tuple(pair) not in west:
                west.append(tuple(pair))

        # Successor states are one of four possible cardinal directions
        succ.append(tuple(north))
        succ.append(tuple(south))
        succ.append(tuple(east))
        succ.append(tuple(west))

        return succ

    def animate_path(self, path):

        # The start_list unpacks the path back into a list
        # This list is a list of tuples of tuples
        start_list = list(self.start_state)
        l = []
        for pair in start_list:
            l.append(pair[0])
            l.append(pair[1])
        start_tuple = tuple(l)
        self.maze.robotloc = tuple(start_tuple)

        for state in path:

            # s is the list of possible pairs
            # that the blind robots may be in
            s = list(state)

            # l is a pair where a robot may be in
            # This will be represented by letters
            l = []
            for pair in s:
                l.append(pair[0])
                l.append(pair[1])
            new = tuple(l)

            print(str(self))
            self.maze.robotloc = tuple(new)
            sleep(1)

            print(str(self.maze))

    def goal_test(self, state):
        if len(state) == 1:
            return True
        return False

    def increment_cost(self, cost, new_state, old_state):
        return cost + 1

## A bit of test code

if __name__ == "__main__":
    test_maze5 = Maze("maze5.maz")
    test_problem = SensorlessProblem(test_maze5)
    print(test_problem.get_successors(test_problem.start_state))
