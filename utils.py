def is_valid_direction(d: str) -> bool:
    return d in ("Up", "Down", "Left", "Right")


def get_opposite_direction(d: str) -> str:
    match d:
        case "Up":
            return "Down"
        case "Down":
            return "Up"
        case "Left":
            return "Right"
        case "Right":
            return "Left"
        case _:
            return ""


def are_opposite_directions(d1: str, d2: str) -> bool:
    return get_opposite_direction(d1) == d2
