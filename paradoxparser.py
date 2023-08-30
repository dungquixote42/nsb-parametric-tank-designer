import os

DIRECTORIES = ["equipment@", "modules@", "technologies@", "upgrades@"]


def get_data(fileName: str, directories: list):
    aa = None
    fileIsFound = False
    for directory in directories:
        if fileName in os.listdir(directory):
            if fileIsFound:
                raise Exception("found more than one files")
            fileHandler = open(os.path.join(directory, fileName), "r")
            fileContent = fileHandler.read() + "\n"
            fileHandler.close()
            aa = parse_content(fileContent)
            fileIsFound = True
    if fileIsFound:
        return aa
    raise Exception("did not find file")


def parse_content(content: str):
    aa = None
    contentIndex = 0
    key = ""
    string = ""
    while contentIndex < len(content):
        character = content[contentIndex]
        contentIndex += 1
        if character in "\t \"":
            continue
        elif character == "\n":
            aa = process_newline(aa, key, string)
            key = ""
            string = ""
        elif character == "#":
            #contentIndex += process_comment(content[contentIndex:])
            contentIndex += content[contentIndex:].index("\n")
        elif character in "=<>":
            key = string
            string = ""
        elif character == "{":
            data, offset = parse_content(content[contentIndex:])
            contentIndex += offset
            aa = process_open_bracket(aa, key, data)
            key = ""
            string = ""
        elif character == "}":
            return process_closed_bracket(aa, key, string), contentIndex
        elif character.isalnum() or character in "._":
            string += character
        else:
            raise Exception("found unhandled character: %c" % character)
    return aa


def process_closed_bracket(aa, key: str, value: str):
    if key == "" and value == "":
        return aa
    elif value.isnumeric():
        return {key: int(value)}
    else:
        return {key: value}


def process_comment(content: str):
    for index in range(0, len(content)):
        if content[index] == "\n":
            return index
    raise Exception("did not find newline")


def process_newline(aa, key: str, value: str):
    if key == "" and value == "":
        return aa
    if value.isnumeric():
        value = int(value)
    if key == "":
        if aa == None:
            return [value]
        elif type(aa) == dict:
            if "noKey" in aa:
                aa["noKey"] += [value]
                return aa
            else:
                aa["noKey"] = [value]
                return aa
        return aa + [value]
    else:
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


def process_open_bracket(aa, key: str, data: dict):
    if aa == None:
        return {key: data}
    elif key not in aa:
        aa[key] = data
        return aa
    suffix = 1
    while (key + str(suffix)) in aa:
        suffix += 1
    aa[key + str(suffix)] = data
    return aa


def verify_data(data: dict):
    for key in data:
        if key == None or key == "":
            raise Exception("found empty key")
        if type(data[key]) == dict:
            verify_data(data[key])
        elif type(data[key]) == list:
            verify_elements(data[key])
        else:
            verify_value(data[key])


def verify_value(value):
    if value == None or value == "":
        raise Exception("found empty value")


def verify_elements(elements: list):
    for i in range(0, len(elements)):
        if elements[i] == None or elements[i] == "":
            raise Exception("found empty element")


if __name__ == "__main__":
    pass
