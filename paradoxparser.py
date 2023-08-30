import os


COUNTS_AS_DATA = "-._"


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


def get_data(filePath: str, verifyData = True):
    fileHandler = open(filePath, "r")
    fileContent = fileHandler.read() + "\n"
    fileHandler.close()
    aa = parse_content(fileContent)
    if verifyData:
        verify_data(aa, filePath)
    return aa


def parse_content(content: str):
    aa = None
    contentIndex = 0
    key = ""
    string = ""
    while contentIndex < len(content):
        character = content[contentIndex]
        contentIndex += 1
        if character in '\t"':
            continue
        elif character == "\n":
            aa = process_newline(aa, key, string)
            key = ""
            string = ""
        elif character == " ":
            process_space()
        elif character == "#":
            contentIndex += content[contentIndex:].index("\n")
        elif character in "=<>":
            key = string
            string = ""
        elif character == "{":
            value, offset = parse_content(content[contentIndex:])
            aa = process_key_value_pair(aa, key, value)
            contentIndex += offset
            key = ""
            string = ""
        elif character == "}":
            #aa = process_closed_bracket(aa, key, string)
            aa = process_newline(aa, key, string)
            return aa, contentIndex
        elif character.isalnum() or character in COUNTS_AS_DATA:
            string += character
        else:
            raise Exception("found unhandled character: %c" % character)
    return aa


# def process_closed_bracket(aa, key: str, string: str):
#     if key == "" and string == "":
#         return aa
#     elif string.isnumeric():
#         return {key: int(string)}
#     return {key: string}


def process_closed_bracket(aa, key: str, string: str):
    if key == "" and string == "":
        return aa
    value = attempt_string_conversion(string)
    if key == "":
        return value
    return {key: value}


def process_key_value_pair(aa, key: str, value):
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


def process_newline(aa, key: str, string: str):
    if key == "" and string == "":
        return aa
    value = attempt_string_conversion(string)
    if key != "":
        return process_key_value_pair(aa, key, value)
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


def process_space():
    pass


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
    print(get_data("test.txt"))
