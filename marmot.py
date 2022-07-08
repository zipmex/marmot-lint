import os, os.path
import sys

def get_module_name(path_from_root):
    with open(path_from_root) as f:
        first_line = f.readline()
        if first_line.find('defmodule') != -1:
            modules_path = first_line.split(" ")[1]
            module_name = modules_path.split(".")[-1]
            return module_name
        else:
            return "not module"

def check_format(root, file_name, module_name, errors):
    formatted_str = file_name.title().replace("_", "").split(".")
    if len(formatted_str) != 2:
        errors["errors"].append("Invalid file extension for {}".format(file_name))
        return

    formatted_file_name = formatted_str[0]

    file_name_token = file_name.split(".")
    extension = file_name_token[1]
    dir_extension_expectaion = {"lib": "ex", "test": "exs"}
    root_dir = root.split("/")[0]
    if dir_extension_expectaion[root_dir] != extension:
        errors["warnings"].append("Invalid file extension expecting {} for directory {} file {}"
        .format(dir_extension_expectaion[root_dir], root_dir, file_name))
        return

    if formatted_file_name != module_name:
        errors["warnings"].append("Naming is not in proper format between {} and {}".format(file_name, module_name))

    all_ch_in_lower = "".join(file_name_token[0].split("_"))
    if all_ch_in_lower != module_name.lower():
        errors["errors"].append("Naming is inconsistent between {} and {}".format(file_name, module_name))
        return
    
    if root_dir == "test" and file_name_token[0].split("_")[-1] != "test":
        errors["errors"].append("File in test directory should have the name test eg. x_test.exs instead of {}".format(file_name))
        return 

def lint(dir_list, excludes):
    result = {"errors": [], "warnings": []}
    for dir in dir_list:
        for root, _, files in os.walk(dir):
            if root in excludes:
                continue
            for file in files:
                full_path = os.path.join(root, file)
                module_name = get_module_name(full_path)
                if module_name != "not module":
                    check_format(root, file, module_name, result)
                    
    for warning in result["warnings"]:
        print("[Warning]", warning)

    if result["errors"] != []:
        for e in result["errors"]:
            print("[Errors]", e)
        sys.exit("[Linter] Some of you file is formatted incorrectly see log")


if __name__ == '__main__':
    lint(["lib", "test"], ["test/support"])