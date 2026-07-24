# 🦫 Invasive Alien Species Impact — Isla Navarino, Chile

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://invasive-alien-species-impact.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: Academic](https://img.shields.io/badge/License-Academic-blue.svg)]()
[![Field](https://img.shields.io/badge/Field_Research-Puerto_Williams_2025-1B3A1E)]()

🌐 **Languages:** English | [Português](README.pt-BR.md) | [Español](README.es.md)

**Field Observation — Puerto Williams, Isla Navarino, Chile**
Residency: March–October 2025 (8 months)
**Observer:** Amauri Almeida de Souza Junior · Environmental Management Technologist

---

## ❓ Research Question

> "How did the 1946 introduction of 20 Canadian beavers irreversibly transform the subantarctic ecosystem of Isla Navarino, and what are the field-visible signs of that impact observable during 2025 treks around Puerto Williams?"

**Answer:** The largest ecological disturbance to subantarctic forests since the last ice age — set in motion by a single human decision. Twenty beavers released for a failed fur industry became a population exceeding 110,000, reshaping tens of thousands of hectares of forest with no natural predators to check their spread.

---

## 📊 Data Summary

| Indicator | Value |
|---|---|
| Estimated beaver population (2025) | 110,000+ |
| Dams mapped (satellite survey) | 70,600 |
| Forest area destroyed | ~31,000 hectares |
| Area colonized | 69,900 km² |
| Estimated annual economic cost | US$ 66 million/year (Argentina) |
| Original introduction | 1946 · 20 Canadian beavers |

---

## 🗺️ The Problem in 3 Phases

```
1946   →  20 Canadian beavers released in Tierra del Fuego
          Goal: fur industry (failed — pelts fetched only US$10–20)

1960s  →  Beavers cross into Chile · No natural predators
          South American trees with no evolutionary defenses against them

2025   →  110,000+ beavers · 70,600 dams · 31,000 ha destroyed
          "The largest subantarctic landscape alteration since the last ice age"
```

---

## 🔵 Key Findings

- **A single 1946 decision reshaped an entire ecosystem** — beavers introduced for a fur trade that never materialized found no natural predators and no evolved plant defenses, enabling unchecked population growth.
- **70,600 dams mapped via satellite** — a 2019 satellite study identified this dam count on the Argentine side alone, illustrating the scale of hydrological disruption across the region.
- **~31,000 hectares of forest destroyed** — dam-driven flooding and felling have altered forest cover at a landscape scale, described in the literature as the largest subantarctic ecological disturbance since the last glacial period.
- **US$66 million/year in estimated economic cost (Argentina)** — beyond ecological damage, the invasion carries a quantifiable economic burden.
- **Field-visible evidence at two beaver dam sites near Puerto Williams** — direct observation at "Castoreira 1" (near the town center) and "Castoreira 2" (near Laguna Rosa) during 8 months of residency.

---

## 🔬 Observation Pipeline

```
Field        →  8 months of residency in Puerto Williams (Mar–Oct 2025)
                Treks and visits to Beaver Dam Sites 1 and 2
                Site 1: near Puerto Williams town center
                Site 2: near Laguna Rosa

Science      →  3rd International CHIC Conference 2025 (attended as guest)
                Discussions with Guilherme (Belgium) and Nicolas (France),
                researchers presenting on beaver invasion dynamics

Data sources →  National Geographic (2019) · GEF Castor · University of
                North Texas (2016) · 2019 satellite study: 70,600 dams
                mapped on the Argentine side · Journal of Biogeography
                (2009): invasion cascade analysis
```

---

## 🗺️ Maps

The dashboard includes two complementary maps:

1. **Top map — True Color (ESRI satellite)** — real satellite visualization of Isla Navarino with markers at the field-visited sites.
2. **Bottom map — Heat map** — distribution of estimated beaver impact intensity based on the scientific literature.

---

## 🖥️ Dashboard Overview

The Streamlit app is organized into five tabs:

1. **🗺️ Map & Analysis** — the true-color satellite map and impact heat map described above.
2. **🔬 Methodology & Pipeline** — the field/science/data pipeline above, and background on the invasion timeline.
3. **💡 What We Found** — the key findings above, plus the overall conclusion.
4. **📷 In the Field** — first-hand photos from both beaver dam sites and the CHIC 2025 conference.
5. **📚 Sources & Credits** — full source list and author credentials.

The full interface — labels, chart titles, and narrative text — is natively trilingual (PT/EN/ES), switchable from the sidebar.

---

## 🛠️ Tech Stack

| Technology | Use |
|---|---|
| Python 3.11 | Core language |
| Streamlit | Dashboard framework |
| Folium + streamlit-folium | Satellite true-color mapping and impact heat map |
| Plotly (Express & Graph Objects) | Data visualization |
| Pandas / NumPy | Data processing |

---

## 📁 Repository Structure

```
invasive-alien-species-impact/
├── app.py                    # Main dashboard (5 tabs, PT/EN/ES)
├── requirements.txt          # Python dependencies
├── README.md                   # This file (English)
├── README.pt-BR.md             # Portuguese version
├── README.es.md                # Spanish version
└── assets/
    └── campo/                 # Field photos
        ├── 01_castoreira_pw_centro.jpg
        ├── 02_selfie_castoreira1_marco2025.jpg   ← featured (full width)
        ├── 03_castoreira2_laguna_rosa.jpg
        ├── 04_castoreira2_laguna_rosa_v2.jpg
        ├── 05_selfie_castoreira2_laguna_rosa.jpg
        ├── 06_conferencia_chic_pw.jpg
        ├── 07_guilherme_nicolas_apresentacao.jpg
        └── 08_brinde_participantes_chic.jpg
```

💡 Missing photos automatically render as labeled placeholders. Drop files into `assets/campo/` using the exact filenames and the app detects them on next run.

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/amaurialmeida/invasive-alien-species-impact.git
cd invasive-alien-species-impact

# Install dependencies
pip install -r requirements.txt

# Create the field-photos folder structure
mkdir -p assets/campo

# Run
streamlit run app.py
```

---

## 🌐 Live App

🔗 **[invasive-alien-species-impact.streamlit.app](https://invasive-alien-species-impact.streamlit.app/)**

Available in 🇧🇷 Portuguese, 🇺🇸 English, and 🇪🇸 Spanish.

---

## 📚 References

- National Geographic Brasil — Haley Cohen Gilliland; photos by Luján Agusti (2019).
- GEF Castor — Global Environment Facility (gefcastor.mma.gob.cl).
- Crego, R.D.; Jiménez, J.E.; Rozzi, R. (2016) — *Biological Invasions*. University of North Texas.
- *Journal of Biogeography* (2009) — invasion cascade analysis; source of the "largest subantarctic landscape alteration since the last ice age" characterization.
- 3rd International CHIC Conference — Puerto Williams (2025).
- Personal field observation — Amauri Almeida de Souza Junior, Puerto Williams, Mar–Oct 2025.

---

## 🔗 Academic / Professional Links

| Platform | Link |
|---|---|
| Lattes | http://lattes.cnpq.br/9545242042800090 |
| Escavador | https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior |

---

## 🌿 Environmental Portfolio

This project is part of the author's environmental research and data science portfolio.
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio)

---

© 2025–2026 · Amauri Almeida de Souza Junior · Invasive Species Research · Isla Navarino, Puerto Williams, Chile
