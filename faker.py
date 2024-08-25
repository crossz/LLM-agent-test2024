from faker import Faker

fake = Faker(locale = 'zh_CN')

# 生成球队模拟数据
def generate_teams(num_teams):
    teams = []
    for _ in range(num_teams):
        team = {
            'name': fake.team_name(),
            'points_scored': fake.random_int(min=50, max=120),
            'rebounds': fake.random_int(min=20, max=70),
            'assists': fake.random_int(min=10, max=50)
        }
        teams.append(team)
    return teams

# 生成球员模拟数据
def generate_players(num_players, teams):
    players = []
    for _ in range(num_players):
        team = fake.random_element(elements=teams)
        player = {
            'name': fake.name(),
            'team_id': team['id'],
            'points': fake.random_int(min=5, max=30),
            'rebounds': fake.random_int(min=2, max=15),
            'assists': fake.random_int(min=1, max=10)
        }
        players.append(player)
    return players

print(generate_players(10, generate_teams(5)))