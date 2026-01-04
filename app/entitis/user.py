from dataclasses import dataclass


@dataclass
class User:
    id: int | None = None
    username: str = ""
    email: str = ""

    def valid_email(self):
        return "@" in self.email and "." in self.email