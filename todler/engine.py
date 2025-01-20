import os
import json
from functools import wraps

from todler.config import TODL_FP
from todler.config import REVERZ_FP
from todler.config import INVERZ_FP

class Engine:

    @staticmethod
    def write(records: list[str]) -> None:
        print(f"Writing {len(records)} records to file.")
        with open(TODL_FP, "w") as f:
            f.writelines(records)
        print("Write complete.")

    @staticmethod
    def read() -> list[str]:
        if os.path.exists(TODL_FP):
            print(f"Reading from {TODL_FP}.")
            with open(TODL_FP) as f:
                lines = f.readlines()
                print(f"Read {len(lines)} records.")
                return lines
        else:
            print(f"{TODL_FP} does not exist. Returning empty list.")
            return []

    @staticmethod
    def log_action(action):
        os.makedirs(os.path.dirname(REVERZ_FP), exist_ok=True)
        if not os.path.exists(REVERZ_FP):
            with open(REVERZ_FP, "w") as a:
                a.write("[]")

        with open(REVERZ_FP, "r") as a:
            try:
                history = json.load(a)
            except json.JSONDecodeError:
                history = []

        history.append(action)
        history = history[-5:]

        with open(REVERZ_FP, "w") as a:
            # noinspection PyTypeChecker
            json.dump(history, a, indent=4)

        redo_stack = []
        os.makedirs(os.path.dirname(INVERZ_FP), exist_ok=True)
        with open(INVERZ_FP, "w") as g:
            # noinspection PyTypeChecker
            json.dump(redo_stack, g, indent=4)

    def action_logger(self, action_type):
        """Decorator for undo/redo functionality"""

        def decorator(func):
            @wraps(func)
            def wrapper(instance, *args):
                result = func(instance, *args)
                if result is None:
                    print("you dun goofed")
                    exit()

                action = {"Action": action_type, "Task": "", "Index": 0}

                if action_type in ["add", "rem", "doner", "cleaner", "edit"]:
                    try:
                        index, task = result
                        action["Task"] = task
                        action["Index"] = index
                    except ValueError:
                        print(f"Error: Expected result format for '{action_type}' not met.")
                        exit()

                self.log_action(action)

                return result

            return wrapper

        return decorator

    @staticmethod
    def process_indexes(records, val):
        try:
            if val == "f":
                return [0]
            elif val == "l":
                return [len(records) - 1]
            elif val == "a":
                confirmation = input("Bruh are you sure about this? (y/n): ")
                if confirmation.lower() != 'y':
                    print("SAVED")
                    exit()
                return [i for i in range(len(records))]
            elif ":" in val:
                start, end = map(int, val.split(":"))
                if start > end:
                    print(f"Error: {start} is larger than {end}")
                    return
                return list(range(start - 1, end))
            elif "," in val:
                return [int(i) - 1 for i in val.split(",")]
            else:
                return [int(val) - 1]

        except ValueError as e:
            print(f"Value Error: {e} \nProvide valid input")
            exit()

    @staticmethod
    def validate_indexes(records, indexes):
        for index in indexes:
            if not 0 <= index + 1 <= len(records):
                print(f"Error {index + 1} out of bundy, exiting...")
                exit()
        return True
