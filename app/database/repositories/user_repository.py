from typing import Optional, List
from datetime import datetime
from app.database.client import get_db_client
from app.database.models import UserModel
from app.mock.users import DEMO_USERS
from app.core.logging_config import logger


class UserRepository:
    def __init__(self):
        # In-memory store initialized with demo users
        self._memory_users: dict[str, UserModel] = {}
        for u in DEMO_USERS:
            user = UserModel(
                id=u["id"],
                email=u["email"],
                password_hash=u["password_hash"],
                full_name=u["full_name"],
                role=u["role"],
                avatar_url=u.get("avatar_url"),
                is_active=u["is_active"],
            )
            self._memory_users[user.email] = user

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        client = get_db_client()
        if client:
            try:
                res = client.table("profiles").select("*").eq("email", email.strip()).execute()
                if res.data:
                    d = res.data[0]
                    return UserModel(
                        id=d["id"],
                        email=d["email"],
                        password_hash="", # Supabase Auth stores password hash
                        full_name=d.get("full_name"),
                        role=d.get("role", "viewer"),
                        avatar_url=d.get("avatar_url"),
                        is_active=d.get("is_active", True),
                    )
            except Exception as e:
                logger.warning(f"Supabase error fetching user: {e}")
        return self._memory_users.get(email.strip().lower())

    async def get_by_id(self, user_id: str) -> Optional[UserModel]:
        client = get_db_client()
        if client:
            try:
                res = client.table("profiles").select("*").eq("id", user_id).execute()
                if res.data:
                    d = res.data[0]
                    return UserModel(
                        id=d["id"],
                        email=d["email"],
                        password_hash="",
                        full_name=d.get("full_name"),
                        role=d.get("role", "viewer"),
                        avatar_url=d.get("avatar_url"),
                        is_active=d.get("is_active", True),
                    )
            except Exception as e:
                logger.warning(f"Supabase error fetching user by id: {e}")
        for u in self._memory_users.values():
            if u.id == user_id:
                return u
        return None

    async def create_user(self, user: UserModel) -> UserModel:
        client = get_db_client()
        if client:
            try:
                client.table("profiles").insert({
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                    "is_active": user.is_active,
                }).execute()
            except Exception as e:
                logger.warning(f"Supabase error creating profile: {e}")
        self._memory_users[user.email.lower()] = user
        return user

    async def update_user(self, user_id: str, updates: dict) -> Optional[UserModel]:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        for k, v in updates.items():
            if hasattr(user, k):
                setattr(user, k, v)
        user.updated_at = datetime.utcnow()

        client = get_db_client()
        if client:
            try:
                client.table("profiles").update(updates).eq("id", user_id).execute()
            except Exception as e:
                logger.warning(f"Supabase error updating user: {e}")

        return user


user_repository = UserRepository()
