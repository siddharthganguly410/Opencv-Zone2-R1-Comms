GRID_SIZE = 3

# Possible moves: up, down, left, right
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid(x, y, visited):
    return (
        0 <= x < GRID_SIZE and
        0 <= y < GRID_SIZE and
        not visited[x][y]
    )

def find_paths(x, y, destination, visited, path, all_paths):
    # If destination reached, store the path
    if (x, y) == destination:
        all_paths.append(path.copy())
        return

    # Explore adjacent cells
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, visited):
            visited[nx][ny] = True
            path.append((nx, ny))
            find_paths(nx, ny, destination, visited, path, all_paths)
            path.pop()
            visited[nx][ny] = False

def robot_paths():
    start = (0, 0)
    destination = (2, 2)

    visited = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]
    visited[0][0] = True

    all_paths = []
    find_paths(0, 0, destination, visited, [start], all_paths)

    return all_paths

# Run
paths = robot_paths()

print(f"Total paths: {len(paths)}\n")
for p in paths:
    print(p)
