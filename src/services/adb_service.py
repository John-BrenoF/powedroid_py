class ADBService:
    def __init__(self, executor):
        self.executor = executor

    def _get_authorized_devices(self):
        output = self.executor.run(["adb", "devices"])
        devices = []
        if output:
            for line in output.split('\n'):
                parts = line.split()
                if len(parts) >= 2 and parts[1] == 'device':
                    devices.append(parts[0])
        return devices

    def _execute_on_devices(self, args):
        devices = self._get_authorized_devices()
        if not devices:
            return "Erro: Nenhum dispositivo autorizado encontrado."
        results = []
        for serial in devices:
            command = ["adb", "-s", serial] + args
            results.append(self.executor.run(command))
        return "\n".join(results)

    def devices(self):
        return self.executor.run(["adb", "devices"])

    def reboot(self):
        return self._execute_on_devices(["reboot"])

    def wake(self):
        return self._execute_on_devices(["shell", "input", "keyevent", "26"])

    def swipe(self):
        return self._execute_on_devices(["shell", "input", "swipe", "300", "1000", "300", "300"])

    def send_pin(self, pin):
        return self._execute_on_devices(["shell", f"input text {pin} && input keyevent 66"])

    def enable_wifi(self):
        return self._execute_on_devices(["tcpip", "5555"])

    def connect_wifi(self, ip):
        return self.executor.run(["adb", "connect", f"{ip}:5555"])
