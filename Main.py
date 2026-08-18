import subprocess
from datetime import date
import os.path
import random
import shutil

import sys
from PIL import Image


class Foxva:
    def __init__(self, minecraft_version:str, name:str):
        self.minecraft_version = minecraft_version
        self.name = name
        self.blocks = {}
        self.items = []

    def block(self, block_name:str, strength:int, sound:str):
        self.blocks[block_name] = {
            "strength": strength,
            "sound": sound
        }

    def item(self, item_name:str, texture:os.PathLike):
        self.items.append(item_name)
        self.texture = texture


    def build(self):

        def is_image(givenFile):
            try:
                with Image.open(givenFile) as img:
                    img.verify()
                    return True
            except (IOError, SyntaxError):
                return False

        available_minecraft_versions = ["26.2"]
        for x in available_minecraft_versions:
            if x == self.minecraft_version:
                print("Selected Minecraft version has an available template")
            else:
                print("Foxva doesn't support the selected Minecraft version yet")
                sys.exit()
        builds_folder = os.path.expanduser('~/Documents/FoxvaBuilds')
        if os.path.isdir(builds_folder):
            print("User has a builds folder")
        else:
            os.mkdir(builds_folder)
            print("Made builds folder")
        print("Moving onto templates")
        templates_folder = os.path.expanduser('~/Documents/FoxvaTemplates')
        templates_utils_folder = os.path.expanduser('~/Documents/FoxvaTemplates/utils')
        template = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}')
        if os.path.isdir(templates_folder):
            if os.path.isdir(template):
                print("User has the correct template")
            else:
                print("User doesn't have the correct template")
                sys.exit()
        else:
            print("User doesn't have templates put in. Foxva has created a folder go to the Github and put in the templates from the Foxva templates folder inside of the Github repository.")
            os.mkdir(templates_folder)
            os.mkdir(templates_utils_folder)
            sys.exit()
        blocks_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/block/ModBlocks.java')
        with open(blocks_file, 'r') as file:
            mod_blocks_file = file.read()

        for name, details in self.blocks.items():
            strength = details["strength"]
            sound = details["sound"]
            register_block_format = f'public static final Block {name.upper()} = registerBlock("{name.lower()}", properties -> new Block(properties.strength({strength}f).requiresCorrectToolForDrops().sound(SoundType.{sound})));'
            mod_blocks_file = mod_blocks_file.replace("    //FoxvaBlockMarker", f"    //FoxvaBlockMarker\n    {register_block_format}")
            language_format = f'"item.template_26_2.{name.lower()}"'
            print(mod_blocks_file)

        language_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/resources/assets/template_26_2/lang/en_us.json')
        items_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/item/ModItems.java')
        data_gen_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/datagen/ModModelProvider.java')
        with open(items_file, 'r') as file:
            mod_items_file = file.read()

        with open(language_file, 'r') as f:
            mod_language_file = f.read()

        with open(data_gen_file, 'r') as f:
            data_gen = f.read()

        item_list_size = len(self.items)
        rotations = 0
        for x in self.items:
            register_item_format = f'public static final Item {x.upper()} = registerItem("{x.lower()}", Item::new);'
            output_accept = f"output.accept({x.upper()});"
            language_format = f'"item.template_26_2.{x.lower()}": "{x}",'
            language_format_end = f'"item.template_26_2.{x.lower()}": "{x}"'
            data_gen_format = f'itemModelGenerators.generateFlatItem(ModItems.{x.upper()}, ModelTemplates.FLAT_ITEM);'
            data_gen = data_gen.replace("        //FoxvaDatagenMarker", f"        //FoxvaDatagenMarker\n        {data_gen_format}")
            mod_items_file = mod_items_file.replace("   //FoxvaMarker Item", f"   //FoxvaMarker Item\n    {register_item_format}")
            mod_items_file = mod_items_file.replace("   //FoxvaMarker.accept", f"    //FoxvaMarker.accept\n              {output_accept}")
            if item_list_size -1 == rotations:
                mod_language_file = mod_language_file.replace("  //FoxvaMarkerJson", f"  //FoxvaMarkerJson\n  {language_format}")
            else:
                mod_language_file = mod_language_file.replace("  //FoxvaMarkerJson", f"  //FoxvaMarkerJson\n  {language_format_end}")
            rotations += 1

        mod_language_file = mod_language_file.replace("  //FoxvaMarkerJson","")
        data_gen = data_gen.replace("        //FoxvaDatagenMarker","")

        des = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy')
        shutil.copytree(template, des)
        new_item_file = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/java/net/foxva/template/item/ModItems.java')
        new_language_file = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/lang/en_us.json')
        new_data_gen = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/java/net/foxva/template/datagen/ModModelProvider.java')

        with open(new_item_file, "w") as file:
            file.write(mod_items_file)

        with open(new_language_file, "w") as file:
            file.write(mod_language_file)

        with open(new_data_gen, "w") as f:
            f.write(data_gen)

        print("Building DataGen...")
        result = subprocess.run(["./gradlew", "runDatagen"], cwd=des, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Datagen failed: {result.stderr}")
            shutil.rmtree(des)
            sys.exit()

        for x in self.items:
            item_texture_des = os.path.expanduser(f'~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/textures/item/{x.lower()}.png')
            if not is_image(self.texture):
                print("Not a valid image or path")
                sys.exit()
            shutil.copyfile(self.texture, item_texture_des)

        folder_id_phase1 = random.randint(5,999)
        folder_id_phase2 = random.randint(0, folder_id_phase1)
        today = date.today()

        final_build = os.path.expanduser(f'~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}|{folder_id_phase2}_{today}')
        shutil.copytree(des, final_build)

        shutil.rmtree(des)

        print("Build successful")
