class CPU:
    def __init__(self, name):
        self.name = name
        self.processingHistory = []

    def getProcessingHistory(self):
        return f"CPU {self.name}: {self.processingHistory}"

    def addInProcessingHistory(self, process):
        self.processingHistory.append(process)