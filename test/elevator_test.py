class Elevator:
    def __init__(self, floors):
        """
        Initialize the elevator simulation.
        :param floors: Number of floors in the building.
        """
        self.floors = floors
        self.current_floor = 0  # Elevator starts at floor 0
        self.direction = "IDLE"  # Initial direction is idle
        self.calls = {i: {"up": False, "down": False, "car": False} for i in range(floors)}

    def press_button(self, floor, direction=None):
        """
        Simulate pressing a button (either inside the elevator or at a floor).
        :param floor: Floor where the button is pressed.
        :param direction: Direction (up/down) if it's a landing call, None if it's an inside call.
        """
        if direction:
            self.calls[floor][direction] = True
        else:
            self.calls[floor]["car"] = True

    def move(self):
        """
        Simulate the elevator moving up or down.
        """
        if self.direction == "UP":
            self.current_floor += 1
        elif self.direction == "DOWN":
            self.current_floor -= 1

        # Handle stopping logic when reaching a requested floor
        if self.calls[self.current_floor]["car"] or \
           (self.direction == "UP" and self.calls[self.current_floor]["up"]) or \
           (self.direction == "DOWN" and self.calls[self.current_floor]["down"]):
            self.open_door()

    def open_door(self):
        """
        Simulate the elevator door opening and clearing floor requests.
        """
        self.calls[self.current_floor]["car"] = False
        self.calls[self.current_floor]["up"] = False
        self.calls[self.current_floor]["down"] = False
        print(f"🚪 Elevator opens at floor {self.current_floor}")

    def decide_next_move(self):
        """
        Determine the next move based on pending requests.
        """
        up_requests = any(self.calls[i]["car"] or self.calls[i]["up"] for i in range(self.current_floor + 1, self.floors))
        down_requests = any(self.calls[i]["car"] or self.calls[i]["down"] for i in range(0, self.current_floor))

        if up_requests:
            self.direction = "UP"
        elif down_requests:
            self.direction = "DOWN"
        else:
            self.direction = "IDLE"

    def run_test(self, scenario_name, actions):
        """
        Execute a test scenario.
        :param scenario_name: Name of the test case.
        :param actions: List of actions to simulate.
        """
        print(f"\n🔍 Running Test: {scenario_name}")
        for action in actions:
            if action["type"] == "press":
                self.press_button(action["floor"], action.get("direction"))
            elif action["type"] == "move":
                self.decide_next_move()
                if self.direction != "IDLE":
                    self.move()

        print(f"✅ Test {scenario_name} completed.\n")


# Define test cases
elevator = Elevator(5)

test_cases = [
    {
        "name": "Single Floor Call",
        "actions": [
            {"type": "press", "floor": 2, "direction": "up"},
            {"type": "move"},
            {"type": "move"},
        ]
    },
    {
        "name": "Multiple Calls",
        "actions": [
            {"type": "press", "floor": 3, "direction": "down"},
            {"type": "press", "floor": 1, "direction": "up"},
            {"type": "move"},
            {"type": "move"},
            {"type": "move"},
        ]
    },
    {
        "name": "Car Call Overlap",
        "actions": [
            {"type": "press", "floor": 0, "direction": "up"},
            {"type": "press", "floor": 4, "direction": "down"},
            {"type": "press", "floor": 2},  # Inside elevator button
            {"type": "move"},
            {"type": "move"},
            {"type": "move"},
        ]
    },
]

# Execute test cases
for test in test_cases:
    elevator.run_test(test["name"], test["actions"])

