import os

DIRECTORIES = ["equipment@", "modules@", "technologies@", "upgrades@"]


def get_data(fileName: str):
    aaReturn = None
    foundFile = False
    for directory in DIRECTORIES:
        if fileName in os.listdir(directory):
            if not foundFile:
                fileHandler = open(os.path.join(directory, fileName), "r")
                fileContent = fileHandler.read() + "\n"
                fileHandler.close()
                aaReturn = parse_content(fileContent)
                foundFile = True
            else:
                raise Exception("found more than one files")
    if foundFile:
        return aaReturn
    raise Exception("did not find file")


def parse_content(content: str):
    aaReturn = None
    contentIndex = 0
    contentLength = len(content) - 1
    key = ""
    string = ""
    while True:
        if contentIndex > contentLength:
            break
        character = content[contentIndex]
        contentIndex += 1
        if character in "\t ":
            continue
        elif character == "\n":
            aaReturn = process_newline(aaReturn, key, string)
            key = ""
            string = ""
        elif character == "#":
            contentIndex += process_comment(content[contentIndex:])
        elif character in "=<>":
            key = string
            string = ""
        elif character == "{":
            data, offset = parse_content(content[contentIndex:])
            contentIndex += offset
            aaReturn = process_open_bracket(aaReturn, key, data)
            key = ""
            string = ""
        elif character == "}":
            aaReturn = process_closed_bracket(aaReturn, key, string)
            return aaReturn, contentIndex
        else:
            string += character
    return aaReturn


def process_closed_bracket(aaReturn, key: str, string: str):
    if key == "" and string == "":
        return aaReturn
    else:
        return {key: string}


def process_comment(content: str):
    for index in range(0, len(content)):
        if content[index] == "\n":
            return index
    return None


def process_newline(aaReturn, key: str, string: str):
    if key == "" and string == "":
        return aaReturn
    elif key == "":
        if aaReturn == None:
            return [string]
        elif type(aaReturn) == dict:
            if "noKey" in aaReturn:
                aaReturn["noKey"] += [string]
                return aaReturn
            else:
                aaReturn["noKey"] = [string]
                return aaReturn
        return aaReturn + [string]
    else:
        if aaReturn == None:
            return {key: string}
        elif key not in aaReturn:
            aaReturn[key] = string
            return aaReturn
        suffix = 1
        while (key + str(suffix)) in aaReturn:
            suffix += 1
        aaReturn[key + str(suffix)] = string
        return aaReturn


def process_open_bracket(aaReturn, key: str, data: dict):
    if aaReturn == None:
        return {key: data}
    elif key not in aaReturn:
        aaReturn[key] = data
        return aaReturn
    suffix = 1
    while (key + str(suffix)) in aaReturn:
        suffix += 1
    aaReturn[key + str(suffix)] = data
    return aaReturn


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
