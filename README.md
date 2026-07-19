# Fernando Silva da Luz — Portfolio

An interactive, game-themed portfolio and résumé site for **Fernando Silva da Luz** — Game Developer (Montréal, QC).
Trilingual (English / Français / Português-BR), single self-contained page, no build step.

## What's inside

```
website/
├── index.html                 # the whole site (HTML + CSS + JS inline)
├── assets/
│   └── resumes/               # 9 PDF résumés (3 roles × 3 languages)
│       ├── Fernando_Silva_da_Luz_GameDev_EN.pdf
│       ├── ..._UnityDev_FR.pdf
│       └── ..._SoftwareDev_PT-BR.pdf
├── .nojekyll                  # lets GitHub Pages serve files/folders as-is
└── README.md
```

Everything is vanilla — no frameworks, no bundler. Fonts load from Google Fonts; the page still works offline with system fallbacks.

## Run locally

Just open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8080
# then visit http://localhost:8080
```

## Deploy (pick one)

**GitHub Pages**
1. Create a repo (e.g. `portfolio` or `FernandoSLuz.github.io`) and push these files to the root.
2. Repo → Settings → Pages → Source: `main` branch, `/root`.
3. Live at `https://FernandoSLuz.github.io/portfolio/` (or the root domain for a `*.github.io` repo).

**Netlify / Vercel / Cloudflare Pages** — drag-and-drop this folder, or point the project at the repo. No build command; publish directory is the folder itself.

## Editing

- **Text & translations** live in the `T` object near the bottom of `index.html` (`en` / `fr` / `ptbr`).
- **Projects, experience, skills, awards** are the `PROJECTS`, `EXP`, `BARS`, `AWARDS` arrays just above `T` — each item carries its three languages inline.
- **Résumé downloads** map to files in `assets/resumes/` by role key + language code, so keep those filenames if you regenerate the PDFs.

## Notes
- The résumés list `fernandosluz.github.io` as the portfolio URL. Once you pick your final domain, update that link in the résumé source (and in the site's contact section if needed).
- Try the Konami code on the site: ↑ ↑ ↓ ↓ ← → ← → B A 🎮
