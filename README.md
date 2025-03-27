# Elevator_SMT_Verification

**SMT-based Formal Verification for Elevator Scheduling Logic**

This project provides a formal verification framework for elevator scheduling control logic implemented on Siemens S7-200 PLCs. It uses SMT (Satisfiability Modulo Theories) techniques and the Cyclone tool to verify key safety and efficiency properties of elevator systems.

---

## 🚀 Features

- ✅ Finite-state modeling of elevator control logic (landing calls, car calls, direction switching)
- ✅ Automated state machine generation for N-story buildings
- ✅ SMT formula generation using Cyclone
- ✅ Verification of temporal properties using Z3 solver
- ✅ Support for stress tests up to 50-story buildings
- 🧾 Visual documentation of formal transition logic available via ProcessOn

---

## 🧠 Core Concepts

The system models elevator scheduling as a finite-state machine and verifies properties such as:

- **Request eventually served**: Every request is eventually satisfied.
- **Valid direction change**: The elevator only changes direction when necessary.
- **Idle behavior**: The elevator only idles when no requests are pending.

These are encoded in Linear Temporal Logic (LTL) and translated to SMT formulas for automated verification.

---

## 📁 Project Structure

```
.
├── docs/                   # Documentation and formulas
│   └── Elevator Formula/   # (optional, moved online—see link below)
├── examples/               # Predefined FSM and SMT models
├── test/                   # Test cases for scenarios
├── auto_fsm_generator.py   # Auto-generates FSM models
├── requirements.txt        # Python dependencies
├── LICENSE                 # Open-source license
└── README.md               # Project overview
```

---

## 📄 Documentation

The complete set of **formal SMT transition formulas** used in this project is available online:

👉 [Elevator Transition Formula (ProcessOn Diagram)](https://www.processon.com/view/link/67c86fc0112574557d1fe993)

This includes visual state transitions, condition expressions, and logic definitions aligned with the Siemens S7-200 PLC model.

---

## 🔧 Requirements

- Python 3.8+
- Z3 SMT Solver
- Cyclone (graph-based SMT encoding tool)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Quick Start

1. Clone the repo:

```bash
git clone https://github.com/yourname/Elevator_SMT_Verification.git
cd Elevator_SMT_Verification
```

2. Generate an FSM for a 10-level building:

```bash
python auto_fsm_generator.py --levels 10 --output examples/fsm_10levels.smt2
```

3. Run SMT verification (requires Z3):

```bash
z3 examples/fsm_10levels.smt2
```

---

## 📚 Citation

If you use this project in your research, please cite:

> Huan Zhang, Li Yi, Long Cheng, Hao Wu. "Formal Verification of Elevator Logic for Safety and Efficiency." 2025.

---

## 📜 License

MIT License © 2025 Huan Zhang, Li Yi, Long Cheng, Hao Wu

