import datetime

class User:
    id: str
    user_name: str
    first_name: str
    last_name: str
    avatar: str
    email: str
    role: str
    status: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, id, user_name, first_name, last_name, avatar, email, role, status, created_at, updated_at):
        self.id = id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.avatar = avatar
        self.email = email
        self.role = role
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def toJson(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar": self.avatar,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
