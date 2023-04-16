import os
import csv


def get_file_names(directory_path):
    """
    USED!
    Gets all files in a directory
    :param directory_path:
    :return:
    """
    filename_list = []
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            # if filename[-3:] == "pdf":
            filename_list.append(filename)

    return filename_list


directory = r'C:\Users\janis.goldmanis\Downloads\RESULTS'
file_names = get_file_names(directory)

result = [["AS"]]
AS_Set = set()


for file_name in file_names:
    result[0].append(file_name)
    print(file_name)
    file_path = os.path.join(directory, file_name)
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        data = list(reader)
    for line in data:
        # print(line)
        if line[0] not in AS_Set:
            AS_Set.add(line[0])
            length = len(result[0])-2
            append = [0] * length
            if len(append) > 0:
                result.append([line[0]+append])
            else:
                result.append([line[0]])

        # Find index
        index = 0
        for row in result:
            # print(row)
            if result[index][0] == line[0]:
                break
            index += 1
        result[index].append(line[1])

for i in range(10):
    print(result[i])

