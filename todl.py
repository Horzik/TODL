#!/usr/bin/env python3
import json
import os.path
import argparse
import unicodedata

from todl.config import TODL_FP
from todl.config import REVERZ_FP
from todl.config import INVERT_FP


def write(records: list[str]) -> None:
    with open(TODL_FP, "w") as f:
        f.writelines(records)


def read() -> list[str]:
    if os.path.exists(TODL_FP):
        with open(TODL_FP, "r") as f:
            lines = f.readlines()
            return lines
    else:
        return []


def log_action(action):
    if os.path.exists(REVERZ_FP):
        with open(REVERZ_FP, "r") as a:
            history = json.load(a)
    else:
        history = []

    history.append(action)
    history = history[-50:]

    with open(REVERZ_FP, "w") as a:
        json.dump(history, a, indent=4)

    redo_stekk = []
    with open(INVERT_FP, "w") as g:
        json.dump(redo_stekk, g, indent=4)

def export(name: str):
    records = read()
    if not records:
        print("Bruh")
        return

    if os.path.exists(name):
        confirmation = input(f"'{name}' already exists. Overwrite? (y/n): ")
        if confirmation.lower() != "y":
            print("Excaping")
            return

    try:
        with open(name, "w") as a:
            a.writelines(records)
            print(f"Saving as {name}")
    except Exception as e:
            print(f"Oopsie: {e}")


def add_todl(args: list[str]) -> None:
    records = read()

    for entry in args:
        parts = entry.split(maxsplit=1)
        action = {"Action": "add", "Task": "", "Index": 0}

        if parts[0].isdigit():
            position = int(parts[0])
            record_content = parts[1] if len(parts) > 1 else ""
            if 1 <= position <= len(records) + 1:
                records.insert(position - 1, record_content + "\n")
                print(f"Added '{record_content}' at position {position}")

                action["Task"] = record_content
                action["Index"] = position
                log_action(action)
            else:
                print(f"Error: Position {position} is out of bounds.")
        else:
            records.append(entry + "\n")
            print(f"Added '{entry}' at position {len(records)}")

            action["Task"] = entry
            action["Index"] = len(records)
            log_action(action)

    write(records)


def rm_records(val: str):
    records = read()
    action = {"Action": "rem", "Task": "", "Index": 0}

    if not records:
        print("Error: There ain't no records to remove")
        return

    try:
        if val == "f":
            indexes = [0]
        elif val == "l":
            indexes = [len(records) - 1]
        elif val == "a":
            confirmation = input("Bruh are you sure about this? (y/n): ")
            if confirmation.lower() != 'y':
                print("SAVED")
                return
            indexes = [i for i in range(len(records))]
        elif ":" in val:
            start, end = map(int, val.split(":"))
            if start > end:
                print(f"Error: {start} is larger than {end}")
                return
            indexes = list(range(start - 1, end))
        elif "," in val:
            indexes = [int(i) - 1 for i in val.split(",")]
        else:
            indexes = [int(val) - 1]

        removed_indexes = []
        removed_tasks = []

        for index in sorted(indexes, reverse=True):
            if 0 <= index < len(records):
                removed_tasks.append(records[index].strip())
                del records[index]
                removed_indexes.append(index + 1)
            else:
                print(f"Error: {index + 1} ain't there")

        if removed_indexes:
            print(f"Removed indexes {removed_indexes}")

        write(records)
        action["Task"] = removed_tasks
        action["Index"] = removed_indexes
        log_action(action)


    except ValueError:
        print(f"Error: Wrong Argument")


def list_records():
    records = read()
    if not records:
        print(f"Error: Ain't shit in here")
    for i, r in enumerate(records):
        print(f"{i + 1}) {r.rstrip("\n")}")


