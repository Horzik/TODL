import json
import os

from todler.engine import Engine
from todler.config import REVERZ_FP
from todler.config import INVERZ_FP


class Undo:

    def __init__(self, engine: Engine):
        self.engine = engine

    @staticmethod
    def undo(records: list[str]):
        with open(REVERZ_FP, "r") as f:
            history = json.load(f)
            if not history:
                print("Nothing to undo")
                exit()

        last_action = history.pop()

        with open(REVERZ_FP, "w") as f:
            # noinspection PyTypeChecker
            json.dump(history, f, indent=4)

        if last_action["Action"] == "add":
            i = last_action["Index"]
            print(i)
            for index in reversed(i):
                if 1 <= index <= len(records):
                    removed_task = records.pop(index - 1)
                    print(f"Removed '{removed_task.strip()}' at position {index}")
                else:
                    print("Errore magoore, can't remove it")
                    exit()

        if last_action["Action"] == "rem":
            for index, task in zip(sorted(last_action["Index"]), reversed(last_action["Task"])):
                if 0 <= index <= len(records) + 1:
                    records.insert(index - 1, task + "\n")
                    print(f"Re-added '{task}' at position '{index}' ")
                else:
                    print(f"Error: Invalid index {index} for reinsertion.")
                    exit()

        if last_action["Action"] == "doner":
            for index, task in zip((last_action["Index"]), last_action["Task"]):
                index = index - 1
                if 0 <= index <= len(records):
                    records.pop(index)
                    records.insert(index, task + "\n")
                else:
                    print(f"Error: Invalid index {index} for reinsertion.")
                    exit()
            print(f"Beef settled")

        if last_action["Action"] == "cleaner":

            for index, task in zip(sorted(last_action["Index"]), last_action["Task"]):
                index = index - 1
                if 0 <= index <= len(records):
                    records.pop(index)
                    records.insert(index, task + "\n")
                else:
                    print(f"Error: Invalid index {index} for reinsertion.")
                    exit()
            print(f"You're beefing again")

        if last_action["Action"] == "edit":  # FINALLY MADE IT WORK DON'T ASK ME (PLS ASK)
            klitoris = []
            kokot = [task.strip("\n") for task in records]
            index = list(range(1, len(records) + 1))
            action = {"Action": "edit", "Task": kokot, "Index": index}

            if os.path.exists(INVERZ_FP):
                with open(INVERZ_FP, "r") as g:
                    klitoris = json.load(g)

            klitoris.append(action)
            klitoris = klitoris[-50:]

            with open(INVERZ_FP, "w") as g:
                # noinspection PyTypeChecker
                json.dump(klitoris, g, indent=4)

            records.clear()
            for index, task in zip(sorted(last_action["Index"]), last_action["Task"]):
                index = index - 1
                if 0 <= index <= len(records):
                    records.insert(index, task + "\n")
                else:
                    print(f"Error: Invalid index {index} for reinsertion.")
                    exit()
            print(f"Edit restored")

            return

        klitoris = []

        if os.path.exists(INVERZ_FP):
            with open(INVERZ_FP, "r") as g:
                klitoris = json.load(g)

        klitoris.append(last_action)
        klitoris = klitoris[-50:]

        with open(INVERZ_FP, "w") as g:
            # noinspection PyTypeChecker
            json.dump(klitoris, g, indent=4)


class Redo:
    def __init__(self, engine: Engine):
        self.engine = engine

    @staticmethod
    def redo(records: list[str]):
        if os.path.exists(INVERZ_FP):
            with open(INVERZ_FP, "r") as g:
                redo_stack = json.load(g)
            if not redo_stack:
                print("Nothing to redo")
                exit()

            last_action = redo_stack.pop()
            with open(REVERZ_FP, "r") as g:
                undo_stack = json.load(g)
            undo_stack.append(last_action)

            with open(REVERZ_FP, "w") as g:
                # noinspection PyTypeChecker
                json.dump(undo_stack, g, indent=4)
            with open(INVERZ_FP, "w") as g:
                # noinspection PyTypeChecker
                json.dump(redo_stack, g, indent=4)

            if last_action["Action"] == "add":
                for index, task in zip(last_action["Index"], last_action["Task"]):
                    if 0 <= index <= len(records) + 1:
                        records.insert(index - 1, task + "\n")
                    else:
                        print(f"Error: Invalid index {index} for reinsertion.")
                        exit()
                print(f"Added '{(last_action["Task"])}' at position {(last_action["Index"])}")

            if last_action["Action"] == "rem":
                for index in sorted((last_action["Index"]), reverse=True):
                    removed_task = records.pop(index - 1)
                    print(f"Removed '{removed_task.strip()}' at position {index}")

            if last_action["Action"] == "doner":
                for index, task in zip(sorted(last_action["Index"]), last_action["Task"]):
                    beef = ''.join([char + '\u0336' for char in task])
                    records[index - 1] = beef + "\n"
                print(f"You keep crossing these toyz: {last_action["Index"]}")

            if last_action["Action"] == "cleaner":
                for index, task in zip(sorted(last_action["Index"]), last_action["Task"]):
                    cleaned_tasks = ''.join(char for char in task if char != '\u0336')
                    records[index - 1] = cleaned_tasks + "\n"
                print("Peacemaker: Now you have no enemies")

            if last_action["Action"] == "edit":
                records.clear()
                for index, task in zip(sorted(last_action["Index"]), last_action["Task"]):
                    index = index - 1
                    if 0 <= index <= len(records):
                        records.insert(index, task + '\n')
                print(f"Edit restored")
