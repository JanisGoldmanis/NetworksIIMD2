def get_values_from_line(line):
    print(line)
    line = line.replace(',', ' ')
    line = line.replace('{', ' ')
    line = line.replace('}', ' ')
    values = line.split()
    return values


line = "                                                1    220      0 6939 7473 45147 {55818} i"
values = get_values_from_line(line)
print(values)