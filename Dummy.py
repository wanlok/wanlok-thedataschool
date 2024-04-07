import csv
import json
import re
import urllib.request
import geograpy
import pycountry


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


def is_year_within_range(year, range):
    if '-' not in range:
        club_within_year = range == year
    elif range[0] == '-':
        club_within_year = range[1:] == year
    elif range[-1] == '-':
        club_within_year = year >= range[:len(range) - 1]
    else:
        slices = range.split('-')
        club_within_year = len(slices) == 2 and int(slices[0]) <= int(year) <= int(slices[1])
    return club_within_year


def get_player_club_dict():
    player_club_dict = dict()
    with open('clubs.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            player_club_dict[row[0]] = row[1]
    return player_club_dict


def download_wikipedia_content(titles):
    content = ''
    titles = urllib.parse.quote(titles)
    url_string = f'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={titles}&rvprop=content&format=json'
    with urllib.request.urlopen(url_string) as url:
        query = json.load(url)['query']
        if 'pages' in query:
            pages = query['pages']
            for page in pages:
                if page != '-1':
                    content = pages[page]['revisions'][-1]['*']
                    if content[0:9].lower() == '#redirect':
                        content = download_wikipedia_content(content[content.index('[[') + 2:content.index(']]')])
    return content


def count_occurrences(target, content):
    count = 0
    target = target.lower()
    while target in content:
        count = count + 1
        content = content[content.index(target) + len(target):]
    return count


# def get_largest_and_second_largest_count(dict):
#     for


def extract_league(club):
    count_dict = dict()

    content = download_wikipedia_content(club)
    content = content.lower()
    content = re.compile(r'[^a-z\s]').sub(' ', content) # alphabet letter or a space
    content = re.compile(r'\s+').sub(' ', content) # consecutive spaces
    content = content.replace('\n', '')

    countries = []
    for country in pycountry.countries:
        countries.append({
            'name_1': country.name,
            'name_2': country.official_name,
            'name_3': country.common_name
        })

    countries.append({'name_1': 'England', 'name_2': 'England', 'name_3': 'England'})
    countries.append({'name_1': 'Scotland', 'name_2': 'Scotland', 'name_3': 'Scotland'})
    countries.append({'name_1': 'Wales', 'name_2': 'Wales', 'name_3': 'Wales'})
    countries.append({'name_1': 'Northern Ireland', 'name_2': 'Northern Ireland', 'name_3': 'Northern Ireland'})
    countries.append({'name_1': 'America', 'name_2': 'America', 'name_3': 'America'})
    countries.append({'name_1': 'Yugoslavia', 'name_2': 'Yugoslavia', 'name_3': 'Yugoslavia'})
    countries.append({'name_1': 'South Korea', 'name_2': 'South Korea', 'name_3': 'South Korea'})
    countries.append({'name_1': 'North Korea', 'name_2': 'North Korea', 'name_3': 'North Korea'})
    countries.append({'name_1': 'Turkey', 'name_2': 'Turkey', 'name_3': 'Turkey'})

    for country in countries:
        count = count_occurrences(country['name_1'], content) + count_occurrences(country['name_2'], content) + count_occurrences(country['name_3'], content)
        if count > 0:
            count_dict[country['name_1']] = count

    print(f'"{club}","{count_dict}"')


def download_club_info_1():
    club_set = set()
    with open('clubs.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            for club in eval(row[1]):
                club_set.add(club['name'])

    downloaded_club_set = set()
    with open('league.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            downloaded_club_set.add(row[0])

    print(f'{len(club_set)} {len(downloaded_club_set)}')

    for club in club_set:
        if club not in downloaded_club_set:
            extract_league(club)

def download_club_info_3():
    club_set = set()
    with open('league.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            if row[1] == '{}':
                print(row[0])


def get_club_name(club_dict, year, player_name):
    club_name = ''
    for club in eval(club_dict[player_name]):
        if 'period' in club and is_year_within_range(year, club['period']):
            club_name = club['name']
            break
    return club_name


def get_goals_by_years():
    year_dict = {}
    player_club_dict = get_player_club_dict()
    club_country_dict = get_club_country_dict()
    for row in get_rows():
        year = row[0]
        for player in row[2]:
            player_name = player[0]
            club_name = get_club_name(player_club_dict, year, player_name)
            club_country = club_country_dict[club_name]
            player[0] = f'"{year}","{row[1]}","{player_name}","{club_name}","{club_country}"'
        for player in row[4]:
            player_name = player[0]
            club_name = get_club_name(player_club_dict, year, player_name)
            club_country = club_country_dict[club_name]
            player[0] = f'"{year}","{row[3]}","{player_name}","{club_name}","{club_country}"'
        add_goals(year_dict, year, row[2])
        add_goals(year_dict, year, row[4])
    for year in year_dict:
        year_dict[year] = sorted(year_dict[year].items(), key=lambda x: x[1], reverse=True)
    return year_dict


def download(country, name, years):
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
                    print(revision)
                    content = download(country, revision[revision.index('[[')+2:revision.index(']]')], years)
                else:
                    try:
                        start = revision.index('years1')
                        end = revision.index('nationalyears1')
                        content = revision[start:end]
                    except:
                        # match_lines = []
                        # for line in revision.split('\n'):
                        #     print(f'LLLLL {line}')
                        print(revision)
                    break
    return content


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
    country_set = set()
    with open('data.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            if len(row[1]) == 0:
                for key in info_dict:
                    country, name = key.split(',')
                    if row[0] == name and country == 'Brazil':
                        years = info_dict[key]
                        print(f'= = = = = = = = = = = = = = = = = = = = = = = = = = = = = =')
                        print(f'{country}, {name}, {years}')
                        download(country, name, years)
                        country_set.add(country)
    for country in country_set:
        print(country)


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


def get_country(country_dict):
    max_country = None
    max_count = None
    for country in country_dict:
        count = country_dict[country]
        if max_count is None or count > max_count:
            max_country = country
            max_count = count
    return max_country


def get_club_country_dict():
    club_country_dict = dict()
    club_country_dict[''] = ''
    club_country_mapping_dict = dict()
    club_country_count_dict = dict()
    with open('club_country_mapping.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            club_country_mapping_dict[row[0]] = row[1]
    with open('club_country_count.csv', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            club_country_count_dict[row[0]] = eval(row[1])
    for club_name in club_country_count_dict:
        country = get_country(club_country_count_dict[club_name])
        if country is None:
            country = club_country_mapping_dict[club_name]
        if ',' in country:
            country = country.split(',')[0]
        club_country_dict[club_name] = country
    return club_country_dict


if __name__ == '__main__':

    # print([download(None, 'Juan_Carreño_(Chilean_footballer)', None)])

    # my_dict = get_player_clubs()
    # for key in my_dict:
    #     print(f'"{key}","{my_dict[key]}"')

    # year_dict = get_goals_by_years()
    # for year in year_dict:
    #     print(f'{year} {year_dict[year]}')

    year_dict = get_goals_by_years()
    for year in year_dict:
        print(f'{year} {year_dict[year]}')

    # download_club_info_1()
    # extract_league('Jeonbuk Hyundai Motors FC')
    # download_club_info_3()
    # dummy()
