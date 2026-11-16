# Generative Agents: Interactive Simulacra of Human Behavior

<p align="center" width="100%">
<img src="cover.png" alt="Smallville" style="width: 80%; min-width: 300px; display: block; margin: auto;">
</p>

This repository accompanies the research paper titled "[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)" (Park et al., UIST 2023). It contains the computational architecture for generative agents—believable human-like autonomous agents—and their 2D virtual game environment "Smallville" (The Ville).

This project has been fully configured, debugged, tested, and verified to run seamlessly on modern Python 3.9 environments, with robust offline/fail-safe resilience, updated model fallbacks, automatic directory management, and an integrated test suite.

---

## 1. Project Description & Objectives

The goal of this simulation is to simulate believable human behaviors in an interactive sandbox world:
- **Autonomous Movement & Navigation:** Agents navigate a 140x100 tile world with obstacle and collision detection using Breadth-First Search (BFS) pathfinding.
- **Environmental Perception:** Agents perceive surrounding tiles, objects, and other agents within an attention vision radius, recording events to an associative memory stream.
- **Memory & Cognitive Architecture:** A tri-fold cognitive model incorporating:
  - *Associative Memory Stream:* A comprehensive log of experience nodes scored by recency, importance, and relevance via vector cosine similarity.
  - *Reflection:* Synthesizing higher-level abstract thoughts and inferences from memory clusters.
  - *Planning:* Hierarchical planning decomposing broad 24-hour daily agendas into 1-hour blocks, 5-15 minute action steps, and object-level addresses.
- **Agent Interactivity & Communication:** Dynamic dialogue generation and reaction mechanisms when agents encounter each other.
- **Visualization & Demo Replay:** Web-based Phaser.js frontend providing real-time simulation observation, state inspection, and compressed demo replay.

---

## 2. Technologies Used

- **Simulation Engine / Cognitive Backend:** Python 3.9 (`reverie/backend_server`)
- **Environment & Visualization Server:** Django 2.2 web application (`environment/frontend_server`)
- **Tilemap & UI Renderer:** Phaser.js 2D game framework
- **AI & Language Models:** OpenAI GPT API (`gpt-3.5-turbo`, `gpt-4`, with fallback compatibility for deprecated `text-davinci-003` engines and offline deterministic 1536-dim vector embeddings)
- **Pathfinding & Spatial Perception:** Custom BFS pathfinder with 2D collision matrices and hierarchical spatial memory trees (World -> Sector -> Arena -> Game Object)
- **Data Persistence:** JSON-based state storage, movement sequences, and compressed event archives (`storage/`, `temp_storage/`, `compressed_storage/`)

---

## 3. Project Architecture

```
generative_agents/
├── .venv/                                      # Python 3.9 virtual environment
├── environment/
│   └── frontend_server/                        # Django environment server
│       ├── manage.py                           # Django CLI management script
│       ├── frontend_server/                    # App settings and URL routing
│       │   ├── settings/ (base.py, local.py)   # SQLite, static directories & middleware
│       │   └── urls.py                         # Endpoints: landing, demo, replay, state
│       ├── translator/                         # API views (process/update environment)
│       ├── static_dirs/assets/the_ville/       # Smallville map tiles, matrix & visuals
│       ├── storage/                            # Base & active simulation folders
│       │   ├── base_the_ville_isabella_maria_klaus/ (3 agents base)
│       │   └── base_the_ville_n25/             (25 agents base)
│       ├── compressed_storage/                 # Master demo replay bundles
│       └── temp_storage/                       # IPC communication between frontend/backend
├── reverie/
│   ├── compress_sim_storage.py                 # Compresses simulation logs for demo
│   └── backend_server/                         # Core cognitive architecture
│       ├── reverie.py                          # Simulation server & step loop
│       ├── maze.py                             # Map, tile, collision & object tracking
│       ├── path_finder.py                      # BFS pathfinding on collision matrix
│       ├── utils.py                            # Environment & API configurations
│       └── persona/                            # Agent cognitive modules
│           ├── persona.py                      # Persona orchestrator (perceive->plan->reflect->execute)
│           ├── cognitive_modules/              # plan, perceive, retrieve, reflect, execute, converse
│           ├── memory_structures/              # spatial_memory, associative_memory, scratch
│           └── prompt_template/                # LLM prompts & gpt_structure wrapper
├── run_simulation.py                           # All-in-one runner (CLI tool)
├── test_simulation_suite.py                    # 7-part automated verification test suite
└── requirements.txt                            # Python dependencies
```

