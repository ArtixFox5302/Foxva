import os.path


class Foxva:
    def __init__(self, minecraft_version, name):
        self.minecraft_version = minecraft_version
        self.name = name
        self.blocks = {}

    def block(self, block_name:str, strength:int, sound:str):
        self.blocks[block_name] = {
            "strength": strength,
            "sound": sound
        }


    def build(self):
        available_minecraft_versions = [26.2]
        for x in available_minecraft_versions:
            if x == self.minecraft_version:
                print("Selected Minecraft version has an available template")
            else:
                print("Foxva doesn't support the selected Minecraft version yet")
                exit()
        builds_folder = os.path.expanduser('~/Documents/FoxvaBuilds')
        if os.path.isdir(builds_folder):
            print("User has a builds folder")
        else:
            os.mkdir(builds_folder)
            print("Made builds folder")
        print("Moving onto templates")
        templates_folder = os.path.expanduser('~/Documents/FoxvaTemplates')
        template = os.path.expanduser(f'~/Documents/FoxvaTemplates/{self.minecraft_version}')
        if os.path.isdir(templates_folder):
            if os.path.isdir(template):
                print("User has the correct template")
            else:
                print("User doesn't have the correct template")
                exit()
        else:
            print("User doesn't have templates put in. Foxva has created a folder go to the Github and put in the templates from the Foxva templates folder inside of the Github repository.")
            os.mkdir(templates_folder)
            exit()

        
