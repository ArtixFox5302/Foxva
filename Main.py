import os.path


class Foxva:
    def __init__(self, version, name):
        self.version = version
        self.name = name

    def build(self):
        builds_folder = os.path.expanduser('~/Documents/FoxvaBuilds')
        if os.path.isdir(builds_folder):
            print("User has a builds folder")
        else:
            os.mkdir(builds_folder)
            print("Made builds folder")
        print("Moving onto templates")
        templates_folder = os.path.expanduser('~/Documents/FoxvaTemplates')
        if os.path.isdir(templates_folder):
            print("User has a templates folder. If it is just the folder and not the actual templates script will fail later.")
        else:
            print("User doesn't have templates put in. Foxva has created a folder go to the Github and put in the templates from the Foxva templates folder inside of the Github repository.")
            os.mkdir(templates_folder)
            exit()
