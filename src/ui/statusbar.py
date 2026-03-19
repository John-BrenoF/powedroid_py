import curses

class StatusBar:
    def __init__(self, adb_service):
        self.adb = adb_service
        if curses.has_colors():
            curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)

    def draw(self, win, h, w, target_device, last_status):
        try:
            dev_count = len(self.adb.get_authorized_devices())
        except:
            dev_count = 0

        conn_status = "ONLINE" if dev_count > 0 else "OFFLINE"
        bar_text = f" ALVO: {target_device if target_device else 'GLOBAL'} | DEVS: {dev_count} [{conn_status}] | MSG: {last_status}"

        win.attron(curses.color_pair(7))
        try:
            win.addstr(h - 1, 0, bar_text.ljust(w))
        except curses.error:
            pass
        win.attroff(curses.color_pair(7))