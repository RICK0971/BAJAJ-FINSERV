# utils.py
import re
from typing import Union

def is_out_of_range(value_str: Union[str, float], range_str: str) -> bool:
    try:
        value = float(value_str) if isinstance(value_str, str) else value_str
        parts = re.findall(r"\d+\.?\d*", range_str)
        if len(parts) == 2:
            low, high = map(float, parts)
            return value < low or value > high
    except (ValueError, TypeError):
        return False
    return False