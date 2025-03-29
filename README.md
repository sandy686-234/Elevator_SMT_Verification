
# 🚦 Elevator_SMT_Verification

**SMT-based Formal Verification for Elevator Scheduling Logic**

This project provides a formal verification framework for elevator scheduling control logic implemented on Siemens S7-200 PLCs. It uses SMT (Satisfiability Modulo Theories) techniques and the Cyclone tool to verify key safety, liveness, and efficiency properties of elevator systems.

---

## 🚀 Features

- ✅ Finite-state modeling of elevator control logic (landing calls, car calls, direction switching)
- ✅ Automated FSM generation with configurable parameters for buildings with any number of levels
- ✅ SMT formula generation using Cyclone: translates FSM states, transitions, and properties into precise SMT-LIB2 constraints
- ✅ Formal verification powered by Z3: Cyclone-generated formulas are verified via bounded model checking using the Z3 SMT solver (v4.13.0)
- ✅ Performance-optimized verification: includes benchmark results demonstrating scalability to 50-level buildings
- 🧾 Visual documentation of transition logic available via ProcessOn

---

## 📁 Project Structure

```
.
├── docs/                   # Documentation and formulas
│   └── Elevator Formula/   # (optional, moved online—see link below)
├── examples/               # Predefined FSM and Cyclone models
├── test/                   # Test cases for scenarios
├── auto_fsm_generator.py   # Auto-generates FSM models in Cyclone syntax
├── requirements.txt        # Python dependencies
├── LICENSE                 # Open-source license
└── README.md               # Project overview
```

---

## 📄 Documentation

The complete set of **formal SMT transition formulas** used in this project is available online:

🔗 [Elevator Transition Formula (ProcessOn Diagram)](https://www.processon.com/view/link/67c86fc0112574557d1fe993)

This includes visual state transitions, condition expressions, and logic definitions aligned with the Siemens S7-200 PLC model.

To learn how to model and verify these systems using **Cyclone**, refer to the official tutorial:

🔗 [Cyclone Tutorial by Hao Wu](https://classicwuhao.github.io/cyclone_tutorial/tutorial-content.html)

The tutorial demonstrates how to represent system behavior as graphs, encode safety and efficiency properties, and generate SMT formulas for verification using the Z3 solver. It serves as a helpful reference for understanding and extending the verification models in this project.

---

## 🔧 Requirements

- Python 3.8+
- Z3 SMT Solver
- Cyclone (graph-based SMT modeling tool)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Quick Start

1. **Clone the repository**:

```bash
git clone https://github.com/sandy686-234/Elevator_SMT_Verification.git
cd Elevator_SMT_Verification
```

2. **Generate Cyclone code** for your elevator system:

```bash
python auto_fsm_generator.py --levels 10
```

This will output the Cyclone model code (in `.cyc` syntax) directly to the terminal.

> 💡 Alternatively, you can modify the script and manually set `n = 10` if running in an IDE or notebook.

3. **Verify using Cyclone**:

- Copy the generated Cyclone code  
- Open the online Cyclone tool: [Cyclone Web Interface](https://classicwuhao.github.io/cyclone_tutorial/tutorial-content.html)  
- Paste the code into the editor  
- Click **“Check”** to run formal verification using the Cyclone engine and Z3 SMT backend

✅ Cyclone will translate the transition system into SMT formulas and verify that key properties (e.g., request servicing, direction switching, idle behavior) hold.

---

## 📚 Citation

If you use this project in your research, please cite:

> Huan Zhang, Li Yi, Long Cheng, Hao Wu.  
> "A Case Study on Verifying Elevator Scheduling Control System in Siemens S7-200 PLC."  
> *Submitted to the 30th International Conference on Formal Methods for Industrial Critical Systems (FMICS), 2025.*

---

## 📜 License

MIT License © 2025  
Huan Zhang, Li Yi, Long Cheng, Hao Wu

