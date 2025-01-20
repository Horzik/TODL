import argparse


class Arguments:

    @staticmethod
    def init_argparse():
        p = argparse.ArgumentParser(
            prog='todler',
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
            dest="list",
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
            help="Undo your last action (up to 5)"
        )

        p.add_argument(
            "--redo",
            "-re",
            action="store_true",
            help="Redo you last undo (up to 5)"
        )

        p.add_argument(
            "--done",
            "-d",
            "-k",
            action="store",
            help="For krossing these fools"
        )

        p.add_argument(
            "--clean",
            "-c",
            action="store",
            help="For cleaning purposes"
        )

        p.add_argument(
            "--export",
            "-x",
            "-s",
            action="store",
            dest="export",
            help="Export these goodz"
        )

        p.add_argument(
            "--edit",
            "-e",
            action="store_true",
            dest="editor",
            help="Editor"
        )

        return p
