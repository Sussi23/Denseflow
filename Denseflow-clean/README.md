# DenseFlow – Cleaned Repository

Money-laundering detection on Ethereum using the **DenseFlow** model (HoloScope + Maximum-Flow).

---

## Repository structure

```
Denseflow-clean/
├── Code/
│   ├── info.py          – Case configuration (case names, source addresses)
│   ├── holodatatran.py  – Data transformation for HoloScope
│   ├── myHoloscope.py   – HoloScope dense-subgraph model
│   ├── myMaxflow.py     – Maximum-flow expansion
│   ├── Datatran_1.py    – Address-index mapping utilities
│   └── Check.py         – Evaluation metrics (Precision, MCR, |M|)
├── inputData/
│   └── AML/
│       ├── AlphaHomora/
│       │   ├── all-normal-tx.csv       ← raw transactions
│       │   ├── all-normal-address.csv  ← all addresses
│       │   └── accounts-hacker.csv     ← ground-truth labels
│       ├── CryptopiaHacker/  (same structure)
│       └── PlusTokenPonzi/   (same structure)
├── spartan2-master/     – Dependency library (HoloScope, Fraudar, CubeFlow, etc.)
├── pipeline.ipynb       – Full pipeline demonstration notebook
└── README.md
```

---

## Pipeline

```
all-normal-tx.csv
     │
     ▼
1. Preprocessing       (address↔index maps, HoloScope tensor CSV)
     │
     ▼
2. HoloScope           (dense suspicious sub-graphs → candidate accounts)
     │
     ▼
3. Max-flow expansion  (trace money flow → suspicious set M)
     │
     ▼
4. Evaluation          Precision · MCR · |M|
```

Open **`pipeline.ipynb`** to run the full pipeline end-to-end.

---

## Metrics

| Metric | Description |
|--------|-------------|
| **Precision** | Fraction of detected accounts that are true heist accounts |
| **MCR** | Money-coverage rate: fraction of illicit transaction value traced |
| **\|M\|** | Size of the detected suspicious account set |

---

## Dependencies

- Python ≥ 3.8
- `ortools`, `pandas`, `numpy`, `treelib`
- `spartan2` (bundled in `spartan2-master/`)

```bash
pip install ortools pandas numpy treelib
```
