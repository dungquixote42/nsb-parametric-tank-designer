import os


class ParadoxParser:
    def __init__(self):
        self.files = []
        self.contents = {}
        self.database = {}

    def add_all_files_and_contents(self, directory: str):
        for fileName in os.listdir(directory):
            if fileName[-4:] != ".txt":
                continue
            fileHandler = open(os.path.join(directory, fileName), "r")
            fileContent = fileHandler.read()
            fileHandler.close()
            fileName = fileName[:-4]
            self.files.append(fileName)
            self.contents[fileName] = fileContent + "\n"

    def parse_all_contents(self):
        for contentKey in self.contents:
            content = self.contents[contentKey]
            self.database[contentKey] = self.parse_content(content)

    def parse_content(self, content: str):
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
                aaReturn = self.process_newline(aaReturn, key, string)
                key = ""
                string = ""
            elif character == "#":
                contentIndex += self.process_comment(content[contentIndex:])
            elif character in "=<>":
                key = string
                string = ""
            elif character == "{":
                data, offset = self.parse_content(content[contentIndex:])
                contentIndex += offset
                aaReturn = self.process_open_bracket(aaReturn, key, data)
                key = ""
                string = ""
            elif character == "}":
                aaReturn = self.process_closed_bracket(aaReturn, key, string)
                return aaReturn, contentIndex
            else:
                string += character
        return aaReturn

    def process_closed_bracket(self, aaReturn, key: str, string: str):
        if key == "" and string == "":
            return aaReturn
        else:
            return {key: string}

    def process_comment(self, content: str):
        for index in range(0, len(content)):
            if content[index] == "\n":
                return index
        return None

    def process_newline(self, aaReturn, key: str, string: str):
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

    def process_open_bracket(self, aaReturn, key: str, data):
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

    def verify_database(self, database: dict):
        for key in database:
            if key == None or key == "":
                raise ValueError
            if type(database[key]) == dict:
                self.verify_database(database[key])
            elif type(database[key]) == list:
                self.verify_entries(database[key])
            else:
                self.verify_entry(database[key])

    def verify_entry(self, entry):
        if entry == None or entry == "":
            raise ValueError

    def verify_entries(self, entries: list):
        for i in range(0, len(entries)):
            if entries[i] == None or entries[i] == "":
                raise ValueError


if __name__ == "__main__":
    pp = ParadoxParser()
