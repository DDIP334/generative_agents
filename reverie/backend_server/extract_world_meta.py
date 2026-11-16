import os, sys, json

os.chdir(os.path.dirname(os.path.abspath(__file__)))
from maze import Maze

m = Maze('the_ville')
print('Maze dimensions:', m.maze_width, 'x', m.maze_height)

# Collect locations for key arenas and objects
arena_locations = {}
object_locations = {}

for y in range(m.maze_height):
    for x in range(m.maze_width):
        arena = m.tiles[y][x]['arena']
        sector = m.tiles[y][x]['sector']
        obj = m.tiles[y][x]['game_object']
        col = (m.collision_maze[y][x] != "0")
        if arena and not col:
            key = f"{sector} -> {arena}"
            if key not in arena_locations:
                arena_locations[key] = []
            arena_locations[key].append((x, y))
        
        if obj and not col:
            obj_key = f"{sector} -> {arena} -> {obj}"
            if obj_key not in object_locations:
                object_locations[obj_key] = []
            object_locations[obj_key].append((x, y))

print('Total walkable arenas found:', len(arena_locations))
summary = {}
for k, pts in arena_locations.items():
    cx = sum([p[0] for p in pts]) // len(pts)
    cy = sum([p[1] for p in pts]) // len(pts)
    summary[k] = {'center': [cx, cy], 'tile_count': len(pts), 'sample_tiles': pts[:5]}

with open('world_locations.json', 'w') as f:
    json.dump(summary, f, indent=2)

obj_summary = {}
for k, pts in object_locations.items():
    cx = sum([p[0] for p in pts]) // len(pts)
    cy = sum([p[1] for p in pts]) // len(pts)
    obj_summary[k] = {'center': [cx, cy], 'tiles': pts}

with open('world_objects.json', 'w') as f:
    json.dump(obj_summary, f, indent=2)

print('Total objects mapped:', len(obj_summary))
for k in sorted(obj_summary.keys())[:15]:
    print(f"{k}: center={obj_summary[k]['center']}")
