import time
import GetFiles
import ReadFile


def main():
    start_time = time.time()

    processing_version_dict = {
        "2002IPv4": 0,
        "2004IPv4": 0,
        "2006IPv4": 0,
        "2007IPv4": 0,
        "2008IPv4": 0,
        "2009IPv4": 1,
        "2009IPv6": 2,
        "2010IPv4": 1,
        "2010IPv6": 3,
        "2011IPv4": 0,
        "2011IPv6": 2,
        "2012IPv4": 0,
        "2012IPv6": 0,
        "2013IPv4": 2,
        "2013IPv6": 2,
        "2014IPv4": 2,
        "2014IPv6": 2,
        "2015IPv4": 2,
        "2015IPv6": 2,
        "2016IPv4": 2,
        "2016IPv6": 2,
        "2017IPv4": 2,
        "2017IPv6": 2,
        "2018IPv4": 2,
        "2018IPv6": 2,
        "2019IPv4": 2,
        "2019IPv6": 2,
        "2020IPv4": 2,
        "2020IPv6": 2,
        "2021IPv4": 2,
        "2021IPv6": 2,
        "2022IPv4": 2,
        "2022IPv6": 2,
        "2023IPv4": 2,
        "2023IPv6": 2,
        }

    folder = 'bgpTables'
    debug = False
    file_info = GetFiles.get_files(folder)

    count = []

    for file in file_info:
        year = file["year"]
        version = file["version"]
        processing_version = processing_version_dict[year+version]

        print(f'\n{year} {version}')

        autonomous_system_count = ReadFile.analyze_file(file['path'], processing_version, debug)
        quantity = len(autonomous_system_count.keys())
        count.append({"version": year+' '+version, "count": quantity})

    end_time = time.time()
    print(f'Elapsed time: {round(end_time - start_time, 2)} seconds')

    print()
    for dict in count:
        print(dict)


if __name__ == "__main__":
    main()
