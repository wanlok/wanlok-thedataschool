import csv


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
        add_goals(year_dict, year, row[2])
        add_goals(year_dict, year, row[4])
    for year in year_dict:
        year_dict[year] = sorted(year_dict[year].items(), key=lambda x: x[1], reverse=True)
    return year_dict


if __name__ == '__main__':
    year_dict = get_goals_by_years()
    for year in year_dict:
        print(f'{year} {year_dict[year]}')
