import copy
import os
import paradoxparser as pp


KEEP_ARCHETYPE = ["inherit"]

PARENT_KEY_LAND_UPGRADES = "upgrades"
PARENT_KEY_TANK_CHASSIS = "equipments"
PARENT_KEY_TANK_MODULES = "equipment_modules"
PARENT_KEY_TECH_GROUPS = "technologies"

PATH_LAND_UPGRADES = os.path.join("upgrades@", "land_upgrades.txt")
PATH_TANK_CHASSIS = os.path.join("equipment@", "tank_chassis.txt")
PATH_TANK_MODULES = os.path.join("modules@", "00_tank_modules.txt")
PATH_TECH_GROUPS = "technologies@"

RELEVANT_CHASSIS_KEYS = ["enable_equipments"]
RELEVANT_MODULE_KEYS = ["enable_equipment_modules"]

TANK_ARCHETYPE_IDENTIFIER = "archetype"
TANK_CHASSIS_IDENTIFIER = "enable_equipments"
TANK_MODULE_IDENTIFIER = "enable_equipment_modules"


class NsbParametricTankDesigner:
    def __init__(self):
        self.Tanks = []
        self.landUpgrades = pp.get_data(PATH_LAND_UPGRADES)[PARENT_KEY_LAND_UPGRADES]
        self.requiredModules = {}
        self.tankChassis = pp.get_data(PATH_TANK_CHASSIS)[PARENT_KEY_TANK_CHASSIS]
        self.tankModules = pp.get_data(PATH_TANK_MODULES)[PARENT_KEY_TANK_MODULES]
        self.tankTemplates = {}
        self.techs = []
        self.validChassisTechs = {}
        self.validModuleTechs = {}
        self.fetch_valid_techs()
        self.generate_tank_templates()

    def add_tech(self, techName: str):
        if techName not in self.validModuleTechs:
            raise Exception("invalid tech")
        if techName in self.techs:
            raise Exception("already researched")
        self.techs.append(techName)

    def remove_tech(self, techName: str):
        self.techs.remove(techName)

    def reset_techs(self):
        self.techs = []

    def fetch_valid_techs(self):
        techGroups = {}
        for fileName in os.listdir(PATH_TECH_GROUPS):
            filePath = os.path.join(PATH_TECH_GROUPS, fileName)
            techGroups[fileName] = pp.get_data(filePath)[PARENT_KEY_TECH_GROUPS]
        for techGroupName, techName in [
            (techGroupName, techName)
            for techGroupName in techGroups
            for techName in techGroups[techGroupName]
        ]:
            tech = techGroups[techGroupName][techName]
            if TANK_CHASSIS_IDENTIFIER in tech and any(
                chassis in tech[TANK_CHASSIS_IDENTIFIER] for chassis in self.tankChassis
            ):
                self.validChassisTechs[techName] = tech[TANK_CHASSIS_IDENTIFIER]
            if TANK_MODULE_IDENTIFIER in tech and any(
                module in tech[TANK_MODULE_IDENTIFIER] for module in self.tankModules
            ):
                self.validModuleTechs[techName] = tech[TANK_MODULE_IDENTIFIER]

    def generate_tank_template(self, tankName: str, tankData: dict, archetype: dict):
        self.tankTemplates[tankName] = copy.deepcopy(archetype)
        for key in tankData:
            if tankData[key] not in KEEP_ARCHETYPE:
                self.tankTemplates[tankName][key] = tankData[key]

    def generate_tank_templates(self):
        for tankName in self.tankChassis:
            tankData = self.tankChassis[tankName]
            if TANK_ARCHETYPE_IDENTIFIER in tankData:
                archetype = self.tankChassis[tankData[TANK_ARCHETYPE_IDENTIFIER]]
                self.generate_tank_template(tankName, tankData, archetype)
                self.generate_required_modules(archetype)

    def generate_tanks(self):
        validChassis = []
        validModules = []
        for techName in self.techs:
            if techName in self.validChassisTechs:
                validChassis += self.validChassisTechs[techName]
            if techName in self.validModuleTechs:
                validModules += self.validModuleTechs[techName]
        for chassis in validChassis:
            tankStats = copy.deepcopy(self.tankTemplates[chassis])


        print(validChassis)
        print(validModules)

    def generate_required_modules(self, archetype: dict):
        for chassis in self.tankChassis:
            


class Tank:
    def __init__(self, template: dict):
        self.stats = copy.deepcopy(template)


if __name__ == "__main__":
    tankDesigner = NsbParametricTankDesigner()
    tankDesigner.add_tech("gwtank_chassis")
    tankDesigner.generate_tanks()
    for tT in tankDesigner.tankTemplates:
        print(tT)

    # print(tankDesigner.validTechs["NSB_armor"]["gwtank_chassis"])
    # print(tankDesigner.validChassisTechs)
    # print(tankDesigner.validModuleTechs)

    # tankDesigner.add_tech("gwtank_chassis")
    # print(tankDesigner.validTechs)
    # print(tankDesigner.techs)

    # landUpgrades = os.path.join("upgrades@", "land_upgrades.txt")
    # landUpgrades = pp.get_data(landUpgrades)

    # tankChassis = os.path.join("equipment@", "tank_chassis.txt")
    # tankChassis = pp.get_data(tankChassis)

    # tankModules = os.path.join("modules@", "00_tank_modules.txt")
    # tankModules = pp.get_data(tankModules)

    # techGroups = {}
    # for fileName in os.listdir("techs@"):
    #     filePath = os.path.join("techs@", fileName)
    #     techGroups[fileName[:-4]] = pp.get_data(filePath)

    # pp.save_as_json("json", landUpgrades, "upgrades")
    # pp.save_as_json("json", tankModules, "equipment_modules")

    # pp.save_as_json("json", tankDesigner.tankTemplates, "light_tank_chassis_0")
    # pp.save_as_json(tankChassis["equipments"], "light_tank_chassis_0")

    # shipHullCarrier = os.path.join("equipment@", "ship_hull_carrier.txt")
    # shipHullCarrier = pp.get_data(shipHullCarrier, True)
    # print(shipHullCarrier)

    # electronicMechanicalEngineering = os.path.join("techs@", "electronic_mechanical_engineering.txt")
    # electronicMechanicalEngineering = pp.get_data(electronicMechanicalEngineering, True)
    # print(electronicMechanicalEngineering)
