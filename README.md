# Remote Healthcare Survey — ETL Pipeline and Statistical Analysis

An end-to-end pipeline for a national survey (n=384 valid responses) on how comfortable people are with remote healthcare technologies collecting their data. Python handles multi-source ETL and feature engineering. R handles the statistical analysis. Open-text responses feed a parallel qualitative analysis, making this a mixed-methods project from a single data collection.

## At a glance

- Multi-source ETL (Python/pandas): ingestion, validation, cleaning, and integration across two online panels and four paper survey instruments, collected in two rounds
- Rule-based data validation with an auditable exclusion log (completion time, duplicate detection, attention and plausibility checks)
- Feature engineering: converting text survey responses to numeric scales and deriving age cohorts
- Randomized four-condition design: every scenario comparison is between randomized groups
- Statistical analysis (R): group comparisons with corrections for multiple testing, reporting effect sizes alongside significance

**Note on data:** this repository contains code only. Raw exports include personally identifiable information (IP addresses, geolocation, panel IDs) and are excluded to protect participant privacy, consistent with the study's research ethics board approval. `raw/` and `python/output/` hold these files locally.

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

- GOAL: Export the transformed dataset to files that will be further analyzed with R
- `opentext.py` exports open-text responses by age cohort for qualitative coding, from a pre-encoding copy so free text is never corrupted by the numeric conversion
- `DataShareAnalysis.R` and `sa6priv.R` read hand-prepared inputs directly; bringing them into the pipeline is roadmap item 2

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
