def generate_elevator_code(n):
    code = f"""
option-trace=true;
graph Elevator{{
    const int FLOORS={n};

    // Landing call buttons for each floor
"""
    # Generate floor landing buttons (up/down)
    for i in range( n ):
        code += f"    bool l{i}_u, l{i}_d;\n"

    # Generate car call buttons
    code += "\n    // Car call buttons\n"
    for i in range( n ):
        code += f"    bool c{i};\n"

    # Elevator state and core nodes
    code += """
    enum {UP, DOWN, NA} DIR;
    int f where f >= 0 && f <= FLOORS - 1; // Current floor

    normal node DoorOpen {}
    normal node MoveUp { f++; }
    normal node MoveDown { f--; }

    normal node CC {}
    normal start node LC {}

    normal node SetMotionUp { DIR = #UP; }
    normal node SetMotionDown { DIR = #DOWN; }
    normal node SetIdle { DIR = #NA; }

    // Initialize state for each floor
"""
    # Generate each floor’s initial node logic
    for i in range( n ):
        code += f"    normal node L{i} {{\n"
        code += f"        c{i} = false;\n"
        code += f"        l{i}_u = false;\n        l{i}_d = false;\n"
        code += "    }\n"

    code += "\n    final normal node DoorClose {}\n"

    # LC -> DoorOpen transition logic
    code += "\n    edge { LC -> DoorOpen \n        where "
    for i in range( n ):
        if i == n - 1:
            code += f"(f == {i} && (l{i}_u || l{i}_d));\n    }}\n"
        else:
            code += f"(f == {i} && (l{i}_u || l{i}_d)) ||\n              "

    # Generate SetMotionUp transitions
    code += f"""
    edge {{ LC -> SetMotionUp
        where (
"""
    for i in range( n - 1 ):
        up_conditions = " || ".join(
            [f"l{j}_u" for j in range( i + 1, n )] + [f"l{j}_d" for j in range( i + 1, n )]
        )
        code += f"            (f == {i} && ({up_conditions}) && (DIR == #UP || DIR == #NA)) ||\n"

    code = code.rstrip( "||\n" ) + "        );\n    }\n"

    # Generate SetMotionDown transitions
    code += f"""
    edge {{ LC -> SetMotionDown
        where (
"""
    for i in range( n - 1, 0, -1 ):
        down_conditions = " || ".join(
            [f"l{j}_d" for j in range( 0, i )] + [f"l{j}_u" for j in range( 0, i )]
        )
        code += f"            (f == {i} && ({down_conditions}) && (DIR == #DOWN || DIR == #NA)) ||\n"

    code = code.rstrip( "||\n" ) + "        );\n    }\n"

    # Door logic
    code += """
    edge { DoorOpen -> CC }
    edge { CC -> DoorClose }
"""

    # Continue moving logic
    code += "    edge { DoorClose -> SetMotionUp\n        where (DIR == #UP && f < FLOORS-1);\n    }\n"
    code += "    edge { DoorClose -> SetMotionDown\n        where (DIR == #DOWN && f > 0);\n    }\n"

    # Idle logic
    code += """
    edge { DoorClose -> SetIdle where 
        (!c0"""
    for i in range( 1, n ):
        code += f" && !c{i}"
    code += ");\n    }\n"

    # Motion transitions
    code += "    edge { SetMotionUp -> MoveUp }\n"
    code += "    edge { SetMotionDown -> MoveDown }\n"
    code += "    edge { MoveUp -> MoveUp }\n"
    code += "    edge { MoveDown -> MoveDown }\n"

    # Stop at specific floors
    for i in range( n ):
        if i > 0:
            code += f"    edge {{ MoveUp -> L{i} where f == {i} && (c{i} || l{i}_d); }}\n"
        if i < n - 1:
            code += f"    edge {{ MoveDown -> L{i} where f == {i} && (c{i} || l{i}_u); }}\n"

    # Each floor opens the door
    for i in range( n ):
        code += f"    edge {{ L{i} -> DoorOpen }}\n"

    # Goal and assertions
    code += f"""
    goal{{
        assert (initial(c0) && !initial(c1) && !initial(c2) && !initial(c3) && initial(f)==3
            && !initial(l0_u) && initial(l1_u) && !initial(l1_d) && initial(l2_d) && !initial(l2_u) 
            && !initial(l3_d) && initial(DIR)==#DOWN);

        check upto 15 condition (L0) reach (CC,LC,L0,L1,L2,L3)
    }}
}}
"""
    return code


# Generate code for 10-floor elevator
n = 10
cyclone_code = generate_elevator_code( n )
print( cyclone_code )
