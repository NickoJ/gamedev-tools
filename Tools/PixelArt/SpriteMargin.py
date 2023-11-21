import sys
from pathlib import Path
import io
import os
import argparse

from SpriteMargin.Base import BaseEngineFixer
from SpriteMargin.Unity import UnityFixer

__parentdir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(__parentdir))

from Engine import Engine

ARG_ATLAS_PATH = "atlas_path"
ARG_ATLAS_PATH_FULL = f"--{ARG_ATLAS_PATH}"
ARG_ENGINE = "engine"
ARG_ENGINE_PATH_FULL = f"--{ARG_ENGINE}"

def read_args() -> tuple[io.TextIOWrapper, Engine]:
    parser = argparse.ArgumentParser()
    parser.add_argument(ARG_ATLAS_PATH_FULL, help="Path to atlas that has to be fixed.", type=argparse.FileType("r"), required=True)
    parser.add_argument(ARG_ENGINE_PATH_FULL, help="Engine that you use.", type=Engine, required=True)

    args = vars(parser.parse_args())

    atlas = args[ARG_ATLAS_PATH]
    engine = args[ARG_ENGINE]

    return atlas, engine

def fix_atlas(atlas: str, engine: Engine):
    engineFixer: BaseEngineFixer 
    
    match engine:
        case Engine.Unity:
            engineFixer = UnityFixer(atlas)
        case _:
            engineFixer = None

    if engineFixer is None:
        raise Exception("Engine not supported.")
    
    engineFixer.fix()

if __name__ == '__main__':
    atlas, engine = read_args()

    atlasPath = os.path.abspath(atlas.name)

    fix_atlas(atlasPath, engine)