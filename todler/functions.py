from todler.engine import Engine

class Functions:

    def __init__(self, engine: Engine):
        self.engine = engine

    @Engine().action_logger("add")
    def add_ind(self, records: list[str], content: str):

        log_positions = []
        log_records = []
        for entry in content:
            parts = entry.split(maxsplit=1)
            print(f"Processing entry: '{entry}'")

            if parts[0].isdigit():
                position = int(parts[0])
                record_content = parts[1] if len(parts) > 1 else ""
                if 1 <= position <= len(records) + 1:
                    records.insert(position - 1, record_content + "\n")
                    print(f"Added '{record_content}' at position {position}")
                    log_records.append(record_content)
                    log_positions.append(position)
                else:
                    print(f"Error: Position {position} is out of bounds.")
                    exit()

            else:
                records.append(entry + "\n")
                print(f"Added '{entry}' at position {len(records)}")
                log_records.append(entry)
                log_positions.append(len(records))

        return log_positions, log_records

    @Engine().action_logger("rem")
    def remove_ind(self, records: list[str], val: str):
        if not records:
            print("Error: There ain't no records to remove")
            exit()

        indexes = self.engine.process_indexes(records, val)
        self.engine.validate_indexes(records, indexes)

        log_positions = []
        log_records = []

        for index in sorted(indexes, reverse=True):
            log_positions.append(index + 1)
            log_records.append(records[index].strip())
            del records[index]

        print(f"Removed records at: {indexes}")

        return log_positions, log_records

    @Engine().action_logger("doner")
    def doner(self, records, val):

        if not records:
            print("U wot m8")
            return

        indexes = self.engine.process_indexes(records, val)
        self.engine.validate_indexes(records, indexes)

        crossed_indexes = []
        crossed_tasks = []
        for index in indexes:
            if 0 <= index < len(records):
                task = ' ' + records[index].strip()
                crossed_task = ''.join([char + '\u0336' for char in task])
                crossed_tasks.append(records[index].strip())
                records[index] = crossed_task + '\n'
                crossed_indexes.append(index + 1)
            else:
                print(f"Error: Position {index + 1} is out of bounds.")
                exit()

        print(f"You krossed these {crossed_indexes} fools ")

        return crossed_indexes, crossed_tasks

    @Engine().action_logger("cleaner")
    def cleaner(self, records, val):

        if not records:
            print("U wot m8")
            return

        indexes = self.engine.process_indexes(records, val)
        self.engine.validate_indexes(records, indexes)

        cleaned_tasks = []
        cleaned_indexes = []
        for index in indexes:
            if 0 <= index < len(records):
                task = records[index].strip()
                cleaned_task = ''.join(char for char in task if char != '\u0336')
                cleaned_tasks.append(records[index].strip())
                cleaned_indexes.append(index + 1)
                records[index] = cleaned_task + "\n"
            else:
                print(f"Error: Position {index + 1} is out of bounds.")
                exit()

        print(f"Made peace with the whole city")

        return cleaned_indexes, cleaned_tasks

    @staticmethod
    def list_records(records: list[str]):

        if not records:
            print(f"Error: Ain't shit in here")
        for i, r in enumerate(records):
            print(f"{i + 1}) {r.rstrip("\n")}")

    @staticmethod
    def export(records: list[str], name: str):

        if not records:
            print("Bruh")
            return

        try:
            with open(name, 'r'):
                confirmation = input(f"'{name}' already exists. Overwrite? (y/n): ")
                if confirmation.lower() != "y":
                    print("Excaping")
                    return
        except FileNotFoundError:
            pass

        try:
            with open(name, "w") as a:
                a.writelines(records)
                print(f"Saving as {name}")
        except Exception as e:
            print(f"Oopsie: {e}")
