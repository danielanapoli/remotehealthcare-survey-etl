# Remote Healthcare Survey — ETL Pipeline and Statistical Analysis

An end-to-end pipeline for a national survey (n=386 valid responses) on how comfortable people are with remote healthcare technologies collecting their data. Python handles multi-source ETL and feature engineering. R handles the statistical analysis. Open-text responses feed a parallel qualitative analysis, making this a mixed-methods project from a single data collection.

## At a glance

- Multi-source ETL (Python/pandas): ingestion, validation, cleaning, and integration across two online panels and four paper survey instruments, collected in two rounds
- Rule-based data validation with an auditable exclusion log (completion time, duplicate detection, attention and plausibility checks)
- Feature engineering: converting text survey responses to numeric scales and deriving age cohorts
- Randomized four-condition design: every scenario comparison is between randomized groups
- Statistical analysis (R): group comparisons with corrections for multiple testing, reporting effect sizes alongside significance

**Note on data:** this repository contains code only. Raw exports include personally identifiable information (IP addresses, geolocation, panel IDs) and are excluded to protect participant privacy, consistent with the study's research ethics board approval. `raw/` and `python/output/` hold these files locally.

## The research question

Remote healthcare technologies collect data ranging from vital signs to identifiable video of a patient at home. The study asked: how comfortable are people with each of five data types (identifiable video, anonymized video, audio, wellness data, vital signs), who are they willing to share that data with, and how do comfort and sharing vary by age, scenario, and prior experience with remote care?

Each participant was assigned to one of four scenario conditions (chronic condition management, at-home emergency, post-operation rehabilitation, symptom screening). Respondents were randomized to condition by the survey instrument.

## Data sources

| Source | Format | Notes |
|---|---|---|
| Prolific panel | Qualtrics CSV export | Online, direct compensated |
| Other online recruitment | Qualtrics CSV export | Online, raffle compensation |
| Paper surveys | Manually entered CSV, one file per condition | Paper, raffle compensation |

The paper channel supported realistic sampling of adults 65+. Online recruitment only would bias the sample toward the most tech-comfortable older adults.

## Pipeline architecture (Python)

```
raw CSVs (online + paper, per round)
        │
        ▼
flag.py ──────► flagList.csv          Stage 1: data validation
        │
        ▼
run.py + clean.py + clean_methods.py   Stage 2-3: extract, clean, transform
        │
        ▼
data_cleaned_raw.csv / .xlsx           Stage 4: load (handoff to R)
        │
        └──► opentext.py  ──► open-text exports by age cohort (qualitative coding)
```

**Stage 1 — Data validation (`flag.py`)**

- GOAL: Flag low-quality responses on four rules: completion under 240 seconds, duplicate timestamps, refused or implausibly short open-text answers, out-of-range birth years
- Restores manually reviewed exceptions through an explicit allowlist, so every inclusion decision is auditable in code
- Outputs `flagList.csv`, the exclusion filter for the cleaning stage
- Currently screens one hardcoded export rather than every raw file; generalizing this is on the roadmap

**Stage 2 — Ingestion and integration (`run.py`, `clean.py`)**

- GOAL: Discover all source files and route each to a per-source handler, since online and paper data need different treatment
- Detects which of the four randomized survey versions each participant received, and aligns all versions into a single schema
- Tags each row with its condition and combines everything into one dataset

**Stage 3 — Transformation and feature engineering (`clean_methods.py`)**

- GOAL: Transform raw data into variables to improve analysis and visualizations
- Rename ~50 machine-generated survey codes to readable names (`EXP3_2` → `BeforeCov_Telephone`)
- Ordinal encoding: converts Likert text responses to numeric scales, with regex handling for formatting inconsistencies between online and paper instruments
- Engineers age features: `Age` derived from birth year, then binned into four age cohorts plus a binary over/under-50 split for higher-powered comparisons
- Includes a written but currently disabled normalization step for free-text race/ethnicity entries (both call sites commented out)

**Stage 4 — Load**

- GOAL: Exports the transformed dataset to files that will be further analyzed with R
- `opentext.py` exports open-text responses by age cohort for qualitative coding, from a pre-encoding copy so free text is never corrupted by the numeric conversion
- `DataShareAnalysis.R` and `sa6priv.R` read hand-prepared inputs directly; bringing them into the pipeline is roadmap item 2

## Statistical analysis (R)

Scripts: `SurveyAnalysis.R`, `ConcernsAnalysis.R`, `DataShareAnalysis.R`, `sa6priv.R`, using `DescTools`, `coin`, and the tidyverse.

Likert responses are ordinal, so the analysis uses Kruskal-Wallis tests (a nonparametric method for comparing groups when responses are ratings rather than true numbers) for overall comparisons across age cohorts and conditions. Significant results get pairwise Wilcoxon follow-up tests with Bonferroni correction, which adjusts the significance threshold to account for running many comparisons. Every significant result also gets an effect size (r = z/√n), because at n=386 a p-value alone can flag differences too small to matter. Several results are explicitly set aside on exactly that basis: statistically significant, but too small to matter in practice.

An example finding, as reported in `SurveyAnalysis.R`:

> A Kruskal-Wallis test revealed a significant effect of age group on likelihood to use remote healthcare technology (χ²(3)=16.46, p < 0.01). Post-hoc Wilcoxon tests with Bonferroni correction showed differences between the 65+ and 35-49 groups (p < 0.01) and the 65+ and 50-64 groups (p = 0.01). Mean likelihood for the 65+ group (M = 3.34) was lower than for the 35-49 (M = 4.13) and 50-64 (M = 3.94) groups.

## Design considerations

- **Validate before cleaning.** Data quality decisions live in their own stage with an auditable output file, not buried inside cleaning logic.
- **Nonparametric tests throughout.** Ordinal data gets ordinal-appropriate methods, at the cost of some statistical power, rather than treating rating points as true numbers.
- **Effect sizes alongside p-values.** Several significant results are reported as too small to matter in practice, for honest reading.
- **One collection, two analysis tracks.** Cleaned data split into a quantitative track (R) and a qualitative track (manual coding in NVivo).

## Repository structure

```
├── raw/                     # Raw survey exports (online/, paper/) — empty in this copy
├── python/
│   ├── run.py               # pipeline entry point
│   ├── clean.py             # per-source cleanup routines
│   ├── clean_methods.py     # transformation and feature engineering
│   ├── flag.py              # data validation
│   ├── scenarios.py         # scenario definitions
│   ├── opentext.py          # open-text exports for qualitative coding
│   ├── raffledraw.py        # standalone raffle-winner draw utility
│   └── output/              # destination for generated CSV/XLSX files
├── r/
│   ├── SurveyAnalysis.R     # demographics, comfort, likelihood analyses
│   ├── ConcernsAnalysis.R   # concern counts by data type and age
│   ├── DataShareAnalysis.R  # sharing recipients by data type, age, scenario
│   └── sa6priv.R            # SA-6/privacy scale analysis by prior experience
└── viz/                     # visualizations + generating scripts
```

## Running the pipeline

1. Place raw Qualtrics/paper exports in `raw/online/` and `raw/paper/`.
2. Run `python/flag.py` to generate `flagList.csv` (excluded low-quality responses).
3. Run `python/run.py` to clean and combine all raw files into `data_cleaned_raw.csv`/`.xlsx`.
4. Run the `r/` scripts against the cleaned data for statistical tests.
5. Run the `viz/` scripts to produce charts from the cleaned/analyzed data.
6. Use `python/opentext.py` to export open-text responses for qualitative coding.