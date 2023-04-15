import time

start = time.time()
# Open the file for reading

AS_set = set()
AS_count = {}
network_to_add_to_next_line = []

AS_longest_path = {
    "destination_id": [],
    "full_path": [],
    "network": [],
    "length": []}

current_network = ''



def sort_longest_paths(dictionary):
    count = len(dictionary["destination_id"])
    if count < 2:
        return dictionary
    length = dictionary["length"]
    destination_id = dictionary["destination_id"]
    full_path = dictionary["full_path"]
    network = dictionary["network"]
    for i in range(count - 1):
        first = count - i - 2
        second = count - i - 1
        # print(count)
        # print(first, second)
        if length[second] > length[first]:
            # print(dictionary)
            length[second], length[first] = length[first], length[second]
            destination_id[second], destination_id[first] = destination_id[first], destination_id[second]
            full_path[second], full_path[first] = full_path[first], full_path[second]
            network[second], network[first] = network[first], network[second]
            # print(dictionary)
    AS_longest_path = {
        "destination_id": destination_id,
        "full_path": full_path,
        "network": network,
        "length": length}
    return AS_longest_path


def is_ip_address(value):
    if value.count('.') == 3:
        return True
    return False


def create_path_set(paths):
    result_set = set()
    result = []
    for path in paths:
        if path not in result_set:
            result.append(path)
            result_set.add(path)
    return list(result)


def count_key(sub_arr):
    return sub_arr[1]


def get_values_from_line(line):
    line.replace(',', ' ')
    line.replace('{', ' ')
    line.replace('}', ' ')
    values = line.split()
    return values


with open('ipv4bgp2023apnic.txt', 'r') as file:
    count = 0
    i = 0

    for line in file:
        values = get_values_from_line(line)

        # Some lines due to long destination address, are split into two lines.
        # They are processed by first reading the first line, skipping post-process and then combining it together
        # when parsing next line
        if len(network_to_add_to_next_line) > 0:
            values = network_to_add_to_next_line + values
            network_to_add_to_next_line = []

        # Check if line is valid for processing
        if len(values) == 0:
            continue

        # Some networks have multiple routes, necessary for tracking longest transits and debugging
        if len(values) > 2:
            if is_ip_address(values[1]) and is_ip_address(values[2]):
                current_network = values[1]

        # Skip lines that aren't routes
        if values[0][0] != '*':
            continue

        # All routes contain the Weight as 0. It's used to determine if the route line is split into two
        # If it's not found, continue to next line.
        try:
            index = values.index('0')
        except ValueError:
            network_to_add_to_next_line = values
            continue

        # Process only best route
        if values[0] != '*>':
            continue

        AS_route = values[index + 1:-1]
        destination_AS = AS_route[-1]
        AS_unique_route = create_path_set(AS_route)
        # print(f'Full route: {AS_route}\nUnique route:{AS_unique_route}\nDestination:{destination_AS}\n')

        if len(AS_longest_path["destination_id"]) < 3:
            if AS_route[0] not in AS_longest_path["destination_id"]:
                AS_longest_path["destination_id"].append(destination_AS)
                AS_longest_path["length"].append(len(AS_unique_route))
                AS_longest_path["full_path"].append(AS_unique_route)
                AS_longest_path["network"].append(current_network)
                AS_longest_path = sort_longest_paths(AS_longest_path)
        else:
            if destination_AS not in AS_longest_path["destination_id"]:
                if len(AS_unique_route) > AS_longest_path["length"][2]:
                    AS_longest_path["destination_id"][2] = destination_AS
                    AS_longest_path["length"][2] = len(AS_unique_route)
                    AS_longest_path["full_path"][2] = AS_unique_route
                    # print(current_network)
                    # print(AS_longest_path["network"])
                    AS_longest_path["network"][2] = current_network
                    # print(AS_longest_path["network"])
                    AS_longest_path = sort_longest_paths(AS_longest_path)

        if destination_AS not in AS_set:
            AS_set.add(destination_AS)
            AS_count[destination_AS] = 0
        AS_count[destination_AS] += 1
        count += 1


most_used_AS = []
for destination_AS in AS_count.keys():
    if len(most_used_AS) < 3:
        most_used_AS.append([destination_AS, AS_count[destination_AS]])
        most_used_AS = sorted(most_used_AS, key=count_key, reverse=True)
        continue
    if AS_count[destination_AS] > most_used_AS[2][1]:
        most_used_AS[2] = [destination_AS, AS_count[destination_AS]]
        most_used_AS = sorted(most_used_AS, key=count_key, reverse=True)

end = time.time()


print(f'Time: {round(end - start, 2)}')
print(f'Total networks: {count}')

print("\nLargest AS by network count")
print(f'| {"AS id":<10} | {"Count":<10} |')
for i in range(len(most_used_AS)):
    print(f'| {most_used_AS[i][0]:>10} | {most_used_AS[i][1]:>10} |')

print("\nLongest path")
for i in range(len(AS_longest_path["destination_id"])):
    print(f'Network: {AS_longest_path["network"][i]} AS ID: {AS_longest_path["destination_id"][i]} Length: {AS_longest_path["length"][i]}')
    print("Route: ", end='')
    for j in AS_longest_path["full_path"][i]:
        print(f'{j} ', end='')
    print()

# print(AS_longest_path)
