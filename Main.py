import subprocess
from datetime import datetime
import os.path
import random
import shutil

import sys
from os import mkdir
from time import strftime

from PIL import Image


class Foxva:
    def __init__(self, minecraft_version:str, name:str, flags:str = ""):
        self.minecraft_version = minecraft_version
        self.name = name
        self.flags = flags
        self.blocks = {}
        self.items = []
        self.foods = {}

    def block(self, block_name:str, strength:int, sound:str):
        self.blocks[block_name] = {
            "strength": strength,
            "sound": sound
        }

    def item(self, item_name:str, texture:os.PathLike):
        self.items.append(item_name)
        self.texture = texture

    def food(self, food_name:str, nutrition:float, saturation:float, consume_time:float, texture:os.PathLike):
        self.foods[food_name] = {
            "nutrition": nutrition,
            "saturation": saturation,
            "consume_time": consume_time,
            "texture": texture
        }

    def build(self):
        lang_entries = []

        def is_image(givenFile):
            try:
                with Image.open(givenFile) as img:
                    img.verify()
                    return True
            except (IOError, SyntaxError):
                return False

        def verbose(message):
            if "-v" in self.flags:
                print(message)

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
        verbose("Finding template language file")
        language_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/resources/assets/template_26_2/lang/en_us.json')
        verbose("Finding template item file")
        items_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/item/ModItems.java')
        verbose("Finding template food file")
        foods_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/food/ModFoods.java')
        verbose("Finding template data generation file")
        data_gen_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/datagen/ModModelProvider.java')
        verbose("Opening items file")
        with open(items_file, 'r') as file:
            mod_items_file = file.read()
        verbose("Opening food file")
        with open(foods_file, 'r') as f:
            mod_food_file = f.read()
        verbose("Opening language file")
        with open(language_file, 'r') as f:
            mod_language_file = f.read()
        verbose("Opening data generation file")
        with open(data_gen_file, 'r') as f:
            data_gen = f.read()

        verbose("Starting items")
        for x in self.items:
            verbose("Making formats")
            register_item_format = f'public static final Item {x.upper()} = registerItem("{x.lower()}", Item::new);'
            output_accept = f"output.accept({x.upper()});"
            language_format = f'"item.template_26_2.{x.lower()}": "{x}"'
            data_gen_format = f'itemModelGenerators.generateFlatItem(ModItems.{x.upper()}, ModelTemplates.FLAT_ITEM);'
            verbose("Developing data generation file")
            data_gen = data_gen.replace("        //FoxvaDatagenMarker", f"        //FoxvaDatagenMarker\n        {data_gen_format}")
            verbose("Developing item file")
            mod_items_file = mod_items_file.replace("   //FoxvaMarker Item", f"   //FoxvaMarker Item\n    {register_item_format}")
            mod_items_file = mod_items_file.replace("   //FoxvaMarker.accept", f"    //FoxvaMarker.accept\n            {output_accept}")
            verbose("Developing language file")
            lang_entries.append(language_format)
        verbose("Finished item development")
        verbose("Starting food")

        for food_name, details in self.foods.items():
            verbose("Getting food details")
            nutrition = details["nutrition"]
            saturation = details["saturation"]
            consume_time = details["consume_time"]
            if isinstance(nutrition, float):
                nutrition = f"{nutrition}f"
            if isinstance(saturation, float):
                saturation = f"{saturation}f"
            if isinstance(consume_time, float):
                consume_time = f"{consume_time}f"
            verbose("Making formats")
            food_properties_format = f'public static final FoodProperties {food_name.upper()} = new FoodProperties.Builder().nutrition({nutrition}).saturationModifier({saturation}).build();'
            food_consumable_format = f'public static final Consumable {food_name.upper()}_CONSUMABLE = Consumables.defaultFood().consumeSeconds({consume_time}).build();'
            add_item_format = f'public static final Item {food_name.upper()} = registerItem("{food_name.lower()}", properties -> new Item(properties.food(ModFoods.{food_name.upper()}, ModFoods.{food_name.upper()}_CONSUMABLE)));'
            add_lang_format = f'"item.template_26_2.{food_name.lower()}": "{food_name}"'
            item_accept_format = f'output.accept({food_name.upper()});'
            data_gen_format = f'itemModelGenerators.generateFlatItem(ModItems.{food_name.upper()}, ModelTemplates.FLAT_ITEM);'
            data_gen = data_gen.replace("        //FoxvaDatagenMarker",f"        //FoxvaDatagenMarker\n        {data_gen_format}")
            verbose("Developing language file")
            lang_entries.append(add_lang_format)
            verbose("Developing item file")
            mod_items_file = mod_items_file.replace("   //FoxvaMarker Item", f"   //FoxvaMarker Item\n    {add_item_format}")
            mod_items_file = mod_items_file.replace("             //FoxvaMarker.accept", f"             //FoxvaMarker.accept\n            {item_accept_format}")
            verbose("Developing food file")
            mod_food_file = mod_food_file.replace("    //FoxvaFoodPropertiesMarker", f"    //FoxvaFoodPropertiesMarker\n    {food_properties_format}")
            mod_food_file = mod_food_file.replace("    //FoxvaFoodConsumablesMarker",f"    //FoxvaFoodConsumablesMarker\n    {food_consumable_format}")
        verbose("Finished food development")
        verbose("Working on language file")
        if lang_entries:
            lang_block = ",\n  ".join(lang_entries)
            mod_language_file = mod_language_file.replace("  //FoxvaMarkerJson", f"  //FoxvaMarkerJson\n  {lang_block}")
        verbose("Getting rid of markers")
        mod_language_file = mod_language_file.replace("  //FoxvaMarkerJson","")
        mod_items_file = mod_items_file.replace("    //FoxvaMarker Item","")
        mod_items_file = mod_items_file.replace("             //FoxvaMarker.accept", "")
        mod_food_file = mod_food_file.replace("    //FoxvaFoodConsumablesMarker", "")
        mod_food_file = mod_food_file.replace("    //FoxvaFoodPropertiesMarker", "")
        data_gen = data_gen.replace("        //FoxvaDatagenMarker","")

        des = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy')
        shutil.copytree(template, des)
        new_item_file = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/java/net/foxva/template/item/ModItems.java')
        new_food_file = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/java/net/foxva/template/food/ModFoods.java')
        new_language_file = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/lang/en_us.json')
        new_data_gen = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/java/net/foxva/template/datagen/ModModelProvider.java')
        verbose("Starting writing to files")
        with open(new_item_file, "w") as file:
            file.write(mod_items_file)

        with open(new_language_file, "w") as file:
            file.write(mod_language_file)

        with open(new_food_file, "w") as file:
            file.write(mod_food_file)

        with open(new_data_gen, "w") as f:
            f.write(data_gen)
        verbose("Files written to")
        print("Building DataGen this may take a minute")
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
        verbose("Placing texture")
        for food_name, details in self.foods.items():
            texture = details["texture"]
            texture_des = os.path.expanduser(f'~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/textures/item/{food_name.lower()}.png')
            if is_image(texture):
                shutil.copyfile(texture, texture_des)
            else:
                print("Not a valid image")
                sys.exit()
        verbose("Creating final build folder")
        time = strftime("%Y-%m-%d %H-%M-%S")

        build_result = subprocess.run(["./gradlew", "build"], cwd=des, capture_output=True, text=True)
        if build_result.returncode != 0:
            print(f"Build failed: {result.stderr}")
            shutil.rmtree(des)
            sys.exit()
        build_location = os.path.expanduser("~/Documents/FoxvaTemplates/utils/template_copy/build/libs/26_2-template-1.0.0.jar")

        if "-s" in self.flags:
            mkdir(os.path.expanduser(f'~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}'))
            final_build = os.path.expanduser(f'~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}/source')
            shutil.copytree(des, final_build)
            shutil.copyfile(build_location, os.path.expanduser(f"~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}/26_2-template-1.0.0.jar"))
            shutil.rmtree(des)
        else:
            mkdir(os.path.expanduser(f'~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}'))
            shutil.copyfile(build_location, os.path.expanduser(f"~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}/26_2-template-1.0.0.jar"))
            shutil.rmtree(des)

        print("Foxva Build successful")
