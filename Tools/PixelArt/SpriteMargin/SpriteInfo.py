class SpriteInfo():
    def __init__(self, name: str, x: int, y: int, width: int, height: int, margin = 0):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = margin
    
    def overlaps(self, other: 'SpriteInfo') -> bool:
        return (self.x - self.margin < other.x + other.width + other.margin and
                self.x + self.width + self.margin > other.x - other.margin and
                self.y - self.margin < other.y + other.height + other.margin and
                self.y + self.height + self.margin > other.y - other.margin)
    
    def get_overlap_x(self, other: 'SpriteInfo') -> int:
        min_x = self.x - self.margin
        min_w = self.width + self.margin * 2
        max_x = other.x - other.margin
        max_w = other.width + other.margin * 2

        return min_x + min_w - max_x
    
    def get_overlap_y(self, other: 'SpriteInfo') -> int:
        min_y = self.y - self.margin
        min_h = self.height + self.margin * 2
        max_y = other.y - other.margin
        max_h = other.height + other.margin * 2

        return min_y + min_h - max_y

    def __copy__(self):
        return SpriteInfo(self.name, self.x, self.y, self.width, self.height)
    
    def __str__(self) -> str:
        return ('{{ "name": "{name}",'
                '"x": {x},'
                '"y": {y},'
                '"width": {width},'
                '"height": {height} }}').format(**self.__dict__)
    
    def __repr__(self) -> str:
        return str(self)

def compare_sprites_increasing(lhv: SpriteInfo, rhv: SpriteInfo) -> int:
    if lhv.x < rhv.x:
        return -1
    elif lhv.x > rhv.x:
        return 1
    elif lhv.y < rhv.y:
        return -1
    elif lhv.y > rhv.y:
        return 1
    else:
        return 0

def compare_sprites_decreasing(lhv: SpriteInfo, rhv: SpriteInfo) -> int:
    return compare_sprites_increasing(rhv, lhv)