from todler.engine import Engine
from todler.functions import Functions
from todler.undo_redo import Undo
from todler.undo_redo import Redo
from todler.editor import Editor

import curses
import argparse


class Operation:
    def __init__(self, engine: Engine, functions: Functions, undo: Undo, redo: Redo, editor: Editor):
        self.engine = engine
        self.functions = functions
        self.undo = undo
        self.redo = redo
        self.editor = editor
        self.records = self.engine.read()

    def process_commands(self, args: argparse.Namespace) -> None:
        print("Processing commands...")
        modified = False

        if args.remove:
            self.functions.remove_ind(self.records, args.remove)
            modified = True

        if args.add:
            self.functions.add_ind(self.records, args.add)
            modified = True

        if args.export:
            self.functions.export(self.records, args.export)
            modified = True

        if args.done:
            self.functions.doner(self.records, args.done)
            modified = True

        if args.clean:
            self.functions.cleaner(self.records, args.clean)
            modified = True

        if args.undo:
            self.undo.undo(self.records)
            modified = True

        if args.redo:
            self.redo.redo(self.records)
            modified = True

        if args.editor:
            curses.wrapper(self.editor.edit)
            # writes itself

        if args.list:
            self.functions.list_records(self.records)

        if modified:
            self.engine.write(self.records)