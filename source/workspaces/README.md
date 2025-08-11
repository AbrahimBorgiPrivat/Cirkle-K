# Rapports

This repository contains the Power BI solution for **Bekey**, designed to deliver insights into key operational metrics such as installations, user activity, and distributions. The dashboards combine detailed semantic modeling with interactive visual reports for end-user exploration.

---

## Project Structure

### `figures/`
This folder contains various assets and icons used within the reports and dashboard design, such as:
- User and installation illustrations (`users.png`, `installed.png`)
- Financial and pricing references (`realiseret.png`, `gns pris.png`)
- Visual aids for technician activities (`MontørMonteringer.png`, `Montørjobs.png`)
- Icons for UI/UX elements (`close-the-door-icon.png`, `users.png`, etc.)

### `finans/`
This is the core of the Power BI model.

- **Finans - Bekey - Rapport**  
  Contains the `Report file` for the main rapport.
  - `.Report`: The report model for the first rapport currently ready for deployment
  - `.SemanticModel`: Dummy semantic model not containing data since the connection is dirsctly to the other semantic model 
  - `.pbip`: Combined project file for this model

  For extended documentation, visit the [BeKey Finance - Visuals](https://northmedia.atlassian.net/wiki/spaces/DRT/pages/35455234/Rapport+Model).

- **Finans - Bekey - SemanticModel**  
  Contains the `Semantic model` for the main rapport.
  - `.Report`: Dummy .Report file cause the file is mandatory in the pbib file structure
  - `.SemanticModel`: The semantic model
  - `.pbip`: Combined project file for this model

  For extended documentation, visit the [BeKey Finance - Semantisk Model](https://northmedia.atlassian.net/wiki/spaces/DRT/pages/14057495/Semantisk+Model).

### `Img | Pages/`
This folder includes page-level visual assets used in reports:
- `Background.png` – Report image for background

### `Tema-BeKey.json`
Custom Power BI theme file that ensures consistent branding, font styles, and color schemes across all visuals and pages.

---

## Getting Started

1. Open the `.pbip` file (`Finans - Bekey.pbip`) in Power BI Desktop.
3. Customize visualizations or extend the model as needed.

---

## Requirements

- Power BI Desktop (version supporting `.pbip` project format)
- Access to relevant Bekey data sources 

---

## Contact

For questions or contributions, please reach out to the NM Datateam.