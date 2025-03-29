# Elevator_SMT_Verification

**SMT-based Formal Verification for Elevator Scheduling Logic**

This project provides a formal verification framework for elevator scheduling control logic implemented on Siemens S7-200 PLCs. It uses SMT (Satisfiability Modulo Theories) techniques and the Cyclone tool to verify key safety and efficiency properties of elevator systems.

---

## 🚀 Features

- ✅ Finite-state modeling of elevator control logic (landing calls, car calls, direction switching)
- ✅ Automated FSM generation with configurable parameters for buildings with any number of floors 
- ✅ SMT formula generation with Cyclone Toos: translates FSM states, transitions, and system properties into precise SMT-LIB2 constraints
- ✅ Formal verification powered by Z3: Cyclone-generated formulas are rigorously verified using the Z3 SMT solver (v4.13.0) through bounded model checking
- ✅ Performance-optimized verification: includes benchmark results for verification times, with efficient modeling enabling rapid verification even for complex systems
- 🧾 Visual documentation of formal transition logic available via ProcessOn

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

To learn how to model and verify these logic systems using **Cyclone**, see the official tutorial:

👉 [Cyclone Tutorial by Hao Wu](https://classicwuhao.github.io/cyclone_tutorial/tutorial-content.html)

The tutorial demonstrates how to represent system behavior as graphs, encode safety and efficiency properties, and generate SMT formulas for verification using Z3. It serves as a helpful reference for understanding and extending the elevator verification models used in this project.

## 🔧 Requirements

- Python 3.8+
- Z3 SMT Solver
- Cyclone (graph-based SMT encoding tool)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

🚀 Quick Start
1. Clone the repository:
bashCopygit clone https://github.com/sandy686-234/Elevator_SMT_Verification.git
cd Elevator_SMT_Verification
2. Generate Cyclone code for your elevator system:
You can run the Python script and specify the number of levels via command-line argument:
bashCopypython auto_fsm_generator.py --levels 10
This will output the Cyclone model code to your terminal.
💡 Tip: Alternatively, you can directly modify the script (e.g., change n = 10 in the code) to set the number of levels manually when working in an IDE or notebook environment.
3. Verify using Cyclone:

Copy the generated Cyclone code
Open the Cyclone Online Tool [Cyclone Tutorial by Hao Wu](https://classicwuhao.github.io/cyclone_tutorial/tutorial-content.html)Paste the code into the Cyclone editor
Click "Check" to run formal verification using Cyclone with Z3 SMT backend

---

## 📚 Citation

If you use this project in your research, please cite:

> Huan Zhang, Li Yi, Long Cheng, Hao Wu. "Formal Verification of Elevator Logic for Safety and Efficiency." 2025.

---

## 📜 License

MIT License © 2025 Huan Zhang, Li Yi, Long Cheng, Hao Wu

