def car_file_path(instance, filename):
    """
    Determines the upload path for car files.
    Args:
        instance: The Car instance
        filename: Original filename
    Returns:
        str: Path where the file should be uploaded
    """
    return f"{instance.organization.name}/{filename}"