import curses
import sys
from pyfiglet import figlet_format
from src.core.executor import CommandExecutor
from src.services.adb_service import ADBService
from src.services.fastboot_service import FastbootService


def start_ui():
    curses.wrapper(run_menu)


def check_output(output):
    if not output or "error" in output.lower():
        return "[FAIL]"
    return "[ OK ]"


def draw_box(stdscr, y, x, h, w):
    for i in range(w):
        stdscr.addch(y, x + i, '-')
        stdscr.addch(y + h, x + i, '-')
    for i in range(h):
        stdscr.addch(y + i, x, '|')
        stdscr.addch(y + i, x + w, '|')

    stdscr.addch(y, x, '+')
    stdscr.addch(y, x + w, '+')
    stdscr.addch(y + h, x, '+')
    stdscr.addch(y + h, x + w, '+')


def run_menu(stdscr):
    executor = CommandExecutor()
    adb = ADBService(executor)
    fastboot = FastbootService(executor)

    curses.curs_set(0)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)   # seleção
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # ok
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # erro
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # título

    menu = [
        "[ADB] Listar dispositivos",
        "[SYS] Reiniciar dispositivo",
        "[PWR] Ligar tela (power)",
        "[SCR] Desbloquear (swipe)",
        "[SEC] Enviar PIN",
        "[NET] Ativar ADB Wi-Fi",
        "[NET] Conectar via IP",
        "[FBT] Listar Fastboot",
        "[FBT] Reiniciar Fastboot",
        "[EXIT] Sair"
    ]

    current = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # ===== TÍTULO ASCII =====
        title = figlet_format("POWEDROID", font="small")
        for i, line in enumerate(title.splitlines()):
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(i, w//2 - len(line)//2, line)
            stdscr.attroff(curses.color_pair(4))

        subtitle = "PY :: Android Control Interface"
        stdscr.addstr(6, w//2 - len(subtitle)//2, subtitle)

        # ===== CAIXA =====
        box_width = 50
        box_height = len(menu) + 2
        start_x = w//2 - box_width//2
        start_y = h//2 - box_height//2

        draw_box(stdscr, start_y, start_x, box_height, box_width)

        # ===== MENU =====
        for i, item in enumerate(menu):
            prefix = ">> " if i == current else "   "
            text = prefix + item

            x = start_x + 2
            y = start_y + 1 + i

            if i == current:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, text)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, text)

        # ===== FOOTER =====
        footer = "[↑↓] Navegar  [ENTER] Selecionar"
        stdscr.addstr(h-2, w//2 - len(footer)//2, footer)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current > 0:
            current -= 1
        elif key == curses.KEY_DOWN and current < len(menu) - 1:
            current += 1
        elif key in [10, 13]:
            stdscr.clear()

            if current == 0:
                out = adb.devices()
            elif current == 1:
                out = adb.reboot()
            elif current == 2:
                out = adb.wake()
            elif current == 3:
                out = adb.swipe()
            elif current == 4:
                stdscr.addstr(0, 0, "PIN: ")
                curses.echo()
                pin = stdscr.getstr().decode()
                curses.noecho()
                out = adb.send_pin(pin)
            elif current == 5:
                out = adb.enable_wifi()
            elif current == 6:
                stdscr.addstr(0, 0, "IP: ")
                curses.echo()
                ip = stdscr.getstr().decode()
                curses.noecho()
                out = adb.connect_wifi(ip)
            elif current == 7:
                out = fastboot.devices()
            elif current == 8:
                out = fastboot.reboot()
            elif current == 9:
                sys.exit()

            status = check_output(out)

            stdscr.clear()

            # STATUS
            if status == "[ OK ]":
                stdscr.attron(curses.color_pair(2))
            else:
                stdscr.attron(curses.color_pair(3))

            stdscr.addstr(1, 2, f"Status: {status}")
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.color_pair(3))

            # OUTPUT BOX
            draw_box(stdscr, 3, 2, 15, w-4)

            stdscr.addstr(4, 4, "Saída:")
            stdscr.addstr(6, 4, out if out else "Sem resposta do dispositivo.")

            stdscr.addstr(h-2, 2, "Pressione qualquer tecla para voltar...")
            stdscr.getch()
