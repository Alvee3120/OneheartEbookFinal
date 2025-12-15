# backend/catalog/validators.py

from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = ('.pdf', '.epub')
MAX_FILE_SIZE_MB = 50


def validate_ebook_file_extension(value):
    name = value.name.lower()
    if not any(name.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise ValidationError(
            f"Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed."
        )


def validate_ebook_file_size(value):
    """
    Safely validate ebook file size.
    Handles cases where value or value.size may be None,
    which happens when editing an object without re-uploading a file.
    """
    if value is None:
        return  # No file uploaded or unchanged file

    filesize = getattr(value, "size", None)
    if filesize is None:
        return  # Skip validation if file size is unavailable

    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

    if filesize > max_bytes:
        raise ValidationError(
            f"Ebook file too large. Max size is {MAX_FILE_SIZE_MB} MB."
        )

