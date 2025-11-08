# CFlows App Documentation

## Models

### Car Model
The `Car` model manages vehicle information and workflow states.

#### Recent Updates (November 8, 2025)
- Made `registration_number` field nullable to support easier migration and data import
- Fixed database migration sequence for timestamps
- Improved URL configuration to prevent admin namespace conflicts

#### Fields
- `organization`: ForeignKey to Organization (owner of the car)
- `make`: Car manufacturer (CharField)
- `model`: Car model (CharField)
- `registration_number`: Unique identifier (CharField)
- `color`: Car color (CharField)
- `year`: Manufacturing year (PositiveIntegerField)
- `mileage`: Current mileage (PositiveIntegerField)
- `files`: Associated files (FileField)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `is_active`: Active status
- `is_archived`: Archive status
- `is_deleted`: Deletion status
- `station_fields`: Current station and status (JSONField)
- `metadata`: Additional car data (JSONField)
- `tags`: Car tags (JSONField)
- `notes`: Car notes (JSONField)
- `messages`: Communication logs (JSONField)
- `custom_car_info`: Custom fields (JSONField)

#### Usage
```python
# Create a new car
car = Car.create_car(
    organization=org,
    make="Volvo",
    model="XC60",
    registration_number="ABC123",
    color="Black",
    year=2023,
    mileage=0
)

# Move car to a new station
car.move_car_to_new_station('repair', status='In progress')

# Get car's current status
status = car.get_current_station_status('repair')
```

## Station Management System

### StationConfiguration Model
The `StationConfiguration` model allows organizations to define custom workflow stations and their allowed statuses.

#### Fields
- `organization`: ForeignKey to Organization
- `name`: Station name (e.g., "Repair", "Quality Check")
- `description`: Detailed description of the station
- `order`: Position in workflow sequence
- `is_active`: Whether the station is currently in use
- `default_status`: Initial status for cars entering this station
- `allowed_statuses`: List of valid statuses for this station
- `required`: Whether the station is mandatory
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

#### Usage
```python
# Create a new station configuration
repair_station = StationConfiguration.objects.create(
    organization=org,
    name="Repair",
    description="Vehicle repair and maintenance station",
    order=2,
    default_status="pending",
    allowed_statuses=["pending", "in progress", "on hold", "completed"],
    required=True
)

# Get all stations for an organization
org_stations = org.station_configurations.all().order_by('order')
```

### Station Fields Structure
The station_fields JSONField stores workflow information:
```json
{
    "incoming": {
        "status": "in stock",
        "timestamp": "2025-11-08T09:14:43.123456",
        "history": []
    },
    "repair": {
        "status": "in progress",
        "timestamp": "2025-11-08T10:00:00.000000",
        "history": [
            {
                "status": "waiting",
                "timestamp": "2025-11-07T15:30:22.123456"
            }
        ]
    },
    "sold": {
        "status": "pending",
        "timestamp": null,
        "history": []
    }
}
```

### Station Management Methods

#### move_car_to_new_station
```python
car.move_car_to_new_station('repair', status='In progress')
```
Moves a car to a new station and records the timestamp.

#### get_current_station_status
```python
status = car.get_current_station_status('repair')
```
Retrieves current status and timestamp for a station.

#### get_station_history
```python
history = car.get_station_history('repair')
```
Gets complete history of status changes for a station.

## File Management

### File Upload
Files are stored in organization-specific directories:
```python
# Files are automatically stored in:
# {organization.name}/{filename}
car.files = uploaded_file
car.save()
```

## Example Workflows

### Setting Up Organization Workflow
```python
# Create workflow stations
stations = [
    {
        "name": "Incoming",
        "order": 1,
        "default_status": "pending",
        "allowed_statuses": ["pending", "received", "rejected"],
        "required": True
    },
    {
        "name": "Repair",
        "order": 2,
        "default_status": "pending",
        "allowed_statuses": ["pending", "in progress", "on hold", "completed"],
        "required": False
    },
    {
        "name": "Quality Check",
        "order": 3,
        "default_status": "pending",
        "allowed_statuses": ["pending", "passed", "failed"],
        "required": True
    }
]

# Create station configurations
for station in stations:
    StationConfiguration.objects.create(
        organization=org,
        **station
    )
```

### Admin Configuration
The admin interface provides a user-friendly way to manage station configurations:
1. Navigate to Admin > Station Configurations
2. Click "Add Station Configuration"
3. Fill in the station details:
   - Name and description
   - Order in workflow
   - Default and allowed statuses
   - Required/Optional setting
4. Save to make the station available for cars in that organization

### Creating and Processing a New Car
```python
# Create new car
car = Car.create_car(
    organization=org,
    make="Volvo",
    model="XC60",
    registration_number="ABC123",
    color="Black",
    year=2023,
    mileage=0
)

# Move through stations
car.move_car_to_new_station('incoming', status='received')
car.move_car_to_new_station('repair', status='inspection')
car.move_car_to_new_station('repair', status='in progress')
car.move_car_to_new_station('repair', status='completed')
car.move_car_to_new_station('sold', status='pending delivery')

# Add notes
if isinstance(car.notes, list):
    car.notes.append({
        "date": datetime.now().isoformat(),
        "note": "Repair completed - all systems checked"
    })
    car.save()

# Add metadata
car.metadata.update({
    "service_history": "Complete",
    "next_service": "2026-11-08"
})
car.save()
```

### Managing Car Status
```python
# Check current status
current_status = car.get_current_station_status('repair')

# View history
repair_history = car.get_station_history('repair')
for entry in repair_history:
    print(f"Status: {entry['status']} at {entry['timestamp']}")
```

## URL Configuration

### Recent Updates (November 8, 2025)
The URL configuration has been optimized to prevent namespace conflicts and improve routing:

#### Main URLs (Mediap/urls.py)
- Removed duplicate admin URLs
- Simplified main URL patterns
- Proper separation of app-specific URLs

#### Root URLs (Mediap/root_urls.py)
- Added admin URLs for the main site only
- Consolidated main site URL patterns
- Improved URL organization for multi-domain support

#### App URLs (cflows/urls.py)
- Car management endpoints
- Station configuration endpoints
- Clean URL patterns without namespace conflicts

This new URL structure ensures proper routing across different domains and prevents the admin namespace warning that was previously occurring.