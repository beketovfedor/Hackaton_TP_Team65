class Letter:
    def __init__(self, data=None):
        data = data or {}
        self.sender = data.get("from", "")
        self.receiver = data.get("to", "")
        self.date = data.get("date", "")
        self.subject = data.get("subject", "")
        self.content = data.get("body", "")
        self.attachments = data.get("attachments", [])

    def __str__(self):
        return (
            f"From: {self.sender}\n"
            f"To: {self.receiver}\n"
            f"Date: {self.date}\n"
            f"Subject: {self.subject}\n"
            f"Content: {self.content}\n"
            f"Attachments: {', '.join(self.attachments)}"
        )


# Совместимость со старым названием класса.
letter = Letter
