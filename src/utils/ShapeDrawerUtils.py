from PIL import ImageDraw


def draw_rectangle(image, coords, outline, width, fill):
    draw = ImageDraw.Draw(image)
    draw.rectangle(coords, outline=outline, width=width, fill=fill)

    return image


def draw_triangle(image, coords, outline, width, fill):
    draw = ImageDraw.Draw(image)
    draw.polygon(coords, outline=outline, width=width, fill=fill)

    return image


def draw_circle(image, coords, outline, width, fill):
    draw = ImageDraw.Draw(image)
    draw.ellipse(coords, outline=outline, width=width, fill=fill)

    return image


def draw_line(image, coords, fill, width):
    draw = ImageDraw.Draw(image)
    draw.line(coords, fill=fill, width=width)

    return image


def write_text(image, text, coords, font, fill):
    draw = ImageDraw.Draw(image)
    draw.text(coords, text, font=font, fill=fill)

    return image


class ShapeDrawerUtils:
    def __init__(self):
        pass
