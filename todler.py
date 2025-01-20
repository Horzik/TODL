from todler.engine import Engine
from todler.arguments import Arguments
from todler.functions import Functions
from todler.operation import Operation
from todler.undo_redo import Undo
from todler.undo_redo import Redo
from todler.editor import Editor

if __name__ == "__main__":

    parsed_args = Arguments().init_argparse().parse_args()

    if not any(vars(parsed_args).values()):
        print("No command provided. Exiting.")
        exit(0)

    engine = Engine()
    functions = Functions(engine)
    undo = Undo(engine)
    redo = Redo(engine)
    editor = Editor(engine)
    operation = Operation(engine, functions, undo, redo, editor)
    operation.process_commands(parsed_args)