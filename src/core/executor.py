import subprocess

class CommandExecutor:
    def run(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return result.stdout.strip() if result.stdout else result.stderr.strip()
        except Exception as e:
            return f"Erro: {e}"
