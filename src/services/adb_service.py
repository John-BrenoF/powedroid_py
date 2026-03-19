class ADBService:
    def __init__(self, executor):
        self.executor = executor

    def get_authorized_devices(self):
        output = self.executor.run(["adb", "devices"])
        devices = []
        if output:
            for line in output.split('\n'):
                parts = line.split()
                if len(parts) >= 2 and parts[1] == 'device':
                    devices.append(parts[0])
        return devices

    def _execute_on_devices(self, args, serial=None):
        if serial:
            devices = [serial]
        else:
            devices = self.get_authorized_devices()

        if not devices:
            return "Erro: Nenhum dispositivo autorizado encontrado."
        results = []
        for serial in devices:
            command = ["adb", "-s", serial] + args
            results.append(self.executor.run(command))
        return "\n".join(results)

    def devices(self):
        return self.executor.run(["adb", "devices"])

    def reboot(self, serial=None):
        return self._execute_on_devices(["reboot"], serial)

    def is_screen_on(self, serial):
        out = self.executor.run(["adb", "-s", serial, "shell", "dumpsys", "power"])
        return "mWakefulness=Awake" in out

    def wake(self, serial=None):
        devices = [serial] if serial else self.get_authorized_devices()
        if not devices:
            return "Erro: Nenhum dispositivo autorizado encontrado."
        results = []
        for dev in devices:
            if not self.is_screen_on(dev):
                results.append(self.executor.run(["adb", "-s", dev, "shell", "input", "keyevent", "26"]))
            else:
                results.append(f"Tela de {dev} já está ligada.")
        return "\n".join(results)

    def swipe(self, serial=None):
        return self._execute_on_devices(["shell", "input", "swipe", "300", "1000", "300", "300"], serial)

    def send_pin(self, pin, serial=None):
        return self._execute_on_devices(["shell", f"input keyevent 224 && input keyevent 82 && sleep 1 && input text {pin} && input keyevent 66"], serial)

    def enable_wifi(self, serial=None):
        return self._execute_on_devices(["tcpip", "5555"], serial)

    def connect_wifi(self, ip):
        return self.executor.run(["adb", "connect", f"{ip}:5555"])

    def get_battery_level(self, serial):
        out = self.executor.run(["adb", "-s", serial, "shell", "dumpsys", "battery"])
        if out and "level:" in out:
            for line in out.split('\n'):
                if "level:" in line:
                    return line.split(':')[1].strip() + "%"
        return "N/A"
