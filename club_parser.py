import csv

from Dummy import download, get_goals_by_years, download_2


def get_player_clubs():
    player_dict = dict()
    with open('data.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            name = row[0]
            club_dict = dict()
            for line in row[1][:-2].split('|'):
                line = line.replace('\\n', '')
                slices = line.split('=')
                if len(slices) > 1:
                    key = slices[0].strip()
                    value = slices[1].replace('[[', '').replace(']]', '').replace('→', '').replace('(loan)', '').strip()
                    if len(value) > 0:
                        if 'years' in key and 'youthyears' not in key and 'collegeyears' not in key and 'manageryears' not in key and 'coaching_years' not in key and 'serviceyears' not in key:
                            key = int(key.replace('years', ''))
                            if key not in club_dict:
                                club_dict[key] = dict()
                            club_dict[key]['period'] = value
                        elif 'clubs' in key and 'youthclubs' not in key and 'managerclubs' not in key:
                            key = int(key.replace('clubs', ''))
                            if key not in club_dict:
                                club_dict[key] = dict()
                            club_dict[key]['name'] = value
            clubs = []
            for i in range(1, len(club_dict) + 1):
                j = i
                while j not in club_dict:
                    j = j + 1
                club = club_dict[j]
                if 'name' in club:
                    clubs.append(club)
            player_dict[name] = clubs
    return player_dict


# if __name__ == '__main__':
#     player_clubs = get_player_clubs()
#     for player in player_clubs:
#         clubs = player_clubs[player]
#         if len(clubs) == 0:
#             print(f'"{player}","{player_clubs[player]}"')
#             # print(f'"{player}","{download(player)}"')

def dummy():
    info_set = set()
    year_dict = get_goals_by_years()
    for year in year_dict:
        for player in year_dict[year]:
            year, country, name = player[0].split(',')
            info_set.add(f'{year},{country},{name}')
    for info in info_set:
        year, country, name = info.split(',')
        if name == 'Teboho Mokoena':
            print(f'"{year},{country},{name}","{[download(year, country, name)]}"')


if __name__ == '__main__':
    # dummy()
    my_dict = get_player_clubs()
    for key in my_dict:
        print(f'"{key}","{my_dict[key]}"')
    # print([download(None, 'Colin_Clarke_(footballer,_born_1962)', None)])