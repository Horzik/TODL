#!/usr/bin/env python3
import json
import os.path
import argparse


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


def undo():

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
            print("Error Nibba, can't remove it")
            return

    if last_action["Action"] == "rem":
        removed_indexes = last_action["Index"]
        removed_tasks = last_action["Task"]

        for index, task in zip (sorted(removed_indexes), removed_tasks):

            index = index - 1
            if 0 <= index <= len(records):
                records.insert(index -1, task + "\n")
            else:
                print(f"Error: Invalid index {index} for reinsertion.")
                return

        print(f"Added '{removed_tasks}' at position {removed_indexes}")

    with open(REVERZ_FP, "w") as f:
        json.dump(history, f, indent=4)

    write(records)


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
        action="store_true",
        help="WIP, nothing to see here"
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


"""
1) del - check array bounds : CHECKERZ
2) remove first / last element : CHECKERZ
3) handle arg clash e.g. remove / add / list together : CHECKERZ except ???
/ right now it first Removes, then Adds 
/ dunno if that's sufficient
4) clear with user y/n input : CHECKERZ
5) insert on position : CHECKERZ except KILLMYSELF
/ it works but not as I intended ( -a42 )
/ to insert on position type "-a "42 content"
/ LEAVE BRITTNEY ALONE
6) zerver : NOPERZ
7) PORNHUB ehhhhh I mean GITHUB : NOPERZ
XTRAS
8) adding multiple words as one wrekkord : CHECKERZ
/ (" ".join())
9) help ain't printing right : CHECKERZ 
/ (formatter_class)
10) ADD - if nic then print NOPERZ 
/ prints arg help, why not the print inside the add function?
11) UNDO - fml
NOTES
-- delete "reverse=True" otherwise RIP
    // ok but prints in reverse (duh)
    // reversing back again for printing is sus
--- 

"""