def undo() -> None:
    with open(REVERZ_FP, "r") as f:
        history = json.load(f)

        if not history:
            print("Lmao tu nic neni")
            return

    last_action = history.pop()
    records = read()

    if last_action["Action"] == "add":
        index = last_action["Index"]
        if 1 <= index <= len(records):
            removed_task = records.pop(index - 1)
            print(f"Removed '{removed_task.strip()}' at position {index}")
        else:
            print("Errore magoore, can't remove it")
            return

    if last_action["Action"] == "rem":
        removed_indexes = last_action["Index"]
        removed_tasks = last_action["Task"]

        for index, task in sorted(zip(removed_indexes, removed_tasks)):
            if 0 <= index <= len(records) + 1:
                records.insert(index - 1, task + "\n")
            else:
                print(f"Error: Invalid index {index} for reinsertion.")
                return

        print(f"Added '{removed_tasks}' at position {removed_indexes}")

    if last_action["Action"] == "doner":
        for index, task in zip(sorted(last_action["Index"]), last_action["Task"]):
            index = index - 1
            if 0 <= index <= len(records):
                records.pop(index)
                records.insert(index, task + "\n")
                print(f"Beef with {index + 1} resolved")
            else:
                print(f"Error: Invalid index {index} for reinsertion.")
                return

    if last_action["Action"] == "cleaner":

        for index, task in zip(sorted(last_action["Index"]), last_action["Task"]):
            index = index - 1
            if 0 <= index <= len(records):
                records.pop(index)
                records.insert(index, task + "\n")
            else:
                print(f"Error: Invalid index {index} for reinsertion.")
                return
        print(f"You're beefing again")

    with open(REVERZ_FP, "w") as f:
        json.dump(history, f, indent=4)

    write(records)
    klitoris = []

    if os.path.exists(INVERT_FP):
        with open(INVERT_FP, "r") as g:
            klitoris = json.load(g)

    klitoris.append(last_action)
    klitoris = klitoris[-50:]

    with open(INVERT_FP, "w") as g:
        json.dump(klitoris, g, indent=4)


def redo() -> None:
    if os.path.exists(INVERT_FP):
        with open(INVERT_FP, "r") as g:
            redo_stack = json.load(g)

        if not redo_stack:
            print("No can do")
            return

        last_action = redo_stack.pop()
        records = read()

        with open(REVERZ_FP, "r") as g:
            undo_stack = json.load(g)
        undo_stack.append(last_action)

        with open(REVERZ_FP, "w") as g:
            json.dump(undo_stack, g, indent=4)

        with open(INVERT_FP, "w") as g:
            json.dump(redo_stack, g, indent=4)

        if last_action["Action"] == "add":
            index = last_action["Index"]
            task = last_action["Task"]
            records.insert(index - 1, task + "\n")
            print(f"Re-added '{task}' at position {index}")

        if last_action["Action"] == "rem":
            removed_indexes = last_action["Index"]
            for index in sorted(removed_indexes, reverse=True):
                removed_task = records.pop(index - 1)
                print(f"Removed '{removed_task.strip()}' at position {index}")

        if last_action["Action"] == "doner":
            for index, task in zip(sorted(last_action["Index"]), last_action["Task"]):
                beef = ''.join([char + '\u0336' for char in task])
                records[index -1] = beef + "\n"
                print(f"You keep crossing these {last_action["Index"]} toyz")

        if last_action["Action"] == "cleaner":
            for index, task in zip(sorted(last_action["Index"]), last_action["Task"]):
                cleaned_tasks = ''.join(char for char in task if unicodedata.category(char) != 'Mn')
                records[index -1] = cleaned_tasks + "\n"
            print("Peacemaker: Now you have no enemies")

        write(records)


