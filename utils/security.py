import uuid

def generate_session_uuid() -> str:
    return str(uuid.uuid4())