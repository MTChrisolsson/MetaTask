# Accounts App Documentation

## Models

### Account Model
The `Account` model extends Django's AbstractBaseUser and implements a custom user model.

#### Fields
- `email`: Email address (used as username)
- `first_name`: User's first name
- `last_name`: User's last name
- `organization`: ForeignKey to Organization (can be null)
- `date_joined`: Timestamp of account creation
- `is_active`: Boolean indicating if account is active
- `is_staff`: Boolean indicating if user has staff privileges
- `is_superuser`: Boolean indicating if user has superuser privileges

#### Usage
```python
# Create a new account
account = Account.objects.create_user(
    email='user@example.com',
    password='secure_password',
    first_name='John',
    last_name='Doe'
)

# Get full name
full_name = account.get_full_name()
```

### Organization Model
Manages organizations and their members with role-based permissions.

#### Fields
- `name`: Organization name
- `slug`: URL-friendly name
- `is_active`: Organization status
- `created_at`: Creation timestamp
- `organization_owner`: ForeignKey to Account
- `members`: ManyToManyField to Account through OrganizationMember
- `organization_roles`: JSONField storing role definitions
- `organization_role_members`: JSONField storing role assignments

#### Usage
```python
# Create an organization
org = Organization.objects.create(
    name="Test Organization",
    slug="test-org",
    organization_owner=account
)

# Add a role
org.add_role('admin', ['manage_members', 'edit_org'])

# Add a member with role
org.add_member(account, role='admin')

# Check member permissions
permissions = org.get_member_permissions(account)
```

### OrganizationMember Model
Manages the relationship between Organizations and Accounts.

#### Fields
- `organization`: ForeignKey to Organization
- `member`: ForeignKey to Account
- `role`: Role name
- `joined_at`: Timestamp when member joined
- `is_active`: Member status

#### Usage
```python
# Create membership
member = OrganizationMember.objects.create(
    organization=org,
    member=account,
    role='admin'
)

# Get all members of an organization
members = org.list_members()
```

## Key Features

### Role-Based Access Control
Organizations support custom roles with specific permissions:
1. Define roles using `add_role()`
2. Assign roles to members using `assign_role_to_member()`
3. Check permissions using `get_member_permissions()`

### Member Management
Organizations provide methods for member management:
- `add_member()`: Add new member with role
- `remove_member()`: Remove member
- `is_member()`: Check membership
- `list_members()`: Get all members

### History Tracking
The system maintains:
- Member join dates
- Role assignment history
- Organization creation dates

## Example Workflows

### Creating a New Organization
```python
# Create owner account
owner = Account.objects.create_user(
    email='owner@example.com',
    password='secure_password'
)

# Create organization
org = Organization.objects.create(
    name='New Company',
    slug='new-company',
    organization_owner=owner
)

# Set up roles
org.add_role('admin', ['manage_members', 'edit_org', 'view_reports'])
org.add_role('member', ['view_reports'])

# Add initial member
org.add_member(owner, role='admin')
```

### Managing Members
```python
# Add new member
new_member = Account.objects.get(email='new@example.com')
org.add_member(new_member, role='member')

# Change member's role
org.assign_role_to_member(new_member, 'admin')

# Remove member
org.remove_member(new_member)
```