def doner(val):
    records = read()
    action = {"Action": "", "Task": "", "Index": 0}

    if not records:
        print("U wot m8")
        return

    try:
        if val == "f":
            indexes = [0]
        elif val == "l":
            indexes = [len(records) - 1]
        elif ":" in val:
            start, end = map(int, val.split(":"))
            if start > end:
                print(f"Error: {start} is larger than {end}")
                return
            indexes = list(range(start - 1, end))
        elif "," in val:
            indexes = [int(i) - 1 for i in val.split(",")]
        elif val == "a":
            confirmation = input("Bruh you really wanna blast 'em? (y/n): ")
            if confirmation.lower() != 'y':
                print("SAVED")
                return
            indexes = [i for i in range(len(records))]

        elif val == "d":                                # All this to clean
            indexes = [i for i in range(len(records))]  # Yes I feel bad
            cleaned_tasks = []
            for index in indexes:
                if 0 <= index < len(records):
                    task = records[index].strip()
                    cleaned_task = ''.join(char for char in task if unicodedata.category(char) != 'Mn')
                    cleaned_tasks.append(records[index].strip())
                    records[index] = cleaned_task + "\n"
            write(records)
            print(f"Made peace with the whole city")
            indexes = [i + 1 for i in indexes]          # The only way to clean/resolve the beef
            action["Task"] = cleaned_tasks              # Can't bother, if you cross a wrong fool
            action["Index"] = indexes                   # you can just undo. Yes the logic is insane
            action["Action"] = "cleaner"                # will rewrite it all anyway
            log_action(action)
            return

        else:
            indexes = [int(val) - 1]

        crossed_indexes = []
        crossed_tasks = []

        for index in indexes:
            if 0 <= index < len(records):
                task = ' ' + records[index].strip()
                crossed_task = ''.join([char + '\u0336' for char in task])
                crossed_tasks.append(records[index].strip())
                records[index] = crossed_task + '\n'
                crossed_indexes.append(index + 1)

        write(records)
        print(f"You krossed these {crossed_indexes} fools ")

        action["Task"] = crossed_tasks
        action["Index"] = crossed_indexes
        action["Action"] = "doner"
        log_action(action)

    except ValueError:
        print("Mackas mi hada")


def init_argparse():
    p = argparse.ArgumentParser(
        prog='todl',
        description='To Do List, duh',
        epilog="Help",
        formatter_class=argparse.RawTextHelpFormatter
    )

    p.add_argument(
        "--add",
        "-a",
        dest="add",
        action='append',
        help='''Add record to TODO list.
Automatically adds to the end.
Use "X Content to add" to insert on position X
Use "-X" To append an X number to the End'''
    )

    p.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all TODO records"
    )

    p.add_argument(
        "--remove",
        "-r",
        action="store",
        dest="remove",
        help='''Remove record from the TODO list.
Use a number of the index you want removed.
Use 'f' to remove first line
Use 'l' to remove the last line
Use '3:5' to remove indexes from 2 to 5
Use '2,13,137' to remove specific indexes
Use 'a' to clear all listings'''
    )

    p.add_argument(
        "--undo",
        "-u",
        action="store_true",
        help="Undoes your last action"
    )

    p.add_argument(
        "--redo",
        "-ree",
        "-m",
        action="store_true",
        help="WIP, nothing to see here"
    )

    p.add_argument(
        "--done",
        "-d",
        "-k",
        action="store",
        help="For krossing these fools"
    )

    p.add_argument(
        "--export",
        "-x",
        "-s",
        action="store",
        dest="export",
        help="Export these goodz"
    )

    return p


if __name__ == "__main__":
    parser = init_argparse()
    parsed_args = parser.parse_args()

    if parsed_args.remove:
        rm_records(parsed_args.remove)

    if parsed_args.add:
        add_todl(parsed_args.add)

    if parsed_args.list:
        list_records()

    if parsed_args.undo:
        undo()

    if parsed_args.redo:
        redo()

    if parsed_args.done:
        doner(parsed_args.done)

    if parsed_args.export:
        export(parsed_args.export)

"""
1) del - check array bounds : CHECKERZ
2) remove first / last element : CHECKERZ
3) handle arg clash e.g. remove / add / list together : CHECKERZ except ???
/first Removes, then Adds 
/ dunno if that's sufficient
4) clear with user y/n input : CHECKERZ
5) insert on position : CHECKERZ except KILLMYSELF
/ it works but not as *I want it to* ( -a42 )
/ to insert on position type [-a "42 content]
/ LEAVE BRITTNEY ALONE
6) zerver : NOPERZ
7) PORNHUB ehhhhh I mean GITHUB : CHECKERZ

XTRAS

8) adding multiple words as one wrekkord : CHECKERZ
/ (" ".join())
9) help ain't printing right : CHECKERZ 
/ (formatter_class)
10) ADD - if nic then print NOPERZ 
/ prints "arg help" instead, why not the "print" inside the add function?
/ clueless
11) UNDO + REDO : CHECKERZ
12) doner kross mania : CHECKERZ
NOTES
-- delete "reverse=True" otherwise RIP
    // ok but prints in reverse (duh)
    // reversing back again for printing is sus
-- 3 != 3 aka 0 based
    // not very based
-- logic not logical but npnp
--next I want:
            "Swap"
            Multiple Lists?
            Peace on Earth
"""
