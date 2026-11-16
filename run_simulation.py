"""
Generative Agents All-in-One Simulation Runner
Allows launching the frontend server, running simulation steps, running the verification suite, or serving demo replays.

Usage:
  python run_simulation.py --server                      # Start environment frontend server on port 8000
  python run_simulation.py --test                        # Run the 7-part comprehensive test suite
  python run_simulation.py --steps 3                     # Run 3 simulation steps with Isabella, Maria & Klaus
  python run_simulation.py --fork <base> --sim <target>  # Fork a custom simulation
  python run_simulation.py --demo                        # Open demo replay instructions
"""

import os
import sys
import argparse
import subprocess
import time
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "environment", "frontend_server")
BACKEND_DIR = os.path.join(ROOT_DIR, "reverie", "backend_server")
VENV_PYTHON = os.path.join(ROOT_DIR, ".venv", "Scripts", "python.exe")

if not os.path.exists(VENV_PYTHON):
    VENV_PYTHON = sys.executable

def start_frontend(port=8000):
    print(f"[*] Starting Django environment frontend server on port {port}...")
    manage_py = os.path.join(FRONTEND_DIR, "manage.py")
    cmd = [VENV_PYTHON, manage_py, "runserver", f"127.0.0.1:{port}"]
    proc = subprocess.Popen(cmd, cwd=FRONTEND_DIR)
    print(f"[*] Frontend server running (PID {proc.pid}). Open: http://127.0.0.1:{port}/")
    return proc

def run_simulation(fork_sim, target_sim, steps=1):
    print(f"[*] Initializing simulation '{target_sim}' forked from '{fork_sim}'...")
    sys.path.insert(0, BACKEND_DIR)
    os.chdir(BACKEND_DIR)
    
    import utils
    from reverie import ReverieServer
    
    target_storage = os.path.join(FRONTEND_DIR, "storage", target_sim)
    if os.path.exists(target_storage):
        print(f"[*] Removing existing storage folder for '{target_sim}'...")
        shutil.rmtree(target_storage)
        
    rs = ReverieServer(fork_sim, target_sim)
    print(f"[*] Loaded world with {len(rs.personas)} agents: {list(rs.personas.keys())}")
    print(f"[*] Advancing simulation by {steps} steps ({steps * rs.sec_per_step} seconds game time)...")
    
    for s in range(steps):
        print(f" -> Computing step {rs.step}...")
        rs.start_server(1)
        # Advance environment state for autonomous progression
        next_env = {}
        for p_name, persona in rs.personas.items():
            curr_pos = rs.personas_tile[p_name]
            next_env[p_name] = {"x": curr_pos[0], "y": curr_pos[1], "maze": rs.maze.maze_name}
        
        env_file = os.path.join(target_storage, "environment", f"{rs.step}.json")
        os.makedirs(os.path.dirname(env_file), exist_ok=True)
        import json
        with open(env_file, "w") as f:
            json.dump(next_env, f, indent=2)

    print(f"[+] Simulation reached step {rs.step} ({rs.curr_time}) successfully!")
    print(f"[*] Simulation data saved to: {target_storage}")

def main():
    parser = argparse.ArgumentParser(description="Generative Agents Simulation Runner")
    parser.add_argument("--test", action="store_true", help="Run full test suite")
    parser.add_argument("--server", action="store_true", help="Start frontend server")
    parser.add_argument("--steps", type=int, default=1, help="Number of steps to simulate")
    parser.add_argument("--fork", type=str, default="base_the_ville_isabella_maria_klaus", help="Fork simulation name")
    parser.add_argument("--sim", type=str, default="auto_simulation_run", help="Target simulation name")
    parser.add_argument("--demo", action="store_true", help="Print demo URLs")
    args = parser.parse_args()

    if args.test:
        test_py = os.path.join(ROOT_DIR, "test_simulation_suite.py")
        subprocess.run([VENV_PYTHON, test_py], check=True)
        return

    if args.demo:
        print("\n=== AVAILABLE PRE-SIMULATED REPLAYS & DEMOS ===")
        print("1. Interactive Demo (Phaser visuals):")
        print("   http://127.0.0.1:8000/demo/July1_the_ville_isabella_maria_klaus-step-3-20/1/3/")
        print("2. Replay Mode:")
        print("   http://127.0.0.1:8000/replay/July1_the_ville_isabella_maria_klaus-step-3-20/1/")
        print("3. Persona Internal State Inspector:")
        print("   http://127.0.0.1:8000/replay_persona_state/July1_the_ville_isabella_maria_klaus-step-3-20/1/Isabella_Rodriguez/")
        print("4. Live Simulation Frontend:")
        print("   http://127.0.0.1:8000/simulator_home\n")
        return

    if args.server:
        proc = start_frontend()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            proc.terminate()
            print("\n[*] Frontend server stopped.")
        return

    run_simulation(args.fork, args.sim, steps=args.steps)

if __name__ == '__main__':
    main()
