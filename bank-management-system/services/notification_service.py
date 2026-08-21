class NotificationService:

    def send(self, email: str, message: str) -> None:
        print(f"[NOTIFICATION] To: {email} | {message}")
