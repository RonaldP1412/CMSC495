#Stores color values for every piece and background
class Color:

    bg = (3, 18, 33)
    cyan = (0,240,240)
    blue = (0,0,240)
    orange = (221,164,34)
    yellow = (241, 239, 47)
    green = (138,234,40)
    purple = (136,44,237)
    red = (207,54,22)

    @classmethod
    def get_color(cls):
        return [cls.bg,cls.cyan,cls.blue,cls.orange,cls.yellow,cls.green,cls.purple,cls.red]
