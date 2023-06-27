def analyze_file(file_name, processing_version, debug=False):
    autonomous_system_set = set()
    autonomous_system_network_count = {}
    unique_networks = set()

    network_to_add_to_next_line = []

    autonomous_system_longest_path = {
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
        if value.count('.') >= 1:
            return True
        if value.count(':') >= 1:
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

    def get_values_from_line(single_line, version):
        single_line = single_line.replace(',', ' ')
        single_line = single_line.replace('{', ' ')
        single_line = single_line.replace('}', ' ')
        values = single_line.split()

        # For empty lines
        if len(values) == 0:
            print('EMPTY VALUES!')
            return values

        if version == 0:
            # Exception if the row has only single value 'i'
            if values[0] == 'i' and len(values) == 1:
                return values

            if len(values) == 1 and 'i' not in values[0]:
                return values

            # Regular situation for rows containing '*>i+IP Address'
            if len(values[0]) > 4 and 'i' in values[0]:
                value = values.pop(0)
                first = value[:3]
                second = value[3:]
                values.insert(0, second)
                values.insert(0, first)

            # For cases when 'i *' is the first value
            if len(values) > 1 and values[1] == 'i' and '*' in values[0]:
                if '>' in values[0]:
                    spacer = ''
                else:
                    spacer = ' '
                values[0] = values[0] + spacer + values.pop(1)

            # For '* i + IP address' cases
            try:
                if len(values[1]) > 1 and values[1][0] == 'i':
                    if '>' in values[0]:
                        spacer = ''
                    else:
                        spacer = ' '
                    values[0] = values[0] + spacer + 'i'
                    values[1] = values[1][1:]
            except IndexError:
                print(values)


            # valid = ['*', '*>', '*>i', '* i']
            # if values[0] not in valid:
            #     print(values)
        # print(values)
        return values

    with open(file_name, 'r') as file:
        count = 0

        next(file)

        for line in file:

            line_array = get_values_from_line(line, processing_version)

            if processing_version == 2:
                if line_array[0] == 'Network':
                    continue

            # Some lines due to long destination address, are split into two lines.
            # They are processed by first reading the first line, skipping post-process and then combining it together
            # when parsing next line
            if processing_version == 0 or processing_version == 2:
                if line_array[-1] not in ['i', '?', 'e']:
                    if len(network_to_add_to_next_line) > 0:
                        network_to_add_to_next_line = line_array
                        continue
                    else:
                        network_to_add_to_next_line = network_to_add_to_next_line + line_array
                        continue
                else:
                    if len(network_to_add_to_next_line) > 0:
                        line_array = network_to_add_to_next_line + line_array
                        network_to_add_to_next_line = []

            # Some networks have multiple routes, necessary for tracking longest transits and debugging
            if len(line_array) > 2:
                if is_ip_address(line_array[1]) and is_ip_address(line_array[2]):
                    current_network = line_array[1]

            if debug:
                print(line_array)
                print(current_network)

            # Process only best route
            if processing_version == 0 or processing_version == 2:
                if '>' not in line_array[0]:
                    continue

            # print(line_array)
            try:
                if processing_version == 0 or processing_version == 2:
                    last_zero_index = len(line_array) - line_array[::-1].index('0') - 1
                elif processing_version == 1:
                    last_zero_index = 3
                elif processing_version == 3:
                    current_network = line_array[0]
                    if current_network in unique_networks:
                        continue
                    last_zero_index = 0
            except ValueError:
                print(line_array)
                continue

            if debug:
                print('Adding Current Network to unique networks')

            unique_networks.add(current_network)

            try:
                if processing_version in [0, 1, 2]:
                    AS_route = line_array[last_zero_index + 1:-1]
                if processing_version in [3]:
                    AS_route = line_array[last_zero_index + 1:]
            except ValueError:
                print(line_array)
                continue

            if len(AS_route) == 0:
                # Skipping internal networks with path length 0
                continue
            destination_AS = AS_route[-1]
            AS_unique_route = create_path_set(AS_route)
            # print(f'Full route: {AS_route}\nUnique route:{AS_unique_route}\nDestination:{destination_AS}\n')

            if len(autonomous_system_longest_path["destination_id"]) < 3:
                if AS_route[0] not in autonomous_system_longest_path["destination_id"]:
                    autonomous_system_longest_path["destination_id"].append(destination_AS)
                    autonomous_system_longest_path["length"].append(len(AS_unique_route))
                    autonomous_system_longest_path["full_path"].append(AS_unique_route)
                    autonomous_system_longest_path["network"].append(current_network)
                    autonomous_system_longest_path = sort_longest_paths(autonomous_system_longest_path)
            else:
                if destination_AS not in autonomous_system_longest_path["destination_id"]:
                    if len(AS_unique_route) > autonomous_system_longest_path["length"][2]:
                        autonomous_system_longest_path["destination_id"][2] = destination_AS
                        autonomous_system_longest_path["length"][2] = len(AS_unique_route)
                        autonomous_system_longest_path["full_path"][2] = AS_unique_route
                        autonomous_system_longest_path["network"][2] = current_network
                        autonomous_system_longest_path = sort_longest_paths(autonomous_system_longest_path)

            if destination_AS not in autonomous_system_set:
                autonomous_system_set.add(destination_AS)
                autonomous_system_network_count[destination_AS] = 0
            autonomous_system_network_count[destination_AS] += 1
            count += 1

    most_used_AS = []
    for destination_AS in autonomous_system_network_count.keys():
        # print(destination_AS, autonomous_system_network_count[destination_AS])
        if len(most_used_AS) < 3:
            most_used_AS.append([destination_AS, autonomous_system_network_count[destination_AS]])
            most_used_AS = sorted(most_used_AS, key=count_key, reverse=True)
            continue
        if autonomous_system_network_count[destination_AS] > most_used_AS[2][1]:
            most_used_AS[2] = [destination_AS, autonomous_system_network_count[destination_AS]]
            most_used_AS = sorted(most_used_AS, key=count_key, reverse=True)

    print(f'Total networks: {len(unique_networks)}')

    print("\nLargest AS by network count")
    print(f'| {"AS id":<10} | {"Count":<10} |')
    for i in range(len(most_used_AS)):
        print(f'| {most_used_AS[i][0]:>10} | {most_used_AS[i][1]:>10} |')

    print("\nLongest path")
    for i in range(len(autonomous_system_longest_path["destination_id"])):
        print(
            f'Network: {autonomous_system_longest_path["network"][i]} AS ID: {autonomous_system_longest_path["destination_id"][i]} Length: {autonomous_system_longest_path["length"][i]}')
        print("Route: ", end='')
        for j in autonomous_system_longest_path["full_path"][i]:
            print(f'{j} ', end='')
        print()
    return autonomous_system_network_count
