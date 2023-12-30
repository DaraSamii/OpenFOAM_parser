import re

def openFoamParser(file_path):
    # Read the content of the file
    with open(file_path, "r") as file:
        text = file.read()

    # Remove comments starting with //
    text = re.sub(r'//.*', '', text)

    # Extract functions block
    func_pattern = re.compile(r'functions\s*{([^}]*)}', re.DOTALL)
    func_matches = func_pattern.findall(text)
    func_dict = {"functions": func_matches}
    text = re.sub(func_pattern, '', text)

    # Extract blocks with names and contents
    pattern = re.compile(r'\s*([^\s{]+)\s*{([^{}]*)}', re.DOTALL)
    matches = pattern.findall(text)
    raw_dict = {name: content.strip() for name, content in matches}

    # Process the contents of each block
    for key, value in raw_dict.items():
        semi_splited = value.split(";")
        semi_splited = [s.strip() for s in semi_splited if s.strip()]  # Remove empty strings
        result_dict = {pair.split()[0]: pair.split()[1:] for pair in semi_splited}
        for i, j in result_dict.items():
            if len(j) == 1:
                result_dict[i] = j[0]

        raw_dict[key] = result_dict

    # Remove blocks with single-word keys and semicolons
    new_text = re.sub(pattern, '', text)

    # Extract blocks with two-word keys and semicolons
    pattern1 = re.compile(r'(\w+)\s+(\w+);', re.DOTALL)
    matches1 = pattern1.findall(new_text)
    raw_dict1 = {name: content.strip() for name, content in matches1}

    # Merge dictionaries
    merged_dict = {**raw_dict, **raw_dict1, **func_dict}

    if merged_dict['functions'] == []:
        merged_dict.pop('functions')
    return merged_dict


def openfoam_file_maker(dictionary,ind=1):
    result = ""
    I = "    "
    for key, value in dictionary.items():
        if isinstance(value, dict):
            # Handle nested dictionaries
            result += f"{key}\n"
            result += f"{{\n"
            result += openfoam_file_maker(value,ind = ind+1)
            result += f"}}\n\n"
            result += "//{}\n".format("-"*90)
        elif isinstance(value, list):
            # Handle lists
            result += "{}{:<40}".format(I*ind,key)
            listing = ""
            for item in value:
                listing += "  {}".format(item)
            result += " {:>40};\n".format(listing)
        else:
            # Handle other types
            result += "{}{:<40} {:>40};\n".format(I*ind, key, value)

    return result

def openfoam_file_witer(dictionary, file_path):
    text = openfoam_file_maker(dictionary)
    with open(file_path,"w") as file:
        file.write(text)
    return text