# NGC Tuesday Night Men's League — Setup & Weekly Workflow

## First-Time Setup (do once)

### 1. Create the GitHub repository

1. Go to https://github.com and sign in
2. Click **New** (green button, top left)
3. Repository name: `mens-golf-league-2026` (or anything you like)
4. Set visibility to **Private** (only you can see it)
5. Click **Create repository**

---

### 2. Upload the files

On the new repo page, click **uploading an existing file** (or use Git if you know it).

Upload these files, maintaining this folder structure:

```
mens-golf-league-2026/
├── index.html
├── build.py
├── README.md
└── data/
    ├── Week_1_May_19_2026__3_.csv
    ├── Week_2_May_26_2026.csv
    ├── Week_3_June_2_2026.csv
    ├── Week_4_June_9_2026.csv
    └── league_data.json
```

> **Tip:** GitHub's web uploader lets you drag-and-drop multiple files at once.
> Create the `data/` folder by typing `data/` before the filename when prompted.

---

### 3. Enable GitHub Pages

1. In your repo, go to **Settings** → **Pages** (left sidebar)
2. Under "Source", select **Deploy from a branch**
3. Branch: **main** · Folder: **/ (root)**
4. Click **Save**

After ~60 seconds your site will be live at:
`https://YOUR-USERNAME.github.io/mens-golf-league-2026/`

---

## Weekly Workflow (every Tuesday after golf)

### Option A — Web upload (no coding needed)

1. Export the week's CSV from Squabbit
2. Go to your GitHub repo → `data/` folder
3. Click **Add file → Upload files**
4. Drag in the new CSV
5. In `build.py`, uncomment/add the new week entry in `WEEK_FILES`
6. Commit both files
7. The site updates automatically in ~30 seconds

### Option B — Command line (faster)

```bash
# Clone once (first time)
git clone https://github.com/YOUR-USERNAME/mens-golf-league-2026.git
cd mens-golf-league-2026

# Each week:
cp ~/Downloads/Week_5_June_16_2026.csv data/
# Edit build.py: uncomment/add the new week in WEEK_FILES
python build.py
git add data/ index.html build.py
git commit -m "Add Week 5"
git push
```

---

## Adding a New Week (build.py)

Open `build.py` and find the `WEEK_FILES` list. Add the new entry:

```python
WEEK_FILES = [
    ("Week_1_May_19_2026__3_.csv",  "Week 1", "May 19, 2026"),
    ("Week_2_May_26_2026.csv",       "Week 2", "May 26, 2026"),
    ("Week_3_June_2_2026.csv",       "Week 3", "June 2, 2026"),
    ("Week_4_June_9_2026.csv",       "Week 4", "June 9, 2026"),
    ("Week_5_June_16_2026.csv",      "Week 5", "June 16, 2026"),  # ← add here
]
```

Then run `python build.py` and commit.

---

## Sharing the Site

The site is private by default (unlisted — only accessible with the exact URL).
To share with the league, just send them the GitHub Pages URL:
`https://YOUR-USERNAME.github.io/mens-golf-league-2026/`

It works on phones too.
