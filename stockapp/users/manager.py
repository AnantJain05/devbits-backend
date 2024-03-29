from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("Email is Required")
        
        email = self.normalize_email(email)
        # user = self.model(email=email, **extra_fields)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError("Super user must have is_staff True")
        
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user