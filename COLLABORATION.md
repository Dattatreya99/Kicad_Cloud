# KiCad Collaboration Guide - Cansat Project

This guide explains how to use Git to keep our project synchronized and avoid losing work.

## 🚀 Daily Workflow

Always follow the **"Pull-Work-Push"** routine to stay in sync.

### 1. Before you start (Sync Down)
Before opening KiCad, always get the latest changes from your partner.
```bash
git pull
```

### 2. Doing the work
*   **Schematic:** You can both work on the schematic, but try to work on different sheets/sections if possible.
*   **PCB Layout:** **Only one person should have the PCB Editor open at a time.** Coordinate via chat before starting layout work.

### 3. Saving your work (Sync Up)
When you finish a task, save all files in KiCad, then run:
```bash
git add .
git commit -m "Briefly describe what you changed"
git push
```

---

## 🛠 Best Practices

### 🛑 Avoid Conflict
*   **Communicate:** Send a quick message like *"I'm working on the PCB now"* to avoid simultaneous edits to the same file.
*   **Small Commits:** Push your changes frequently (e.g., after finishing one sub-circuit) rather than waiting until the end of the day.

### 📁 File Management
*   **Do NOT rename files:** KiCad relies on specific filenames to link the Schematic to the PCB.
*   **Gitignore:** The `.gitignore` file is already set up to hide temporary/backup files. Don't worry about the `*-bak` files; they won't be uploaded.

### 💥 If you get a "Merge Conflict"
If you both edited the same file and Git complains, **don't panic**.
1. Stop what you are doing.
2. If you are unsure how to fix it, contact your partner.
3. Usually, you can use KiCad's **Visual Diff** tools (if using KiCad 9) or a tool like [CadLab.io](https://cadlab.io) to see the differences.

---

## 🔗 Repository
Main Branch: `main`
URL: [https://github.com/Dattatreya99/Kicad_Cloud](https://github.com/Dattatreya99/Kicad_Cloud)
