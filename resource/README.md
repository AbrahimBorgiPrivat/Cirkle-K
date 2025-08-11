# Files Directory

This directory contains external data files used in the project.

---

## Structure Overview

<details>
<summary><strong>/json/</strong> - Auto-Generated Data</summary>

- Collection of JSON files related to geographical and address information.
- Examples:
  - `DAGI_Kommuneinddeling_1.json`
  - `DAR_Adresse_1.json`
  - etc.

**Note:** These files are **ignored by Git** to keep the repository clean and lightweight.

</details>

---

## How to Populate `/json`

Run the following command to download and enrich the `/json` files:

```bash
python source/code/scripts/pipelines/datafordeler_main.py