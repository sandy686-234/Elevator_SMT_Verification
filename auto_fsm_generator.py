def generate_elevator_code(n):
    code = f"""
option-trace=true;
graph Elevator{{
    const int FLOORS={n};

    //landing call buttons
"""
    # 生成楼层按钮（上下行）
    for i in range(n):
        if i == 0:
            code += f"    bool l{i}_u;\n"  # 第一层只有上行按钮
        elif i == n - 1:
            code += f"    bool l{i}_d;\n"  # 最高层只有下行按钮
        else:
            code += f"    bool l{i}_u, l{i}_d;\n"

    # 生成车内楼层按钮
    code += "\n    //car call buttons\n"
    for i in range(n):
        code += f"    bool c{i};\n"

    # 电梯状态和基础节点
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

    // 初始化楼层状态
"""
    # 生成每一层的初始化状态
    for i in range(n):
        code += f"    final normal node L{i} {{\n"
        code += f"        c{i} = false;\n"
        if i == 0:  # 第一层
            code += f"        l{i}_u = false;\n"
        elif i == n - 1:  # 最高层
            code += f"        l{i}_d = false;\n"
        else:
            code += f"        l{i}_u = false;\n        l{i}_d = false;\n"
        code += "    }\n"

    code += "\n    final normal node DoorClose{}\n"

    # LC -> DoorOpen 逻辑（处理特殊楼层）
    code += "    edge { LC -> DoorOpen \n    where "
    edge_conditions = []
    for i in range(n):
        if i == 0:
            edge_conditions.append(f"(f == {i} && l{i}_u)")  # 第一层只能上行
        elif i == n - 1:
            edge_conditions.append(f"(f == {i} && l{i}_d)")  # 最高层只能下行
        else:
            edge_conditions.append(f"(f == {i} && (l{i}_u || l{i}_d))")
    code += " ||\n           ".join(edge_conditions) + ";\n    }\n"

    # LC -> 特定楼层的边缘条件
    for i in range(n):
        if i == 0:
            code += f"    edge {{ LC -> L{i} where f == {i} && l{i}_u; }}\n"
        elif i == n - 1:
            code += f"    edge {{ LC -> L{i} where f == {i} && l{i}_d; }}\n"
        else:
            # 上行和下行分别处理
            code += f"    edge {{ LC -> L{i} where f == {i} && (DIR == #UP || DIR == #NA) && l{i}_u; }}\n"
            code += f"    edge {{ LC -> L{i} where f == {i} && (DIR == #DOWN || DIR == #NA) && l{i}_d; }}\n"

    # 修改 SetMotionUp 逻辑，去掉最高层的上行条件
    code += f"""
    edge {{ LC -> SetMotionUp
    where (
"""
    up_conditions = []
    for i in range(n - 1):
        up_floor_conditions = [f"l{j}_u" for j in range(i + 1, n - 1)]  # 排除最高层
        if up_floor_conditions:
            up_conditions.append(f"(f == {i} && ({' || '.join(up_floor_conditions)}) && (DIR == #UP || DIR == #NA))")
    code += " ||\n          ".join(up_conditions) + "\n    );\n    }\n"

    # 修改 SetMotionDown 逻辑，去掉最低层的下行条件
    code += f"""
    edge {{ LC -> SetMotionDown
    where (
"""
    down_conditions = []
    for i in range(n - 1, 0, -1):
        down_floor_conditions = [f"l{j}_d" for j in range(1, i)]  # 排除最低层
        if down_floor_conditions:
            down_conditions.append(
                f"(f == {i} && ({' || '.join(down_floor_conditions)}) && (DIR == #DOWN || DIR == #NA))")
    code += " ||\n          ".join(down_conditions) + "\n    );\n    }\n"

    # 车厢呼叫的开门逻辑
    code += """
    edge { LC -> DoorOpen
       where """
    car_call_conditions = []
    for i in range(n):
        car_call_conditions.append(f"(f == {i} && c{i})")
    code += " ||\n             ".join(car_call_conditions) + ";\n    }\n"

    # 后续部分保持不变（从门的开关和状态转换逻辑开始）
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
    for i in range(n - 1):
        car_conditions = [f"c{j}" for j in range(i + 1, n)]
        # 最高层不添加上行条件
        landing_conditions = [f"l{j}_u" if j != n-1 else '' for j in range(i + 1, n - 1)]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            up_floor_conditions.append(f"(f == {i} && ({' || '.join(conditions)}))")
    code += "                    " + " ||\n                    ".join(up_floor_conditions)
    code += f""")
            ) ||
            ((DIR == #DOWN || DIR ==#NA) &&
                (
"""
    down_floor_conditions = []
    for i in range(n - 1):
        car_conditions = [f"c{j}" for j in range(i + 1, n)]
        # 最高层不添加下行条件
        landing_conditions = [f"l{j}_d" if j != n-1 else '' for j in range(i + 1, n - 1)]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            down_floor_conditions.append(f"(f == {i} && ({' || '.join(conditions)}))")
    code += "                    " + " ||\n                    ".join(down_floor_conditions)
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
    for i in range(1, n):
        car_conditions_lower = [f"c{j}" for j in range(0, i)]
        # 最低层不添加下行条件
        landing_conditions_lower = [f"l{j}_d" if j != 0 else '' for j in range(1, i)]
        conditions = [cond for cond in car_conditions_lower + landing_conditions_lower if cond]
        if conditions:
            up_down_conditions.append(f"(f == {i} && ({' || '.join(conditions)}))")
    code += "                    " + " ||\n                    ".join(up_down_conditions)
    code += f""")
            ) ||
            ((DIR == #DOWN || DIR ==#NA)&&
                (
"""
    down_conditions = []
    for i in range(n - 1, 0, -1):
        car_conditions = [f"c{j}" for j in range(0, i)]
        # 最低层不添加上行条件
        landing_conditions = [f"l{j}_u" if j != 0 else '' for j in range(1, i)]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            down_conditions.append(f"(f == {i} && ({' || '.join(conditions)}))")
    code += "                    " + " ||\n                    ".join(down_conditions)
    code += """)
            )
        );
    }

    edge { DoorClose -> SetIdle where 
"""
    idle_conditions = [f"!c{i}" for i in range(n)]
    code += "        (" + " && ".join(idle_conditions)
    code += f") || \n"

    for i in range(n):
        code += f"        (f == {i} && c{i}) || \n"

    code = code.rstrip(" || \n") + ";\n    }\n"

    # SetIdle 到特定楼层的转换
    for i in range(n):
        if i == 0:
            code += f"    edge {{ SetIdle -> L{i} where f == {i} && (c{i} || l{i}_u); }}\n"
        elif i == n - 1:
            code += f"    edge {{ SetIdle -> L{i} where f == {i} && (c{i} || l{i}_d); }}\n"
        else:
            code += f"    edge {{ SetIdle -> L{i} where f == {i} && (c{i} || (l{i}_u || l{i}_d)); }}\n"

    # 修改 SetIdle -> SetMotionUp 的逻辑
    code += """
    edge { SetIdle -> SetMotionUp
     where (
            ((DIR == #UP || DIR == #NA)&& 
                (
"""
    up_floor_conditions = []
    for i in range(n - 1):
        car_conditions = [f"c{j}" for j in range(i + 1, n)]
        # 最高层不添加上行条件
        landing_conditions = [f"l{j}_u" if j != n-1 else '' for j in range(i + 1, n - 1)]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            up_floor_conditions.append(f"(f == {i} && ({' || '.join(conditions)}))")
    code += "                    " + " ||\n                    ".join(up_floor_conditions)
    code += f""")
            ) ||
            ((DIR == #DOWN || DIR ==#NA) &&
                (
"""
    down_floor_conditions = []
    for i in range(n - 1):
        car_conditions = [f"c{j}" for j in range(i + 1, n)]
        # 最高层不添加下行条件
        landing_conditions = [f"l{j}_d" if j != n-1 else '' for j in range(i + 1, n - 1)]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            down_floor_conditions.append(f"(f == {i} && ({' || '.join(conditions)}))")
    code += "                    " + " ||\n                    ".join(down_floor_conditions)
    code += """)
            )
        );
    }

    // 修改 SetIdle -> SetMotionDown 的逻辑
    edge { SetIdle -> SetMotionDown
  where (
            ((DIR == #UP || DIR == #NA) && 
                (
"""
    up_down_conditions = []
    for i in range(1, n):
        car_conditions_lower = [f"c{j}" for j in range(0, i)]
        # 最低层不添加下行条件
        landing_conditions_lower = [f"l{j}_d" if j != 0 else '' for j in range(1, i)]
        conditions = [cond for cond in car_conditions_lower + landing_conditions_lower if cond]
        if conditions:
            up_down_conditions.append(f"(f == {i} && ({' || '.join(conditions)}))")
    code += "                    " + " ||\n                    ".join(up_down_conditions)
    code += f""")
            ) ||
            ((DIR == #DOWN || DIR ==#NA)&&
                (
"""
    down_conditions = []
    for i in range(n - 1, 0, -1):
        car_conditions = [f"c{j}" for j in range(0, i)]
        # 最低层不添加上行条件
        landing_conditions = [f"l{j}_u" if j != 0 else '' for j in range(1, i)]
        conditions = [cond for cond in car_conditions + landing_conditions if cond]
        if conditions:
            down_conditions.append(f"(f == {i} && ({' || '.join(conditions)}))")
    code += "                    " + " ||\n                    ".join(down_conditions)
    code += """)
            )
        );
    }
"""

    # 上下运动节点转换
    code += """
    edge { SetMotionUp -> MoveUp }
    edge { MoveUp -> MoveUp }
"""
    for i in range(1, n):
        # 最高层不能继续上行，且不使用最高层的上行按钮
        code += f"    edge {{ MoveUp -> L{i} where f == {i} && ((l{i-1}_u && DIR == #UP) || c{i} ); }}\n"

    code += """
    edge { SetMotionDown -> MoveDown }
    edge { MoveDown -> MoveDown }
"""
    for i in range(n-1):
        # 最低层不能继续下行，且不使用最低层的下行按钮
        code += f"    edge {{ MoveDown -> L{i} where f == {i} && (l{i+1}_d && DIR == #DOWN) || c{i}; }}\n"

    # 各楼层开门
    for i in range(n):
        code += f"    edge {{ L{i} -> DoorOpen }}\n"

    # 目标和验证条件
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


n = 4
cyclone_code = generate_elevator_code(n)
print(cyclone_code)
