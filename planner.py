import sys

"""
implement Uniform Cost Search (UCS) and Depth First Search (DFS)

return:
    1. one action per line (N, S, W, S, E, ...)
    2. generated set (all nodes added to the frontier throughout the search)
    3. expanded set (all nodes actually expanded from the frontier set throughout the search)
"""

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

    pass

def ucs(grid, dirty, blocked, start):
    # sets needed: frontier, explored, action (for node recounting and path return)
    # use FIFO queue
    # traverse grid using UCS rules, avoiding blocked, checking off dirty until empty

    return actions, generated, expanded

def dfs(grid, dirty, blocked, start):
    # sets needed: frontier, explored, action (for node recounting and path return)
    # use LIFO stack
    # traverse grid according to DFS, avoiding blocked, checking off dirty until empty

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