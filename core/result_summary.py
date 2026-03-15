def summarize_pattern(patterns):
    total_stock = len(patterns)
    total_waste = 0
    total_used = 0

    for p in patterns:
        total_waste += p.remaining()
        total_used += p.used_length()

    efficiency = total_used / (total_used + total_waste)

    return {
        "total_used": total_stock,
        "total_waste": total_waste,
        "efficiency": efficiency
    }