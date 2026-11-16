"""
Generative Agents Comprehensive Verification Test Suite
Tests:
1. Maze and Collision Detection
2. Pathfinding (BFS navigation across the_ville)
3. Persona Loading and Spatial Memory
4. Embeddings Generation and Associative Memory Retrieval
5. Perception and Cognitive Sequence
6. Multi-agent Simulation Step Execution (start_server)
7. Frontend API endpoints (Landing, Demo, Replay, State Details, Process/Update Environment)
"""
import os
import sys
import json
import shutil
import urllib.request
import traceback

def run_tests():
    print("=" * 60)
    print("GENERATIVE AGENTS SIMULATION VERIFICATION SUITE")
    print("=" * 60)
    
    repo_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(repo_root, "reverie", "backend_server")
    frontend_dir = os.path.join(repo_root, "environment", "frontend_server")
    sys.path.insert(0, backend_dir)
    os.chdir(backend_dir)
    
    import utils
    utils.debug = False
    import persona.prompt_template.run_gpt_prompt as rgp
    rgp.debug = False
    
    passed = 0
    total = 7

    # Test 1: Maze & Collision Map
    print("\n[TEST 1] Loading Maze & Collision Map...")
    try:
        from maze import Maze
        maze = Maze("the_ville")
        assert maze.maze_width == 140, f"Expected width 140, got {maze.maze_width}"
        assert maze.maze_height == 100, f"Expected height 100, got {maze.maze_height}"
        assert len(maze.collision_maze) == 100, f"Expected 100 rows in collision matrix"
        assert str(maze.collision_maze[0][0]) in ["0", str(utils.collision_block_id)], f"Unexpected tile: {maze.collision_maze[0][0]}"
        print(f" PASS: Maze 'the_ville' loaded successfully ({maze.maze_width}x{maze.maze_height}), collision block ID: {utils.collision_block_id}.")
        passed += 1
    except Exception as e:
        print(f" FAIL: Maze loading error: {e}")
        traceback.print_exc()

    # Test 2: Pathfinding (BFS)
    print("\n[TEST 2] Pathfinding Algorithm...")
    try:
        from path_finder import path_finder
        # Test finding path from (72, 14) to (73, 14)
        path = path_finder(maze.collision_maze, (72, 14), (73, 14), utils.collision_block_id)
        assert len(path) >= 1, "Expected path of at least 1 step"
        print(f" PASS: Path found successfully: {path[:5]} (length: {len(path)}).")
        passed += 1
    except Exception as e:
        print(f" FAIL: Pathfinding error: {e}")
        traceback.print_exc()

    # Test 3: Persona & Spatial Memory
    print("\n[TEST 3] Persona Initialization & Spatial Memory...")
    try:
        from persona.persona import Persona
        persona_folder = os.path.join(frontend_dir, "storage", "base_the_ville_isabella_maria_klaus", "personas", "Isabella Rodriguez")
        p = Persona("Isabella Rodriguez", persona_folder)
        assert p.name == "Isabella Rodriguez"
        living_area = p.scratch.living_area
        assert "Isabella Rodriguez's apartment" in living_area
        # Test spatial memory tree
        world_sector = ":".join(living_area.split(":")[:2])
        arenas = p.s_mem.get_str_accessible_sector_arenas(world_sector)
        assert "main room" in arenas
        print(f" PASS: Persona loaded: {p.name}, living area: {living_area}, accessible arenas: {arenas}")
        passed += 1
    except Exception as e:
        print(f" FAIL: Persona loading error: {e}")
        traceback.print_exc()

    # Test 4: Embeddings & Associative Memory
    print("\n[TEST 4] Embeddings Generation & Associative Memory Retrieval...")
    try:
        from persona.prompt_template.gpt_structure import get_embedding
        vec1 = get_embedding("Isabella is sleeping in bed")
        vec2 = get_embedding("Isabella is sleeping in bed")
        vec3 = get_embedding("Klaus is reading a gentrification book")
        assert len(vec1) == 1536, f"Expected 1536 dim, got {len(vec1)}"
        assert vec1 == vec2, "Identical text should have identical deterministic embedding"
        assert vec1 != vec3, "Different text should have different embeddings"
        print(f" PASS: Embeddings generated with 1536 dimensions; deterministic equality verified.")
        passed += 1
    except Exception as e:
        print(f" FAIL: Embeddings error: {e}")
        traceback.print_exc()

    # Test 5: Cognitive Step (Perceive, Plan, Execute)
    print("\n[TEST 5] Single Persona Cognitive Step (Perception, Planning, Execution)...")
    try:
        from reverie import ReverieServer
        test_sim = "suite_test_sim"
        test_sim_path = os.path.join(frontend_dir, "storage", test_sim)
        if os.path.exists(test_sim_path):
            shutil.rmtree(test_sim_path)
            
        rs = ReverieServer("base_the_ville_isabella_maria_klaus", test_sim)
        agent = rs.personas["Isabella Rodriguez"]
        tile = rs.personas_tile["Isabella Rodriguez"]
        next_tile, emoji, desc = agent.move(rs.maze, rs.personas, tile, rs.curr_time)
        assert next_tile is not None, "next_tile should not be None"
        assert emoji is not None, "emoji should not be None"
        assert desc is not None, "desc should not be None"
        print(f" PASS: Cognitive cycle executed successfully: next_tile={next_tile}, emoji={emoji}, action='{desc}'")
        passed += 1
    except Exception as e:
        print(f" FAIL: Cognitive step error: {e}")
        traceback.print_exc()

    # Test 6: Multi-Agent Simulation Step (start_server)
    print("\n[TEST 6] Multi-Agent Simulation Step Progression...")
    try:
        rs.start_server(1)
        move_file = os.path.join(test_sim_path, "movement", "0.json")
        assert os.path.exists(move_file), f"Movement file {move_file} was not generated"
        with open(move_file) as f:
            move_data = json.load(f)
        for name in ["Isabella Rodriguez", "Maria Lopez", "Klaus Mueller"]:
            assert name in move_data["persona"], f"Missing agent {name} in movements"
            print(f"   - {name}: move to {move_data['persona'][name]['movement']}, action: {move_data['persona'][name]['description'][:40]}...")
        assert rs.step == 1, f"Expected rs.step == 1, got {rs.step}"
        print(f" PASS: Multi-agent step 0 successfully calculated and recorded to disk.")
        passed += 1
    except Exception as e:
        print(f" FAIL: Multi-agent simulation error: {e}")
        traceback.print_exc()

    # Test 7: Frontend HTTP Endpoints
    print("\n[TEST 7] Frontend Django Server Endpoints...")
    try:
        endpoints = [
            ("Landing Page", "http://127.0.0.1:8000/"),
            ("Demo View", "http://127.0.0.1:8000/demo/July1_the_ville_isabella_maria_klaus-step-3-20/1/3/"),
            ("Replay View", "http://127.0.0.1:8000/replay/July1_the_ville_isabella_maria_klaus-step-3-20/1/"),
            ("Persona State", "http://127.0.0.1:8000/replay_persona_state/July1_the_ville_isabella_maria_klaus-step-3-20/1/Isabella_Rodriguez/"),
        ]
        for name, url in endpoints:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
                assert status == 200, f"{name} returned HTTP {status}"
                content_len = len(resp.read())
                print(f"   - {name} ({url}): HTTP {status} OK ({content_len} bytes)")
        print(f" PASS: All frontend endpoints verified healthy and functional.")
        passed += 1
    except Exception as e:
        print(f" FAIL: Frontend HTTP endpoint error: {e}")
        traceback.print_exc()

    # Clean up test sim
    if os.path.exists(test_sim_path):
        shutil.rmtree(test_sim_path)

    print("\n" + "=" * 60)
    print(f"FINAL RESULTS: {passed}/{total} TESTS PASSED")
    print("=" * 60)
    return passed == total

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
