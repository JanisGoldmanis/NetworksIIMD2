import os


def get_year(folder):
    return folder[-4:]


def get_version(file_name):
    name = file_name.upper()
    if "IPV6" in name:
        return "IPv6"
    return "IPv4"


def get_files(folder):
    result = []
    for root, directories, files in os.walk(folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            parent_folder_name = os.path.basename(os.path.dirname(file_path))

            year = get_year(parent_folder_name)
            version = get_version(filename)

            file_info = {"name": filename, "year": year, "version": version, "path": file_path}
            result.append(file_info)
    return result


