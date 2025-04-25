import sys
import queue

"""
implement Uniform Cost Search (UCS) and Depth First Search (DFS)

return:
    1. one action per line (N, S, W, S, E, ...)
    2. generated set (all nodes added to the frontier throughout the search)
    3. expanded set (all nodes actually expanded from the frontier set throughout the search)
"""

# ********************* NEED TO ADD CARDINAL DIRECTION TO EACH PARENT ENTRY WHEN UPDATED SO WE CAN RETRACE

DIRECTIONS = ["N", "E", "S", "W"]

def get_args_and_parse():
    # parse cmd line args and text file
    # return search method, grid, dirty set, blocked set, start position

    if len(sys.argv) != 3:
        print("Usage: python3 planner.py <search-method> <world-file>")
        sys.exit(1)

    search = sys.argv[1]
    world_file = sys.argv[2]

    try:
        with open(world_file, 'r') as f:
            cols = int(f.readline())
            rows = int(f.readline())
            grid = [list(line.strip()) for line in f]
    except:
        print(f"ERROR: Could not open or read file '{world_file}'.")
        sys.exit(1)

    dirty = set()
    blocked = set()

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                start = (i, j)
            elif cell == '*':
                dirty.add((i, j))
            elif cell == '#':
                blocked.add((i, j))

    if search == "uniform-cost":
        actions, generated, expanded = ucs(grid, dirty, blocked, start)
    elif search == "depth-first":
        actions, generated, expanded = dfs(grid, dirty, blocked, start)
    else:
        print("ERROR: Invalid search method.")
        return

def reconstruct_path(parents: dict, state: tuple(int, int)):
    # starting from the end of the dict, reconstruct the path
    pass

def ucs(grid: list, dirty: set, blocked: set, start: tuple(int, int)):
    # sets needed: frontier, explored, action (for node recounting and path return)
    # use FIFO queue
    # traverse grid using UCS (dijikstra's) rules, avoiding blocked, checking off dirty until empty
    frontier = queue.PriorityQueue()
    visited = set()
    parents = {}
    generated = 0
    expanded = 0
    num_cols = len(grid[0])
    num_rows = len(grid)

    # add start to frontier and parents
    parents[start] = (0, None)
    frontier.put((0, start))

    while frontier:
        # loop through, popping from the frontier
        # each pop gets added to the visited list (cardinal dir + col + row)
        state = frontier.get()
        visited.add(state)
        expanded += 1

        # if this coordinate in the dirty set, remove it
        if state in dirty:
            dirty.remove(state)
            # if dirty set empty, break out of loop and return actions and num of generated + expanded nodes
            if len(dirty) == 0:
                return reconstruct_path(parents, state), generated, expanded

        for dir in DIRECTIONS:
            if dir == 'N':
                child = state[0] - 1, state[1]
            elif dir == 'E':
                child = state[0], state[1] + 1
            elif dir == 'S':
                child = state[0] + 1, state[1]
            elif dir == 'W':
                child = state[0], state[1] - 1

            # calculate new cost for the child
            new_cost = parents[state][0] + 1
            
            # when expanding frontier, don't add child if: 
            #   if direction in visited
            #   if direction out of bounds
            #   if direction is blocked
            if child in visited or child in blocked:
                continue
            if child[0] < 0 or child[0] >= num_rows or child[1] < 0 or child[1] >= num_cols:
                continue

            # add child to frontier and parents if not already seen or it has a better path
            if child not in parents or new_cost < parents[child][0]:
                parents[child] = (new_cost, state)
                frontier.put((new_cost, child))
                generated += 1
    
    print("ERROR: Unable to find solution.")
    sys.exit(1)

def dfs(grid: list, dirty: set, blocked: set, start: tuple(int, int)):
    # sets needed: frontier, explored, action (for node recounting and path return)
    # use LIFO stack
    # traverse grid according to DFS, avoiding blocked, checking off dirty until empty
    frontier = []

    return actions, generated, expanded

def main():
    search, grid, dirty, blocked, start = get_args_and_parse()

    if search == "uniform-cost":
        actions, generated, expanded = ucs(grid, dirty, blocked, start)
    elif search == "depth-first":
        actions, generated, expanded = dfs(grid, dirty, blocked, start)
    else:
        print("ERROR: Invalid search method.")
        return

    for action in actions:
        print(action)
    print(f"{generated} nodes generated")
    print(f"{expanded} nodes generated")

    return

if __name__ == "__main__":
    main()