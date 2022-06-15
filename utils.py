def converter_bytes_para_gb(bytes: float) -> float:

    gb = bytes / 1024 / 1024 / 1024
    return round(gb, 2)