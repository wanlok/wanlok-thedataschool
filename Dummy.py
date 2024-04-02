import csv
import json
import urllib.request


def get_name_and_time(x):
    goal = [y.replace('(P)', '').replace('(OG)', '').strip() for y in x.split('·')]
    slices = goal[1].split('+')
    additional_time = 0
    if len(slices) > 1:
        additional_time = int(slices[1])
    return [goal[0], int(slices[0]), additional_time]


def get_goals(x):
    return [get_name_and_time(z) for z in filter(lambda y: len(y) > 0, x.split('|'))]


def get_rows():
    rows = []
    with open('matches_1930_2022.csv', encoding='utf-8') as csv_file:
        row_count = 0
        for row in csv.reader(csv_file, delimiter=','):
            if row_count > 0:
                year = row[21]
                team_1 = row[0]
                team_1_goals = get_goals(row[22])
                team_1_penalty_goals = get_goals(row[28])
                # team_1_own_goals = get_goals(row[26], 'OG')
                team_1_own_goals = []

                team_2 = row[1]
                team_2_goals = get_goals(row[23])
                team_2_penalty_goals = get_goals(row[29])
                # team_2_own_goals = get_goals(row[27], 'OG')
                team_2_own_goals = []

                team_1_goals = sorted(team_1_goals + team_1_penalty_goals + team_2_own_goals, key=lambda x: (x[1], x[2]))
                team_2_goals = sorted(team_2_goals + team_2_penalty_goals + team_1_own_goals, key=lambda x: (x[1], x[2]))

                rows.append([year, team_1, team_1_goals, team_2, team_2_goals])
            row_count = row_count + 1
    return rows


def add_goals(year_dict, year, x):
    if year in year_dict:
        name_dict = year_dict[year]
    else:
        name_dict = {}
        year_dict[year] = name_dict
    for result in x:
        name = result[0]
        if name in name_dict:
            name_dict[name] = name_dict[name] + 1
        else:
            name_dict[name] = 1


def get_goals_by_years():
    year_dict = {}
    for row in get_rows():
        year = row[0]
        for player in row[2]:
            player[0] = f'{year},{row[1]},{player[0]}'
        for player in row[4]:
            player[0] = f'{year},{row[3]},{player[0]}'
        add_goals(year_dict, year, row[2])
        add_goals(year_dict, year, row[4])
    for year in year_dict:
        year_dict[year] = sorted(year_dict[year].items(), key=lambda x: x[1], reverse=True)
    return year_dict


def download(year, country, name):
    content = ''
    titles = urllib.parse.quote(name)
    url_string = f'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={titles}&rvprop=content&format=json'
    with urllib.request.urlopen(url_string) as url:
        data = json.load(url)
        pages = data['query']['pages']
        for key in pages:
            if key != '-1':
                revision = pages[key]['revisions'][-1]['*']
                if revision[0:9] == '#REDIRECT':
                    content = download(revision[revision.index('[[')+2:revision.index(']]')])
                else:
                    try:
                        start = revision.index('years1')
                        end = revision.index('nationalyears1')
                        content = revision[start:end]
                    except:
                        match_lines = []
                        for line in revision.split('\n'):
                            print(f'LLLLL {line}')
                        print(f'{year} {country} {name}')
                        print(revision)
                        break
    return content


def download_2(name, country):
    contents = []
    titles = urllib.parse.quote(name)
    url_string = f'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={titles}&rvprop=content&format=json'
    with urllib.request.urlopen(url_string) as url:
        data = json.load(url)
        pages = data['query']['pages']
        for key in pages:
            if key != '-1':
                revision = pages[key]['revisions'][-1]['*']
                if revision[0:9] == '#REDIRECT':
                    contents = download_2(revision[revision.index('[[')+2:revision.index(']]')], country)
                else:
                    lines = revision.split('\n')
                    for line in lines:
                        if 'football' in line:
                            print(line)
                    # if len(contents) == 1:
                    #     print(f'AAAAA {contents[0]}')
    return contents


def download_all():
    info_set = set()
    year_dict = get_goals_by_years()
    for year in year_dict:
        for player in year_dict[year]:
            _, country, name = player[0].split(',')
            info_set.add(f'{country},{name}')
    for info in info_set:
        country, name = info.split(',')
        print(f'"{name}","{[download(name)]}"')




def get_player_countries():
    player_countries = []
    names = []
    year_dict = get_goals_by_years()
    for year in year_dict:
        for player in year_dict[year]:
            names.append(player[0])
    with open('Player Clubs.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            target = row[0]

            for name in names:
                if target in name:
                    player_countries.append(name)
                    break
    return player_countries


def get_empty_players():
    info_dict = dict()
    year_dict = get_goals_by_years()
    for year in year_dict:
        for player in year_dict[year]:
            year, country, name = player[0].split(',')
            key = f'{country},{name}'
            if key in info_dict:
                info_dict[key].append(year)
            else:
                info_dict[key] = [year]
    with open('data.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            if len(row[1]) == 0:
                for key in info_dict:
                    _, name = key.split(',')
                    if row[0] == name:
                        print(f'{key},{info_dict[key]}')


# if __name__ == '__main__':
#     year_dict = get_goals_by_years()
#     for year in year_dict:
#         print(f'{year} {year_dict[year]}')


# if __name__ == '__main__':
#     players = set()
#     year_dict = get_goals_by_years()
#     for year in year_dict:
#         for player in year_dict[year]:
#             players.add(player[0])
#     for player in players:
#         print(player)


if __name__ == '__main__':
    # download_all()
    get_empty_players()
    # download('Júnior')
