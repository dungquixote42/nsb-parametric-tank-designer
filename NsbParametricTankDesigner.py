import copy
import os
import paradoxparser as pp


ARCHETYPE_IDENTIFIER = "archetype"

KEEP_ARCHETYPE = ["inherit"]

PARENT_KEY_LAND_UPGRADES = "upgrades"
PARENT_KEY_TANK_CHASSIS = "equipments"
PARENT_KEY_TANK_MODULES = "equipment_modules"
PARENT_KEY_TECHNOLOGY_GROUPS = "technologies"

PATH_LAND_UPGRADES = os.path.join("upgrades@", "land_upgrades.txt")
PATH_TANK_CHASSIS = os.path.join("equipment@", "tank_chassis.txt")
PATH_TANK_MODULES = os.path.join("modules@", "00_tank_modules.txt")
PATH_TECHNOLOGY_GROUPS = "technologies@"


class NsbParametricTankDesigner:
    def __init__(self):
        self.Tanks = []
        self.landUpgrades = pp.get_data(PATH_LAND_UPGRADES)[PARENT_KEY_LAND_UPGRADES]
        self.tankChassis = pp.get_data(PATH_TANK_CHASSIS)[PARENT_KEY_TANK_CHASSIS]
        self.tankModules = pp.get_data(PATH_TANK_MODULES)[PARENT_KEY_TANK_MODULES]
        self.tankTemplates = {}
        self.technologies = []
        self.validTechnologies = {}
        self.fetch_valid_technologies()
        self.generate_tank_templates()

    def add_technology(self, technology: str):
        if technology not in self.validTechnologies:
            raise Exception("invalid technology")
        if technology in self.technologies:
            raise Exception("already researched")
        self.technologies.append(technology)

    def remove_technology(self, technology: str):
        self.technologies.remove(technology)

    def reset_technologies(self):
        self.technologies = []

    def fetch_valid_technologies(self):
        self.technologyGroups = {}
        for fileName in os.listdir(PATH_TECHNOLOGY_GROUPS):
            filePath = os.path.join(PATH_TECHNOLOGY_GROUPS, fileName)
            self.technologyGroups[fileName[:-4]] = pp.get_data(filePath)
        for technologyGroup in self.technologyGroups:
            self.validTechnologies[technologyGroup] = self.technologyGroups[
                technologyGroup
            ][PARENT_KEY_TECHNOLOGY_GROUPS]

    def generate_tank_template(self, tankName: str, tankData: dict, archetype: dict):
        self.tankTemplates[tankName] = copy.deepcopy(archetype)
        for key in tankData:
            if tankData[key] not in KEEP_ARCHETYPE:
                self.tankTemplates[tankName][key] = tankData[key]

    def generate_tank_templates(self):
        for tankName in self.tankChassis:
            tankData = self.tankChassis[tankName]
            if ARCHETYPE_IDENTIFIER in tankData:
                archetype = self.tankChassis[tankData[ARCHETYPE_IDENTIFIER]]
                self.generate_tank_template(tankName, tankData, archetype)


class Tank:
    def __init__(self, template: dict):
        self.statistics = copy.deepcopy(template)


if __name__ == "__main__":
    tankDesigner = NsbParametricTankDesigner()
    # print(tankDesigner.validTechnologies["NSB_armor"]["gwtank_chassis"])
    for key in tankDesigner.validTechnologies:
        print(key)

    # tankDesigner.add_technology("gwtank_chassis")
    # print(tankDesigner.validTechnologies)
    # print(tankDesigner.technologies)

    # landUpgrades = os.path.join("upgrades@", "land_upgrades.txt")
    # landUpgrades = pp.get_data(landUpgrades)

    # tankChassis = os.path.join("equipment@", "tank_chassis.txt")
    # tankChassis = pp.get_data(tankChassis)

    # tankModules = os.path.join("modules@", "00_tank_modules.txt")
    # tankModules = pp.get_data(tankModules)

    # technologyGroups = {}
    # for fileName in os.listdir("technologies@"):
    #     filePath = os.path.join("technologies@", fileName)
    #     technologyGroups[fileName[:-4]] = pp.get_data(filePath)

    # pp.save_as_json("json", landUpgrades, "upgrades")
    # pp.save_as_json("json", tankModules, "equipment_modules")

    # pp.save_as_json("json", tankDesigner.tankTemplates, "light_tank_chassis_0")
    # pp.save_as_json(tankChassis["equipments"], "light_tank_chassis_0")

    # shipHullCarrier = os.path.join("equipment@", "ship_hull_carrier.txt")
    # shipHullCarrier = pp.get_data(shipHullCarrier, True)
    # print(shipHullCarrier)

    # electronicMechanicalEngineering = os.path.join("technologies@", "electronic_mechanical_engineering.txt")
    # electronicMechanicalEngineering = pp.get_data(electronicMechanicalEngineering, True)
    # print(electronicMechanicalEngineering)
