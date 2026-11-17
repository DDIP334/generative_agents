# Attribution & Project Provenance

This project builds upon pioneering open-source research and incorporates open-source tools, assets, and libraries. This document provides clear and transparent attribution to all original creators, research contributors, and asset authors.

---

## 1. Original Project Attribution

- **Original Research Title:** *Generative Agents: Interactive Simulacra of Human Behavior*
- **Authors & Researchers:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein
- **Affiliations:** Stanford University & Google Research
- **Publication:** Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST '23), October 2023
- **Paper URL:** [https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)
- **Original Code Repository:** [https://github.com/joonspk-research/generative_agents](https://github.com/joonspk-research/generative_agents)
- **Original Copyright:** Copyright 2023 Joon Sung Park
- **Original License:** Apache License, Version 2.0 (see [LICENSE](file:///d:/Project/generative_agents/LICENSE))

The core cognitive architecture (associative memory stream, reflection, planning, spatial memory tree, and reverie server) is the intellectual property of the original authors.

---

## 2. 2026 Modifications & Enhancements

Modified and expanded in 2026 by project contributors. Key enhancements include:

1. **16-Bit Retro Pixel-Art User Interface:**
   - Designed and engineered a complete retro 16-bit pixel-art interface inspired by classic SNES/GBA RPG interfaces.
   - Replaced modern glassmorphic panels with warm wood/parchment pixel-bordered frames, 3D beveled buttons with pressed animation states, segmented need meters, and retro RPG dialogue boxes.
   - Integrated open-source pixel typography (`Press Start 2P`, `Silkscreen`, `Pixelify Sans`).
2. **God Simulator Mode & Divine Command System:**
   - Implemented a natural-language **"GOD'S COMMAND"** NLP console allowing free-form English instructions to control individual citizens or the entire town.
   - Built a dedicated **God Mode World Authority Drawer** for real-time control of simulation speed, celestial time scrubbing, seasons, weather, town food reserves, treasury, and world cataclysms.
   - Implemented direct citizen interventions (instant gifts, fines, forced actions, click-to-move tile target reticle, and divine blessings).
   - Designed an on-demand clean observer UI where inspector panels slide out only on resident selection and dismiss when clicking empty ground.
3. **Living 2D AI Society Simulation:**
   - Implemented real-time autonomous simulation for 15 Smallville citizens with dynamic utility AI modeling 6 vital needs (Hunger, Energy, Health, Happiness, Hygiene, Social).
   - Embedded a pre-computed zero-latency BFS pathfinding engine traversing 4,158 validated walkable tiles on the 140x100 Smallville map.
   - Added proximity comic speech bubbles, town economy circulation, and dynamic day/night ambient daylight filtering.
4. **3D Autonomous Robot Navigation Lab (`/3d/`):**
   - Implemented an interactive Three.js 3D simulation of an autonomous robot navigating a 3D maze using multi-ray LiDAR sensor perception, collision detection, and reinforcement learning.
5. **Runtime Fixes & Fail-Safe Resilience:**
   - Resolved environment working directory discrepancies and missing movement log directories.
   - Fixed spatial memory address lookups (`KeyError: 'kitchen'`) and provided local mock LLM fallbacks for 100% offline reliability.
   - Built an automated 7-part test suite and end-to-end Selenium browser test runners.

---

## 3. Third-Party Software & Asset Attribution

| Component | Author / Project | License | Purpose in Project |
| :--- | :--- | :--- | :--- |
| **Phaser 3** (`v3.55.2`) | Richard Davey (Photon Storm Ltd) | MIT License | 2D game canvas rendering, sprite animations, camera control, and tilemap layers |
| **Three.js** (`r128`) | Ricardo Cabello (mrdoob) | MIT License | 3D autonomous robot lab rendering, scene lighting, and mesh geometry |
| **Chart.js** (`v3.9.1`) | Chart.js Contributors | MIT License | Real-time society analytics (happiness, health, business revenues) |
| **Press Start 2P** | CodeMan38 | SIL Open Font License, 1.1 | Retro 8-bit arcade headers, badges, and button labels |
| **Silkscreen** | Jason Kottke | SIL Open Font License, 1.1 | 16-bit retro UI labels, dialog prompts, and numbers |
| **Pixelify Sans** | Stefie Justprince | SIL Open Font License, 1.1 | Readable retro pixel typography for thoughts, bios, and descriptions |
| **CuteRPG Tilesets** | Original Game Assets | Academic / Educational Use | 2D tilemap visuals for Smallville terrain and interiors |
| **Django** (`2.2.x`) | Django Software Foundation | 3-Clause BSD License | Backend web server, URL routing, and template rendering |

For complete license texts of third-party dependencies, see [THIRD_PARTY_LICENSES.md](file:///d:/Project/generative_agents/THIRD_PARTY_LICENSES.md).
