import sys
import queue

"""
implement Uniform Cost Search (UCS) and Depth First Search (DFS)

return:
    1. one action per line (N, S, W, S, E, ...)
    2. generated set (all nodes added to the frontier throughout the search)
    3. expanded set (all nodes actually expanded from the frontier set throughout the search)
"""

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
                
    print("Dirty set:", dirty)
    print("Blocked set:", blocked) 

    return search, grid, dirty, blocked, start

def reconstruct_path(parents: dict, state):
    print("Parents:")
    for key, value in parents.items():
        print(f"{key} : {value}")

    actions = []
    current = state
    while True:
        cost, parent, action = parents[current]
        if parent is None:
            break
        actions.append(action)
        current = parent
    actions.reverse()
    return actions

def ucs(grid: list, dirty: set, blocked: set, start):
    frontier = queue.PriorityQueue()
    visited = set()
    expanded = 0
    generated = 0
    
    start_state = (start[0], start[1], frozenset(dirty))
    parents = {start_state: (0, None, None)}  # cost, parent_state, action
    frontier.put((0, start_state))
    num_rows = len(grid)
    num_cols = len(grid[0])

    while not frontier.empty():
        cost, state = frontier.get()
        if state in visited:
            continue
        visited.add(state)
        expanded += 1

        row, col, dirty_rem = state
        
        # clean if needed
        if (row, col) in dirty_rem:
            dirty_rem = dirty_rem - {(row, col)}
            
        # goal check
        if not dirty_rem:
            return reconstruct_path(parents, state), generated, expanded

        for dir in DIRECTIONS:
            if dir == 'N': nr, nc = row - 1, col
            elif dir == 'E': nr, nc = row, col + 1
            elif dir == 'S': nr, nc = row + 1, col
            elif dir == 'W': nr, nc = row, col - 1
            else: continue
            
            # bounds & blocked
            if nr < 0 or nr >= num_rows or nc < 0 or nc >= num_cols or (nr, nc) in blocked:
                continue
            
            # carry over dirty_rem; cleaning happens at expansion
            new_state = (nr, nc, dirty_rem)
            new_cost = cost + 1
            if new_state in visited:
                continue
            
            # add/relax
            if new_state not in parents or new_cost < parents[new_state][0]:
                parents[new_state] = (new_cost, state, dir)
                frontier.put((new_cost, new_state))
                generated += 1

    print("ERROR: Unable to find solution.")
    sys.exit(1)

def dfs(grid: list, dirty: set, blocked: set, start):
    # sets needed: frontier, explored, action (for node recounting and path return)
    # use LIFO stack
    # traverse grid according to DFS, avoiding blocked, checking off dirty until empty

    pass

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
    print(f"{expanded} nodes expanded")

    return

if __name__ == "__main__":
    main()