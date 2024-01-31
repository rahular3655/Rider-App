import os
from uuid import uuid4


def random_file_name(instance, filename):
    parts = filename.split("/")
    name, ext = os.path.splitext(parts.pop())
    parts.append(f"{uuid4()}{ext}")
    return "/".join(parts)