def generate_elevator_code(n):
    code = f"""
option-trace=true;
graph Elevator{{
    const int FLOORS={n};

    //landing call buttons
"""
    # Generate floor buttons (up/down)
    for i in range( n ):
        if i == 0:
            code += f"    bool l{i}_u;\n"  # First floor: only up button
        elif i == n - 1:
            code += f"    bool l{i}_d;\n"  # Top floor: only down button
        else:
            code += f"    bool l{i}_u, l{i}_d;\n"

    # Generate car call buttons
    code += "\n    //car call buttons\n"
    for i in range( n ):
        code += f"    bool c{i};\n"

    # Elevator state and basic nodes
    code += """
    enum {UP,DOWN,NA} DIR;
    int f where f >= 0 && f <= FLOORS - 1; //current floor

   final normal node DoorOpen{}
   final normal node MoveUp{f++;}
   final normal node MoveDown{f--;}

    //car call
    final normal node CC{}
    final normal start node LC{}

    final normal node SetMotionUp{DIR=#UP;}
    final normal node SetMotionDown{DIR=#DOWN;}
    final normal node SetIdle{DIR=#NA;}

    // Initialize floor state
"""
    # Initialize each floor state
    for i in range( n ):
        code += f"    final normal node L{i} {{\n"
        code += f"        c{i} = false;\n"
        if i == 0:
            code += f"        l{i}_u = false;\n"
        elif i == n - 1:
            code += f"        l{i}_d = false;\n"
        else:
            code += f"        l{i}_u = false;\n        l{i}_d = false;\n"
        code += "    }\n"

    code += "\n    final normal node DoorClose{}\n"

    # LC -> DoorOpen (handle special floors)
    code += "    edge { LC -> DoorOpen \n    where "
    edge_conditions = []
    for i in range( n ):
        if i == 0:
            edge_conditions.append( f"(f == {i} && l{i}_u)" )
        elif i == n - 1:
            edge_conditions.append( f"(f == {i} && l{i}_d)" )
        else:
            edge_conditions.append( f"(f == {i} && (l{i}_u || l{i}_d))" )
    code += " ||\n           ".join( edge_conditions ) + ";\n    }\n"

    # LC -> specific floor edge conditions
    for i in range( n ):
        if i == 0:
            code += f"    edge {{ LC -> L{i} where f == {i} && l{i}_u; }}\n"
        elif i == n - 1:
            code += f"    edge {{ LC -> L{i} where f == {i} && l{i}_d; }}\n"
        else:

            code += f"    edge {{ LC -> L{i} where f == {i} && (DIR == #UP || DIR == #NA) && l{i}_u; }}\n"
            code += f"    edge {{ LC -> L{i} where f == {i} && (DIR == #DOWN || DIR == #NA) && l{i}_d; }}\n"

    code += f"""
    edge {{ LC -> SetMotionUp
    where (
"""
    up_conditions = []
    for i in range( n - 1 ):
        up_floor_conditions = [f"l{j}_u || l{j}_d " for j in range( i + 1, n - 1 )]
        up_floor_conditions += [f"l{n - 1}_d"]
        if up_floor_conditions:
            up_conditions.append(
                f"(f == {i} && ({' || '.join( up_floor_conditions )}) && (DIR == #UP || DIR == #NA))" )
    code += " ||\n          ".join( up_conditions ) + "\n    );\n    }\n"

    code += f"""
    edge {{ LC -> SetMotionDown
    where (
"""
    down_conditions = []
    for i in range( n - 1, 0, -1 ):
        down_floor_conditions = [f"l{j}_d || l{j}_u" for j in range( 1, i )]
        down_floor_conditions += [f"l0_u"]
        if down_floor_conditions:
            down_conditions.append(
                f"(f == {i} && ({' || '.join( down_floor_conditions )}) && (DIR == #DOWN || DIR == #NA))" )
    code += " ||\n          ".join( down_conditions ) + "\n    );\n    }\n"

    # Logic for door opening on car call
    code += """
    edge { LC -> DoorOpen
       where """
    car_call_conditions = []
    for i in range( n ):
        car_call_conditions.append( f"(f == {i} && c{i})" )
    code += " ||\n             ".join( car_call_conditions ) + ";\n    }\n"

    code += """
    edge { DoorOpen -> CC }
    edge { CC -> DoorClose }

    // Continue upward or change direction to upward
    edge { DoorClose -> SetMotionUp
        where (
            ((DIR == #UP || DIR == #NA)&& 
                (
"""
    up_floor_conditions = []
    for i in range( n - 1 ):
        car_conditions = [f"c{j}" for j in range( i + 1, n )]

        landing_conditions = [f"l{j}_u" if j != n - 1 else '' for j in range( i + 1, n - 1 )]
        landing_conditions += [f"l{n - 1}_d"]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            up_floor_conditions.append( f"(f == {i} && ({' || '.join( conditions )}))" )
    code += "                    " + " ||\n                    ".join( up_floor_conditions )
    code += f""")
            ) ||
            ((DIR == #DOWN || DIR ==#NA) &&
                (
"""""
    down_floor_conditions = []
    for i in range( n - 1 ):

        negative_conditions = []
        for j in range( i ):
            negative_conditions.append( f"c{j}" )
            if j > 0:
                negative_conditions.append( f"l{j}_d" )
            if j < n - 1:
                negative_conditions.append( f"l{j}_u" )

        car_conditions = [f"c{j}" for j in range( i + 1, n )]
        landing_conditions = [f"l{j}_d" for j in range( i + 1, n )]
        if i + 1 < n - 1:
            landing_conditions += [f"l{j}_u" for j in range( i + 1, n - 1 )]

        conditions = [cond for cond in car_conditions + landing_conditions if cond]

        if negative_conditions and conditions:

            down_floor_conditions.append(
                f"(f == {i} && !({' || '.join( negative_conditions )}) && ({' || '.join( conditions )}))"
            )
        elif conditions:

            down_floor_conditions.append( f"(f == {i} && ({' || '.join( conditions )}))" )

    code += "                    " + " ||\n                    ".join( down_floor_conditions )
    code += """)
            )
        );
    }


    // Continue downward or change direction to downward
    edge { DoorClose -> SetMotionDown
        where (
            ((DIR == #UP || DIR == #NA) && 
                (
"""
    up_down_conditions = []

    for i in range( 1, n ):

        upper_conditions = []
        if i < n - 1:
            for j in range( i + 1, n ):
                upper_conditions.append( f"c{j}" )
                if j < n - 1:
                    upper_conditions.append( f"l{j}_u" )
                if j > 0:
                    upper_conditions.append( f"l{j}_d" )

        not_expr = f"!({' || '.join( upper_conditions )})" if upper_conditions else ""

        lower_conditions = []
        for j in range( 0, i ):
            lower_conditions.append( f"c{j}" )
            if j == 0:
                lower_conditions.append( "l0_u" )
            else:
                lower_conditions.append( f"l{j}_u" )
                lower_conditions.append( f"l{j}_d" )

        line = f"(f == {i} && "
        if not_expr:
            line += f"{not_expr} && "
        line += f"({' || '.join( lower_conditions )}))"
        up_down_conditions.append( line )

    code += "                    " + " ||\n                    ".join( up_down_conditions )
    code += f""")
            ) ||
            ((DIR == #DOWN || DIR ==#NA)&&
                (
"""
    down_conditions = []
    for i in range( n - 1, 0, -1 ):
        car_conditions = [f"c{j}" for j in range( 0, i )]

        landing_conditions = [f"l{j}_d" if j != 0 else '' for j in range( 1, i )]
        landing_conditions += [f"l{0}_u"]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            down_conditions.append( f"(f == {i} && ({' || '.join( conditions )}))" )
    code += "                    " + " ||\n                    ".join( down_conditions )
    code += """)
            )
        );
    }



    edge { DoorClose -> SetIdle where 
"""
    idle_conditions = [f"!c{i}" for i in range( n )]
    code += "        (" + " && ".join( idle_conditions )
    code += f") || \n"

    for i in range( n ):
        code += f"        (f == {i} && c{i}) || \n"

    code = code.rstrip( " || \n" ) + ";\n    }\n"

    for i in range( n ):
        if i == 0:
            code += f"    edge {{ SetIdle -> L{i} where f == {i} && (c{i} || l{i}_u); }}\n"
        elif i == n - 1:
            code += f"    edge {{ SetIdle -> L{i} where f == {i} && (c{i} || l{i}_d); }}\n"
        else:
            code += f"    edge {{ SetIdle -> L{i} where f == {i} && (c{i} || (l{i}_u || l{i}_d)); }}\n"

    code += """
    edge { SetIdle -> SetMotionUp
     where (
            ((DIR == #UP || DIR == #NA)&& 
                (
"""
    up_floor_conditions = []
    for i in range( n - 1 ):
        car_conditions = [f"c{j}" for j in range( i + 1, n )]

        landing_conditions = [f"l{j}_u" if j != n - 1 else '' for j in range( i + 1, n - 1 )]
        landing_conditions += [f"l{n - 1}_d"]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            up_floor_conditions.append( f"(f == {i} && ({' || '.join( conditions )}))" )
    code += "                    " + " ||\n                    ".join( up_floor_conditions )
    code += f""")
            ) ||
            ((DIR == #DOWN || DIR ==#NA) &&
                (
"""
    down_floor_conditions = []
    for i in range( n - 1 ):
        car_conditions = [f"c{j}" for j in range( i + 1, n )]
        landing_conditions = []
        for j in range( i + 1, n ):
            if j < n - 1:
                landing_conditions.append( f"l{j}_u" )
                landing_conditions.append( f"l{j}_d" )
            if j == n - 1:
                landing_conditions.append( f"l{j}_d" )

        conditions = [cond for cond in car_conditions + landing_conditions if cond]

        if i == 0:

            if conditions:
                down_floor_conditions.append(
                    f"(f == {i} && ({' || '.join( conditions )}))"
                )
        else:

            lower_conditions = [f"c{j}" for j in range( 0, i )]
            for j in range( 0, i ):
                if j == 0:
                    lower_conditions.append( "l0_u" )
                else:
                    lower_conditions.append( f"l{j}_u" )
                    lower_conditions.append( f"l{j}_d" )
            not_expr = f"!({' || '.join( lower_conditions )})"
            if conditions:
                down_floor_conditions.append(
                    f"(f == {i} && {not_expr} && ({' || '.join( conditions )}))"
                )
    code += "                    " + " ||\n                    ".join( down_floor_conditions )
    code += """)
            )
        );
    }

    edge { SetIdle -> SetMotionDown
  where (
            ((DIR == #UP || DIR == #NA) && 
                (
"""
    up_down_conditions = []
    for i in range( 1, n ):
        car_conditions_lower = [f"c{j}" for j in range( 0, i )]

        landing_conditions_lower = []
        for j in range( 0, i ):
            if j == 0:
                landing_conditions_lower.append( "l0_u" )
            else:
                landing_conditions_lower.append( f"l{j}_u" )
                landing_conditions_lower.append( f"l{j}_d" )
        down_expr = f"({' || '.join( car_conditions_lower + landing_conditions_lower )})"

        not_expr = ""
        if i < n - 1:
            upper_conditions = []
            for j in range( i + 1, n ):
                upper_conditions.append( f"c{j}" )
                if j < n - 1:
                    upper_conditions.append( f"l{j}_u" )
                    upper_conditions.append( f"l{j}_d" )
                if j == n - 1:
                    upper_conditions.append( f"l{j}_d" )
            not_expr = f"!({' || '.join( upper_conditions )}) && "

        up_down_conditions.append( f"(f == {i} && {not_expr}{down_expr})" )
    code += "                    " + " ||\n                    ".join( up_down_conditions )
    code += f""")
            ) ||
            ((DIR == #DOWN || DIR ==#NA)&&
                (
"""
    down_conditions = []
    for i in range( n - 1, 0, -1 ):
        car_conditions = [f"c{j}" for j in range( 0, i )]

        landing_conditions = [f"l{j}_d" if j != 0 else '' for j in range( 1, i )]
        landing_conditions += [f"l{0}_u"]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            down_conditions.append( f"(f == {i} && ({' || '.join( conditions )}))" )
    code += "                    " + " ||\n                    ".join( down_conditions )
    code += """)
            )
        );
    }
"""

    code += """
    edge { SetMotionUp -> MoveUp }
    edge { MoveUp -> MoveUp }
"""
    for i in range( 1, n - 1 ):
        code += f"    edge {{ MoveUp -> L{i} where f == {i} && ((l{i}_u && DIR == #UP) || c{i} ); }}\n"
    code += f"    edge {{ MoveUp -> L{n - 1} where f == {n - 1} && ((l{n - 1}_d && DIR == #UP) || c{n - 1} ); }}\n"
    code += """
    edge { SetMotionDown -> MoveDown }
    edge { MoveDown -> MoveDown }
"""
    for i in range( n - 2, 0, -1 ):
        code += f"    edge {{ MoveDown -> L{i} where f == {i} && (l{i}_d && DIR == #DOWN) || c{i}; }}\n"
    code += f"    edge {{ MoveDown -> L{0} where f == {0} && (l{0}_u && DIR == #DOWN ||  c{0} ); }}\n"

    for i in range( n ):
        code += f"    edge {{ L{i} -> DoorOpen }}\n"

    code += f"""
    goal{{
        assert ( initial(c0) && !initial(c1) && !initial(c2) && !initial(c3) && initial(f)==3
                && !initial(l0_u) && initial(l1_u) && !initial(l1_d) && initial(l2_d) && !initial(l2_u)
                && !initial(l3_d) && initial(DIR)==#DOWN
                );

         check for 17 condition (L0) reach (CC,LC,L0,L1,L2,L3)
    }}
}}
"""
    return code

def save_cyclone_file(code, filename="output.cyclone"):
    with open(filename, 'w') as file:
        file.write(code)


n = 4
code = generate_elevator_code(n)
save_cyclone_file(code)
