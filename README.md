# Olivier Gossner's Quarto website

A first working template for gossner.me, prepared on 17 September 2026. It contains 48 research records: the original 29 entries, three recent arXiv preprints, 13 additional journal articles, one chapter, one editorial and one archived working paper. It also includes teaching notes, the workshop archive, selected media and the linked CV. The design is editable and the collection still needs the content review described in `migration/CONTENT-REVIEW.md`.

This standalone Quarto website is published by GitHub Pages from https://github.com/OliGoss/OliGoss.github.io. On 18 September 2026, gossner.me was connected to GitHub and the production profile was deployed. HTTP serving and domain checks pass; HTTPS certificate issuance is still pending. GitHub Actions builds and publishes updates to the main branch.

## Everyday editing in your browser

You can do small edits without FTP, a terminal, or installing Quarto.

| What you want to change | File to open |
|---|---|
| Affiliations, research areas, contact | `index.qmd` |
| One paper's title, authors, abstract, PDF or publication status | Its `.qmd` file in `papers/` |
| Teaching notes and links | `teaching-material/index.qmd` |
| Workshop programmes | `ttw/index.qmd` |
| Media contributions | `press/index.qmd` |
| SInfoNiA introduction | `sinfonia/index.qmd` |
| CV download | Replace `cv.pdf`, then update its displayed date in `cv/index.qmd` |

Open a file, click the pencil icon, change the text, and choose **Commit changes** to save. A successful build publishes the change. A failed check prevents the new version from replacing the working website.

The `.qmd` files contain ordinary text with light formatting. `##` starts a section; `[link text](address)` creates a link. The short block between `---` lines at the top contains the page's title and other settings. You can edit content locally in Quarto's supported visual editors too, but no local software is required for browser edits.

## Two common editing tasks

1. **Change the research description.** Open `index.qmd`, edit the paragraph under “Research”, and save. Check the resulting homepage.
2. **Add a paper.** Upload the PDF to `assets/papers/` using **Add file → Upload files**. Copy `_templates/new-paper.qmd` into a new file under `papers/`, for example `papers/my-new-paper.qmd`. Replace its title, authors, year, publication line, PDF address and abstract. Save. The research page includes it automatically.

Use ordinary hyphenated PDF filenames, such as `strategic-type-spaces.pdf`. GitHub's browser uploads support files up to 25 MiB; all the copied PDFs are below this size.

Use `status: "chapter"` for chapters, `"editorial"` for editorial work, or `"archived"` for earlier working papers. Each appears in its own research section.

For a draft paper set `status: "working"`; for a published paper use `status: "published"`. Update `publication` and the `citation` block together when the journal, year, volume, pages or DOI changes. The `author` list supplies machine-readable authors and the paper page; `byline` controls the sentence shown in the research list.

For papers hosted on arXiv, `pdf` may be an arXiv PDF URL and `arxiv-url` the abstract-page URL. These PDF links follow the latest version on arXiv, avoiding a second copy to maintain. Titles and abstracts in this site remain editable snapshots.

The research index reads the paper files automatically; there is no second list to edit.

The initial paper files retain the website's abstract text, including the explicitly labelled older working-paper abstract for the insurance-accounting paper. The regression paper now has its correct abstract, checked against the archived author manuscript. The bibliography additions and citation corrections were checked on 18 September 2026; provenance is recorded in `migration/bibliography-additions-2026-09-18.json`.

## GitHub setup — completed 18 September 2026

1. Use your own GitHub account so you retain ownership.
2. Create a public repository named **OliGoss.github.io**. Public source is required for GitHub Pages on the free plan. Only this website folder belongs there: do not upload private documents, billing information, passwords, or the surrounding workspace.
3. Add the contents of this folder, including `.github/workflows/publish.yml` and `.nojekyll`. The initial bulk upload and hidden files are easiest for me or another helper to handle; the browser workflow above is for subsequent everyday edits. Do not upload `_site` or `.quarto`.
4. In repository **Settings → Pages**, choose **GitHub Actions** as the publishing source.
5. In **Settings → Secrets and variables → Actions → Variables**, set `SITE_PROFILE` to `preview` (this is also the default).
6. Run **Build and publish website** from the Actions tab. The result should appear at `https://OliGoss.github.io/`. Review it there before setting any custom domain.

The initial preview requests search engines not to index it. This is not privacy protection: the preview and the repository are public. The workflow deliberately expects a root website, rather than a `/repository-name/` subdirectory, so existing document addresses remain valid.

The repository variable `SITE_PROFILE` is now `production`; keep that value for the live website. See `migration/TRANSITION.md` for launch status and rollback instructions. Subsequent saves to the `main` branch publish automatically. To require approval of updates, use a branch and a pull request; the workflow builds and checks pull requests without deploying them. It does not create hosted previews for individual pull requests.

## Local preview — optional

Install Quarto 1.10.18 and Python 3.11 or later if you want to work locally. No R, Jupyter, WordPress, or additional Python packages are required.

```sh
quarto preview --profile preview
```

To build and check all pages:

```sh
quarto render --profile preview
python3 scripts/check-site.py
```

Use `--profile production` only for the approved domain launch. The bundled workflow pins the Quarto version used to verify this template; updates should be tested before changing that pin.

## How old links are preserved

The copied PDFs remain at their original `wp-content/uploads/...` addresses. Keep that folder intact even though the site no longer runs WordPress. The CV also has the convenient new address `/cv.pdf`, while the historical January 2024 file remains available at its old address.

`migration/legacy-routes.json` maps old article pages to the new paper pages. The post-render script creates HTML redirect pages for those URLs. GitHub Pages cannot supply custom HTTP 301 rules: these are immediate browser redirects with a normal link fallback. Query-string publication IDs are handled by a small script. Old research pagination links lead to the unified research index.

`scripts/check-site.py` checks local links, anchors, legacy pages, archived-file hashes, and total site size before publishing. It does not check every external service or certify the accuracy of imported publication data.

## Files for the handover

- `migration/TRANSITION.md`: staged launch and rollback plan.
- `migration/CONTENT-REVIEW.md`: content to confirm before launch.
- `migration/asset-manifest.json`: copied public assets, original addresses and checksums.
- `migration/legacy-routes.json`: old-to-new page mapping.
- `migration/publication-import.json`: publication import inventory.

The source files are portable: they can be hosted elsewhere if GitHub Pages is no longer the preferred option.
