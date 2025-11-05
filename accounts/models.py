# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users require email adress')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Sätt standardfält för superanvändare
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusers must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusers must have is_superuser=True.')
            
        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.SET_NULL,      # Keep the user if the organisation gets deleted
        related_name='members',
        null=True,                      # Allows that user is not connected to org
        blank=True,
        verbose_name="Connecting Organisation"
    )
    
    # Ange Manager och fält
    objects = AccountManager()
    
    # Det fält som används för inloggning
    USERNAME_FIELD = 'email'
    # Fält som frågas vid skapande av superanvändare
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Organization Name")
    slug = models.SlugField(unique=True, help_text="Used in URL:s and/or as identifier")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organization"
        
    def __str__(self):
        return self.name