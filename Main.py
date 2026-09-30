import subprocess
import threading
import os.path
import shutil
import sys
from os import mkdir
from time import strftime
from PIL import Image
import platform
class Foxva:
    def __init__(self, minecraft_version:str, name:str, flags:str = ""):
        self.minecraft_version = minecraft_version
        self.name = name
        self.flags = flags
        self.blocks = {}
        self.items = {}
        self.foods = {}

    def block(self, block_name:str, strength:int, sound:str, texture:os.PathLike | str):
        self.blocks[block_name] = {
            "strength": strength,
            "sound": sound,
            "texture": texture
        }

    def item(self, item_name:str, texture:os.PathLike | str):
        self.items[item_name] = {
            "texture": texture
        }

    def food(self, food_name:str, nutrition:float, saturation:float, consume_time:float, texture:os.PathLike | str):
        self.foods[food_name] = {
            "nutrition": nutrition,
            "saturation": saturation,
            "consume_time": consume_time,
            "texture": texture
        }

    def build(self):
        lang_entries = []

        def is_image(given_file):
            try:
                with Image.open(given_file) as img:
                    img.verify()
                    return True
            except (IOError, SyntaxError):
                return False

        x = 0
        def b():
            import time
            bagels = 0
            while x != 1:
                bagels += 1
                print("BAGEL")
                time.sleep(0.0005)
            print(f"You ate {bagels} bagels while this code ran")

        des = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy')
        def shit(error):
            if os.path.isdir(des):
                shutil.rmtree(des)

            print(f"The following error has occurred: {error}")
            sys.exit()

        b_thread = threading.Thread(target=b, daemon=True)
        if "b" in self.flags:
            b_thread.start()

        available_minecraft_versions = ["26.2"]
        for x in available_minecraft_versions:
            if x == self.minecraft_version:
                print("Selected Minecraft version has an available template")
            else:
                shit("Invalid Minecraft version")
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
                shit("Incorrect template")
        else:
            os.mkdir(templates_folder)
            os.mkdir(templates_utils_folder)
            shit("User does not have the correct template")

        gradle_wrapper_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/gradle/wrapper/gradle-wrapper.properties.txt')
        gradle_properties_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/gradle.properties.txt')
        texture_folder = os.path.expanduser(f'~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/textures/item')
        item_folder = os.path.expanduser(f'~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/textures/item')
        block_folder = os.path.expanduser(f'~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/textures/block')
        print("Running template checks")
        if os.path.isfile(gradle_wrapper_file):
            print("Fixing file name mismatch")
            old_file_wrapper = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/gradle/wrapper/gradle-wrapper.properties.txt')
            new_file_wrapper = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/gradle/wrapper/gradle-wrapper.properties')
            os.rename(old_file_wrapper, new_file_wrapper)
        if os.path.isfile(gradle_properties_file):
            print("Fixing file name mismatch")
            old_file_properties = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/gradle.properties.txt')
            new_file_properties = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/gradle.properties')
            os.rename(old_file_properties,new_file_properties)

        blocks_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/block/ModBlocks.java')
        language_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/resources/assets/template_26_2/lang/en_us.json')
        items_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/item/ModItems.java')
        foods_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/food/ModFoods.java')
        data_gen_file = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}/src/main/java/net/foxva/template/datagen/ModModelProvider.java')
        with open(items_file, 'r') as file:
            mod_items_file = file.read()
        with open(foods_file, 'r') as f:
            mod_food_file = f.read()
        with open(blocks_file, 'r') as file:
            mod_blocks_file = file.read()
        with open(language_file, 'r') as f:
            mod_language_file = f.read()
        with open(data_gen_file, 'r') as f:
            data_gen = f.read()

        for item_name, details in self.items.items():
            new_name = item_name.replace(" ", "_")
            register_item_format = f'public static final Item {new_name.upper()} = registerItem("{new_name.lower()}", Item::new);'
            output_accept = f"output.accept({new_name.upper()});"
            language_format = f'"item.template_26_2.{new_name.lower()}": "{item_name}"'
            data_gen_format = f'itemModelGenerators.generateFlatItem(ModItems.{new_name.upper()}, ModelTemplates.FLAT_ITEM);'
            data_gen = data_gen.replace("        //FoxvaDatagenMarkerItem",f"        //FoxvaDatagenMarkerItem\n        {data_gen_format}")
            mod_items_file = mod_items_file.replace("    //FoxvaMarkerItem",f"    //FoxvaMarkerItem\n    {register_item_format}")
            mod_items_file = mod_items_file.replace("   //FoxvaMarker.accept",f"    //FoxvaMarker.accept\n            {output_accept}")
            lang_entries.append(language_format)


        for food_name, details in self.foods.items():
            nutrition = details["nutrition"]
            saturation = details["saturation"]
            consume_time = details["consume_time"]
            if isinstance(saturation, float):
                saturation = f"{saturation}f"
            if isinstance(consume_time, float):
                consume_time = f"{consume_time}f"
            new_name = food_name.replace(" ", "_")
            food_properties_format = f'public static final FoodProperties {new_name.upper()} = new FoodProperties.Builder().nutrition({nutrition}).saturationModifier({saturation}).build();'
            food_consumable_format = f'public static final Consumable {new_name.upper()}_CONSUMABLE = Consumables.defaultFood().consumeSeconds({consume_time}).build();'
            add_item_format = f'public static final Item {new_name.upper()} = registerItem("{new_name.lower()}", properties -> new Item(properties.food(ModFoods.{new_name.upper()}, ModFoods.{new_name.upper()}_CONSUMABLE)));'
            add_lang_format = f'"item.template_26_2.{new_name.lower()}": "{food_name}"'
            item_accept_format = f'output.accept({new_name.upper()});'
            data_gen_format = f'itemModelGenerators.generateFlatItem(ModItems.{new_name.upper()}, ModelTemplates.FLAT_ITEM);'
            data_gen = data_gen.replace("        //FoxvaDatagenMarkerItem",f"        //FoxvaDatagenMarkerItem\n        {data_gen_format}")
            lang_entries.append(add_lang_format)
            mod_items_file = mod_items_file.replace("    //FoxvaMarkerItem", f"    //FoxvaMarkerItem\n    {add_item_format}")
            mod_items_file = mod_items_file.replace("             //FoxvaMarker.accept", f"             //FoxvaMarker.accept\n            {item_accept_format}")
            mod_food_file = mod_food_file.replace("    //FoxvaFoodPropertiesMarker", f"    //FoxvaFoodPropertiesMarker\n    {food_properties_format}")
            mod_food_file = mod_food_file.replace("    //FoxvaFoodConsumablesMarker",f"    //FoxvaFoodConsumablesMarker\n    {food_consumable_format}")

        for block_name, details in self.blocks.items():
            strength = details["strength"]
            sound = details["sound"]
            new_name = block_name.replace(" ", "_")
            if isinstance(strength, float):
                strength = f"{strength}f"
            register_block_format = f'public static final Block {new_name.upper()} = registerBlock("{new_name.lower()}", properties -> new Block(properties.strength({strength}).requiresCorrectToolForDrops().sound(SoundType.{sound.upper()})));'
            block_datagen_format = f'blockModelGenerators.createTrivialCube(ModBlocks.{new_name.upper()});'
            block_lang_format = f'"block.template_26_2.{new_name.lower()}": "{block_name}"'
            mod_blocks_file = mod_blocks_file.replace("    //FoxvaMarker",f"    //FoxvaMarker\n    {register_block_format}")
            data_gen = data_gen.replace("        //FoxvaDatagenMarkerBlock",f"        //FoxvaDatagenMarkerBlock\n        {block_datagen_format}")
            lang_entries.append(block_lang_format)

        if lang_entries:
            lang_block = ",\n  ".join(lang_entries)
            mod_language_file = mod_language_file.replace("  //FoxvaMarkerJson", f"  //FoxvaMarkerJson\n  {lang_block}")
        mod_language_file = mod_language_file.replace("  //FoxvaMarkerJson","")
        mod_items_file = mod_items_file.replace("    //FoxvaMarker Item","")
        mod_items_file = mod_items_file.replace("             //FoxvaMarker.accept", "")
        mod_food_file = mod_food_file.replace("    //FoxvaFoodConsumablesMarker", "")
        mod_food_file = mod_food_file.replace("    //FoxvaFoodPropertiesMarker", "")
        mod_blocks_file = mod_blocks_file.replace("    //FoxvaMarker", "")
        data_gen = data_gen.replace("        //FoxvaDatagenMarkerItem","")
        data_gen = data_gen.replace("        //FoxvaDatagenMarkerBlock", "")

        shutil.copytree(template, des)
        new_item_file = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/java/net/foxva/template/item/ModItems.java')
        new_food_file = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/java/net/foxva/template/food/ModFoods.java')
        mew_block_file = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/java/net/foxva/template/block/ModBlocks.java')
        new_language_file = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/lang/en_us.json')
        new_data_gen = os.path.expanduser('~/Documents/FoxvaTemplates/utils/template_copy/src/main/java/net/foxva/template/datagen/ModModelProvider.java')
        with open(new_item_file, "w") as file:
            file.write(mod_items_file)

        with open(new_language_file, "w") as file:
            file.write(mod_language_file)

        with open(new_food_file, "w") as file:
            file.write(mod_food_file)

        with open(mew_block_file, "w") as file:
            file.write(mod_blocks_file)

        with open(new_data_gen, "w") as f:
            f.write(data_gen)

        if not os.path.isdir(texture_folder):
            mkdir(texture_folder)
        if not os.path.isdir(item_folder):
            mkdir(item_folder)
        if not os.path.isdir(block_folder):
            mkdir(block_folder)

        print("Building DataGen this may take a minute")
        os.chmod(os.path.join(des, "gradlew"), 0o755)
        if platform.system() == "Linux":
            result = subprocess.run(["./gradlew", "runDatagen"], cwd=des, capture_output=True, text=True)
        elif platform.system() == "Windows":
            result = subprocess.run(["gradlew.bat", "runDatagen"], cwd=des, capture_output=True, text=True, shell=True)
        else:
            shit("MacOS is not supported yet or could not detect OS")

        print(result.stdout)
        if result.returncode != 0:
            shit(f"Data gen failed {result.stderr}")

        for item_name, details in self.items.items():
            texture = details["texture"]
            suffix = texture.suffix
            new_name = item_name.replace(" ", "_")
            if not suffix == ".png":
                shit("Invalid image format, please use the PNG format")

            texture_des = os.path.expanduser(f'~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/textures/item/{new_name.lower()}.png')
            if is_image(texture):
                shutil.copyfile(texture, texture_des)

        for food_name, details in self.foods.items():
            texture = details["texture"]
            suffix = texture.suffix
            new_name = food_name.replace(" ", "_")
            if not suffix == ".png":
                shit("Invalid image format, please use the PNG format")

            texture_des = os.path.expanduser(f'~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/textures/item/{new_name.lower()}.png')
            if is_image(texture):
                shutil.copyfile(texture, texture_des)
            else:
                shit("Invalid image")

        for block_name, details in self.blocks.items():
            texture = details["texture"]
            suffix = texture.suffix
            new_name = block_name.replace(" ", "_")
            if not suffix == ".png":
                shit(f"Invalid image format, please use the PNG format")

            texture_des = os.path.expanduser(f'~/Documents/FoxvaTemplates/utils/template_copy/src/main/resources/assets/template_26_2/textures/block/{new_name.lower()}.png')
            if is_image(texture):
                shutil.copyfile(texture, texture_des)
            else:
                shit("Invalid image")

        time = strftime("%Y-%m-%d %H-%M-%S")

        def return_code(build_res):
            if build_res.returncode != 0:
                shit(f"Build failed: {build_res.stderr}")

        if platform.system() == "Linux":
            build_result = subprocess.run(["./gradlew", "build"], cwd=des, capture_output=True, text=True)
            return_code(build_result)
        elif platform.system() == "Windows":
            build_result = subprocess.run(["gradlew.bat", "build"], cwd=des, capture_output=True, text=True, shell=True)
            return_code(build_result)
        else:
            shit("MacOS is not supported yet or could not detect OS")
        build_location = os.path.expanduser("~/Documents/FoxvaTemplates/utils/template_copy/build/libs/26_2-template-1.0.0.jar")

        if "s" in self.flags:
            mkdir(os.path.expanduser(f'~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}'))
            final_build = os.path.expanduser(f'~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}/source')
            shutil.copytree(des, final_build)
            shutil.copyfile(build_location, os.path.expanduser(f"~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}/26_2-template-1.0.0.jar"))
            shutil.rmtree(des)
        else:
            mkdir(os.path.expanduser(f'~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}'))
            shutil.copyfile(build_location, os.path.expanduser(f"~/Documents/FoxvaBuilds/{self.name}_{self.minecraft_version}_{time}/26_2-template-1.0.0.jar"))
            shutil.rmtree(des)
        x = 1
        import time
        time.sleep(0.0005)
        print("Foxva Build successful")
