from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom user model
class User(AbstractUser):
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=15, null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile = models.ImageField(upload_to="profile/")
    role = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    username = None

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.fullname

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Case(models.Model):
    case_name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100)
    assigned_officer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_officer", null=True, blank=True)
    upload_at = models.DateField(auto_now_add=True)


class EvidenceFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='evidence/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    hash_value = models.CharField(max_length=128)
    previous_hash = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.file.name
    

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)