def serialize(x, y, z):
    # Shift the coordinates to avoid negative values
    x_shifted = x + (1 << 20)  # Shift by 2^20
    y_shifted = y + (1 << 20)
    z_shifted = z + (1 << 20)

    # Combine the shifted coordinates into a single value
    value = (x_shifted << 42) | (y_shifted << 21) | z_shifted
    return hex(value)


def deserialize(value):
    value = int(value, 16)

    # Extract the shifted coordinates from the single value
    x_shifted = (value >> 42) & ((1 << 21) - 1)
    y_shifted = (value >> 21) & ((1 << 21) - 1)
    z_shifted = value & ((1 << 21) - 1)

    # Shift the coordinates back to their original values
    x = x_shifted - (1 << 20)
    y = y_shifted - (1 << 20)
    z = z_shifted - (1 << 20)

    return f"{x}, {y}, {z}"
