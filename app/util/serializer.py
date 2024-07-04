def serialize(x, y, z):
    # Ensure the coordinates fit within 32 bits
    x &= 0xFFFFFFFF
    y &= 0xFFFFFFFF
    z &= 0xFFFFFFFF

    # Pack the coordinates into two 64-bit integers
    packed1 = (x | (y << 32)) & 0xFFFFFFFFFFFFFFFF
    packed2 = z & 0xFFFFFFFFFFFFFFFF

    # Obfuscate the packed values with XOR
    obfuscated1 = packed1 ^ SECRET_KEY
    obfuscated2 = packed2 ^ SECRET_KEY

    return obfuscated1, obfuscated2


def deserialize(obfuscated1, obfuscated2):
    # De-obfuscate the packed values with XOR
    packed1 = obfuscated1 ^ SECRET_KEY
    packed2 = obfuscated2 ^ SECRET_KEY

    # Unpack the coordinates
    x = packed1 & 0xFFFFFFFF
    y = (packed1 >> 32) & 0xFFFFFFFF
    z = packed2 & 0xFFFFFFFF

    return x, y, z
