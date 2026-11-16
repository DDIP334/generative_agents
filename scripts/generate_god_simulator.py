import os
import json

# Output template path
TEMPLATE_PATH = r"D:\Project\generative_agents\environment\frontend_server\templates\living_society\living_society.html"
STANDALONE_PATH = r"D:\Project\generative_agents\living_society_simulation.html"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Smallville — 2D Living AI Society & Divine God Simulator</title>
  <!-- Phaser 3 -->
  <script src="https://cdn.jsdelivr.net/npm/phaser@3.55.2/dist/phaser.min.js"></script>
  <!-- Chart.js for real-time town analytics -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
  <style>
    :root {
      --bg-dark: #070a12;
      --card-bg: rgba(13, 20, 36, 0.92);
      --card-border: rgba(56, 189, 248, 0.28);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-hover: #0284c7;
      --gold: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.4);
      --divine-purple: #a855f7;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }

    body {
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      overflow: hidden;
      width: 100vw;
      height: 100vh;
    }

    /* Fullscreen Game Canvas */
    #game-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
      background: #0f172a;
    }

    #game-container canvas {
      display: block;
      width: 100% !important;
      height: 100% !important;
    }

    /* Weather Canvas Overlay (Rain, Snow, Lightning) */
    #weather-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 2;
    }

    /* Ambient Lighting Overlay (Day/Night & Drought Tint) */
    #ambient-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 3;
      transition: background-color 1.5s ease-in-out;
    }

    /* Screen Flash Overlay for Lightning & Cataclysms */
    #flash-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 4;
      background: rgba(255, 255, 255, 0);
      transition: background-color 0.08s ease;
    }

    /* ==========================================================================
       TOP STATUS BAR & NAVIGATION
       ========================================================================== */
    .top-bar {
      position: absolute;
      top: 12px;
      left: 16px;
      right: 16px;
      height: 56px;
      background: rgba(13, 20, 36, 0.94);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 0 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 20;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.65);
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-badge {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--gold);
      box-shadow: 0 0 10px var(--gold);
      animation: divinePulse 1.8s infinite;
    }

    @keyframes divinePulse {
      0% { transform: scale(0.9); opacity: 0.8; box-shadow: 0 0 8px var(--gold); }
      50% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 16px #eab308; }
      100% { transform: scale(0.9); opacity: 0.8; box-shadow: 0 0 8px var(--gold); }
    }

    .brand-title {
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: -0.2px;
      background: linear-gradient(135deg, #f8fafc 0%, #38bdf8 50%, #f59e0b 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .brand-subtitle {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* Simulation Clock & Speed Controls */
    .clock-section {
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(30, 41, 59, 0.75);
      padding: 5px 14px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .clock-display {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      font-size: 1rem;
      color: #f1f5f9;
      font-variant-numeric: tabular-nums;
    }

    .weather-badge {
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 0.8rem;
      color: #cbd5e1;
      padding: 3px 8px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 6px;
    }

    .season-badge {
      font-size: 0.75rem;
      color: #a78bfa;
      font-weight: 600;
      padding: 2px 6px;
      background: rgba(168, 85, 247, 0.15);
      border-radius: 4px;
    }

    .time-ctrl-btn {
      background: #1e293b;
      border: 1px solid #475569;
      color: #cbd5e1;
      padding: 4px 9px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }

    .time-ctrl-btn:hover, .time-ctrl-btn.active {
      background: var(--gold);
      color: #090d16;
      border-color: var(--gold);
      font-weight: 700;
    }

    /* Top Action Buttons */
    .top-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-action-nav {
      background: #1e293b;
      border: 1px solid #334155;
      color: #e2e8f0;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      text-decoration: none !important;
    }

    .btn-action-nav:hover {
      background: #334155;
      border-color: var(--accent);
      color: var(--accent);
    }

    .btn-god-powers {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%);
      border: 1px solid #f59e0b;
      color: #fde047;
      font-weight: 700;
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.25);
    }

    .btn-god-powers:hover {
      background: linear-gradient(135deg, #f59e0b 0%, #a855f7 100%);
      color: #090d16;
      border-color: #fde047;
      box-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
    }

    .btn-command-toggle {
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.25) 0%, rgba(14, 165, 233, 0.2) 100%);
      border: 1px solid #38bdf8;
      color: #38bdf8;
      font-weight: 700;
    }

    .btn-command-toggle:hover {
      background: #38bdf8;
      color: #090d16;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
    }

    /* ==========================================================================
       LEFT ROSTER PANE (COLLAPSIBLE / DRAWER)
       ========================================================================== */
    .left-roster-pane {
      position: absolute;
      top: 78px;
      left: 16px;
      width: 290px;
      bottom: 70px;
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      z-index: 15;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
      transform: translateX(-340px);
      opacity: 0;
      pointer-events: none;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
    }

    .left-roster-pane.open {
      transform: translateX(0);
      opacity: 1;
      pointer-events: all;
    }

    .pane-header {
      padding: 12px 14px 10px 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .pane-title {
      font-size: 0.88rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--accent);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .btn-close-pane {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.1rem;
      cursor: pointer;
      padding: 2px 6px;
      border-radius: 4px;
    }

    .btn-close-pane:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }

    .roster-count {
      font-size: 0.74rem;
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent);
      padding: 2px 7px;
      border-radius: 10px;
      font-weight: 700;
    }

    .roster-filter-tabs {
      display: flex;
      gap: 4px;
      padding: 8px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .roster-tab {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 4px 7px;
      border-radius: 4px;
      cursor: pointer;
    }

    .roster-tab.active {
      background: #334155;
      color: var(--text-main);
    }

    .roster-list {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .roster-list::-webkit-scrollbar { width: 4px; }
    .roster-list::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }

    .citizen-card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      padding: 7px 9px;
      display: flex;
      align-items: center;
      gap: 9px;
      cursor: pointer;
      transition: all 0.18s ease;
    }

    .citizen-card:hover {
      background: rgba(51, 65, 85, 0.85);
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateX(2px);
    }

    .citizen-card.selected {
      background: rgba(2, 132, 199, 0.3);
      border-color: var(--accent);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
    }

    .citizen-card.divine-controlled {
      border-color: var(--gold);
      box-shadow: 0 0 12px var(--gold-glow);
    }

    .citizen-avatar-wrapper {
      position: relative;
      width: 38px;
      height: 38px;
      flex-shrink: 0;
    }

    .citizen-avatar {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      border: 2px solid var(--accent);
      background: #1e293b;
      object-fit: cover;
    }

    .citizen-card.divine-controlled .citizen-avatar {
      border-color: var(--gold);
    }

    .citizen-status-dot {
      position: absolute;
      bottom: -1px;
      right: -1px;
      width: 9px;
      height: 9px;
      border-radius: 50%;
      border: 2px solid #0f172a;
    }

    .status-work { background: #38bdf8; }
    .status-home { background: #10b981; }
    .status-eat { background: #f59e0b; }
    .status-social { background: #a855f7; }
    .status-sleep { background: #64748b; }
    .status-divine { background: #eab308; }

    .citizen-info {
      flex: 1;
      min-width: 0;
    }

    .citizen-name-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2px;
    }

    .citizen-name {
      font-size: 0.82rem;
      font-weight: 700;
      color: #f1f5f9;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .citizen-job {
      font-size: 0.7rem;
      color: var(--text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 3px;
    }

    .citizen-mini-bar {
      width: 100%;
      height: 3px;
      background: #1e293b;
      border-radius: 2px;
      overflow: hidden;
    }

    .citizen-mini-fill {
      height: 100%;
      background: var(--success);
      border-radius: 2px;
      transition: width 0.3s;
    }

    /* ==========================================================================
       RIGHT DEEP INSPECTOR HUD (SLIDE-OUT ON AGENT CLICK ONLY)
       ========================================================================== */
    .right-inspector-pane {
      position: absolute;
      top: 78px;
      right: 16px;
      width: 380px;
      bottom: 70px;
      background: var(--card-bg);
      backdrop-filter: blur(18px);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      z-index: 15;
      box-shadow: 0 14px 44px rgba(0, 0, 0, 0.65);
      overflow-y: auto;
      padding: 16px;
      gap: 12px;
      transform: translateX(440px);
      opacity: 0;
      pointer-events: none;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
    }

    .right-inspector-pane.open {
      transform: translateX(0);
      opacity: 1;
      pointer-events: all;
    }

    .right-inspector-pane::-webkit-scrollbar { width: 4px; }
    .right-inspector-pane::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }

    .inspector-header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .inspector-mode-pill {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .mode-autonomous {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .mode-divine {
      background: rgba(245, 158, 11, 0.2);
      color: #fde047;
      border: 1px solid #f59e0b;
      box-shadow: 0 0 10px rgba(245, 158, 11, 0.3);
    }

    .inspector-profile-header {
      display: flex;
      gap: 12px;
      align-items: center;
      background: rgba(30, 41, 59, 0.75);
      padding: 12px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .inspector-avatar {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      border: 2px solid var(--accent);
      background: #1e293b;
      object-fit: cover;
    }

    .inspector-bio {
      flex: 1;
      min-width: 0;
    }

    .inspector-bio h2 {
      font-size: 1.1rem;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 2px;
    }

    .inspector-bio p {
      font-size: 0.75rem;
      color: var(--text-muted);
      line-height: 1.3;
    }

    .cam-shortcuts-row {
      display: flex;
      gap: 5px;
      margin-top: 6px;
      flex-wrap: wrap;
    }

    .btn-cam-shortcut {
      background: #1e293b;
      border: 1px solid #475569;
      color: #cbd5e1;
      border-radius: 4px;
      padding: 3px 7px;
      font-size: 0.68rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }

    .btn-cam-shortcut:hover, .btn-cam-shortcut.active {
      background: var(--accent);
      color: #090d16;
      border-color: var(--accent);
    }

    /* Active Internal Thought Callout */
    .thought-bubble-card {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 10px;
      padding: 10px 12px;
      position: relative;
    }

    .thought-label {
      font-size: 0.7rem;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .thought-text {
      font-size: 0.82rem;
      color: #f1f5f9;
      line-height: 1.4;
      font-style: italic;
    }

    .thought-location {
      font-size: 0.7rem;
      color: var(--text-muted);
      margin-top: 5px;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* Divine Interventions Card */
    .divine-actions-card {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(168, 85, 247, 0.08) 100%);
      border: 1px solid rgba(245, 158, 11, 0.4);
      border-radius: 10px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .divine-title {
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #fde047;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .divine-btn-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }

    .btn-divine-action {
      background: #1e293b;
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #f1f5f9;
      padding: 6px 8px;
      border-radius: 6px;
      font-size: 0.73rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      justify-content: center;
      transition: all 0.15s;
    }

    .btn-divine-action:hover {
      background: #334155;
      border-color: var(--gold);
      color: #fde047;
      transform: translateY(-1px);
    }

    .btn-divine-full {
      grid-column: span 2;
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
      border-color: #f59e0b;
      color: #fef08a;
      font-weight: 700;
    }

    .btn-divine-full:hover {
      background: #f59e0b;
      color: #090d16;
    }

    /* Needs Section */
    .section-headline {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .needs-grid {
      display: flex;
      flex-direction: column;
      gap: 6px;
      background: rgba(30, 41, 59, 0.5);
      padding: 10px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .need-row {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .need-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.72rem;
      color: #cbd5e1;
      font-weight: 600;
    }

    .need-track {
      width: 100%;
      height: 5px;
      background: #1e293b;
      border-radius: 3px;
      overflow: hidden;
    }

    .need-fill {
      height: 100%;
      border-radius: 3px;
      transition: width 0.3s ease, background-color 0.3s ease;
    }

    /* Financials & Economy */
    .econ-badge-card {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }

    .econ-stat {
      background: rgba(30, 41, 59, 0.6);
      padding: 8px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.05);
      text-align: center;
    }

    .econ-stat-title {
      font-size: 0.65rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 600;
    }

    .econ-stat-value {
      font-size: 1.05rem;
      font-weight: 800;
      margin-top: 1px;
    }

    .relations-list, .memory-stream {
      display: flex;
      flex-direction: column;
      gap: 5px;
      max-height: 110px;
      overflow-y: auto;
    }

    .relations-list::-webkit-scrollbar, .memory-stream::-webkit-scrollbar { width: 3px; }
    .relations-list::-webkit-scrollbar-thumb, .memory-stream::-webkit-scrollbar-thumb { background: #334155; }

    .relation-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 5px 8px;
      background: rgba(30, 41, 59, 0.5);
      border-radius: 6px;
      font-size: 0.72rem;
    }

    .memory-item {
      padding: 5px 8px;
      background: rgba(30, 41, 59, 0.5);
      border-radius: 6px;
      font-size: 0.72rem;
      color: #cbd5e1;
      border-left: 2px solid var(--accent);
    }

    /* ==========================================================================
       DIVINE COMMAND CONSOLE ("GOD'S COMMAND")
       ========================================================================== */
    .divine-console-container {
      position: absolute;
      bottom: 14px;
      left: 50%;
      transform: translateX(-50%);
      width: min(840px, 92vw);
      background: rgba(13, 20, 36, 0.94);
      backdrop-filter: blur(18px);
      border: 1px solid rgba(245, 158, 11, 0.45);
      box-shadow: 0 0 25px rgba(245, 158, 11, 0.25), 0 10px 40px rgba(0, 0, 0, 0.75);
      border-radius: 14px;
      padding: 10px 14px;
      z-index: 25;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.3s ease;
    }

    .console-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .console-title-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.76rem;
      font-weight: 800;
      color: #fde047;
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }

    .console-status-pill {
      font-size: 0.7rem;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .console-input-row {
      display: flex;
      gap: 8px;
      align-items: center;
    }

    .god-input {
      flex: 1;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 8px;
      padding: 9px 14px;
      color: #f8fafc;
      font-size: 0.88rem;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    .god-input:focus {
      border-color: #f59e0b;
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.35);
    }

    .btn-execute-divine {
      background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      color: #090d16;
      border: none;
      border-radius: 8px;
      padding: 9px 18px;
      font-size: 0.84rem;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 0 14px rgba(245, 158, 11, 0.4);
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .btn-execute-divine:hover {
      transform: translateY(-1px);
      box-shadow: 0 0 20px rgba(245, 158, 11, 0.65);
    }

    .suggestion-chips-row {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 2px;
    }

    .suggestion-chips-row::-webkit-scrollbar { height: 3px; }
    .suggestion-chips-row::-webkit-scrollbar-thumb { background: #334155; }

    .chip-btn {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: #cbd5e1;
      border-radius: 12px;
      padding: 3px 9px;
      font-size: 0.7rem;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.15s;
    }

    .chip-btn:hover {
      background: rgba(56, 189, 248, 0.2);
      border-color: var(--accent);
      color: #f8fafc;
    }

    /* Execution Feedback Alert Box */
    .command-feedback-card {
      display: none;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid #10b981;
      border-radius: 8px;
      padding: 7px 10px;
      font-size: 0.76rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      animation: fadeIn 0.25s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .feedback-left {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .feedback-badge {
      font-weight: 800;
      color: #34d399;
      background: rgba(16, 185, 129, 0.15);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.68rem;
    }

    .feedback-text {
      color: #f1f5f9;
    }

    /* ==========================================================================
       DEDICATED GOD MODE WORLD CONTROL DRAWER (#god-mode-drawer)
       ========================================================================== */
    .god-drawer-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(6px);
      z-index: 50;
      display: none;
      justify-content: center;
      align-items: center;
    }

    .god-drawer-overlay.open {
      display: flex;
    }

    .god-drawer-box {
      width: min(860px, 94vw);
      max-height: 86vh;
      background: #0b1120;
      border: 1px solid #f59e0b;
      box-shadow: 0 0 35px rgba(245, 158, 11, 0.3), 0 20px 60px rgba(0, 0, 0, 0.85);
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .god-drawer-header {
      padding: 14px 20px;
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.18) 0%, rgba(168, 85, 247, 0.18) 100%);
      border-bottom: 1px solid rgba(245, 158, 11, 0.3);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .god-drawer-title {
      font-size: 1.15rem;
      font-weight: 800;
      color: #fde047;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .god-drawer-body {
      padding: 20px;
      overflow-y: auto;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .god-power-section {
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .god-sec-title {
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--accent);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .control-row {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .control-label {
      font-size: 0.74rem;
      color: #cbd5e1;
      display: flex;
      justify-content: space-between;
      font-weight: 600;
    }

    .power-btn-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }

    .btn-power-option {
      background: #1e293b;
      border: 1px solid #475569;
      color: #e2e8f0;
      padding: 6px 8px;
      border-radius: 6px;
      font-size: 0.74rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.15s;
    }

    .btn-power-option:hover, .btn-power-option.active {
      background: var(--gold);
      color: #090d16;
      border-color: #fde047;
      font-weight: 700;
    }

    .god-range-slider {
      width: 100%;
      height: 6px;
      accent-color: #f59e0b;
      cursor: pointer;
    }

    /* ==========================================================================
       DIVINE EVENT LOG DRAWER
       ========================================================================== */
    .divine-log-drawer {
      position: absolute;
      top: 78px;
      left: 16px;
      width: 320px;
      max-height: 480px;
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      z-index: 15;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.65);
      display: none;
      flex-direction: column;
      overflow: hidden;
    }

    .divine-log-drawer.open {
      display: flex;
    }

    .log-list {
      padding: 10px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 6px;
      flex: 1;
    }

    .log-list::-webkit-scrollbar { width: 3px; }
    .log-list::-webkit-scrollbar-thumb { background: #334155; }

    .log-entry {
      background: rgba(30, 41, 59, 0.6);
      border-radius: 6px;
      padding: 6px 8px;
      font-size: 0.72rem;
      line-height: 1.35;
      border-left: 3px solid var(--accent);
    }

    .log-entry.divine { border-left-color: var(--gold); }
    .log-entry.weather { border-left-color: #06b6d4; }
    .log-entry.event { border-left-color: #a855f7; }

    .log-time {
      font-size: 0.65rem;
      color: var(--text-muted);
      font-weight: 700;
      margin-bottom: 2px;
    }

    /* Zoom Controls */
    .zoom-controls {
      position: absolute;
      right: 20px;
      bottom: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      z-index: 10;
    }

    .btn-zoom {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--card-border);
      color: #f1f5f9;
      font-size: 1.15rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s;
    }

    .btn-zoom:hover {
      background: #334155;
      color: var(--accent);
    }

    /* Modals Generic */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(6px);
      z-index: 100;
      display: none;
      justify-content: center;
      align-items: center;
    }

    .modal-overlay.open { display: flex; }

    .modal-box {
      width: min(720px, 92vw);
      max-height: 85vh;
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8);
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 10px;
    }

    .modal-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--accent);
    }

    .btn-close-modal {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.3rem;
      cursor: pointer;
    }

    .btn-close-modal:hover { color: #fff; }
  </style>
</head>
<body>

  <!-- Fullscreen Phaser Game Canvas -->
  <div id="game-container"></div>

  <!-- Particle Weather Canvas (Rain, Snow, Storm) -->
  <canvas id="weather-canvas"></canvas>

  <!-- Ambient Light Day/Night Overlay -->
  <div id="ambient-overlay"></div>

  <!-- Screen Flash for Cataclysms / Lightning -->
  <div id="flash-overlay"></div>

  <!-- ==========================================================================
       TOP STATUS BAR & NAVIGATION
       ========================================================================== -->
  <header class="top-bar">
    <div class="brand-section">
      <div class="brand-badge">
        <div class="status-dot"></div>
        <div>
          <div class="brand-title">👑 SMALLVILLE // GOD SIMULATOR</div>
          <div class="brand-subtitle" id="society-status-sub">15 AUTONOMOUS RESIDENTS • DIVINE AUTHORITY ACTIVE</div>
        </div>
      </div>
    </div>

    <!-- Simulation Time & Playback Controls -->
    <div class="clock-section">
      <div class="clock-display">
        <span id="clock-day">MON</span>
        <span id="clock-time" style="color:var(--accent);">08:00 AM</span>
      </div>
      <div class="season-badge" id="season-badge">🌸 Spring</div>
      <div class="weather-badge" id="weather-badge">
        <span id="weather-icon">☀️</span>
        <span id="weather-desc">Sunny</span>
      </div>
      <button class="time-ctrl-btn" id="btn-play-pause">⏸ PAUSE</button>
      <div style="display:flex; gap:3px;">
        <button class="time-ctrl-btn" data-speed="0.5">0.5x</button>
        <button class="time-ctrl-btn active" data-speed="1">1x</button>
        <button class="time-ctrl-btn" data-speed="2">2x</button>
        <button class="time-ctrl-btn" data-speed="5">5x</button>
        <button class="time-ctrl-btn" data-speed="10">10x</button>
      </div>
    </div>

    <!-- Action Bar Buttons -->
    <div class="top-actions">
      <button class="btn-action-nav btn-god-powers" id="btn-toggle-god-drawer">👑 God Powers</button>
      <button class="btn-action-nav btn-command-toggle" id="btn-focus-command">⚡ God's Command</button>
      <button class="btn-action-nav" id="btn-toggle-roster">👥 Residents (<span id="top-roster-count">15</span>)</button>
      <button class="btn-action-nav" id="btn-toggle-log">📜 Event Log</button>
      <button class="btn-action-nav" id="btn-open-analytics">📊 Analytics</button>
      <button class="btn-action-nav" id="btn-open-saveload">💾 Save / Load</button>
      <a href="/" class="btn-action-nav" style="color:#94a3b8;">&larr; Portal</a>
    </div>
  </header>

  <!-- ==========================================================================
       LEFT ROSTER PANE (COLLAPSED BY DEFAULT)
       ========================================================================== -->
  <aside class="left-roster-pane" id="left-roster-pane">
    <div class="pane-header">
      <div class="pane-title">👥 Town Residents</div>
      <div style="display:flex; align-items:center; gap:8px;">
        <div class="roster-count" id="roster-count">15 Citizens</div>
        <button class="btn-close-pane" id="btn-close-roster">&times;</button>
      </div>
    </div>
    <div class="roster-filter-tabs">
      <button class="roster-tab active" data-filter="all">All</button>
      <button class="roster-tab" data-filter="working">Working</button>
      <button class="roster-tab" data-filter="social">Social</button>
      <button class="roster-tab" data-filter="home">Home</button>
    </div>
    <div class="roster-list" id="citizen-roster-list">
      <!-- Populated dynamically -->
    </div>
  </aside>

  <!-- ==========================================================================
       RIGHT DEEP INSPECTOR HUD (SLIDE-OUT ON AGENT CLICK ONLY)
       ========================================================================== -->
  <aside class="right-inspector-pane" id="right-inspector-pane">
    <div class="inspector-header-bar">
      <div class="inspector-mode-pill mode-autonomous" id="inspect-mode-pill">
        <span>🤖</span>
        <span id="inspect-mode-text">Autonomous AI Mode</span>
      </div>
      <button class="btn-close-pane" id="btn-close-inspector">&times;</button>
    </div>

    <!-- Profile Header -->
    <div class="inspector-profile-header">
      <img src="/static/assets/characters/profile/Isabella_Rodriguez.png" class="inspector-avatar" id="inspect-avatar" alt="Citizen">
      <div class="inspector-bio">
        <h2 id="inspect-name">Isabella Rodriguez</h2>
        <p id="inspect-job" style="color:var(--accent); font-weight:600;">Cafe Owner & Barista</p>
        <p id="inspect-traits" style="font-size:0.72rem;">Age 34 • Friendly, Outgoing</p>
        <div class="cam-shortcuts-row">
          <button class="btn-cam-shortcut" id="btn-cam-follow">🎯 Follow</button>
          <button class="btn-cam-shortcut" id="btn-cam-focus">📍 Focus</button>
          <button class="btn-cam-shortcut" id="btn-cam-home">🏠 Home</button>
          <button class="btn-cam-shortcut" id="btn-cam-work">🏢 Work</button>
          <button class="btn-cam-shortcut" id="btn-open-schedule">🗓️ Schedule</button>
        </div>
      </div>
    </div>

    <!-- Active Internal Thought -->
    <div class="thought-bubble-card">
      <div class="thought-label">💭 Active Internal Thought</div>
      <div class="thought-text" id="inspect-thought">
        "Morning cafe rush is starting! Let's get the fresh espresso machine calibrated."
      </div>
      <div class="thought-location" id="inspect-location">
        📍 Hobbs Cafe &bull; behind the cafe counter
      </div>
    </div>

    <!-- DIVINE INTERVENTIONS (DIRECT GOD CONTROLS) -->
    <div class="divine-actions-card">
      <div class="divine-title">
        <span>⚡ Divine Interventions</span>
        <span style="font-size:0.65rem; color:#94a3b8;">Direct Authority</span>
      </div>
      <div class="divine-btn-grid">
        <button class="btn-divine-action" id="btn-god-give-money">💰 +$100 Gift</button>
        <button class="btn-divine-action" id="btn-god-take-money">💸 -$50 Fine</button>
        <button class="btn-divine-action" id="btn-god-force-work">🏢 Force Work</button>
        <button class="btn-divine-action" id="btn-god-force-home">🏠 Force Home</button>
        <button class="btn-divine-action" id="btn-god-force-cafe">☕ Force Cafe</button>
        <button class="btn-divine-action" id="btn-god-force-park">🌳 Force Park</button>
        <button class="btn-divine-action" id="btn-god-force-sleep">🛏️ Force Sleep</button>
        <button class="btn-divine-action" id="btn-god-target-tile">🎯 Click Map Tile</button>
        <button class="btn-divine-action btn-divine-full" id="btn-god-bless-needs">✨ Divine Blessing (Max All Needs 100%)</button>
        <button class="btn-divine-action btn-divine-full" id="btn-god-release-control" style="background:#1e293b; color:#94a3b8; border-color:#475569;">🕊️ Release Control to Autonomous AI</button>
      </div>
    </div>

    <!-- Needs Grid -->
    <div>
      <div class="section-headline">
        <span>Vital Needs & State</span>
        <span id="inspect-overall-mood" style="color:var(--success); font-weight:700;">Happy (88%)</span>
      </div>
      <div class="needs-grid">
        <div class="need-row">
          <div class="need-header">
            <span>🍞 Hunger</span>
            <span id="val-hunger">25%</span>
          </div>
          <div class="need-track"><div class="need-fill" id="bar-hunger" style="width:25%; background:var(--success);"></div></div>
        </div>

        <div class="need-row">
          <div class="need-header">
            <span>⚡ Energy</span>
            <span id="val-energy">85%</span>
          </div>
          <div class="need-track"><div class="need-fill" id="bar-energy" style="width:85%; background:var(--accent);"></div></div>
        </div>

        <div class="need-row">
          <div class="need-header">
            <span>❤️ Health</span>
            <span id="val-health">95%</span>
          </div>
          <div class="need-track"><div class="need-fill" id="bar-health" style="width:95%; background:var(--success);"></div></div>
        </div>

        <div class="need-row">
          <div class="need-header">
            <span>😊 Happiness</span>
            <span id="val-happiness">88%</span>
          </div>
          <div class="need-track"><div class="need-fill" id="bar-happiness" style="width:88%; background:#eab308;"></div></div>
        </div>

        <div class="need-row">
          <div class="need-header">
            <span>🚿 Hygiene</span>
            <span id="val-hygiene">80%</span>
          </div>
          <div class="need-track"><div class="need-fill" id="bar-hygiene" style="width:80%; background:#06b6d4;"></div></div>
        </div>

        <div class="need-row">
          <div class="need-header">
            <span>💬 Social</span>
            <span id="val-social">75%</span>
          </div>
          <div class="need-track"><div class="need-fill" id="bar-social" style="width:75%; background:var(--divine-purple);"></div></div>
        </div>
      </div>
    </div>

    <!-- Economic Status -->
    <div>
      <div class="section-headline">Economic Status</div>
      <div class="econ-badge-card">
        <div class="econ-stat">
          <div class="econ-stat-title">Wallet Balance</div>
          <div class="econ-stat-value" id="val-money" style="color:#10b981;">$450</div>
        </div>
        <div class="econ-stat">
          <div class="econ-stat-title">Hourly Wage</div>
          <div class="econ-stat-value" id="val-wage" style="color:var(--accent);">$24/hr</div>
        </div>
      </div>
    </div>

    <!-- Social Relationships -->
    <div>
      <div class="section-headline">Social Connections</div>
      <div class="relations-list" id="inspect-relations-list"></div>
    </div>

    <!-- Memories -->
    <div>
      <div class="section-headline">Recent Memories & Encounters</div>
      <div class="memory-stream" id="inspect-memory-stream"></div>
    </div>
  </aside>

  <!-- ==========================================================================
       DIVINE COMMAND CONSOLE ("GOD'S COMMAND")
       ========================================================================== -->
  <div class="divine-console-container" id="divine-console">
    <div class="console-header">
      <div class="console-title-pill">
        <span>⚡ GOD'S COMMAND</span>
        <span style="color:#94a3b8; font-weight:500;">• Type Natural-Language Simulation Directives</span>
      </div>
      <div class="console-status-pill">
        <span id="console-mode-indicator">🟢 NLP Engine Ready</span>
      </div>
    </div>

    <!-- Command Input & Submit -->
    <div class="console-input-row">
      <input type="text" id="god-command-input" class="god-input" placeholder='Type a divine command... e.g. "Make Isabella go to cafe", "Give Klaus 500 coins", "Make it rain", "Make everyone gather at Johnson Park"'>
      <button class="btn-execute-divine" id="btn-submit-divine">⚡ EXECUTE WILL</button>
    </div>

    <!-- Suggestion Chips -->
    <div class="suggestion-chips-row">
      <button class="chip-btn" data-cmd="Make Isabella go to cafe">☕ Make Isabella go to cafe</button>
      <button class="chip-cmd chip-btn" data-cmd="Make Klaus visit the park">🌳 Make Klaus visit the park</button>
      <button class="chip-cmd chip-btn" data-cmd="Give Maria 500 coins">💰 Give Maria 500 coins</button>
      <button class="chip-cmd chip-btn" data-cmd="Make everyone gather at Johnson Park">📢 Gather everyone at Johnson Park</button>
      <button class="chip-cmd chip-btn" data-cmd="Make it rain for two hours">🌧️ Make it rain for two hours</button>
      <button class="chip-cmd chip-btn" data-cmd="Make everyone go to sleep">🛏️ Make everyone go to sleep</button>
      <button class="chip-cmd chip-btn" data-cmd="Trigger Town Festival">🎪 Trigger Town Festival</button>
      <button class="chip-cmd chip-btn" data-cmd="Increase the happiness of all residents">✨ Increase happiness of all residents</button>
      <button class="chip-cmd chip-btn" data-cmd="Create a food shortage in the town">⚠️ Create food shortage</button>
    </div>

    <!-- Execution Feedback Alert -->
    <div class="command-feedback-card" id="command-feedback-card">
      <div class="feedback-left">
        <span class="feedback-badge" id="feedback-badge">DIVINE WILL</span>
        <span class="feedback-text" id="feedback-text">Command executed successfully.</span>
      </div>
      <button class="btn-close-pane" id="btn-close-feedback">&times;</button>
    </div>
  </div>

  <!-- ==========================================================================
       DEDICATED GOD MODE WORLD CONTROL DRAWER
       ========================================================================== -->
  <div class="god-drawer-overlay" id="god-drawer-overlay">
    <div class="god-drawer-box">
      <div class="god-drawer-header">
        <div class="god-drawer-title">
          <span>👑 GOD MODE — COMPLETE WORLD AUTHORITY</span>
        </div>
        <button class="btn-close-pane" id="btn-close-god-drawer" style="font-size:1.4rem;">&times;</button>
      </div>

      <div class="god-drawer-body">
        <!-- 1. World Simulation Flow -->
        <div class="god-power-section">
          <div class="god-sec-title">⏳ 1. Society Flow & Playback</div>
          <div class="power-btn-grid" style="grid-template-columns: 1fr 1fr 1fr;">
            <button class="btn-power-option" id="btn-drawer-pause">⏸ Pause</button>
            <button class="btn-power-option active" id="btn-drawer-resume">▶ Resume</button>
            <button class="btn-power-option" id="btn-drawer-reset" style="color:#ef4444;">🔄 Reset</button>
          </div>
          <div class="control-row">
            <div class="control-label">
              <span>Simulation Speed</span>
              <span id="label-speed-val">1x Normal</span>
            </div>
            <div class="power-btn-grid" style="grid-template-columns: repeat(5, 1fr);">
              <button class="btn-power-option" data-god-speed="0.5">0.5x</button>
              <button class="btn-power-option active" data-god-speed="1">1x</button>
              <button class="btn-power-option" data-god-speed="2">2x</button>
              <button class="btn-power-option" data-god-speed="5">5x</button>
              <button class="btn-power-option" data-god-speed="10">10x</button>
            </div>
          </div>
        </div>

        <!-- 2. Celestial Time & Seasons -->
        <div class="god-power-section">
          <div class="god-sec-title">☀️ 2. Celestial Time & Seasons</div>
          <div class="control-row">
            <div class="control-label">
              <span>Time of Day Scrub</span>
              <span id="label-drawer-time" style="color:var(--accent);">08:00 AM</span>
            </div>
            <input type="range" min="0" max="1439" value="480" class="god-range-slider" id="slider-time-scrub">
          </div>
          <div class="power-btn-grid" style="grid-template-columns: repeat(4, 1fr);">
            <button class="btn-power-option" data-jump-time="6">🌅 Dawn</button>
            <button class="btn-power-option" data-jump-time="12">☀️ Noon</button>
            <button class="btn-power-option" data-jump-time="18">🌇 Sunset</button>
            <button class="btn-power-option" data-jump-time="0">🌙 Night</button>
          </div>
          <div class="control-row">
            <div class="control-label">
              <span>Season of the Year</span>
            </div>
            <div class="power-btn-grid" style="grid-template-columns: repeat(4, 1fr);">
              <button class="btn-power-option active" data-god-season="Spring">🌸 Spring</button>
              <button class="btn-power-option" data-god-season="Summer">☀️ Summer</button>
              <button class="btn-power-option" data-god-season="Autumn">🍂 Autumn</button>
              <button class="btn-power-option" data-god-season="Winter">❄️ Winter</button>
            </div>
          </div>
        </div>

        <!-- 3. Environmental Powers & Weather -->
        <div class="god-power-section">
          <div class="god-sec-title">🌧️ 3. Environmental Powers & Weather</div>
          <div class="power-btn-grid">
            <button class="btn-power-option active" data-god-weather="Sunny">☀️ Sunny</button>
            <button class="btn-power-option" data-god-weather="Rain">🌧️ Rain</button>
            <button class="btn-power-option" data-god-weather="Storm">⛈️ Storm</button>
            <button class="btn-power-option" data-god-weather="Snow">❄️ Snow</button>
            <button class="btn-power-option" data-god-weather="Drought">🔥 Drought</button>
            <button class="btn-power-option" data-god-weather="Overcast">☁️ Overcast</button>
          </div>
          <div class="control-row">
            <div class="control-label">
              <span>Ambient Lighting Override</span>
            </div>
            <div class="power-btn-grid" style="grid-template-columns: 1fr 1fr 1fr;">
              <button class="btn-power-option active" id="btn-ambient-auto">🕒 Auto Clock</button>
              <button class="btn-power-option" id="btn-ambient-day">☀️ Force Day</button>
              <button class="btn-power-option" id="btn-ambient-night">🌙 Force Night</button>
            </div>
          </div>
        </div>

        <!-- 4. Resources & Economy -->
        <div class="god-power-section">
          <div class="god-sec-title">🌾 4. Resources & Economy</div>
          <div class="control-row">
            <div class="control-label">
              <span>Town Food Reserves</span>
              <span id="label-food-val">180 Units</span>
            </div>
            <div class="power-btn-grid" style="grid-template-columns: 1fr 1fr 1fr;">
              <button class="btn-power-option" id="btn-add-food">➕ +50 Food</button>
              <button class="btn-power-option" id="btn-sub-food">➖ -50 Food</button>
              <button class="btn-power-option" id="btn-famine" style="color:#ef4444;">⚠️ Famine (0)</button>
            </div>
          </div>
          <div class="control-row">
            <div class="control-label">
              <span>Town Treasury & Stimulus</span>
              <span id="label-econ-val">$5,240</span>
            </div>
            <div class="power-btn-grid" style="grid-template-columns: 1fr 1fr;">
              <button class="btn-power-option" id="btn-stimulus-boom">💰 +$2,000 Stimulus</button>
              <button class="btn-power-option" id="btn-econ-crash" style="color:#ef4444;">📉 Economic Panic</button>
            </div>
          </div>
        </div>

        <!-- 5. Major Town Events & Festivals -->
        <div class="god-power-section" style="grid-column: span 2;">
          <div class="god-sec-title">🎪 5. Major World Events & Gatherings</div>
          <div class="power-btn-grid" style="grid-template-columns: repeat(4, 1fr);">
            <button class="btn-power-option" id="btn-event-festival">🎉 Town Festival</button>
            <button class="btn-power-option" id="btn-event-gather-park">📢 Gather in Park</button>
            <button class="btn-power-option" id="btn-event-curfew">😴 Town Curfew</button>
            <button class="btn-power-option" id="btn-event-work-rush">💼 Morning Rush</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       DIVINE EVENT LOG DRAWER
       ========================================================================== -->
  <aside class="divine-log-drawer" id="divine-log-drawer">
    <div class="pane-header">
      <div class="pane-title">📜 Divine Event Log</div>
      <button class="btn-close-pane" id="btn-close-log">&times;</button>
    </div>
    <div class="log-list" id="divine-log-list">
      <!-- Logs inserted dynamically -->
    </div>
  </aside>

  <!-- Zoom Floating Buttons -->
  <div class="zoom-controls">
    <button class="btn-zoom" id="btn-zoom-in" title="Zoom In">+</button>
    <button class="btn-zoom" id="btn-zoom-out" title="Zoom Out">&minus;</button>
    <button class="btn-zoom" id="btn-zoom-reset" title="Reset View">&#8635;</button>
  </div>

  <!-- Modals: Analytics, Schedule, Save/Load -->
  <div class="modal-overlay" id="modal-analytics">
    <div class="modal-box">
      <div class="modal-header">
        <div class="modal-title">📊 Smallville Town Analytics & Society Health</div>
        <button class="btn-close-modal">&times;</button>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
        <div style="background:#1e293b; padding:16px; border-radius:10px;">
          <h4 style="margin-bottom:8px; color:var(--accent); font-size:0.9rem;">Citizen Happiness & Needs Index</h4>
          <canvas id="chart-happiness" height="180"></canvas>
        </div>
        <div style="background:#1e293b; padding:16px; border-radius:10px;">
          <h4 style="margin-bottom:8px; color:var(--success); font-size:0.9rem;">Town Economic Velocity & Business Revenues</h4>
          <canvas id="chart-economy" height="180"></canvas>
        </div>
      </div>
    </div>
  </div>

  <div class="modal-overlay" id="modal-schedule">
    <div class="modal-box" style="max-width:550px;">
      <div class="modal-header">
        <div class="modal-title" id="schedule-modal-title">🗓️ Citizen Daily Schedule</div>
        <button class="btn-close-modal">&times;</button>
      </div>
      <div id="schedule-timeline" style="display:flex; flex-direction:column; gap:8px; max-height:60vh; overflow-y:auto;"></div>
    </div>
  </div>

  <div class="modal-overlay" id="modal-saveload">
    <div class="modal-box" style="max-width:500px;">
      <div class="modal-header">
        <div class="modal-title">💾 Save & Load Simulation State</div>
        <button class="btn-close-modal">&times;</button>
      </div>
      <p style="font-size:0.85rem; color:var(--text-muted);">
        Save all citizen positions, needs, wallets, relationships, and history.
      </p>
      <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
        <button class="btn-action-nav" id="btn-save-local" style="justify-content:center; background:#0284c7; color:#fff;">
          💾 Save Current State to Local Storage
        </button>
        <button class="btn-action-nav" id="btn-load-local" style="justify-content:center; background:#10b981; color:#fff;">
          📂 Load State from Local Storage
        </button>
        <button class="btn-action-nav" id="btn-export-json" style="justify-content:center;">
          📥 Download State JSON File
        </button>
        <button class="btn-action-nav" id="btn-reset-sim" style="justify-content:center; color:#ef4444; border-color:#ef4444;">
          🔄 Reset Simulation to Day 1 Morning
        </button>
      </div>
    </div>
  </div>

  <!-- Include Simulation Logic Script -->
  <script>
    /* ==========================================================================
       SIMULATION DATA & STATE INITIALIZATION
       ========================================================================== */
    window.SIM_DATA = {
      collisionGrid: null,
      citizens: null,
      locations: null
    };

    window.isMapTargetSelectionActive = false;

    // Global Simulation Engine Class
    class SocietySimulation {
      constructor() {
        this.citizens = [];
        this.selectedCitizen = null;
        this.followCamera = true;
        this.speed = 1;
        this.isRunning = true;
        
        // Simulation Clock: starts Day 1 (Monday), 08:00 AM
        this.day = 1;
        this.dayName = "Monday";
        this.hour = 8;
        this.minute = 0;
        this.season = "Spring";
        this.weather = "Sunny";
        this.weatherIcon = "☀️";
        this.forceAmbient = null; // null for auto, 'day', 'night'

        // Town Economic Totals
        this.townFoodReserves = 180;
        this.townEconomy = 5240;
        this.businessRevenues = {
          "Hobbs Cafe": 240,
          "The Rose & Crown Pub": 380,
          "The Willows Market": 410,
          "Harvey Oak Supply": 190
        };

        // Event Journal
        this.eventLog = [];

        // Historical Metrics for Analytics
        this.historyMetrics = {
          times: [],
          avgHappiness: [],
          avgHealth: [],
          cafeRevenue: [],
          pubRevenue: [],
          marketRevenue: []
        };
      }

      initCitizens(citizenDefs) {
        this.citizens = citizenDefs.map((def, idx) => {
          return {
            id: idx,
            name: def.name,
            underscore: def.name.replace(/ /g, '_'),
            age: def.age,
            occupation: def.occupation,
            workplace_name: def.workplace_name,
            workplace_coords: [...def.workplace_coords],
            home_name: def.home_name,
            home_coords: [...def.home_coords],
            bed_coords: [...def.bed_coords],
            bathroom_coords: [...def.bathroom_coords],
            personality: def.personality,
            traits: def.traits || ["friendly"],
            bio: def.bio,
            money: def.money || 250,
            hourly_wage: def.hourly_wage || 20,
            schedule: def.schedule,

            // Live Coordinates on 140x100 grid
            tileX: def.home_coords[0],
            tileY: def.home_coords[1],
            pixelX: def.home_coords[0] * 32 + 16,
            pixelY: def.home_coords[1] * 32 + 16,
            facing: 'down',
            isWalking: false,
            currentPath: [],
            pathIndex: 0,

            // Dynamic Needs (0 to 100)
            hunger: 20 + Math.floor(Math.random() * 20),
            energy: 85 + Math.floor(Math.random() * 15),
            health: 95,
            happiness: 85 + Math.floor(Math.random() * 10),
            hygiene: 80 + Math.floor(Math.random() * 15),
            social: 75 + Math.floor(Math.random() * 15),

            // Activity State
            currentAction: "Morning routine at home",
            actionEmoji: "🌅",
            currentThought: `Waking up in ${def.home_name}. Ready for the day ahead.`,
            locationText: def.home_name,
            state: "home", // home, work, eat, social, sleep, divine

            // Divine Intervention State
            divineCommand: null, // { action: string, dest: [x,y], resumeState: string }

            // Relationships
            relationships: this.generateInitialRelationships(def.name),

            // Memories
            memories: [
              { time: "08:00 AM", text: `Woke up feeling well-rested in ${def.home_name}.` }
            ],

            // Phaser Sprite Reference
            sprite: null,
            speechBubble: null,
            speechText: null,
            emojiIcon: null,
            bubbleHideTimeout: null,
            chatTimer: 0
          };
        });
      }

      generateInitialRelationships(name) {
        const network = {
          "Isabella Rodriguez": [
            { name: "Klaus Mueller", relation: "Regular Customer & Friend", affinity: 85 },
            { name: "Maria Lopez", relation: "Close Friend & Neighbor", affinity: 90 },
            { name: "Arthur Burton", relation: "Pub Landlord Neighbor", affinity: 80 }
          ],
          "Klaus Mueller": [
            { name: "Isabella Rodriguez", relation: "Cafe Friend", affinity: 85 },
            { name: "Abigail Chen", relation: "Research Colleague", affinity: 88 }
          ],
          "Maria Lopez": [
            { name: "Isabella Rodriguez", relation: "Best Friend", affinity: 92 },
            { name: "Carlos Gomez", relation: "Friend", affinity: 78 }
          ]
        };
        return network[name] || [
          { name: "Isabella Rodriguez", relation: "Town Friend", affinity: 75 },
          { name: "Arthur Burton", relation: "Acquaintance", affinity: 70 }
        ];
      }

      formatTime(h, m) {
        const period = h >= 12 ? "PM" : "AM";
        const displayH = h % 12 === 0 ? 12 : h % 12;
        const displayM = m < 10 ? `0${m}` : m;
        return `${displayH}:${displayM} ${period}`;
      }

      // Tick Simulation Forward
      tickSimulation() {
        if (!this.isRunning) return;

        // Advance in-game time
        this.minute += 1;
        if (this.minute >= 60) {
          this.minute = 0;
          this.hour += 1;
          this.onHourChange();
        }
        if (this.hour >= 24) {
          this.hour = 0;
          this.day += 1;
          const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
          this.dayName = days[(this.day - 1) % 7];
          this.onDayChange();
        }

        // Update Clock HUD
        document.getElementById('clock-day').innerText = this.dayName.substring(0, 3).toUpperCase();
        document.getElementById('clock-time').innerText = this.formatTime(this.hour, this.minute);
        document.getElementById('label-drawer-time').innerText = this.formatTime(this.hour, this.minute);

        // Update Ambient Daylight
        this.updateAmbientDaylight();

        // Update each Citizen's Needs & Decision-making
        this.citizens.forEach(c => this.updateCitizen(c));

        // Check for Nearby Proximity Conversations
        this.checkConversations();

        // Update Inspector HUD for Selected Citizen
        if (this.selectedCitizen) {
          this.updateInspectorHUD(this.selectedCitizen);
        }
      }

      setTime(h, m = 0) {
        this.hour = Math.max(0, Math.min(23, h));
        this.minute = Math.max(0, Math.min(59, m));
        document.getElementById('clock-time').innerText = this.formatTime(this.hour, this.minute);
        document.getElementById('label-drawer-time').innerText = this.formatTime(this.hour, this.minute);
        this.updateAmbientDaylight();
      }

      setWeather(wName) {
        const weathers = {
          "Sunny": { icon: "☀️", desc: "Sunny" },
          "Rain": { icon: "🌧️", desc: "Rain" },
          "Storm": { icon: "⛈️", desc: "Storm" },
          "Snow": { icon: "❄️", desc: "Snow" },
          "Drought": { icon: "🔥", desc: "Drought" },
          "Overcast": { icon: "☁️", desc: "Overcast" }
        };
        const target = weathers[wName] || weathers["Sunny"];
        this.weather = target.desc;
        this.weatherIcon = target.icon;
        document.getElementById('weather-icon').innerText = target.icon;
        document.getElementById('weather-desc').innerText = target.desc;
        
        // Update weather canvas particle mode
        if (window.weatherEngine) {
          window.weatherEngine.setMode(this.weather);
        }

        this.logEvent(`Weather set to ${this.weather} by Divine Authority.`, null, "weather", target.icon);
      }

      setSeason(sName) {
        this.season = sName;
        const emojis = { "Spring": "🌸", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️" };
        const emoji = emojis[sName] || "🌸";
        document.getElementById('season-badge').innerText = `${emoji} ${sName}`;
        this.logEvent(`Season changed to ${sName} by Divine Will.`, null, "divine", "🌍");
      }

      updateAmbientDaylight() {
        const overlay = document.getElementById('ambient-overlay');
        if (!overlay) return;

        if (this.forceAmbient === 'day') {
          overlay.style.backgroundColor = "rgba(0,0,0,0)";
          return;
        } else if (this.forceAmbient === 'night') {
          overlay.style.backgroundColor = "rgba(15, 23, 42, 0.65)";
          return;
        }

        if (this.weather === 'Drought') {
          overlay.style.backgroundColor = "rgba(180, 83, 9, 0.22)"; // sepia heat haze
          return;
        }

        const h = this.hour + this.minute / 60;
        let color = "rgba(0, 0, 0, 0)";

        if (h >= 5 && h < 7) {
          // Dawn sunrise (warm peach)
          const factor = (h - 5) / 2;
          color = `rgba(251, 146, 60, ${0.25 * (1 - factor)})`;
        } else if (h >= 7 && h < 17) {
          // Clear Day
          color = "rgba(0, 0, 0, 0)";
        } else if (h >= 17 && h < 19.5) {
          // Golden Sunset
          const factor = (h - 17) / 2.5;
          color = `rgba(249, 115, 22, ${0.22 * factor})`;
        } else if (h >= 19.5 && h < 22) {
          // Dusk Twilight
          const factor = (h - 19.5) / 2.5;
          color = `rgba(30, 27, 75, ${0.2 + factor * 0.35})`;
        } else {
          // Deep Night
          color = "rgba(15, 23, 42, 0.58)";
        }
        overlay.style.backgroundColor = color;
      }

      onHourChange() {
        // Hourly wage payout
        this.citizens.forEach(c => {
          if (c.state === 'work') {
            c.money += c.hourly_wage;
            c.memories.unshift({
              time: this.formatTime(this.hour, this.minute),
              text: `Earned $${c.hourly_wage} for shift at ${c.workplace_name}.`
            });
            if (c.memories.length > 25) c.memories.pop();
          }
        });

        // Drought penalty
        if (this.weather === 'Drought') {
          this.townFoodReserves = Math.max(0, this.townFoodReserves - 4);
        }

        this.recordAnalyticsSnapshot();
      }

      onDayChange() {
        this.logEvent(`A new day begins in Smallville: ${this.dayName}, Day ${this.day}.`, null, "event", "🌅");
      }

      updateCitizen(c) {
        // 1. Natural Need Shifts
        c.hunger = Math.min(100, c.hunger + 0.28);
        c.hygiene = Math.max(0, c.hygiene - 0.14);

        if (c.state === 'sleep') {
          c.energy = Math.min(100, c.energy + 1.2);
          c.health = Math.min(100, c.health + 0.1);
        } else {
          c.energy = Math.max(0, c.energy - (c.state === 'work' ? 0.35 : 0.2));
          c.social = Math.max(0, c.social - 0.12);
        }

        // Happiness calculation
        let happinessTarget = 90;
        if (c.hunger > 70) happinessTarget -= 25;
        if (c.energy < 25) happinessTarget -= 30;
        if (c.hygiene < 30) happinessTarget -= 15;
        if (c.social < 30) happinessTarget -= 15;
        if (c.money < 50) happinessTarget -= 20;
        c.happiness = Math.round(c.happiness * 0.95 + happinessTarget * 0.05);

        // Health calculation
        if (c.hunger > 90 || c.energy < 5) c.health = Math.max(20, c.health - 0.5);
        else c.health = Math.min(100, c.health + 0.2);

        // If under active Divine Command, do not let basic schedule interrupt!
        if (c.divineCommand && c.divineCommand.active) {
          // If citizen reached destination, divine command completes
          if (!c.isWalking && c.tileX === c.divineCommand.dest[0] && c.tileY === c.divineCommand.dest[1]) {
            c.divineCommand.ticksAtDest = (c.divineCommand.ticksAtDest || 0) + 1;
            if (c.divineCommand.ticksAtDest > 15) { // after ~15 simulation seconds, release control
              c.divineCommand.active = false;
              c.state = c.divineCommand.resumeState || 'home';
              c.currentAction = "Resumed daily autonomous routine";
              c.actionEmoji = "🕊️";
              this.logEvent(`${c.name} fulfilled Divine Command and returned to daily routine.`, c.name, "divine", "🕊️");
            }
          }
          return;
        }

        // 2. Adaptive Utility AI: Needs Overrides
        const timeKey = `${this.hour < 10 ? '0' + this.hour : this.hour}:00`;

        if (c.energy <= 15 && c.state !== 'sleep') {
          c.state = 'sleep';
          c.currentAction = "Exhausted, heading to bed to sleep";
          c.actionEmoji = "💤";
          c.currentThought = `Too exhausted to continue. Going home to ${c.home_name} to sleep.`;
          this.setCitizenTarget(c, c.bed_coords[0], c.bed_coords[1]);
          return;
        }

        if (c.state === 'sleep' && c.energy >= 92) {
          c.state = 'home';
          c.currentAction = "Waking up and stretching";
          c.actionEmoji = "🌅";
          c.currentThought = "Feeling well-rested! Time to begin morning activities.";
        }

        if (c.hunger >= 75 && c.state !== 'eat' && c.state !== 'sleep') {
          c.state = 'eat';
          c.actionEmoji = "🥪";

          if (c.money >= 10 && Math.random() < 0.6) {
            const isPub = (this.hour >= 17);
            const venue = isPub ? "The Rose & Crown Pub" : "Hobbs Cafe";
            const cost = isPub ? 14 : 6;
            const dest = isPub ? [60, 31] : [77, 22];

            c.money -= cost;
            this.businessRevenues[venue] += cost;
            this.townFoodReserves = Math.max(0, this.townFoodReserves - 2);

            c.currentAction = `Eating meal at ${venue}`;
            c.currentThought = `Hungry! Stopped by ${venue} to enjoy a meal (-$${cost}).`;
            this.setCitizenTarget(c, dest[0], dest[1]);
          } else {
            c.currentAction = `Cooking home meal in ${c.home_name}`;
            c.currentThought = "Looking for something to eat in the kitchen fridge.";
            this.setCitizenTarget(c, c.home_coords[0], c.home_coords[1]);
          }
          c.hunger = Math.max(5, c.hunger - 45);
          c.happiness = Math.min(100, c.happiness + 8);
          return;
        }

        if (c.hygiene <= 25 && c.state !== 'hygiene' && c.state !== 'sleep') {
          c.state = 'home';
          c.currentAction = `Using bathroom in ${c.home_name}`;
          c.actionEmoji = "🚿";
          c.currentThought = "Need to freshen up with a quick shower.";
          this.setCitizenTarget(c, c.bathroom_coords[0], c.bathroom_coords[1]);
          c.hygiene = 98;
          return;
        }

        // 3. Scheduled Routine Tasks
        if (c.schedule && c.schedule[timeKey] && !c.isWalking && c.state !== 'sleep') {
          const entry = c.schedule[timeKey];
          c.currentAction = entry.action;
          c.actionEmoji = entry.emoji || "🚶";
          c.currentThought = `Schedule: ${entry.action}.`;
          
          if (entry.action.toLowerCase().includes('work') || entry.action.toLowerCase().includes('shift')) {
            c.state = 'work';
          } else if (entry.action.toLowerCase().includes('sleep')) {
            c.state = 'sleep';
          } else if (entry.action.toLowerCase().includes('walk') || entry.action.toLowerCase().includes('park')) {
            c.state = 'social';
          }

          this.setCitizenTarget(c, entry.loc[0], entry.loc[1]);
        }
      }

      setCitizenTarget(c, targetX, targetY) {
        if (!window.SIM_DATA.collisionGrid) return;
        if (c.tileX === targetX && c.tileY === targetY) return;

        const path = findPathBFS(window.SIM_DATA.collisionGrid, c.tileX, c.tileY, targetX, targetY);
        if (path && path.length > 0) {
          c.currentPath = path;
          c.pathIndex = 0;
          c.isWalking = true;
        }
      }

      checkConversations() {
        for (let i = 0; i < this.citizens.length; i++) {
          for (let j = i + 1; j < this.citizens.length; j++) {
            const a = this.citizens[i];
            const b = this.citizens[j];

            if (a.state === 'sleep' || b.state === 'sleep') continue;
            if (a.chatTimer > 0 || b.chatTimer > 0) continue;

            const dist = Math.hypot(a.tileX - b.tileX, a.tileY - b.tileY);
            if (dist <= 2.8) {
              if (Math.random() < 0.35) {
                this.triggerConversation(a, b);
                return;
              }
            }
          }
        }
      }

      triggerConversation(a, b) {
        a.chatTimer = 18;
        b.chatTimer = 18;
        a.social = Math.min(100, a.social + 15);
        b.social = Math.min(100, b.social + 15);
        a.happiness = Math.min(100, a.happiness + 6);
        b.happiness = Math.min(100, b.happiness + 6);

        const dialogues = [
          [`"Hey ${b.name.split(' ')[0]}! How's your day going?"`, `"Good to see you, ${a.name.split(' ')[0]}! Just enjoying the town."`],
          [`"Did you feel that sudden divine breeze earlier?"`, `"Yes! It feels like the heavens themselves are watching over Smallville today."`],
          [`"Heading over to Hobbs Cafe soon?"`, `"Definitely! Best coffee in the county."`],
          [`"The weather today is truly something."`, `"Smallville always has surprises for us."`]
        ];

        const pair = dialogues[Math.floor(Math.random() * dialogues.length)];

        this.displaySpeechBubble(a, pair[0]);
        setTimeout(() => this.displaySpeechBubble(b, pair[1]), 1800);

        const timeStr = this.formatTime(this.hour, this.minute);
        a.memories.unshift({ time: timeStr, text: `Chatted with ${b.name}: ${pair[0]}` });
        b.memories.unshift({ time: timeStr, text: `Chatted with ${a.name}: ${pair[1]}` });

        this.logEvent(`${a.name} and ${b.name} shared a conversation.`, a.name, "social", "💬");
      }

      displaySpeechBubble(citizen, text) {
        if (!citizen.speechBubble || !citizen.speechText) return;
        citizen.speechText.setText(text.replace(/"/g, ''));
        citizen.speechBubble.visible = true;
        citizen.speechText.visible = true;

        clearTimeout(citizen.bubbleHideTimeout);
        citizen.bubbleHideTimeout = setTimeout(() => {
          if (citizen.speechBubble) citizen.speechBubble.visible = false;
          if (citizen.speechText) citizen.speechText.visible = false;
        }, 3800);
      }

      logEvent(text, actor = null, category = "divine", emoji = "⚡") {
        const timeStr = this.formatTime(this.hour, this.minute);
        const entry = { time: timeStr, text, actor, category, emoji };
        this.eventLog.unshift(entry);
        if (this.eventLog.length > 80) this.eventLog.pop();

        // Append to drawer log DOM
        const logContainer = document.getElementById('divine-log-list');
        if (logContainer) {
          const div = document.createElement('div');
          div.className = `log-entry ${category}`;
          div.innerHTML = `<div class="log-time">${timeStr} • ${category.toUpperCase()}</div><div>${emoji} ${text}</div>`;
          logContainer.prepend(div);
          if (logContainer.children.length > 50) logContainer.removeChild(logContainer.lastChild);
        }
      }

      recordAnalyticsSnapshot() {
        const timeStr = `${this.dayName.substring(0,3)} ${this.formatTime(this.hour, 0)}`;
        this.historyMetrics.times.push(timeStr);

        const avgHappy = Math.round(this.citizens.reduce((acc, c) => acc + c.happiness, 0) / this.citizens.length);
        const avgHealth = Math.round(this.citizens.reduce((acc, c) => acc + c.health, 0) / this.citizens.length);
        this.historyMetrics.avgHappiness.push(avgHappy);
        this.historyMetrics.avgHealth.push(avgHealth);

        this.historyMetrics.cafeRevenue.push(this.businessRevenues["Hobbs Cafe"]);
        this.historyMetrics.pubRevenue.push(this.businessRevenues["The Rose & Crown Pub"]);
        this.historyMetrics.marketRevenue.push(this.businessRevenues["The Willows Market"]);

        if (this.historyMetrics.times.length > 24) {
          this.historyMetrics.times.shift();
          this.historyMetrics.avgHappiness.shift();
          this.historyMetrics.avgHealth.shift();
          this.historyMetrics.cafeRevenue.shift();
          this.historyMetrics.pubRevenue.shift();
          this.historyMetrics.marketRevenue.shift();
        }
      }

      updateInspectorHUD(c) {
        document.getElementById('inspect-avatar').src = `/static/assets/characters/profile/${c.underscore}.png`;
        document.getElementById('inspect-name').innerText = c.name;
        document.getElementById('inspect-job').innerText = c.occupation;
        document.getElementById('inspect-traits').innerText = `Age ${c.age} • ${(c.traits || []).join(', ')}`;
        document.getElementById('inspect-thought').innerText = `"${c.currentThought}"`;
        document.getElementById('inspect-location').innerText = `📍 ${c.locationText || c.home_name}`;

        // Mode Pill
        const modePill = document.getElementById('inspect-mode-pill');
        const modeText = document.getElementById('inspect-mode-text');
        if (c.divineCommand && c.divineCommand.active) {
          modePill.className = "inspector-mode-pill mode-divine";
          modeText.innerText = "⚡ Divine Intervention Active";
        } else {
          modePill.className = "inspector-mode-pill mode-autonomous";
          modeText.innerText = "🤖 Autonomous AI Mode";
        }

        // Needs
        const setNeed = (id, val, color) => {
          document.getElementById(`val-${id}`).innerText = `${Math.round(val)}%`;
          const bar = document.getElementById(`bar-${id}`);
          bar.style.width = `${Math.max(0, Math.min(100, val))}%`;
          bar.style.backgroundColor = color;
        };

        setNeed('hunger', c.hunger, c.hunger > 60 ? 'var(--warning)' : 'var(--success)');
        setNeed('energy', c.energy, c.energy < 30 ? 'var(--danger)' : 'var(--accent)');
        setNeed('health', c.health, c.health < 40 ? 'var(--danger)' : 'var(--success)');
        setNeed('happiness', c.happiness, '#eab308');
        setNeed('hygiene', c.hygiene, '#06b6d4');
        setNeed('social', c.social, 'var(--divine-purple)');

        document.getElementById('inspect-overall-mood').innerText = `${c.happiness > 70 ? 'Happy' : 'Neutral'} (${Math.round(c.happiness)}%)`;
        document.getElementById('val-money').innerText = `$${c.money}`;
        document.getElementById('val-wage').innerText = `$${c.hourly_wage}/hr`;

        // Render Relationships
        const relContainer = document.getElementById('inspect-relations-list');
        if (relContainer) {
          relContainer.innerHTML = (c.relationships || []).map(r => `
            <div class="relation-item">
              <span><strong>${r.name}</strong> • ${r.relation}</span>
              <span style="color:var(--accent); font-weight:700;">${r.affinity}%</span>
            </div>
          `).join('');
        }

        // Render Memories
        const memContainer = document.getElementById('inspect-memory-stream');
        if (memContainer) {
          memContainer.innerHTML = (c.memories || []).slice(0, 5).map(m => `
            <div class="memory-item">
              <span style="color:var(--accent); font-weight:700;">[${m.time}]</span> ${m.text}
            </div>
          `).join('');
        }
      }
    }

    /* ==========================================================================
       BFS PATHFINDER (ZERO LATENCY 140x100)
       ========================================================================== */
    function findPathBFS(grid, startX, startY, targetX, targetY) {
      if (!grid || grid.length === 0) return [];
      const h = grid.length;
      const w = grid[0].length;

      if (startX < 0 || startX >= w || startY < 0 || startY >= h) return [];
      if (startX === targetX && startY === targetY) return [];

      // If target is blocked, find nearest walkable tile
      if (grid[targetY][targetX] === 1) {
        let found = false;
        for (let r = 1; r <= 3; r++) {
          for (let dy = -r; dy <= r; dy++) {
            for (let dx = -r; dx <= r; dx++) {
              const nx = targetX + dx;
              const ny = targetY + dy;
              if (nx >= 0 && nx < w && ny >= 0 && ny < h && grid[ny][nx] === 0) {
                targetX = nx;
                targetY = ny;
                found = true;
                break;
              }
            }
            if (found) break;
          }
          if (found) break;
        }
        if (!found) return [];
      }

      const queue = [[startX, startY]];
      const visited = new Uint8Array(w * h);
      const parent = new Int32Array(w * h).fill(-1);

      visited[startY * w + startX] = 1;
      let foundTarget = false;

      const dirs = [[0, -1], [0, 1], [-1, 0], [1, 0]];

      let head = 0;
      while (head < queue.length) {
        const [cx, cy] = queue[head++];
        if (cx === targetX && cy === targetY) {
          foundTarget = true;
          break;
        }

        for (const [dx, dy] of dirs) {
          const nx = cx + dx;
          const ny = cy + dy;
          if (nx >= 0 && nx < w && ny >= 0 && ny < h && grid[ny][nx] === 0) {
            const nIdx = ny * w + nx;
            if (!visited[nIdx]) {
              visited[nIdx] = 1;
              parent[nIdx] = cy * w + cx;
              queue.push([nx, ny]);
            }
          }
        }
      }

      if (!foundTarget) return [];

      const path = [];
      let curr = targetY * w + targetX;
      const startIdx = startY * w + startX;

      while (curr !== startIdx && curr !== -1) {
        path.push([curr % w, Math.floor(curr / w)]);
        curr = parent[curr];
      }

      return path.reverse();
    }

    /* ==========================================================================
       WEATHER CANVAS ENGINE (RAIN, SNOW, STORM, FLASH)
       ========================================================================== */
    class WeatherEngine {
      constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.mode = "Sunny";
        this.particles = [];
        this.resize();
        window.addEventListener('resize', () => this.resize());
        this.animate();
      }

      resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
      }

      setMode(mode) {
        this.mode = mode;
        this.particles = [];
        const count = mode === "Rain" ? 140 : (mode === "Storm" ? 220 : (mode === "Snow" ? 100 : 0));
        for (let i = 0; i < count; i++) {
          this.particles.push({
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            speed: mode === "Snow" ? (1 + Math.random() * 2) : (10 + Math.random() * 14),
            length: mode === "Snow" ? (2 + Math.random() * 3) : (12 + Math.random() * 16),
            drift: (Math.random() - 0.5) * 1.5
          });
        }
      }

      triggerLightning() {
        const flash = document.getElementById('flash-overlay');
        if (!flash) return;
        flash.style.backgroundColor = "rgba(255, 255, 255, 0.75)";
        setTimeout(() => { flash.style.backgroundColor = "rgba(255, 255, 255, 0)"; }, 90);
        setTimeout(() => {
          flash.style.backgroundColor = "rgba(255, 255, 255, 0.4)";
          setTimeout(() => { flash.style.backgroundColor = "rgba(255, 255, 255, 0)"; }, 70);
        }, 140);
      }

      animate() {
        requestAnimationFrame(() => this.animate());
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        if (this.mode === "Sunny" || this.mode === "Overcast" || this.mode === "Drought") return;

        if (this.mode === "Storm" && Math.random() < 0.005) {
          this.triggerLightning();
        }

        if (this.mode === "Rain" || this.mode === "Storm") {
          this.ctx.strokeStyle = "rgba(147, 197, 253, 0.65)";
          this.ctx.lineWidth = 1.5;
          this.ctx.beginPath();
          for (const p of this.particles) {
            this.ctx.moveTo(p.x, p.y);
            this.ctx.lineTo(p.x - 2, p.y + p.length);
            p.y += p.speed;
            p.x -= 1.2;
            if (p.y > this.canvas.height) { p.y = -20; p.x = Math.random() * this.canvas.width; }
          }
          this.ctx.stroke();
        } else if (this.mode === "Snow") {
          this.ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
          for (const p of this.particles) {
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.length, 0, Math.PI * 2);
            this.ctx.fill();
            p.y += p.speed;
            p.x += Math.sin(p.y * 0.03) * 0.8;
            if (p.y > this.canvas.height) { p.y = -10; p.x = Math.random() * this.canvas.width; }
          }
        }
      }
    }

    /* ==========================================================================
       NATURAL-LANGUAGE DIVINE COMMAND PARSER & ENGINE
       ========================================================================== */
    class DivineCommandEngine {
      constructor(sim) {
        this.sim = sim;
      }

      execute(rawText) {
        if (!rawText || !rawText.trim()) return { success: false, msg: "Please enter a command." };
        const text = rawText.trim().toLowerCase();

        // 1. Weather Commands
        if (text.includes("rain")) {
          this.sim.setWeather("Rain");
          return { success: true, msg: "🌧️ Divine Rain summoned upon Smallville." };
        }
        if (text.includes("storm") || text.includes("thunder") || text.includes("lightning")) {
          this.sim.setWeather("Storm");
          return { success: true, msg: "⛈️ Violent Divine Thunderstorm unleashed." };
        }
        if (text.includes("snow") || text.includes("blizzard")) {
          this.sim.setWeather("Snow");
          return { success: true, msg: "❄️ Soft winter snow blanketed the town." };
        }
        if (text.includes("sunny") || text.includes("clear") || text.includes("sunshine")) {
          this.sim.setWeather("Sunny");
          return { success: true, msg: "☀️ Bright golden sunshine restored over Smallville." };
        }
        if (text.includes("drought") || text.includes("heatwave")) {
          this.sim.setWeather("Drought");
          return { success: true, msg: "🔥 Scorching drought cast over Smallville." };
        }

        // 2. World Events & Cataclysms
        if (text.includes("festival") || text.includes("celebration") || text.includes("party")) {
          return this.triggerFestival();
        }
        if (text.includes("food shortage") || text.includes("famine") || text.includes("starvation")) {
          this.sim.townFoodReserves = 5;
          this.sim.citizens.forEach(c => {
            c.hunger = Math.min(100, c.hunger + 40);
            c.currentThought = "Food is running out in town! We need emergency provisions.";
          });
          this.sim.logEvent("A severe food shortage has struck Smallville!", null, "event", "⚠️");
          return { success: true, msg: "⚠️ Emergency food shortage declared (5 Food units remaining)." };
        }
        if (text.includes("gather") && (text.includes("park") || text.includes("johnson park") || text.includes("everyone") || text.includes("all"))) {
          return this.gatherAllInPark();
        }
        if ((text.includes("everyone") || text.includes("all residents") || text.includes("all citizens")) && (text.includes("sleep") || text.includes("bed") || text.includes("curfew"))) {
          this.sim.citizens.forEach(c => {
            c.state = 'sleep';
            c.currentAction = "Divine Curfew: Returning home to bed";
            c.actionEmoji = "💤";
            c.currentThought = "A divine exhaustion has settled over the town. Heading to sleep.";
            this.sim.setCitizenTarget(c, c.bed_coords[0], c.bed_coords[1]);
          });
          this.sim.logEvent("Divine Curfew: All residents ordered to sleep.", null, "divine", "💤");
          return { success: true, msg: "💤 Divine Curfew enacted: All 15 residents are walking home to sleep." };
        }
        if (text.includes("increase happiness") || text.includes("make everyone happy") || text.includes("heal everyone") || text.includes("feed everyone")) {
          this.sim.citizens.forEach(c => {
            c.happiness = 100;
            c.health = 100;
            c.hunger = 10;
            c.energy = 100;
            c.currentThought = "I feel blessed by an unseen celestial grace!";
          });
          this.sim.logEvent("Divine Blessing bestowed upon all citizens (100% Needs).", null, "divine", "✨");
          return { success: true, msg: "✨ Divine Blessing granted: All residents restored to 100% Happiness, Health, and Energy." };
        }
        if (text.includes("unemployed") && (text.includes("job") || text.includes("work"))) {
          return { success: true, msg: "💼 All residents are actively assigned town professions." };
        }

        // 3. Citizen Specific Commands
        // Find matching target citizen
        let targetCitizen = null;
        for (const c of this.sim.citizens) {
          const firstName = c.name.split(' ')[0].toLowerCase();
          const fullName = c.name.toLowerCase();
          if (text.includes(fullName) || text.includes(firstName)) {
            targetCitizen = c;
            break;
          }
        }

        if (targetCitizen) {
          // Check for Money commands
          const moneyMatch = text.match(/(?:give|grant|award|send)\s+.*?(\d+)\s*(?:coins|dollars|money|\$)?/i) || text.match(/\$(\d+)/);
          if (moneyMatch && (text.includes("give") || text.includes("grant") || text.includes("send"))) {
            const amount = parseInt(moneyMatch[1]);
            targetCitizen.money += amount;
            targetCitizen.memories.unshift({
              time: this.sim.formatTime(this.sim.hour, this.sim.minute),
              text: `Received a divine blessing of $${amount}!`
            });
            this.sim.logEvent(`Granted $${amount} to ${targetCitizen.name}.`, targetCitizen.name, "divine", "💰");
            selectCitizen(targetCitizen);
            return { success: true, msg: `💰 Granted $${amount} to ${targetCitizen.name} (New Balance: $${targetCitizen.money}).` };
          }

          // Check for Destination Commands
          if (text.includes("work") || text.includes("job") || text.includes("office") || text.includes("counter")) {
            executeDivineMoveTarget(targetCitizen, targetCitizen.workplace_coords[0], targetCitizen.workplace_coords[1], "work", `Heading to work at ${targetCitizen.workplace_name}`);
            return { success: true, msg: `🏢 ${targetCitizen.name} commanded to work at ${targetCitizen.workplace_name}.` };
          }
          if (text.includes("home") || text.includes("apartment") || text.includes("house")) {
            executeDivineMoveTarget(targetCitizen, targetCitizen.home_coords[0], targetCitizen.home_coords[1], "home", `Heading home to ${targetCitizen.home_name}`);
            return { success: true, msg: `🏠 ${targetCitizen.name} commanded to return to ${targetCitizen.home_name}.` };
          }
          if (text.includes("park") || text.includes("johnson park") || text.includes("gazebo")) {
            executeDivineMoveTarget(targetCitizen, 39, 44, "social", "Visiting Johnson Park");
            return { success: true, msg: `🌳 ${targetCitizen.name} commanded to visit Johnson Park.` };
          }
          if (text.includes("cafe") || text.includes("hobbs cafe") || text.includes("coffee")) {
            executeDivineMoveTarget(targetCitizen, 77, 22, "eat", "Visiting Hobbs Cafe");
            return { success: true, msg: `☕ ${targetCitizen.name} commanded to visit Hobbs Cafe.` };
          }
          if (text.includes("pub") || text.includes("rose & crown") || text.includes("bar")) {
            executeDivineMoveTarget(targetCitizen, 60, 31, "eat", "Visiting The Rose & Crown Pub");
            return { success: true, msg: `🍺 ${targetCitizen.name} commanded to visit The Rose & Crown Pub.` };
          }
          if (text.includes("sleep") || text.includes("bed")) {
            executeDivineMoveTarget(targetCitizen, targetCitizen.bed_coords[0], targetCitizen.bed_coords[1], "sleep", "Going to sleep in bed");
            return { success: true, msg: `🛏️ ${targetCitizen.name} commanded to sleep.` };
          }
        }

        return {
          success: false,
          msg: `Unrecognized command. Try e.g. "Make Isabella go to cafe", "Give Klaus 500 coins", "Make it rain", or "Gather everyone at Johnson Park".`
        };
      }

      triggerFestival() {
        this.sim.townEconomy += 1500;
        this.sim.townFoodReserves += 80;
        this.sim.setWeather("Sunny");

        this.sim.citizens.forEach(c => {
          c.happiness = Math.min(100, c.happiness + 25);
          c.currentThought = "The Town Festival is happening! Everyone is gathering in Johnson Park to celebrate!";
          c.currentAction = "Celebrating at Smallville Town Festival";
          c.actionEmoji = "🎉";
          // Scatter slightly around Johnson Park center [39, 44]
          const offsetDX = Math.floor(Math.random() * 5) - 2;
          const offsetDY = Math.floor(Math.random() * 5) - 2;
          this.sim.setCitizenTarget(c, 39 + offsetDX, 44 + offsetDY);
        });

        this.sim.logEvent("Town Festival underway at Johnson Park! All residents celebrating.", null, "event", "🎉");
        if (camera) camera.centerOn(39 * 32, 44 * 32);
        return { success: true, msg: "🎉 Smallville Town Festival initiated! All 15 residents converging on Johnson Park." };
      }

      gatherAllInPark() {
        this.sim.citizens.forEach(c => {
          c.currentThought = "Summoned to Johnson Park by divine decree!";
          c.currentAction = "Gathering at Johnson Park";
          c.actionEmoji = "📢";
          const offsetDX = Math.floor(Math.random() * 7) - 3;
          const offsetDY = Math.floor(Math.random() * 7) - 3;
          this.sim.setCitizenTarget(c, 39 + offsetDX, 44 + offsetDY);
        });
        this.sim.logEvent("All residents commanded to assemble at Johnson Park.", null, "divine", "📢");
        if (camera) camera.centerOn(39 * 32, 44 * 32);
        return { success: true, msg: "📢 Divine decree issued: All residents navigating to Johnson Park gazebo." };
      }
    }

    /* ==========================================================================
       PHASER 3 GAME SCENE & RENDERING
       ========================================================================== */
    const sim = new SocietySimulation();
    window.societySim = sim;
    const commandEngine = new DivineCommandEngine(sim);

    const phaserConfig = {
      type: Phaser.AUTO,
      parent: 'game-container',
      width: window.innerWidth,
      height: window.innerHeight,
      pixelArt: true,
      physics: {
        default: 'arcade',
        arcade: { gravity: { y: 0 } }
      },
      scene: {
        preload: phaserPreload,
        create: phaserCreate,
        update: phaserUpdate
      }
    };

    let phaserGame;
    let phaserScene;
    let camera;
    let followTarget = null;
    let isDragging = false;
    let dragStartX = 0;
    let dragStartY = 0;
    let divineReticle = null;

    function phaserPreload() {
      phaserScene = this;
      this.load.crossOrigin = '';

      // Load Tilesets
      this.load.image("blocks_1", "/static/assets/the_ville/visuals/map_assets/blocks/blocks_1.png");
      this.load.image("walls", "/static/assets/the_ville/visuals/map_assets/v1/Room_Builder_32x32.png");
      this.load.image("interiors_pt1", "/static/assets/the_ville/visuals/map_assets/v1/interiors_pt1.png");
      this.load.image("interiors_pt2", "/static/assets/the_ville/visuals/map_assets/v1/interiors_pt2.png");
      this.load.image("interiors_pt3", "/static/assets/the_ville/visuals/map_assets/v1/interiors_pt3.png");
      this.load.image("interiors_pt4", "/static/assets/the_ville/visuals/map_assets/v1/interiors_pt4.png");
      this.load.image("interiors_pt5", "/static/assets/the_ville/visuals/map_assets/v1/interiors_pt5.png");
      this.load.image("CuteRPG_Field_B", "/static/assets/the_ville/visuals/map_assets/cute_rpg_word_VXAce/tilesets/CuteRPG_Field_B.png");
      this.load.image("CuteRPG_Field_C", "/static/assets/the_ville/visuals/map_assets/cute_rpg_word_VXAce/tilesets/CuteRPG_Field_C.png");
      this.load.image("CuteRPG_Harbor_C", "/static/assets/the_ville/visuals/map_assets/cute_rpg_word_VXAce/tilesets/CuteRPG_Harbor_C.png");
      this.load.image("CuteRPG_Village_B", "/static/assets/the_ville/visuals/map_assets/cute_rpg_word_VXAce/tilesets/CuteRPG_Village_B.png");
      this.load.image("CuteRPG_Forest_B", "/static/assets/the_ville/visuals/map_assets/cute_rpg_word_VXAce/tilesets/CuteRPG_Forest_B.png");
      this.load.image("CuteRPG_Desert_C", "/static/assets/the_ville/visuals/map_assets/cute_rpg_word_VXAce/tilesets/CuteRPG_Desert_C.png");
      this.load.image("CuteRPG_Mountains_B", "/static/assets/the_ville/visuals/map_assets/cute_rpg_word_VXAce/tilesets/CuteRPG_Mountains_B.png");
      this.load.image("CuteRPG_Desert_B", "/static/assets/the_ville/visuals/map_assets/cute_rpg_word_VXAce/tilesets/CuteRPG_Desert_B.png");
      this.load.image("CuteRPG_Forest_C", "/static/assets/the_ville/visuals/map_assets/cute_rpg_word_VXAce/tilesets/CuteRPG_Forest_C.png");

      // Load Tilemap JSON
      this.load.tilemapTiledJSON("smallville_map", "/static/assets/the_ville/visuals/the_ville_jan7.json");

      // Load Speech Bubble
      this.load.image('speech_bubble_img', "/static/assets/speech_bubble/v3.png");

      // Load Character Atlases
      const characterNames = [
        "Isabella_Rodriguez", "Klaus_Mueller", "Maria_Lopez", "Arthur_Burton",
        "John_Lin", "Mei_Lin", "Eddy_Lin", "Giorgio_Rossi", "Tom_Moreno",
        "Jane_Moreno", "Sam_Moore", "Abigail_Chen", "Carlos_Gomez", "Hailey_Johnson", "Francisco_Lopez"
      ];

      characterNames.forEach(cName => {
        this.load.atlas(cName, `/static/assets/characters/${cName}.png`, "/static/assets/characters/atlas.json");
      });
    }

    function phaserCreate() {
      const map = this.make.tilemap({ key: "smallville_map" });

      const collisions = map.addTilesetImage("blocks", "blocks_1");
      const walls = map.addTilesetImage("Room_Builder_32x32", "walls");
      const interiors_pt1 = map.addTilesetImage("interiors_pt1", "interiors_pt1");
      const interiors_pt2 = map.addTilesetImage("interiors_pt2", "interiors_pt2");
      const interiors_pt3 = map.addTilesetImage("interiors_pt3", "interiors_pt3");
      const interiors_pt4 = map.addTilesetImage("interiors_pt4", "interiors_pt4");
      const interiors_pt5 = map.addTilesetImage("interiors_pt5", "interiors_pt5");
      const CuteRPG_Field_B = map.addTilesetImage("CuteRPG_Field_B", "CuteRPG_Field_B");
      const CuteRPG_Field_C = map.addTilesetImage("CuteRPG_Field_C", "CuteRPG_Field_C");
      const CuteRPG_Harbor_C = map.addTilesetImage("CuteRPG_Harbor_C", "CuteRPG_Harbor_C");
      const CuteRPG_Village_B = map.addTilesetImage("CuteRPG_Village_B", "CuteRPG_Village_B");
      const CuteRPG_Forest_B = map.addTilesetImage("CuteRPG_Forest_B", "CuteRPG_Forest_B");
      const CuteRPG_Desert_C = map.addTilesetImage("CuteRPG_Desert_C", "CuteRPG_Desert_C");
      const CuteRPG_Mountains_B = map.addTilesetImage("CuteRPG_Mountains_B", "CuteRPG_Mountains_B");
      const CuteRPG_Desert_B = map.addTilesetImage("CuteRPG_Desert_B", "CuteRPG_Desert_B");
      const CuteRPG_Forest_C = map.addTilesetImage("CuteRPG_Forest_C", "CuteRPG_Forest_C");

      const tilesetGroup = [
        CuteRPG_Field_B, CuteRPG_Field_C, CuteRPG_Harbor_C, CuteRPG_Village_B,
        CuteRPG_Forest_B, CuteRPG_Desert_C, CuteRPG_Mountains_B, CuteRPG_Desert_B, CuteRPG_Forest_C,
        interiors_pt1, interiors_pt2, interiors_pt3, interiors_pt4, interiors_pt5, walls
      ];

      // Create Layers
      map.createLayer("Bottom Ground", tilesetGroup, 0, 0);
      map.createLayer("Exterior Ground", tilesetGroup, 0, 0);
      map.createLayer("Exterior Decoration L1", tilesetGroup, 0, 0);
      map.createLayer("Exterior Decoration L2", tilesetGroup, 0, 0);
      map.createLayer("Interior Ground", tilesetGroup, 0, 0);
      map.createLayer("Wall", [CuteRPG_Field_C, walls], 0, 0);
      map.createLayer("Interior Furniture L1", tilesetGroup, 0, 0);
      map.createLayer("Interior Furniture L2 ", tilesetGroup, 0, 0);

      const foregroundL1 = map.createLayer("Foreground L1", tilesetGroup, 0, 0);
      const foregroundL2 = map.createLayer("Foreground L2", tilesetGroup, 0, 0);
      foregroundL1.setDepth(2);
      foregroundL2.setDepth(2);

      // Camera setup
      camera = this.cameras.main;
      camera.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
      camera.setZoom(1.1);
      camera.centerOn(77 * 32, 22 * 32);

      // Divine Reticle for click target
      divineReticle = this.add.circle(0, 0, 16, 0xf59e0b, 0.4);
      divineReticle.setStrokeStyle(2, 0xfde047);
      divineReticle.setDepth(10);
      divineReticle.visible = false;

      // Setup Walking Animations
      sim.citizens.forEach(c => {
        const cKey = c.underscore;
        this.anims.create({
          key: `${cKey}-down-walk`,
          frames: this.anims.generateFrameNames(cKey, { prefix: "down-walk.", start: 0, end: 3, zeroPad: 3 }),
          frameRate: 6,
          repeat: -1
        });
        this.anims.create({
          key: `${cKey}-up-walk`,
          frames: this.anims.generateFrameNames(cKey, { prefix: "up-walk.", start: 0, end: 3, zeroPad: 3 }),
          frameRate: 6,
          repeat: -1
        });
        this.anims.create({
          key: `${cKey}-left-walk`,
          frames: this.anims.generateFrameNames(cKey, { prefix: "left-walk.", start: 0, end: 3, zeroPad: 3 }),
          frameRate: 6,
          repeat: -1
        });
        this.anims.create({
          key: `${cKey}-right-walk`,
          frames: this.anims.generateFrameNames(cKey, { prefix: "right-walk.", start: 0, end: 3, zeroPad: 3 }),
          frameRate: 6,
          repeat: -1
        });

        // Create Character Sprite
        const sprite = this.physics.add.sprite(c.pixelX, c.pixelY, cKey, "down");
        sprite.setDepth(1);
        sprite.displayWidth = 36;
        sprite.displayHeight = 44;
        sprite.setInteractive({ cursor: 'pointer' });

        sprite.on('pointerdown', (pointer) => {
          pointer.event.stopPropagation();
          selectCitizen(c);
        });

        c.sprite = sprite;

        // Activity Emoji Badge
        c.emojiIcon = this.add.text(c.pixelX - 10, c.pixelY - 42, c.actionEmoji, {
          font: '18px monospace',
          padding: { x: 4, y: 4 },
          backgroundColor: '#0f172a',
          color: '#ffffff'
        });
        c.emojiIcon.setDepth(3);

        // Comic Speech Bubble
        c.speechBubble = this.add.image(c.pixelX + 60, c.pixelY - 35, 'speech_bubble_img');
        c.speechBubble.setDepth(4);
        c.speechBubble.displayWidth = 135;
        c.speechBubble.displayHeight = 65;
        c.speechBubble.visible = false;

        c.speechText = this.add.text(c.pixelX - 10, c.pixelY - 55, '', {
          font: '10px sans-serif',
          color: '#000000',
          wordWrap: { width: 110 }
        });
        c.speechText.setDepth(5);
        c.speechText.visible = false;
      });

      // Canvas Map Click Handler: Deselect or Divine Click-to-Move
      this.input.on('pointerdown', (pointer) => {
        if (pointer.rightButtonDown()) return;
        const worldPoint = camera.getWorldPoint(pointer.x, pointer.y);
        const tileX = Math.floor(worldPoint.x / 32);
        const tileY = Math.floor(worldPoint.y / 32);

        if (window.isMapTargetSelectionActive && sim.selectedCitizen) {
          // Send selected citizen to this exact tile!
          executeDivineMoveTarget(sim.selectedCitizen, tileX, tileY, "divine", `Navigating to target [${tileX}, ${tileY}] by Divine Decree`);
          window.isMapTargetSelectionActive = false;
          document.body.style.cursor = 'default';
          return;
        }

        // Click on empty ground closes the inspector HUD!
        deselectCitizen();
      });

      // Camera Dragging
      this.input.on('pointerdown', (pointer) => {
        if (pointer.rightButtonDown() || pointer.middleButtonDown() || this.input.keyboard.checkDown(this.input.keyboard.addKey('SPACE'))) {
          isDragging = true;
          dragStartX = pointer.x;
          dragStartY = pointer.y;
          followTarget = null;
        }
      });

      this.input.on('pointermove', (pointer) => {
        if (isDragging) {
          camera.scrollX -= (pointer.x - dragStartX) / camera.zoom;
          camera.scrollY -= (pointer.y - dragStartY) / camera.zoom;
          dragStartX = pointer.x;
          dragStartY = pointer.y;
        }
      });

      this.input.on('pointerup', () => { isDragging = false; });

      // Mouse Wheel Zoom
      this.input.on('wheel', (pointer, gameObjects, deltaX, deltaY) => {
        if (deltaY > 0) camera.setZoom(Math.max(0.45, camera.zoom - 0.1));
        else camera.setZoom(Math.min(2.4, camera.zoom + 0.1));
      });
    }

    function phaserUpdate(time, delta) {
      if (followTarget && !isDragging) {
        camera.centerOn(
          Phaser.Math.Linear(camera.midPoint.x, followTarget.x, 0.08),
          Phaser.Math.Linear(camera.midPoint.y, followTarget.y, 0.08)
        );
      }

      // Update Citizen Movements along BFS Path
      sim.citizens.forEach(c => {
        if (c.isWalking && c.currentPath.length > 0) {
          const targetTile = c.currentPath[c.pathIndex];
          const targetPxX = targetTile[0] * 32 + 16;
          const targetPxY = targetTile[1] * 32 + 16;

          const dx = targetPxX - c.pixelX;
          const dy = targetPxY - c.pixelY;
          const dist = Math.hypot(dx, dy);

          const moveStep = 90 * (delta / 1000) * sim.speed;

          if (dist <= moveStep) {
            c.pixelX = targetPxX;
            c.pixelY = targetPxY;
            c.tileX = targetTile[0];
            c.tileY = targetTile[1];
            c.pathIndex++;

            if (c.pathIndex >= c.currentPath.length) {
              c.isWalking = false;
              c.sprite.anims.stop();
              c.sprite.setTexture(c.underscore, c.facing);
            }
          } else {
            const vx = (dx / dist) * moveStep;
            const vy = (dy / dist) * moveStep;
            c.pixelX += vx;
            c.pixelY += vy;

            if (Math.abs(dx) > Math.abs(dy)) c.facing = dx > 0 ? 'right' : 'left';
            else c.facing = dy > 0 ? 'down' : 'up';
            c.sprite.anims.play(`${c.underscore}-${c.facing}-walk`, true);
          }
        }

        // Sync Sprite Position
        if (c.sprite) {
          c.sprite.x = c.pixelX;
          c.sprite.y = c.pixelY;

          if (c.emojiIcon) {
            c.emojiIcon.x = c.pixelX - 10;
            c.emojiIcon.y = c.pixelY - 42;
            c.emojiIcon.setText(c.actionEmoji);
          }
          if (c.speechBubble) {
            c.speechBubble.x = c.pixelX + 60;
            c.speechBubble.y = c.pixelY - 35;
          }
          if (c.speechText) {
            c.speechText.x = c.pixelX - 10;
            c.speechText.y = c.pixelY - 55;
          }
        }
      });
    }

    /* ==========================================================================
       UI INTERACTION & DIVINE ACTIONS
       ========================================================================== */
    function selectCitizen(c) {
      sim.selectedCitizen = c;
      followTarget = c.sprite;
      sim.updateInspectorHUD(c);

      // Open Inspector HUD
      const inspector = document.getElementById('right-inspector-pane');
      if (inspector) inspector.classList.add('open');

      // Highlight in Roster
      document.querySelectorAll('.citizen-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.id == c.id);
      });
    }

    function deselectCitizen() {
      sim.selectedCitizen = null;
      followTarget = null;
      const inspector = document.getElementById('right-inspector-pane');
      if (inspector) inspector.classList.remove('open');
      document.querySelectorAll('.citizen-card').forEach(card => card.classList.remove('selected'));
    }

    function executeDivineMoveTarget(c, targetX, targetY, stateType = "divine", actionDesc = "Moving by Divine Decree") {
      c.state = stateType;
      c.currentAction = actionDesc;
      c.actionEmoji = "⚡";
      c.currentThought = `An overwhelming divine clarity compels me to visit [${targetX}, ${targetY}]!`;
      c.divineCommand = { active: true, action: actionDesc, dest: [targetX, targetY], resumeState: 'home', ticksAtDest: 0 };
      
      sim.setCitizenTarget(c, targetX, targetY);

      if (divineReticle) {
        divineReticle.x = targetX * 32 + 16;
        divineReticle.y = targetY * 32 + 16;
        divineReticle.visible = true;
        phaserScene.tweens.add({
          targets: divineReticle,
          scale: { from: 1.5, to: 1.0 },
          alpha: { from: 1.0, to: 0.3 },
          duration: 600,
          yoyo: true,
          repeat: 3,
          onComplete: () => { divineReticle.visible = false; }
        });
      }

      sim.logEvent(`Divine Decree: Sent ${c.name} to [${targetX}, ${targetY}].`, c.name, "divine", "⚡");
      sim.updateInspectorHUD(c);
    }

    function renderRosterList(filter = 'all') {
      const container = document.getElementById('citizen-roster-list');
      if (!container) return;

      const filtered = sim.citizens.filter(c => {
        if (filter === 'all') return true;
        if (filter === 'working') return c.state === 'work';
        if (filter === 'social') return c.state === 'social' || c.state === 'eat';
        if (filter === 'home') return c.state === 'home' || c.state === 'sleep';
        return true;
      });

      container.innerHTML = filtered.map(c => `
        <div class="citizen-card ${sim.selectedCitizen && sim.selectedCitizen.id === c.id ? 'selected' : ''} ${c.divineCommand && c.divineCommand.active ? 'divine-controlled' : ''}" data-id="${c.id}">
          <div class="citizen-avatar-wrapper">
            <img src="/static/assets/characters/profile/${c.underscore}.png" class="citizen-avatar" alt="${c.name}">
            <div class="citizen-status-dot status-${c.state}"></div>
          </div>
          <div class="citizen-info">
            <div class="citizen-name-row">
              <span class="citizen-name">${c.name}</span>
              <span style="font-size:0.95rem;">${c.actionEmoji}</span>
            </div>
            <div class="citizen-job">${c.occupation}</div>
            <div class="citizen-mini-bar">
              <div class="citizen-mini-fill" style="width:${c.happiness}%;"></div>
            </div>
          </div>
        </div>
      `).join('');

      container.querySelectorAll('.citizen-card').forEach(card => {
        card.addEventListener('click', () => {
          const id = parseInt(card.dataset.id);
          const c = sim.citizens.find(item => item.id === id);
          if (c) selectCitizen(c);
        });
      });
    }

    /* ==========================================================================
       INITIALIZATION ON WINDOW LOAD
       ========================================================================== */
    window.addEventListener('load', async () => {
      try {
        const [gridRes, citizensRes, locsRes] = await Promise.all([
          fetch('/static/assets/the_ville/the_ville_collision_grid.json'),
          fetch('/static/assets/the_ville/society_citizens.json'),
          fetch('/static/assets/the_ville/world_locations.json')
        ]);

        window.SIM_DATA.collisionGrid = await gridRes.json();
        window.SIM_DATA.citizens = await citizensRes.json();
        window.SIM_DATA.locations = await locsRes.json();

        // Initialize Society
        sim.initCitizens(window.SIM_DATA.citizens);

        // Start Phaser Game
        phaserGame = new Phaser.Game(phaserConfig);

        // Start Weather Canvas Engine
        window.weatherEngine = new WeatherEngine('weather-canvas');

        // Populate Roster
        renderRosterList();

        // Setup Simulation Clock Interval
        setInterval(() => {
          sim.tickSimulation();
        }, 1000 / sim.speed);

        // Setup Play / Pause
        const btnPlay = document.getElementById('btn-play-pause');
        btnPlay.addEventListener('click', () => {
          sim.isRunning = !sim.isRunning;
          btnPlay.innerText = sim.isRunning ? '⏸ PAUSE' : '▶ RESUME';
          btnPlay.classList.toggle('active', !sim.isRunning);
        });

        // Top Speed buttons
        document.querySelectorAll('.time-ctrl-btn[data-speed]').forEach(btn => {
          btn.addEventListener('click', () => {
            document.querySelectorAll('.time-ctrl-btn[data-speed]').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            sim.speed = parseFloat(btn.dataset.speed);
          });
        });

        // Left Roster Toggle & Close
        const rosterPane = document.getElementById('left-roster-pane');
        document.getElementById('btn-toggle-roster').addEventListener('click', () => {
          rosterPane.classList.toggle('open');
        });
        document.getElementById('btn-close-roster').addEventListener('click', () => {
          rosterPane.classList.remove('open');
        });

        // Right Inspector Close
        document.getElementById('btn-close-inspector').addEventListener('click', () => {
          deselectCitizen();
        });

        // Event Log Drawer Toggle & Close
        const logDrawer = document.getElementById('divine-log-drawer');
        document.getElementById('btn-toggle-log').addEventListener('click', () => {
          logDrawer.classList.toggle('open');
        });
        document.getElementById('btn-close-log').addEventListener('click', () => {
          logDrawer.classList.remove('open');
        });

        // God Powers Drawer Toggle & Close
        const godOverlay = document.getElementById('god-drawer-overlay');
        document.getElementById('btn-toggle-god-drawer').addEventListener('click', () => {
          godOverlay.classList.add('open');
        });
        document.getElementById('btn-close-god-drawer').addEventListener('click', () => {
          godOverlay.classList.remove('open');
        });

        // Focus Command Bar
        document.getElementById('btn-focus-command').addEventListener('click', () => {
          const input = document.getElementById('god-command-input');
          input.focus();
          input.scrollIntoView({ behavior: 'smooth' });
        });

        // Submit Divine Command
        const submitCommand = () => {
          const input = document.getElementById('god-command-input');
          const res = commandEngine.execute(input.value);
          const feedbackCard = document.getElementById('command-feedback-card');
          const feedbackBadge = document.getElementById('feedback-badge');
          const feedbackText = document.getElementById('feedback-text');

          feedbackCard.style.display = 'flex';
          feedbackBadge.innerText = res.success ? "DIVINE WILL" : "GUIDANCE";
          feedbackBadge.style.color = res.success ? "#34d399" : "#f59e0b";
          feedbackText.innerText = res.msg;

          if (res.success) input.value = '';
        };

        document.getElementById('btn-submit-divine').addEventListener('click', submitCommand);
        document.getElementById('god-command-input').addEventListener('keydown', (e) => {
          if (e.key === 'Enter') submitCommand();
        });

        document.getElementById('btn-close-feedback').addEventListener('click', () => {
          document.getElementById('command-feedback-card').style.display = 'none';
        });

        // Suggestion Chips
        document.querySelectorAll('.suggestion-chips-row button').forEach(chip => {
          chip.addEventListener('click', () => {
            const input = document.getElementById('god-command-input');
            input.value = chip.dataset.cmd;
            submitCommand();
          });
        });

        // Inspector Divine Interventions
        document.getElementById('btn-god-give-money').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          sim.selectedCitizen.money += 100;
          sim.logEvent(`Granted $100 to ${sim.selectedCitizen.name}.`, sim.selectedCitizen.name, "divine", "💰");
          sim.updateInspectorHUD(sim.selectedCitizen);
        });

        document.getElementById('btn-god-take-money').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          sim.selectedCitizen.money = Math.max(0, sim.selectedCitizen.money - 50);
          sim.logEvent(`Deducted $50 from ${sim.selectedCitizen.name}.`, sim.selectedCitizen.name, "divine", "💸");
          sim.updateInspectorHUD(sim.selectedCitizen);
        });

        document.getElementById('btn-god-bless-needs').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          const c = sim.selectedCitizen;
          c.hunger = 10;
          c.energy = 100;
          c.health = 100;
          c.happiness = 100;
          c.hygiene = 100;
          c.social = 100;
          c.currentThought = "A warm celestial light enveloped me, soothing my soul!";
          sim.logEvent(`Bestowed Divine Blessing on ${c.name} (100% Needs).`, c.name, "divine", "✨");
          sim.updateInspectorHUD(c);
        });

        document.getElementById('btn-god-force-work').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          const c = sim.selectedCitizen;
          executeDivineMoveTarget(c, c.workplace_coords[0], c.workplace_coords[1], "work", `Force Shift at ${c.workplace_name}`);
        });

        document.getElementById('btn-god-force-home').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          const c = sim.selectedCitizen;
          executeDivineMoveTarget(c, c.home_coords[0], c.home_coords[1], "home", `Force Return to ${c.home_name}`);
        });

        document.getElementById('btn-god-force-cafe').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          executeDivineMoveTarget(sim.selectedCitizen, 77, 22, "eat", "Visiting Hobbs Cafe");
        });

        document.getElementById('btn-god-force-park').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          executeDivineMoveTarget(sim.selectedCitizen, 39, 44, "social", "Visiting Johnson Park");
        });

        document.getElementById('btn-god-force-sleep').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          const c = sim.selectedCitizen;
          executeDivineMoveTarget(c, c.bed_coords[0], c.bed_coords[1], "sleep", "Sent to sleep in bed");
        });

        document.getElementById('btn-god-release-control').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          const c = sim.selectedCitizen;
          c.divineCommand = null;
          c.state = 'home';
          c.currentAction = "Resumed autonomous living";
          c.actionEmoji = "🕊️";
          sim.logEvent(`Released control of ${c.name} back to Autonomous AI.`, c.name, "divine", "🕊️");
          sim.updateInspectorHUD(c);
        });

        // Click Map Tile Target Mode
        document.getElementById('btn-god-target-tile').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          window.isMapTargetSelectionActive = true;
          document.body.style.cursor = 'crosshair';
          alert(`Click any walkable tile on the map to send ${sim.selectedCitizen.name} there.`);
        });

        // Camera Shortcuts in Inspector
        document.getElementById('btn-cam-follow').addEventListener('click', () => {
          if (sim.selectedCitizen) followTarget = sim.selectedCitizen.sprite;
        });
        document.getElementById('btn-cam-focus').addEventListener('click', () => {
          if (sim.selectedCitizen && camera) camera.centerOn(sim.selectedCitizen.pixelX, sim.selectedCitizen.pixelY);
        });
        document.getElementById('btn-cam-home').addEventListener('click', () => {
          if (sim.selectedCitizen && camera) camera.centerOn(sim.selectedCitizen.home_coords[0] * 32, sim.selectedCitizen.home_coords[1] * 32);
        });
        document.getElementById('btn-cam-work').addEventListener('click', () => {
          if (sim.selectedCitizen && camera) camera.centerOn(sim.selectedCitizen.workplace_coords[0] * 32, sim.selectedCitizen.workplace_coords[1] * 32);
        });
        document.getElementById('btn-open-schedule').addEventListener('click', () => {
          if (!sim.selectedCitizen) return;
          const modal = document.getElementById('modal-schedule');
          document.getElementById('schedule-modal-title').innerText = `🗓️ 24h Routine • ${sim.selectedCitizen.name}`;
          const timeline = document.getElementById('schedule-timeline');
          timeline.innerHTML = Object.entries(sim.selectedCitizen.schedule || {}).map(([t, item]) => `
            <div style="background:#1e293b; padding:8px 12px; border-radius:6px; font-size:0.8rem; display:flex; justify-content:space-between; align-items:center;">
              <span style="color:var(--accent); font-weight:700;">${t}</span>
              <span>${item.emoji || '🚶'} ${item.action}</span>
            </div>
          `).join('');
          modal.classList.add('open');
        });

        // God Drawer Power Buttons
        document.getElementById('btn-drawer-pause').addEventListener('click', () => {
          sim.isRunning = false;
          btnPlay.innerText = '▶ RESUME';
        });
        document.getElementById('btn-drawer-resume').addEventListener('click', () => {
          sim.isRunning = true;
          btnPlay.innerText = '⏸ PAUSE';
        });
        document.getElementById('btn-drawer-reset').addEventListener('click', () => {
          location.reload();
        });

        document.querySelectorAll('button[data-god-speed]').forEach(btn => {
          btn.addEventListener('click', () => {
            document.querySelectorAll('button[data-god-speed]').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            sim.speed = parseFloat(btn.dataset.godSpeed);
            document.getElementById('label-speed-val').innerText = `${sim.speed}x`;
          });
        });

        // Time Slider Scrub
        const timeSlider = document.getElementById('slider-time-scrub');
        timeSlider.addEventListener('input', () => {
          const val = parseInt(timeSlider.value);
          const h = Math.floor(val / 60);
          const m = val % 60;
          sim.setTime(h, m);
        });

        document.querySelectorAll('button[data-jump-time]').forEach(btn => {
          btn.addEventListener('click', () => {
            const h = parseInt(btn.dataset.jumpTime);
            sim.setTime(h, 0);
            timeSlider.value = h * 60;
          });
        });

        document.querySelectorAll('button[data-god-season]').forEach(btn => {
          btn.addEventListener('click', () => {
            document.querySelectorAll('button[data-god-season]').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            sim.setSeason(btn.dataset.godSeason);
          });
        });

        document.querySelectorAll('button[data-god-weather]').forEach(btn => {
          btn.addEventListener('click', () => {
            document.querySelectorAll('button[data-god-weather]').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            sim.setWeather(btn.dataset.godWeather);
          });
        });

        document.getElementById('btn-ambient-auto').addEventListener('click', () => {
          sim.forceAmbient = null;
          sim.updateAmbientDaylight();
        });
        document.getElementById('btn-ambient-day').addEventListener('click', () => {
          sim.forceAmbient = 'day';
          sim.updateAmbientDaylight();
        });
        document.getElementById('btn-ambient-night').addEventListener('click', () => {
          sim.forceAmbient = 'night';
          sim.updateAmbientDaylight();
        });

        // Events in drawer
        document.getElementById('btn-event-festival').addEventListener('click', () => {
          commandEngine.triggerFestival();
        });
        document.getElementById('btn-event-gather-park').addEventListener('click', () => {
          commandEngine.gatherAllInPark();
        });
        document.getElementById('btn-event-curfew').addEventListener('click', () => {
          commandEngine.execute("make everyone go to sleep");
        });
        document.getElementById('btn-event-work-rush').addEventListener('click', () => {
          sim.citizens.forEach(c => {
            executeDivineMoveTarget(c, c.workplace_coords[0], c.workplace_coords[1], "work", `Morning Work Rush at ${c.workplace_name}`);
          });
        });

        document.getElementById('btn-add-food').addEventListener('click', () => {
          sim.townFoodReserves += 50;
          document.getElementById('label-food-val').innerText = `${sim.townFoodReserves} Units`;
          sim.logEvent("Granted +50 Food reserves to town.", null, "divine", "🌾");
        });
        document.getElementById('btn-sub-food').addEventListener('click', () => {
          sim.townFoodReserves = Math.max(0, sim.townFoodReserves - 50);
          document.getElementById('label-food-val').innerText = `${sim.townFoodReserves} Units`;
        });
        document.getElementById('btn-famine').addEventListener('click', () => {
          commandEngine.execute("create a food shortage in the town");
        });

        document.getElementById('btn-stimulus-boom').addEventListener('click', () => {
          sim.townEconomy += 2000;
          sim.citizens.forEach(c => c.money += 150);
          document.getElementById('label-econ-val').innerText = `$${sim.townEconomy}`;
          sim.logEvent("Economic Stimulus granted (+$2,000 treasury, +$150/citizen).", null, "divine", "💰");
        });

        // Zoom Buttons
        document.getElementById('btn-zoom-in').addEventListener('click', () => {
          if (camera) camera.setZoom(Math.min(2.4, camera.zoom + 0.2));
        });
        document.getElementById('btn-zoom-out').addEventListener('click', () => {
          if (camera) camera.setZoom(Math.max(0.45, camera.zoom - 0.2));
        });
        document.getElementById('btn-zoom-reset').addEventListener('click', () => {
          if (camera) camera.setZoom(1.1);
        });

        // Setup Modals
        setupModal('btn-open-analytics', 'modal-analytics', renderAnalyticsCharts);
        setupModal('btn-open-saveload', 'modal-saveload');

        sim.logEvent("Smallville Divine God Simulator initialized. 15 citizens active.", null, "divine", "👑");
      } catch (err) {
        console.error("Simulation asset error:", err);
      }
    });

    function setupModal(triggerId, modalId, onOpen = null) {
      const trigger = document.getElementById(triggerId);
      const modal = document.getElementById(modalId);
      if (!trigger || !modal) return;

      trigger.addEventListener('click', () => {
        modal.classList.add('open');
        if (onOpen) onOpen();
      });

      modal.querySelectorAll('.btn-close-modal').forEach(btn => {
        btn.addEventListener('click', () => modal.classList.remove('open'));
      });

      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('open');
      });
    }

    let happinessChartInstance = null;
    let economyChartInstance = null;

    function renderAnalyticsCharts() {
      const happyCanvas = document.getElementById('chart-happiness');
      const econCanvas = document.getElementById('chart-economy');
      if (!happyCanvas || !econCanvas) return;

      if (happinessChartInstance) happinessChartInstance.destroy();
      if (economyChartInstance) economyChartInstance.destroy();

      const labels = sim.historyMetrics.times.length > 0 ? sim.historyMetrics.times : ["08:00 AM"];
      const happyData = sim.historyMetrics.avgHappiness.length > 0 ? sim.historyMetrics.avgHappiness : [85];
      const healthData = sim.historyMetrics.avgHealth.length > 0 ? sim.historyMetrics.avgHealth : [95];

      happinessChartInstance = new Chart(happyCanvas, {
        type: 'line',
        data: {
          labels,
          datasets: [
            { label: 'Avg Happiness', data: happyData, borderColor: '#38bdf8', backgroundColor: 'rgba(56, 189, 248, 0.1)', fill: true, tension: 0.3 },
            { label: 'Avg Health', data: healthData, borderColor: '#10b981', backgroundColor: 'transparent', borderDash: [4, 4] }
          ]
        },
        options: { responsive: true, scales: { y: { min: 0, max: 100 } } }
      });

      const cafeData = sim.historyMetrics.cafeRevenue.length > 0 ? sim.historyMetrics.cafeRevenue : [240];
      const pubData = sim.historyMetrics.pubRevenue.length > 0 ? sim.historyMetrics.pubRevenue : [380];

      economyChartInstance = new Chart(econCanvas, {
        type: 'line',
        data: {
          labels,
          datasets: [
            { label: 'Hobbs Cafe', data: cafeData, borderColor: '#f59e0b', tension: 0.3 },
            { label: 'Rose & Crown Pub', data: pubData, borderColor: '#a855f7', tension: 0.3 }
          ]
        },
        options: { responsive: true }
      });
    }
  </script>
</body>
</html>
"""

# Write to template file
with open(TEMPLATE_PATH, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Successfully generated God Simulator template at {TEMPLATE_PATH} ({len(HTML_CONTENT)} bytes)")
