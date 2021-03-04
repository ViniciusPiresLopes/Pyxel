from vector import Vec2


def clamp(value, min_, max_):
    if value < min_:
        return min_
    if value > max_:
        return max_
    
    return value


def get_line_pixels(start_pos: Vec2, end_pos: Vec2) -> []:
    start_pos.x = round(start_pos.x)
    start_pos.y = round(start_pos.y)
    end_pos.x = round(end_pos.x)
    end_pos.y = round(end_pos.y)

    dist = Vec2(
        end_pos.x - start_pos.x,
        end_pos.y - start_pos.y
    )

    if abs(dist.x) > abs(dist.y):
        steps = abs(dist.x)
    else:
        steps = abs(dist.y)
    
    if steps == 0:
        return [start_pos.copy()]

    increment = Vec2(
        dist.x / (steps),
        dist.y / (steps)
    )

    pixels = []
    pos = start_pos.copy()
    for i in range(steps):
        pos.x += increment.x
        pos.y += increment.y
        pixels.append(Vec2(round(pos.x), round(pos.y)))
    
    return pixels
