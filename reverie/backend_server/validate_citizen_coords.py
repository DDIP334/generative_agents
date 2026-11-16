import json
from collections import deque

grid = json.load(open('d:/Project/generative_agents/environment/frontend_server/static_dirs/assets/the_ville/the_ville_collision_grid.json'))
citizens = json.load(open('d:/Project/generative_agents/environment/frontend_server/static_dirs/assets/the_ville/society_citizens.json'))
h, w = len(grid), len(grid[0])

# Flood fill from Isabella (73, 14)
queue = deque([(73, 14)])
visited = set([(73, 14)])
while queue:
    cx, cy = queue.popleft()
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == 0 and (nx, ny) not in visited:
            visited.add((nx, ny))
            queue.append((nx, ny))

print('Total reachable network tiles:', len(visited))

def fix_coord(pt):
    if tuple(pt) in visited:
        return pt
    best = None
    best_d = 999
    for vx, vy in visited:
        d = abs(vx - pt[0]) + abs(vy - pt[1])
        if d < best_d:
            best_d = d
            best = [vx, vy]
    return best

updated = False
for c in citizens:
    for field in ['home_coords', 'bed_coords', 'bathroom_coords', 'workplace_coords']:
        old = c[field]
        fixed = fix_coord(old)
        if old != fixed:
            print(f"{c['name']} {field}: {old} -> {fixed}")
            c[field] = fixed
            updated = True
    for t_str, sch in c['schedule'].items():
        old_loc = sch['loc']
        fixed_loc = fix_coord(old_loc)
        if old_loc != fixed_loc:
            sch['loc'] = fixed_loc
            updated = True

with open('d:/Project/generative_agents/environment/frontend_server/static_dirs/assets/the_ville/society_citizens.json', 'w') as f:
    json.dump(citizens, f, indent=2)

print('Coordinates validation complete! All citizens verified 100% reachable.')
