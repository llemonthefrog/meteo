def parse_bme_values(vals):
    """
    Converts BME280 values (t, p, h) to float.
    Extracts only the digits, period, and signs.
    """
    def to_float(s):
        try:
            return float(s)
        except (ValueError, TypeError):
            pass

        out = []
        for ch in str(s):
            if ch.isdigit() or ch in ".-eE":
                out.append(ch)

        try:
            return float("".join(out))
        except:
            return float('nan')

    t, p, h = vals
    return to_float(t), to_float(p), to_float(h)
