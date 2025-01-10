def write_bytes(uri, bytes):
    """
    Write image bytes from different file systems
    """
    
    # Try luck with standard python file system
    with open(uri, mode="wb") as f:
        f.write(bytes)