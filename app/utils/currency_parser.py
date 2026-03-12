def parse_inr(value) -> float:
    """
    Converts Indian currency notation into numeric rupees.

    Examples:
    50L  -> 5000000
    2Cr  -> 20000000
    10Cr -> 100000000
    """

    # If already numeric, return directly
    if isinstance(value, (int, float)):
        return float(value)

    value = value.strip().lower()

    if value.endswith("cr"):
        number = float(value[:-2])
        return number * 10000000

    if value.endswith("l"):
        number = float(value[:-1])
        return number * 100000

    return float(value)