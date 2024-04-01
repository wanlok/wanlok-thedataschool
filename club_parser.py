import csv

def get_player_clubs():
    player_dict = dict()
    with open('Player Clubs.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            name = row[0]
            club_dict = dict()
            for line in row[1][2:-2].split('|'):
                line = line.replace('\\n', '')
                slices = line.split('=')
                if len(slices) > 1:
                    key = slices[0].strip()
                    value = slices[1].replace('[[', '').replace(']]', '').replace('→', '').replace('(loan)', '').strip()
                    if len(value) > 0:
                        if 'years' in key and 'youthyears' not in key and 'manageryears' not in key:
                            key = int(key.replace('years', ''))
                            if key not in club_dict:
                                club_dict[key] = dict()
                            club_dict[key]['period'] = value
                        elif 'clubs' in key and 'youthclubs' not in key and 'managerclubs' not in key:
                            key = int(key.replace('clubs', ''))
                            if key not in club_dict:
                                club_dict[key] = dict()
                            club_dict[key]['club'] = value
            clubs = []
            for i in range(1, len(club_dict) + 1):
                j = i
                while j not in club_dict:
                    j = j + 1
                clubs.append(club_dict[j])
            player_dict[name] = clubs
    return player_dict


if __name__ == '__main__':
    player_clubs = get_player_clubs()
    for player in player_clubs:
        print(f'{player} {player_clubs[player]}')


