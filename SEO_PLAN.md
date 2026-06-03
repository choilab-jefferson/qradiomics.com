# SEO Strategy for qradiomics.com & qradiomics CLI

To improve the search ranking for "radiomics" and "qradiomics cli," we should focus on **E-E-A-T (Experience, Expertise, Authoritativeness, and Trustworthiness)** within the medical imaging and AI niche.

## 1. Content & Keyword Optimization (On-Page SEO)

### A. Targeted Keyword Integration
*   **Primary Keywords:** `Radiomics CLI`, `Open Source Radiomics`, `Reproducible Radiomics`, `Medical Image Analysis CLI`.
*   **Secondary Keywords:** `PyRadiomics wrapper`, `TCIA dataset processing`, `Lung cancer radiomics tools`, `Radiomics workflow automation`.
*   **Action:** Ensure these keywords appear in `<h1>`, `<h2>` tags, and the first paragraph of key pages (Home, Project, Intro post).

### B. Add Meta Descriptions to All Content
*   Currently, many posts lack explicit `description` fields in their front matter. Hugo PaperMod uses this for the `<meta name="description">` tag.
*   **Action:** Add a 150-160 character summary to each post's front matter.
    ```yaml
    description: "qradiomics is an open-source CLI tool for reproducible radiomics research, supporting PyRadiomics integration and TCIA dataset automation."
    ```

### C. Technical Documentation & Tutorials
*   Create a dedicated "Documentation" or "Get Started" page specifically for the CLI. Search engines love long-form technical content with code blocks (`pip install qradiomics`, etc.).
*   **Action:** Expand the `/projects/qradiomics/` page or create a `/docs/` section.

## 2. Technical SEO (Site Health)

### A. Structured Data (Schema.org)
*   Implement `SoftwareApplication` schema for the qradiomics CLI. This helps Google display "rich snippets" (stars, version, etc.) in search results.
*   **Action:** Add a JSON-LD script to the head of the CLI project page.

### B. Image Alt Text
*   Medical imaging sites have many plots/scans. Ensure every image in `images/` folders has descriptive `alt` text containing keywords (e.g., "Radiomics feature heat map for lung cancer").

## 3. Off-Page SEO & Authority Building

### A. GitHub & PyPI Optimization
*   The CLI's README on GitHub is a powerful SEO asset. Ensure the GitHub repo description contains "Radiomics CLI" and "Medical Imaging."
*   **Action:** Ensure `qradiomics` is published on PyPI with a rich description and link back to `qradiomics.com`.

### B. Backlink Strategy
*   **Academic Citations:** Link to the site from your Google Scholar, ResearchGate, and ORCID profiles.
*   **Community Engagement:** Mention the tool in radiomics-related forums (e.g., PyRadiomics GitHub Discussions, Discourse).
*   **TCIA/Datasets:** If the tool simplifies TCIA usage, try to get it listed on the TCIA "Tools" or "Resources" pages.

## 4. Local & Community SEO (Radiomics Specific)

*   **Radiomics Ontology:** Use standardized terms from the IBSI (Image Biomarker Standardisation Initiative).
*   **Interoperability:** Highlight integration with tools like 3D Slicer, ITK-SNAP, or OHIF.

---
*Drafted by Gemini CLI for qradiomics.com*
