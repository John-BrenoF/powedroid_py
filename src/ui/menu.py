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

def run_menu(stdscr):
    def draw_box(win, y, x, h, w, title=""):
        win.attron(curses.color_pair(5))
        try:
            win.addch(y, x, curses.ACS_ULCORNER)
            win.addch(y, x + w - 1, curses.ACS_URCORNER)
            win.addch(y + h - 1, x, curses.ACS_LLCORNER)
            win.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)
            win.hline(y, x + 1, curses.ACS_HLINE, w - 2)
            win.hline(y + h - 1, x + 1, curses.ACS_HLINE, w - 2)
            win.vline(y + 1, x, curses.ACS_VLINE, h - 2)
            win.vline(y + 1, x + w - 1, curses.ACS_VLINE, h - 2)
        except curses.error:
            pass
        if title:
            win.addstr(y, x + 2, f" {title} ", curses.A_BOLD)
        win.attroff(curses.color_pair(5))

    executor = CommandExecutor()
    adb = ADBService(executor)
    fastboot = FastbootService(executor)

    curses.curs_set(0)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)    # seleção (alto contraste)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # ok
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # erro
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # título (estilo cyber)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)    # bordas (azul escuro)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # ícones (amarelo)

    menu = [
        ("", "Listar dispositivos (ADB)"),
        ("", "Reiniciar dispositivo"),
        ("", "Ligar tela (Power)"),
        ("", "Desbloquear (Swipe)"),
        ("", "Enviar PIN"),
        ("", "Ativar ADB Wi-Fi"),
        ("", "Conectar via IP"),
        ("", "Listar Fastboot"),
        ("", "Reiniciar Fastboot"),
        ("", "Sair")
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
        box_width = 54
        box_height = len(menu) + 2
        start_x = w // 2 - box_width // 2
        start_y = h//2 - box_height//2

        draw_box(stdscr, start_y, start_x, box_height, box_width, "Menu Principal")

        # ===== MENU =====
        for i, (icon, label) in enumerate(menu):
            prefix = " ▶ " if i == current else "   "
            x = start_x + 2
            y = start_y + 1 + i
            text_content = f"{icon}  {label}"

            if i == current:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, (prefix + text_content).ljust(box_width - 4), curses.A_BOLD)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(6))
                stdscr.addstr(y, x + len(prefix), icon)
                stdscr.attroff(curses.color_pair(6))
                stdscr.addstr(y, x + len(prefix) + 3, label)

        # ===== FOOTER =====
        footer = " [↑↓] Navegar  [ENTER] Selecionar "
        stdscr.attron(curses.color_pair(5))
        stdscr.addstr(h-2, w//2 - len(footer)//2, footer)
        stdscr.attroff(curses.color_pair(5))

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
                draw_box(stdscr, h//2-2, w//2-15, 5, 30, "Entrada")
                stdscr.addstr(h//2, w//2-13, "Digite o PIN: ")
                curses.echo()
                pin = stdscr.getstr().decode()
                curses.noecho()
                out = adb.send_pin(pin)
            elif current == 5:
                out = adb.enable_wifi()
            elif current == 6:
                draw_box(stdscr, h//2-2, w//2-15, 5, 30, "Entrada")
                stdscr.addstr(h//2, w//2-13, "Digite o IP: ")
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

            # OUTPUT BOX (Maior e mais organizada)
            res_h = h - 6
            res_w = w - 4
            draw_box(stdscr, 3, 2, res_h, res_w, "Saída do Comando")

            if out:
                lines = out.split('\n')
                max_lines = res_h - 2
                for idx, line in enumerate(lines[:max_lines]):
                    stdscr.addstr(4 + idx, 4, line[:res_w-4])
            else:
                stdscr.addstr(5, 4, "Sem resposta ou saída vazia.")

            stdscr.attron(curses.A_BLINK)
            stdscr.addstr(h-2, 2, "Pressione qualquer tecla para voltar...")
            stdscr.attroff(curses.A_BLINK)
            stdscr.getch()
