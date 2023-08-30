import ParadoxParser

DIRECTORIES = ["equipment@", "modules@", "technologies@", "upgrades@"]

if __name__ == "__main__":
    pp = ParadoxParser.ParadoxParser()
    
    for directory in DIRECTORIES:
        pp.add_all_files_and_contents(directory)
    pp.parse_all_contents()

    print(pp.files)
    for key in pp.contents:
        print(key)
        