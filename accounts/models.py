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
        related_name='primary_members',
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
    organization_owner = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='owned_organizations',
        null=True,
        blank=True,
        
    )
    organization_roles = models.JSONField(
        default=dict,
        help_text="Define roles and permissions for organization members",
        null=True,
        blank=True
    )
    members = models.ManyToManyField(
        Account,
        through='OrganizationMember',
        related_name='member_organizations'
    )
    organization_role_members = models.JSONField(
        default=dict,
        help_text="Mapping of organization roles to member IDs",
        null=True,
        blank=True
    )
    
    def add_member(self, member, role_name='member'):
        if not self.organization_roles or role_name not in self.organization_roles:
            raise ValueError(f"Role '{role_name}' is not defined in organization")
        # Create or update the organization membership
        org_member, created = OrganizationMember.objects.get_or_create(
            organization=self,
            member=member,
            defaults={'role': role_name}
        )
        # Assign the role in the JSON field
        self.assign_role_to_member(member, role_name)        
        return org_member
    
    def remove_member(self, member):
        try:
            org_member = OrganizationMember.objects.get(organization=self, member=member)
            org_member.delete()
            # Also remove from role mapping
            for role, members in self.organization_role_members.items():
                member_id = str(member.id)
                if member_id in members:
                    members.remove(member_id)
            self.save()
            return True
        except OrganizationMember.DoesNotExist:
            return False
    
    def list_members(self):
        return OrganizationMember.objects.filter(organization=self)
    
    def is_member(self, member):
        return self.members.filter(id=member.id).exists()
    
    
    # Organization Roles functions
    def add_role(self, role_name, permissions):
        if not self.organization_roles:
            self.organization_roles = {}
        self.organization_roles[role_name] = permissions
        self.save()
    def remove_role(self, role_name):
        if role_name in self.organization_roles:
            del self.organization_roles[role_name]
            self.save()
            return True
        return False
    
    def assign_role_to_member(self, member, role_name):
        if role_name not in self.organization_roles:
            raise ValueError("Role does not exist in organization.")
        if not self.organization_role_members:
            self.organization_role_members = {}
        
        if role_name not in self.organization_role_members:
            self.organization_role_members[role_name] = []
        
        member_id = str(member.id)
        if member_id not in self.organization_role_members[role_name]:
            self.organization_role_members[role_name].append(member_id)
            self.save()
        OrganizationMember.objects.update_or_create(
            organization=self,
            member=member,
            defaults={
                "role": role_name
            }
        )
    
    def get_member_role(self, member):
        for role, members in self.organization_role_members.items():
            if str(member.id) in members:
                return role
        return None
    
    def get_member_permissions(self, member):
        role = self.get_member_role(member)
        if role and role in self.organization_roles:
            return self.organization_roles[role]
        return []

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organization"
        
    def __str__(self):
        return self.name
    
class OrganizationMember(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    member = models.ForeignKey(Account, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, verbose_name="Member Role")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'member')
        verbose_name = "Organization Member"
        verbose_name_plural = "Organization Members"

    def __str__(self):
        return f"{self.member.get_full_name()} - {self.organization.name} ({self.role})"