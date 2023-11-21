import yaml
import os

from .SpriteInfo import SpriteInfo
from .Base import BaseEngineFixer

class UnityFixer(BaseEngineFixer):
    def __init__(self, atlas: str):
        meta_data = self.__get_meta_file(atlas)
        sprites = self.__get_sprites(meta_data)
        super().__init__(atlas, sprites)

    def fix(self):
        super().fix()
        meta_data = self.__get_meta_file(super().atlas)  
        self.__replace_sprites(meta_data)
        with open(super().atlas + ".meta", "w") as yamlFile:
            yaml.safe_dump(meta_data,
                                  yamlFile,
                                  encoding="utf-8", 
                                  allow_unicode=True,
                                  sort_keys=False)

    def __get_meta_file(self, atlasPath: str) -> dict:
        yamlPath = atlasPath + ".meta"

        if not os.path.exists(yamlPath):
            raise Exception("No meta file found for the atlas.")

        with open(yamlPath, "r") as yamlFile:
            metaData = yaml.safe_load(yamlFile)
        
        return metaData

    def __get_sprites(self, metaData: dict) -> list[SpriteInfo]:
        spritesMeta = metaData["TextureImporter"]["spriteSheet"]["sprites"]
        sprites = [SpriteInfo(
            m["name"], 
            m["rect"]["x"], 
            m["rect"]["y"], 
            m["rect"]["width"], 
            m["rect"]["height"]) for m in spritesMeta]
        return sprites

    def __replace_sprites(self, metaData: dict):
        spritesMeta = metaData["TextureImporter"]["spriteSheet"]["sprites"]
        new_sprites = { s.name: s for s in super().new_sprites }
        remove = []
        for m in spritesMeta:
            if m["name"] not in new_sprites:
                remove.append(m)
                continue

            sprite = new_sprites[m["name"]]
            m["rect"]["x"] = sprite.x
            m["rect"]["y"] = sprite.y
            m["rect"]["width"] = sprite.width
            m["rect"]["height"] = sprite.height
        
        for r in remove:
            spritesMeta.remove(r)
