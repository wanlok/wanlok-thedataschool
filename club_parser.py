import csv

if __name__ == '__main__':
    with open('Player Clubs.csv', encoding='utf-8') as csv_file:
        row_count = 0
        for row in csv.reader(csv_file, delimiter=','):
            name = row[0]
            content = row[1][2:-2].split('\\n')
            print(name)
            for line in content:
                slices = line.split('=')
                if len(slices) > 1:
                    key = slices[0].strip()
                    value = slices[1].strip()
                    print(f'{key} = {value}')

