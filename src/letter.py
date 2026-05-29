class letter:
    def __init__(self, data):
        self.sender = 
        self.receiver =
        self.date =
        self.subject =
        self.content = 
        self.attachments = []
    
    def __str__(self):
        return f"From: {self.sender}\nTo: {self.receiver}\nDate: {self.date}\nSubject: {self.subject}\nContent: {self.content}\nAttachments: {', '.join(self.attachments)}"