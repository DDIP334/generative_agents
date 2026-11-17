# Changelog

All notable changes to this project are documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/) and follows [Keep a Changelog](https://keepachangelog.com/).

The original baseline for this repository is the research code for **"Generative Agents: Interactive Simulacra of Human Behavior"** (Park et al., Stanford University & Google Research, 2023), originally distributed under the Apache License 2.0.

---

## [5.0.0] - 2026-11-16

### Added
- **16-Bit Retro Pixel-Art UI Design System:**
  - Complete visual overhaul of all UI menus, HUD overlays, cards, buttons, and progress indicators into a cohesive retro 16-bit pixel-art style inspired by classic SNES/GBA RPG interfaces.
  - Integration of authentic open-source pixel typography: Google Fonts `'Press Start 2P'`, `'Silkscreen'`, and `'Pixelify Sans'`.
  - Custom pixel-art beveled button classes (`.pixel-btn-green`, `.pixel-btn-orange`, `.pixel-btn-red`, `.pixel-btn-gold`, `.pixel-btn-wood`, `.pixel-btn-blue`) with 3D bevels, pressed states (`transform: translateY(3px)`), and pixel border outlines.
  - Segmented retro need bars with repeating block ticks for Hunger, Energy, Health, Happiness, Hygiene, and Social.
  - Warm retro color palette based on warm wood/parchment (`#df9b6d`, `#63331d`, `#3b1d10`, `#26140e`), cream highlights (`#fffbeb`), and vibrant 16-bit arcade action accents.
  - D-pad style retro camera zoom controls (`+`, `-`, `↻`).
  - Pixel-art character avatar frames with gold bevel borders.
  - Retro speech and thought message bubbles with cream backgrounds, chunky dark borders, and pixelated quotation styling.
- **GitHub Attribution & Open-Source Compliance Files:**
  - Added `ATTRIBUTION.md` with detailed provenance for Stanford University / Google Research generative agents, third-party libraries, and newly authored components.
  - Added `NOTICE` complying with Apache License 2.0 Section 4(d).
  - Added `THIRD_PARTY_LICENSES.md` documenting licenses for Phaser 3, Chart.js, Google Fonts, Selenium, and tilesets.
  - Added `CHANGELOG.md` providing an exhaustive versioned history of modifications.
  - Added Apache-2.0 modification notice headers to modified source files.

### Changed
- Converted all modern CSS cards and glassmorphism elements in `living_society.html` and standalone `living_society_simulation.html` to crisp pixel-art panels.
- Re-styled the top HUD status ribbon, citizen roster drawer, deep inspector HUD, God's Command console, and God Powers modal to pixel-perfect styling.

---

## [4.0.0] - 2026-11-16

### Added
- **God Simulator Mode & Divine Command System:**
  - Built natural-language **"GOD'S COMMAND"** NLP execution console at bottom-center allowing free-text commands (e.g. *"Make Isabella go to cafe"*, *"Give Klaus 500 coins"*, *"Make it rain"*, *"Gather everyone at Johnson Park"*, *"Make everyone go to sleep"*).
  - Real-time command interpreter with intent extraction, entity targeting (single citizens, groups, all), and visual feedback alerts (`[DIVINE WILL] -> [STATUS] -> [OUTCOME]`).
  - **God Mode World Authority Drawer (`👑 God Powers`):**
    - Simulation speed control (`0.5x`, `1x`, `2x`, `5x`, `10x`).
    - 24-hour Celestial Time scrub slider (`00:00` to `23:59`) and presets (*Dawn 06:00, Noon 12:00, Sunset 18:00, Midnight 00:00*).
    - Season selector (*Spring, Summer, Autumn, Winter*) and daylight override (*Auto, Force Day, Force Night*).
    - Weather manipulation engine (*Sunny, Rain, Storm, Snow, Drought, Overcast*).
    - Town economic levers (*Town Food Reserves +50/-50/Famine, Town Treasury stimulus/panic*).
    - One-click cataclysms and town events (*Town Festival, Community Gathering, Curfew, Morning Rush*).
  - **Direct Citizen Interventions in Inspector:**
    - Instant monetary gifts/fines (`+$100`, `-$50`).
    - Divine blessing restoring 100% of all 6 vital needs.
    - Forced navigation commands (*Work, Home, Cafe, Park, Sleep*).
    - Interactive **Click-to-Move Target Reticle** on Phaser canvas.
    - Dual mode state machine: `🤖 Autonomous AI Mode` vs `⚡ Divine Intervention Mode` (agents temporarily execute divine orders then resume autonomous routines).
  - **Weather Particle Canvas Overlay:**
    - 60 FPS HTML5 Canvas engine rendering angled raindrop streaks, wind-drifting snowflakes, and lightning flash screen pulses.
- **Clean Observer UI:**
  - Roster and Inspector panels hidden by default for an unobstructed fullscreen view of Smallville.
  - Inspector appears only upon clicking a resident sprite; closes when clicking empty canvas tiles or close button.

---

## [3.0.0] - 2026-11-15

### Added
- **Living 2D AI Society in Smallville:**
  - Integrated 15 fully articulated citizen personas from Stanford's original generative agents research (Isabella Rodriguez, Klaus Mueller, Maria Lopez, Arthur Burton, John Lin, Mei Lin, Eddy Lin, Giorgio Rossi, Tom Moreno, Jane Moreno, Sam Moore, Abigail Chen, Carlos Gomez, Hailey Johnson, Francisco Lopez).
  - Mapped 222 interactive furniture and utility objects across 10 depth layers on the 140x100 tilemap (`the_ville_jan7.json`).
  - Zero-latency BFS pathfinding running against pre-computed collision grid `the_ville_collision_grid.json` (4,158 validated walkable tiles).
  - Dynamic Utility AI modeling 6 vital needs (Hunger, Energy, Health, Happiness, Hygiene, Social).
  - Proximity comic speech bubbles triggering contextual conversations when citizens are within 3 tiles of each other.
  - Town economy loop: salaries paid for work shifts, spending at Hobbs Cafe and Rose & Crown Pub, and crop harvests by farmer Giorgio Rossi.
  - Interactive day/night ambient lighting transitions matching real simulation clock.
  - Town Analytics Dashboard powered by Chart.js tracking average happiness, health, and business revenues.

---

## [2.0.0] - 2026-11-15

### Added
- **3D Autonomous Robot Navigation Lab (`/3d/`):**
  - Interactive 3D simulation with Three.js rendering an autonomous mobile robot in a complex maze.
  - 5-ray multi-directional LiDAR distance sensors with dynamic raycast visualization.
  - Reinforcement Learning / Q-Learning agent with collision avoidance, goal attraction, and dynamic reward telemetry.
  - Real-time HUD displaying episode count, total steps, reward velocity, distance to destination, and LiDAR sensor readouts.
  - Offline standalone simulation bundle in `robot_3d_simulation.html`.

---

## [1.0.0] - 2026-11-15

### Fixed
- **Runtime Discrepancies & Path Resolution:**
  - Resolved `FileNotFoundError: storage` by anchoring working directory in `manage.py`.
  - Added automatic directory creation (`os.makedirs(..., exist_ok=True)`) in `reverie.py` for movement step logs.
  - Fixed spatial address lookup exceptions (`KeyError: 'kitchen'`) in `run_gpt_prompt.py` through persona spatial tree validation.
  - Added resilient local mock fallbacks for LLM completions to allow full offline operation without OpenAI API keys.
- **Dependency & Environment Setup:**
  - Configured Python 3.9 virtual environment (`.venv`) with verified pinned dependencies (`Django==2.2`, `numpy`, `selenium`).
  - Created automated 7-part test suite in `test_simulation_suite.py` verifying persona cognitive functions, spatial trees, BFS pathfinder, maze loading, and server responsiveness.