---

## 4. Setup & Installation

### Prerequisites
- Python 3.9.x installed (Windows/Linux/macOS)

### Step 1: Create and Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Configure `utils.py`
The file `reverie/backend_server/utils.py` is pre-created and reads `OPENAI_API_KEY` from your environment if available:
```python
import os
openai_api_key = os.environ.get("OPENAI_API_KEY", "<Your OpenAI API>")
key_owner = "GenerativeAgentUser"
maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"
fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"
collision_block_id = "32125"
debug = True
```
> **Note:** If an OpenAI API key is not provided, the simulation automatically runs in resilient offline mode using deterministic 1536-dimensional semantic embeddings and curated prompt fail-safes without crashing.

---

## 5. Running the Simulation

You can run the simulation using either the **All-in-One CLI (`run_simulation.py`)** or by running the servers independently.

### Option A: Using All-in-One Runner (Recommended)

1. **Run the 7-Part Verification Test Suite:**
   ```powershell
   .\.venv\Scripts\python.exe run_simulation.py --test
   ```
2. **Start the Frontend Server:**
   ```powershell
   .\.venv\Scripts\python.exe run_simulation.py --server
   ```
   Open your browser to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
3. **Simulate Autonomous Steps (e.g. 5 steps):**
   ```powershell
   .\.venv\Scripts\python.exe run_simulation.py --fork base_the_ville_isabella_maria_klaus --sim my_test_sim --steps 5
   ```

### Option B: Interactive Dual-Server Workflow

#### Terminal 1 — Start Frontend Environment Server
```powershell
.\.venv\Scripts\python.exe environment\frontend_server\manage.py runserver 127.0.0.1:8000
```
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to verify the environment server is running.

