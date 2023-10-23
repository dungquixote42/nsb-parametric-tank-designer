import json
import os


COUNTS_AS_DATA = "-.@_"


def attempt_string_conversion(string: str):
    isFloat = False
    for character in string:
        isMinus = character == "-"
        isNumber = character.isnumeric()
        isPeriod = character == "."
        if not isMinus and not isNumber and not isPeriod:
            return string
        elif isFloat and isPeriod:
            return string
        elif isPeriod:
            isFloat = True
    if isFloat:
        return float(string)
    return int(string)


def character_is_data(character: str):
    return character.isalnum() or character in COUNTS_AS_DATA


def commit_current_key_and_string(aa, key: str, string: str, substitutionTable: dict):
    if key == "" and string == "":
        return aa
    value = attempt_string_conversion(string)
    if key != "":
        return process_key_value_pair(aa, key, value, substitutionTable)
    elif aa == None:
        return value
    elif type(aa) == dict:
        if "_" not in aa:
            aa["_"] = value
        elif type(aa["_"]) == list:
            aa["_"] += [value]
        else:
            aa["_"] = [aa["_"]] + [value]
        return aa
    elif type(aa) == list:
        return aa + [value]
    else:
        return [aa] + [value]


def get_data(filePath: str, verifyData=True):
    fileHandler = open(filePath, "r")
    fileContent = fileHandler.read() + "\n"
    fileHandler.close()
    aa = parse_content(fileContent)
    if verifyData:
        verify_data(aa, filePath)
    return aa


def handle_space(content: str, contentIndex: int, inQuotes: bool):
    if inQuotes:
        return " ", " "
    elif space_is_delimiter(content, contentIndex):
        return "\n", ""
    return " ", ""


def space_is_delimiter(content: str, contentIndex: int):
    for character in content[contentIndex:]:
        if character == " ":
            continue
        elif character_is_data(character):
            break
        else:
            return False
    for character in content[:contentIndex][::-1]:
        if character == " ":
            continue
        elif character_is_data(character):
            return True
        else:
            return False
    return False


def parse_content(content: str, substitutionTable: dict = {}):
    aa = None
    contentIndex = 0
    inQuotes = False
    maxIndex = len(content) - 1
    key = ""
    string = ""
    while True:
        if contentIndex > maxIndex:
            break
        character = content[contentIndex]
        contentIndex += 1
        if character == " ":
            newCharacter, oldCharacter = handle_space(content, contentIndex, inQuotes)
            character = newCharacter
            string += oldCharacter
        if character in "\t ":
            continue
        elif character == "\n":
            aa = commit_current_key_and_string(aa, key, string, substitutionTable)
            key = ""
            string = ""
        elif character == '"':
            inQuotes = not inQuotes
        elif character == "#":
            contentIndex += content[contentIndex:].index("\n")
        elif character in "=<>":
            key = string
            string = ""
        elif character == "{":
            value, offset = parse_content(content[contentIndex:], substitutionTable)
            aa = process_key_value_pair(aa, key, value, substitutionTable)
            contentIndex += offset
            key = ""
            string = ""
        elif character == "}":
            aa = commit_current_key_and_string(aa, key, string, substitutionTable)
            return aa, contentIndex
        elif character_is_data(character):
            string += character
        else:
            raise Exception("found unhandled character: %c" % character)
    return aa


def process_key_value_pair(aa, key: str, value, substitutionTable: dict):
    if key[0] == "@":
        substitutionTable[key] = value
        return aa
    if type(value) == str and value[0] == "@":
        value = substitutionTable[value]
    if aa == None:
        return {key: value}
    elif key not in aa:
        aa[key] = value
        return aa
    suffix = 1
    while (key + str(suffix)) in aa:
        suffix += 1
    aa[key + str(suffix)] = value
    return aa


def save_as_json(data: dict, key: str, directory: str = "json"):
    fileHandler = open(os.path.join(directory, key + ".json"), "w")
    json.dump(data[key], fileHandler)
    fileHandler.close()


def test(directories: list):
    for directory, fileName in [(a, b) for a in directories for b in os.listdir(a)]:
        if fileName[-4:] == ".txt":
            get_data(os.path.join(directory, fileName))


def verify_data(data: dict, filePath: str):
    for key in data:
        if key == None or key == "":
            raise Exception("found empty key in %s" % filePath)
        if type(data[key]) == dict:
            verify_data(data[key], filePath)
        elif type(data[key]) == list:
            verify_elements(data[key])
        elif data == None or data == "":
            raise Exception("found empty data")


def verify_elements(elements: list):
    if None in elements or "" in elements:
        raise Exception("found empty element")


if __name__ == "__main__":
    data = get_data(os.path.join("technologies@", "NSB_armor.txt"))
    save_as_json(data["technologies"], "basic_light_tank_chassis")
