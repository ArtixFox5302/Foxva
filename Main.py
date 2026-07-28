import json
import os
import shutil
from pathlib import Path


class Mod:
    def __init__(self, mod_name, mod_version="1.0.0"):
        self.Mod_Name = mod_name
        self.Mod_Version = mod_version
        self.Blocks = []
        self.Items = []

    def block(self, hardness:int, resistance:int, needed_tool, sound:os.PathLike, texture:os.PathLike, glow:int, block_name:str):
        self.Blocks.append({"hardness":hardness,"resistance": resistance,"needed_tool": needed_tool,"sound": sound,"texture": texture,"glow": glow,"block_name": block_name})
        pass

    def item(self, item_texture:os.PathLike, item_id:str):
        self.Items.append({"item_texture":item_texture, "item_id":item_id})
        pass

    def build(self):
        template_name = f"{self.Mod_Name} {self.Mod_Version}"
        mod_name = self.Mod_Name

        script_dir = Path(__file__).resolve().parent
        parent_dir = script_dir.parent
        builds_folder = parent_dir / "Builds"

        source_template = "Foxva/template-folder"
        new_template = builds_folder / template_name

        shutil.copytree(source_template,new_template)

        mod_conf = new_template / "src" / "main" / "resources" / "fabric.mod.json"

        with open(mod_conf, "r") as file:
            data = json.load(file)

        mod_name_lower = mod_name.lower()
        mod_name_upper = mod_name.upper()

        data["id"] = mod_name_lower
        data["name"] = mod_name_upper
        data["version"] = self.Mod_Version

        with open(mod_conf, "w") as file:
            json.dump(data, file, indent=4)