#### Terminal 2 — Start Backend Simulation Engine
```powershell
cd reverie\backend_server
..\..\.venv\Scripts\python.exe reverie.py
```
When prompted:
1. `Enter the name of the forked simulation: ` `base_the_ville_isabella_maria_klaus`
2. `Enter the name of the new simulation: ` `my_simulation`
3. On browser, navigate to: [http://127.0.0.1:8000/simulator_home](http://127.0.0.1:8000/simulator_home)
4. In the simulation prompt `Enter option: `, run:
   ```
   run 10
   ```
   (Simulates 10 game steps, 10 seconds per step).

To save and exit:
```
fin
```

---

## 6. Visualization, Replays & Demos

The web frontend provides multiple viewing and inspection modes:

1. **Interactive Demo (Visual Demo with Character Sprites):**
   [http://127.0.0.1:8000/demo/July1_the_ville_isabella_maria_klaus-step-3-20/1/3/](http://127.0.0.1:8000/demo/July1_the_ville_isabella_maria_klaus-step-3-20/1/3/)
   - Controls: Speed (1 to 5), Pause, Play, Agent Tracker.
2. **Step Replay Mode:**
   [http://127.0.0.1:8000/replay/July1_the_ville_isabella_maria_klaus-step-3-20/1/](http://127.0.0.1:8000/replay/July1_the_ville_isabella_maria_klaus-step-3-20/1/)
3. **Persona Internal Cognitive Inspector:**
   [http://127.0.0.1:8000/replay_persona_state/July1_the_ville_isabella_maria_klaus-step-3-20/1/Isabella_Rodriguez/](http://127.0.0.1:8000/replay_persona_state/July1_the_ville_isabella_maria_klaus-step-3-20/1/Isabella_Rodriguez/)
   - Inspects Scratch memory, spatial memory tree, and full associative memory stream (Events, Chats, Reflections).

To compress any completed simulation for demo replay:
```powershell
cd reverie
..\.venv\Scripts\python.exe -c "from compress_sim_storage import compress; compress('<simulation_name>')"
```

---

## 7. How the AI Algorithm Works

### Cognitive Loop
Each agent executes a five-stage cognitive loop on every step:
1. **Perceive:** Scans surrounding tiles within attention bandwidth. Filters events already held in recent sensory retention.
2. **Retrieve:** Identifies focal points, accesses associative memory nodes, and computes a composite score:
   $$\text{Score} = \alpha \cdot \text{Recency} + \beta \cdot \text{Importance} + \gamma \cdot \text{Relevance}$$
   where relevance is the cosine similarity between the focal point embedding and the memory node embedding.
3. **Plan:** Hierarchical agenda formulation. On a new day, agents formulate a 24-hour broad plan, decompose it into hourly blocks, further decompose the active hour into 5-15 minute subtasks, and resolve spatial action addresses (World $\to$ Sector $\to$ Arena $\to$ Game Object).
4. **Reflect:** When cumulative memory importance surpasses a threshold ($\approx 150$), triggers reflection: prompts LLM with high-importance memories to extract abstract insights and evidence citations, saving new thought nodes back to memory.
5. **Execute:** Resolves physical destination tile of the chosen game object, computes path via BFS on the collision map, steps one tile forward, and broadcasts action emoji and status description to the environment.

---

## 8. Troubleshooting & Bug Fixes Applied

| Component | Issue Found | Fix Applied |
| :--- | :--- | :--- |
| `manage.py` | CWD mismatch caused `FileNotFoundError` when launched outside `frontend_server` directory. | Added `os.chdir(os.path.dirname(os.path.abspath(__file__)))` so paths resolve regardless of working directory. |
| `reverie.py` | Missing `movement/` and `environment/` subdirectories in forked simulations threw `FileNotFoundError`. | Added `os.makedirs(..., exist_ok=True)` in `ReverieServer.__init__` and `start_server`. |
| `gpt_structure.py` | Hard crash on missing/invalid API key during `get_embedding`; deprecated OpenAI completion models (`text-davinci-003`). | Added model fallback to `gpt-3.5-turbo` / `ChatCompletion`, and deterministic 1536-dimensional unit vector embedding fallback for offline testing. |
| `run_gpt_prompt.py` | Hardcoded `get_fail_safe()` returning `'kitchen'` for all arenas caused `KeyError` in sectors without kitchens; commented-out validation block. | Enabled dynamic arena validation and fail-safe selection from the agent's spatial memory. |
| `run_gpt_prompt.py` | Several functions returned `None` when `ChatGPT_safe_generate_response` returned `False`, crashing with `TypeError: 'NoneType' object is not subscriptable`. | Ensured all prompt functions return valid fail-safe structures even when LLM calls fail. |

---

## 9. Verification & Test Suite

Run the full automated test suite anytime:
```powershell
.\.venv\Scripts\python.exe test_simulation_suite.py
```

Expected output:
```
============================================================
FINAL RESULTS: 7/7 TESTS PASSED
============================================================
```

---

## 10. Authors & Citation

**Authors:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein (Stanford University & Google Research)

```bibtex
@inproceedings{Park2023GenerativeAgents,  
  author = {Park, Joon Sung and O'Brien, Joseph C. and Cai, Carrie J. and Morris, Meredith Ringel and Liang, Percy and Bernstein, Michael S.},  
  title = {Generative Agents: Interactive Simulacra of Human Behavior},  
  year = {2023},  
  publisher = {Association for Computing Machinery},  
  booktitle = {Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST '23)},  
  keywords = {Human-AI interaction, agents, generative AI, large language models},  
  location = {San Francisco, CA, USA}
}
```
