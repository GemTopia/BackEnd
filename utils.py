def int_to_unique_string(num):
    """
    Hashes an integer and returns a unique string representation.
    """
    hash_val = hash(num+100000000)
    hex_str = hex(hash_val)[2:]  # Remove "0x" prefix
    return hex_str
