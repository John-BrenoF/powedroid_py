class FastbootService:
    def __init__(self, executor):
        self.executor = executor

    def devices(self):
        return self.executor.run(["fastboot", "devices"])

    def reboot(self):
        return self.executor.run(["fastboot", "reboot"])
