from dataclasses import dataclass

from app.models.role import Role


@dataclass
class Message:
    role: Role
    content: str

    def to_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content,
        }