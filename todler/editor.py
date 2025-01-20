import sys
import curses

from io import StringIO
from todler.engine import Engine


class Editor:
    def __init__(self, engine: Engine):

        self.engine = engine
        self.cursor_x = 0
        self.cursor_y = 0
        self.lines = []

    def render(self, stdscr):

        stdscr.erase()
        height, width = stdscr.getmaxyx()
        max_lines = height - 5
        viewport_start = max(0, self.cursor_y - (height // 2))
        viewport_end = min(len(self.lines), viewport_start + max_lines)
        visual_row = 0
        horizontal_start = 0

        for i in range(viewport_start, viewport_end):
            line_to_display = self.lines[i].rstrip()

            if self.cursor_x < width:
                horizontal_start = 0
            else:
                horizontal_start = self.cursor_x - (width // 2)

            horizontal_start = max(0, horizontal_start)
            visible_line = line_to_display[horizontal_start:horizontal_start + width]
            stdscr.addstr(visual_row, 0, f"{i + 1}: {visible_line}")
            visual_row += 1

        adjusted_cursor_y = self.cursor_y - viewport_start
        adjusted_cursor_x = min(self.cursor_x - horizontal_start + len(str(self.cursor_y + 1)) + 2, width - 1)

        if height > 4:
            debug_info = f"Cursor: ({self.cursor_y}, {self.cursor_x}), Size: ({height}, {width})"
            stdscr.addstr(height - 3, 0, f"     Terminal Size: {height} rows, {width} columns, {debug_info}")
            stdscr.addstr(height - 4, 0, "||| CTRL + W = SAVE ||| CTRL + E = EXIT ||| CTRL + K = DONE ||| CTRL + L = CLEAN |||")

        stdscr.move(adjusted_cursor_y, adjusted_cursor_x)
        stdscr.refresh()

    def handle_input(self, key):

        if key == curses.KEY_UP and self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
        elif key == curses.KEY_DOWN and self.cursor_y < len(self.lines) - 1:
            self.cursor_y += 1
            self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
        elif key == curses.KEY_LEFT:
            if self.cursor_x > 0:
                self.cursor_x -= 1
            elif self.cursor_y > 0:
                self.cursor_y -= 1
                self.cursor_x = len(self.lines[self.cursor_y])
        elif key == curses.KEY_RIGHT:
            if self.cursor_x < len(self.lines[self.cursor_y]):
                self.cursor_x += 1
            elif self.cursor_y < len(self.lines) - 1:
                self.cursor_y += 1
                self.cursor_x = 0
        elif key == 10:  # ENTER
            current_line = self.lines[self.cursor_y]
            new_line = current_line[self.cursor_x:]
            self.lines[self.cursor_y] = current_line[:self.cursor_x]
            self.lines.insert(self.cursor_y + 1, new_line)
            self.cursor_y += 1
            self.cursor_x = 0
        elif key == curses.KEY_BACKSPACE:
            if self.cursor_x > 0:
                current_line = list(self.lines[self.cursor_y])
                del current_line[self.cursor_x - 1]
                self.lines[self.cursor_y] = ''.join(current_line)
                self.cursor_x -= 1
            elif self.cursor_y > 0:
                previous_line_length = len(self.lines[self.cursor_y - 1])
                merged_line = self.lines[self.cursor_y - 1] + self.lines[self.cursor_y]
                del self.lines[self.cursor_y]
                self.lines[self.cursor_y - 1] = merged_line
                self.cursor_y -= 1
                self.cursor_x = previous_line_length
        elif key == curses.KEY_DC:
            current_line_length = len(self.lines[self.cursor_y])
            if self.cursor_x < current_line_length:
                current_line = list(self.lines[self.cursor_y])
                del current_line[self.cursor_x]
                self.lines[self.cursor_y] = ''.join(current_line)
            elif self.cursor_x == current_line_length and self.cursor_y < len(self.lines) - 1:
                merged_line = self.lines[self.cursor_y] + self.lines[self.cursor_y + 1]
                del self.lines[self.cursor_y + 1]
                self.lines[self.cursor_y] = merged_line
        else:
            if 32 <= key <= 126:
                current_line = list(self.lines[self.cursor_y])
                current_line.insert(self.cursor_x, chr(key))
                self.lines[self.cursor_y] = ''.join(current_line)
                self.cursor_x += 1

    @Engine().action_logger("edit")
    def edit(self, stdscr):

        self.lines = [line.rstrip() for line in self.engine.read()]

        if not self.lines:
            self.lines = [""]

        height, width = stdscr.getmaxyx()
        kokot_lines = self.lines[:]  # For saving upon exit if any changes were made
        origo_lines = self.lines[:]  # For logging
        origo_indexes = list(range(1, len(self.lines) + 1))
        saved = False
        curses.curs_set(1)

        while True:
            self.render(stdscr)
            key = stdscr.getch()

            if key == curses.KEY_RESIZE:
                height, width = stdscr.getmaxyx()
                self.cursor_y = min(self.cursor_y, height - 1)
                self.cursor_x = min(self.cursor_x, width - 1)

            # CTRL + W = WRITE / SAVE
            if key == 23:

                # stdout for the "write" print
                original_stdout = sys.stdout
                captured_output = StringIO()
                sys.stdout = captured_output

                lines_to_save = [line + "\n" for line in self.lines]
                self.engine.write(lines_to_save)

                kokot_lines = self.lines[:]
                saved = True

                # stdout reverse
                sys.stdout = original_stdout
                output = captured_output.getvalue()

                stdscr.move(height - 3, 0)
                stdscr.clrtoeol()
                stdscr.addstr(output)
                stdscr.addstr("File saved! Press any key to continue.")
                stdscr.refresh()
                stdscr.getch()


            # CTRL + E = EXIT
            elif key == 5:
                if self.lines != kokot_lines:
                    stdscr.move(height - 2, 0)
                    stdscr.clrtoeol()
                    stdscr.addstr("Want to save? (Y/N): ")
                    char = stdscr.getch()
                    if char in [ord('y'), ord('Y')]:
                        lines_to_save = [line + "\n" for line in self.lines]
                        self.engine.write(lines_to_save)
                        return origo_indexes, origo_lines
                    elif char in [ord('n'), ord('N')]:
                        if saved:
                            return origo_indexes, origo_lines
                        else:
                            break
                    else:
                        pass
                else:
                    if saved:
                        return origo_indexes, origo_lines
                    else:
                        break

            # CTRL + K = KROSS
            elif key == 11:
                current_line = self.lines[self.cursor_y].strip()

                if '\u0336' in current_line:
                    continue

                crossed_task = ''.join([char + '\u0336' for char in current_line])
                self.lines[self.cursor_y] = crossed_task

            elif key == 12:
                current_line = self.lines[self.cursor_y].strip()
                cleaned_task = ''.join([char for char in current_line if char != '\u0336'])
                self.lines[self.cursor_y] = cleaned_task


            self.handle_input(key)