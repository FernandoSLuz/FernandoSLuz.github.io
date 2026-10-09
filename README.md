# Fernando Silva da Luz — Portfolio

Trilingual portfolio and résumé site for Fernando Silva da Luz, a senior software engineer based in Montréal. The portfolio covers C++/Qt medical software, Python applied AI and computer vision, developer tools, and Unity products.

## Structure

```text
index.html                    # HTML, CSS, JavaScript and translations
generate_resumes.py           # Source for the résumé PDFs
assets/resumes/               # 3 role variants × 3 languages
  Fernando_Silva_da_Luz_GameDev_EN.pdf
  Fernando_Silva_da_Luz_GameDev_FR.pdf
  Fernando_Silva_da_Luz_GameDev_PT-BR.pdf
  Fernando_Silva_da_Luz_UnityDev_EN.pdf
  Fernando_Silva_da_Luz_UnityDev_FR.pdf
  Fernando_Silva_da_Luz_UnityDev_PT-BR.pdf
  Fernando_Silva_da_Luz_SoftwareDev_EN.pdf
  Fernando_Silva_da_Luz_SoftwareDev_FR.pdf
  Fernando_Silva_da_Luz_SoftwareDev_PT-BR.pdf
.nojekyll                     # Serve the static files directly
README.md
```

The site uses vanilla HTML, CSS and JavaScript, with no build step. Fonts load from Google Fonts and fall back to system fonts.

## Run locally

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080`. The language selector switches between English, French and Brazilian Portuguese, including the page title and description.

## Edit content

- `T.en`, `T.fr` and `T.ptbr` in `index.html` contain the page text and metadata.
- `EXP`, `PROJECTS`, `BARS`, `STACK`, `XR` and `AWARDS` contain the experience, project and skills content. `BARS` lists work areas and supporting technologies; it does not assign numerical proficiency scores.
- `RESUMES` defines the three download cards. `RESUME_LANG` maps the UI languages to the existing PDF filenames.
- `generate_resumes.py` is the source for the nine PDFs. Keep its facts consistent with the site, regenerate the files when the source changes, and inspect the generated documents before publishing.

Keep the existing résumé filenames when replacing a current download so that shared links continue to work. The website and generated PDFs are separate files; updating one does not update the other.

## Content boundaries

- The 13+ years refer to overall software experience, not tenure in any single language or AI discipline.
- The completed degree is the B.Sc. in Computer Science from FMU, completed in June 2024. Do not describe the unfinished Game Design studies as a completed degree.
- VEKARRA is in development. Its Steam page is the primary project link; cooperative play is still in development.
- AI-Pulse's current architecture uses local GGUF inference through llama.cpp. Cloud-provider fallback belongs to its earlier 1.x architecture and needs that historical qualification if discussed.
- AgentFare is an alpha CLI for session-log cost analysis and rule-based routing recommendations. Its estimates do not demonstrate answer quality or realized cost savings.
- Describe registration scripts as evaluation work and segmentation as inference using models developed by others. Do not disclose internal product names or unreleased employer features.
- Add metrics, certifications or expertise claims only when they have supporting evidence.

## Publish

The existing site is served at `https://fernandosluz.github.io/` from the `main` branch of `FernandoSLuz/FernandoSLuz.github.io` using GitHub Pages. Its Pages build and deployment workflow is managed by GitHub rather than checked into this repository.

After an approved update reaches `main`, verify the Pages deployment result, the three language views, and all nine PDF URLs. The publishing process serves the committed PDFs; it does not execute `generate_resumes.py`.

## Interaction

The original visual layout, project cards, language selector and Konami-code interaction are retained.
