import copy
from PIL import Image
from functools import cmp_to_key
from .SpriteInfo import SpriteInfo as si
from .SpriteInfo import compare_sprites_increasing as compare_increasing
from .SpriteInfo import compare_sprites_decreasing as compare_decreasing

class BaseEngineFixer:
    def __init__(self, atlas: str, sprites: list[si]):
        self._atlas = atlas
        self.__orig_sprites = sprites
        self.__prepareNewSprites()
    
    @property
    def atlas(self):
        return self._atlas
    
    @property
    def new_sprites(self):
        return self._new_sprites

    def fix(self):
        atlas = Image.open(self._atlas)
        oldW, oldH = atlas.size
        newW, newH = self.__calculate_new_image_size()
        width = max(oldW, newW)
        height = max(oldH, newH)
        cropped = atlas.crop((0, 0, width, height))
        atlas = atlas.resize((width, height))

        for x in range(0, width):
            for y in range(0, height):
                atlas.putpixel((x, y), (0, 0, 0, 0))

        pixel_map = atlas.load()

        orig_sprites = { s.name: s for s in self.__orig_sprites }
        new_sprites = self._new_sprites

        for s in new_sprites:
            orig_s = orig_sprites[s.name]

            for x in range(-1, s.width + 1):
                ox = max(0, min(x, s.width - 1))
                for y in range(-1, s.height + 1):
                    oy = max(0, min(y, s.height - 1))
                    pixel_map[x + s.x, newH - (y + s.y + 1)] = cropped.getpixel((orig_s.x + ox, oldH - (orig_s.y + oy + 1)))

        atlas.save(self._atlas)
    
    def __prepareNewSprites(self):
        newSprites = [copy.copy(s) for s in self.__orig_sprites.copy()]
        newSprites.sort(key=cmp_to_key(compare_increasing))
        BaseEngineFixer.__deleteOverlappingSprites(newSprites)
        BaseEngineFixer.__moveSprites(newSprites)
        newSprites.sort(key=cmp_to_key(compare_decreasing))
        self._new_sprites = newSprites
    
    def __calculate_new_image_size(self) -> tuple[int, int]:
        w = 0
        h = 0

        for s in self._new_sprites:
            w = max(w, s.x + s.width + 1)
            h = max(h, s.y + s.height + 1)
        
        return (w, h)

    def __deleteOverlappingSprites(sprites: list[si]):
        candidates: list[int] = []
        
        for i in range(len(sprites)):
            for j in range(i + 1, len(sprites)):
                if j in candidates:
                    continue

                if sprites[i].overlaps(sprites[j]):
                    candidates.append(j)
        
        candidates.sort(reverse=True)

        for c in candidates:
            del sprites[c]
    
    def __moveSprites(sprites: list[si]):
        for i in range(len(sprites)):
            sprites[i].x += 1
            sprites[i].y += 1
            sprites[i].margin = 1

            BaseEngineFixer.__move_overlapped_sprites(sprites, i)

            BaseEngineFixer.__move_overlapped_sprites(sprites, i)
    
    def __move_overlapped_sprites(sprites: list[si], current: int):
            overlaps_count = 1

            while overlaps_count > 0:
                overlaps_count = 0
                for i in range(0, len(sprites)):
                    for j in range(0, len(sprites)):
                        if j == i or current == j:
                            continue
                    
                        if sprites[i].overlaps(sprites[j]):
                            overlaps_count += 1

                            over_x = sprites[i].get_overlap_x(sprites[j])
                            over_y = sprites[i].get_overlap_y(sprites[j])

                            if over_x > over_y:
                                over_x = 0
                            elif over_y > over_x:
                                over_y = 0

                            sprites[j].x += over_x
                            sprites[j].y += over_y
