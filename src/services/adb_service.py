class ADBService:
    def __init__(self, executor):
        self.executor = executor

    def devices(self):
        return self.executor.run(["adb", "devices"])

    def reboot(self):
        return self.executor.run(["adb", "reboot"])

    def wake(self):
        return self.executor.run(["adb", "shell", "input", "keyevent", "26"])

    def swipe(self):
        return self.executor.run(["adb", "shell", "input", "swipe", "300", "1000", "300", "300"])

    def send_pin(self, pin):
        return self.executor.run(["adb", "shell", "input", "text", pin]) + "\n" + \
               self.executor.run(["adb", "shell", "input", "keyevent", "66"])

    def enable_wifi(self):
        return self.executor.run(["adb", "tcpip", "5555"])

    def connect_wifi(self, ip):
        return self.executor.run(["adb", "connect", f"{ip}:5555"])
