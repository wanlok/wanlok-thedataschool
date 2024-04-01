import csv

if __name__ == '__main__':
    with open('Player Clubs.csv', encoding='utf-8') as csv_file:
        row_count = 0
        for row in csv.reader(csv_file, delimiter=','):
            name = row[0]
            content = row[1][2:-2].split('|')
            my_dict = dict()
            for line in content:
                line = line.replace('\\n', '')
                slices = line.split('=')
                if len(slices) > 1:
                    key = slices[0].strip()
                    value = slices[1].replace('[[', '').replace(']]', '').replace('→', '').replace('(loan)', '').strip()
                    if len(value) > 0:
                        if 'years' in key and 'youthyears' not in key and 'manageryears' not in key:
                            key = int(key.replace('years', ''))
                            if key not in my_dict:
                                my_dict[key] = dict()
                            my_dict[key]['period'] = value
                        elif 'clubs' in key and 'youthclubs' not in key and 'managerclubs' not in key:
                            key = int(key.replace('clubs', ''))
                            if key not in my_dict:
                                my_dict[key] = dict()
                            my_dict[key]['club'] = value
            print(name)
            for key in my_dict:
                print(f'{key} {my_dict[key]}')



