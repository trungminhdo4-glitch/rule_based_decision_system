# Rule-Based Adaptive Decision System

Ein modulares, erklärbares und adaptives regelbasiertes Entscheidungssystem in Python.

Dieses Projekt dient als Lern- und Demonstrationsprojekt für:
- saubere Software-Architektur
- regelbasierte Entscheidungslogik
- Explainable AI (nachvollziehbare Entscheidungen)
- adaptive Systeme (Gewichte, Parameter, Thresholds)

---

## 🚀 Features

- ✅ **Rule-based Decision Engine**
  - Jede Regel bewertet Eingabedaten unabhängig
  - Scores werden gewichtet und aggregiert

- 🧠 **Explainability**
  - Jede Entscheidung ist vollständig erklärbar
  - Gründe, Scores und Gewichte werden gespeichert

- 🔁 **Adaptive Mechanismen**
  - Dynamische Anpassung der Regelgewichte
  - Anpassung von Regelparametern (z. B. Risikoschwellen)
  - Adaptive Decision Thresholds (ACCEPT / HOLD / REJECT)

- 📊 **Historien- & Performance-Tracking**
  - Speicherung vergangener Entscheidungen
  - Statistische Auswertung (Mean, Min, Max)
  - Visualisierung der Entscheidungsverläufe

---

## 🗂 Projektstruktur

```text
rule_based_decision_system/
│
├── core/
│   ├── rules/                 # Einzelne Entscheidungsregeln
│   │   ├── base_rule.py
│   │   ├── value_rule.py
│   │   ├── risk_rule.py
│   │   └── volatility_rule.py
│   │
│   ├── rule_engine.py          # Führt Regeln aus
│   ├── decision.py             # Entscheidungslogik
│   └── system_setup.py         # Initialisierung des Systems
│
├── evaluation/
│   ├── adaptive.py             # Adaptive Engine
│   ├── explanation.py          # Explainability
│   ├── history.py              # Historische Speicherung
│   ├── scorer.py               # Score-Aggregation
│   └── visualization.py        # Plots & Visuals
│
├── data/
│   └── input_data.py           # Beispieldaten
│
├── main.py                     # Orchestrator (Entry Point)
├── requirements.txt
└── README.md
```

---

## 🛠 Setup & Ausführung

```bash
git clone https://github.com/trungminhdo4-glitch/rule_based_decision_system.git
cd rule_based_decision_system

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt

# Demo ausführen (erzeugt Matplotlib-Fenster am Ende)
python main.py

# Tests ausführen
python -m pytest
```

Benötigt Python 3.12 (getestet mit 3.12.6).

Hinweis für Windows-Konsolen mit Legacy-Codepage (cp1252): die Demo-Ausgabe
enthält Unicode-Zeichen (z. B. „≥"). Mit `PYTHONUTF8=1` (oder Windows-Terminal)
läuft `python main.py` vollständig durch.
