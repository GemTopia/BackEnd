from django.contrib.auth.models import BaseUserManager
import secrets
def int_to_unique_string(num: int) -> str:
    """
    Hashes an integer and returns a unique string representation.
    """
    hash_val = hash(num+100000000)
    hex_str = hex(hash_val)[2:]  # Remove "0x" prefix
    return hex_str

class UserManager(BaseUserManager):
    def create_user(self, user_name, email, password,inviter_id ):
        if not user_name:
            raise ValueError("Users must have a username")

        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must have a password")
        
        user = self.model(
            user_name=user_name,
            email=self.normalize_email(email),
            inviter_id=inviter_id

        )
        user.set_password(password)
        user.save(using=self._db)
        user.referrer_code=int_to_unique_string(user.id)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password):
        user = self.create_user(
            user_name=user_name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user