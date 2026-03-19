class FastbootService:
    def __init__(self, executor):
        self.executor = executor

    def devices(self):
        return self.executor.run(["fastboot", "devices"])

    def reboot(self):
        if not self.devices():
            return "Erro: Nenhum dispositivo Fastboot detectado."
        return self.executor.run(["fastboot", "reboot"])

    def boot(self):
        if not self.devices():
            return "Erro: Nenhum dispositivo Fastboot detectado."
        return self.executor.run(["fastboot", "reboot"])
