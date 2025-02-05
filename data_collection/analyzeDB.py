import sqlite3
import matplotlib.pyplot as plt

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def get_wins(conn):
    cur = conn.cursor()

    team_shorts = {}

    teams_wins = {}

    cur.execute("""
                SELECT teams.csv_name,
                    teams.short_name, 
                    COUNT(CASE WHEN games.ftr = 'H' THEN 1 ELSE NULL END) AS home_wins,
                    COUNT(CASE WHEN games.ftr = 'A' THEN 1 ELSE NULL END) AS away_wins
                FROM teams
                LEFT JOIN games ON teams.id = games.home_id OR teams.id = games.away_id
                GROUP BY teams.csv_name
                ORDER BY teams.csv_name ASC;
                """)


    for row in cur.fetchall():
        team_name, team_short, home_wins, away_wins = row
        total_wins = home_wins + away_wins
        team_shorts[team_name] = team_short
        teams_wins[team_short] = total_wins

    
    colors = ['#EF0107', '#95BFE5', '#DA291C', '#FF0000', '#0057B8',
            '#6C1D45', '#0070B5', '#034694', '#1B458F', '#003399',
            '#000000', '#0E63AD', '#FEAE37', '#FFCD00', '#003090',
            '#C8102E', '#6CABDD', '#DA291C', '#DE1B22', '#241F20',
            '#00A650', '#DD0000', '#EE2737', '#D71920', '#E03A3E',
            '#EB172B', '#000000', '#132257', '#FBEE23', '#122F67',
            '#7A263A', '#FDB913'
            ]
    
    fig, ax = plt.subplots(figsize=(12, 6)) 

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    plt.bar(range(len(teams_wins)), list(teams_wins.values()), align='center', width= 0.5, color= colors)
    
    t_list = list(map(lambda x: x + ' - ' + str(team_shorts[x]), team_shorts.keys()))
    
    handles = [plt.Rectangle((0,0),1,1, color=color) for color in colors]

    plt.legend(handles, t_list, loc='upper right', bbox_to_anchor=(1.1, 1.0), prop={'size': 7})
    
    plt.ylabel('Number of Wins')

    plt.title('Number of Wins by Team from 2016/17 to 2022/23 Seasons of the Premier League')

    plt.xlabel('Team')

    plt.xticks(range(len(teams_wins)), list(teams_wins.keys()))

    plt.show()

    print(teams_wins)

def get_teams_articles(conn):

    cur = conn.cursor()

    team_shorts = {}

    team_references = {}

    cur.execute("""
        SELECT teams.csv_name, teams.short_name, COUNT(article_named_teams.named_team_id) AS team_references
        FROM teams
        LEFT JOIN article_named_teams ON teams.id = article_named_teams.named_team_id
        GROUP BY teams.name
        ORDER BY teams.csv_name ASC;
    """)

    for row in cur.fetchall():
        team_name, team_short, references = row
        team_references[team_name] = references
        team_shorts[team_name] = team_short

    colors = ['#EF0107', '#95BFE5', '#DA291C', '#FF0000', '#0057B8',
            '#6C1D45', '#0070B5', '#034694', '#1B458F', '#003399',
            '#000000', '#0E63AD', '#FEAE37', '#FFCD00', '#003090',
            '#C8102E', '#6CABDD', '#DA291C', '#DE1B22', '#241F20',
            '#00A650', '#DD0000', '#EE2737', '#D71920', '#E03A3E',
            '#EB172B', '#000000', '#132257', '#FBEE23', '#122F67',
            '#7A263A', '#FDB913'
            ]
    
    fig, ax = plt.subplots(figsize=(12, 6)) 

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    plt.bar(range(len(team_references)), list(team_references.values()), align='center', width= 0.5, color= colors)
    
    t_list = list(map(lambda x: x + ' - ' + str(team_shorts[x]), team_shorts.keys()))
    
    handles = [plt.Rectangle((0,0),1,1, color=color) for color in colors]

    plt.legend(handles, t_list, loc='upper right', bbox_to_anchor=(1.06, 1.0), prop={'size': 7})

    plt.title('Number of Times Teams were Referenced in the News Articles')

    plt.ylabel('Number of Articles')

    plt.xlabel('Team')

    plt.xticks(range(len(team_shorts)), list(team_shorts.values()))

    plt.show()

    print(team_references)

def get_average_number_goals_team(conn):

    cur = conn.cursor()

    team_shorts = {}

    team_goals = {}

    cur.execute("""
        SELECT teams.csv_name, teams.short_name, seasons.last_year AS season_end_year,
        SUM(CASE WHEN teams.id = games.home_id THEN games.home_goals ELSE games.away_goals END) AS total_goals
        FROM teams
        LEFT JOIN games ON teams.id = games.home_id OR teams.id = games.away_id
        LEFT JOIN seasons ON games.season_id = seasons.id
        GROUP BY teams.csv_name, teams.short_name, seasons.last_year
        ORDER BY teams.csv_name ASC, seasons.last_year ASC;
    """)

    for row in cur.fetchall():
        team_name, team_short, season_year, avg_goals = row
        team_goals.setdefault(team_name, []).append(avg_goals)
        team_shorts[team_name] = team_short

    colors = ['#EF0107', '#95BFE5', '#DA291C', '#FF0000', '#0057B8',
            '#6C1D45', '#0070B5', '#034694', '#1B458F', '#003399',
            '#000000', '#0E63AD', '#FEAE37', '#FFCD00', '#003090',
            '#C8102E', '#6CABDD', '#DA291C', '#DE1B22', '#241F20',
            '#00A650', '#DD0000', '#EE2737', '#D71920', '#E03A3E',
            '#EB172B', '#000000', '#132257', '#FBEE23', '#122F67',
            '#7A263A', '#FDB913'
            ]
    
    fig, ax = plt.subplots(figsize=(12, 6)) 

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    team_names = list(team_goals.keys())
    avg_goals_per_season = [sum(team_goals[team]) / len(team_goals[team]) for team in team_names]

    plt.bar(range(len(team_names)), avg_goals_per_season, align='center', width= 0.5, color= colors)
    
    t_list = list(map(lambda x: x + ' - ' + str(team_shorts[x]), team_shorts.keys()))
    
    handles = [plt.Rectangle((0,0),1,1, color=color) for color in colors]

    plt.legend(handles, t_list, loc='upper right', bbox_to_anchor=(1.08, 1.0), prop={'size': 7})

    plt.title('Average Number of Goals per Season for Each Team')

    plt.ylabel('Average Number of Goals')

    plt.xlabel('Team')

    plt.xticks(range(len(team_shorts)), list(team_shorts.values()))

    plt.show()

def get_most_news_weeks(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT subquery.wk, AVG(num_articles) AS avg_num_articles
        FROM (
            SELECT games.wk, COUNT(articles.id) AS num_articles
            FROM games
            LEFT JOIN articles ON games.id = articles.game_id
            GROUP BY games.wk
        ) AS subquery
        GROUP BY subquery.wk
        ORDER BY subquery.wk ASC;
    """)

    week_avg_articles = []

    for row in cur.fetchall():
        week, avg_articles = row
        week_avg_articles.append((week, avg_articles))
    
    fig, ax = plt.subplots(figsize=(12, 6))

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    weeks = [row[0] for row in week_avg_articles]
    avg_articles = [row[1] for row in week_avg_articles]

    plt.bar(range(len(weeks)), avg_articles, align='center', width=0.5)

    plt.title('Average Number of News Articles per Week throughout the 2016/17 to 2022/23 Seasons')

    plt.ylabel('Average Number of Articles')

    plt.xlabel('Week')

    plt.xticks(range(len(weeks)), weeks)

    plt.show()

def top10_scorers(conn):

    cur = conn.cursor()

    cur.execute("""
                SELECT players.Name AS player_name, SUM(players_stats.Goals) AS total_goals FROM players
                JOIN players_stats ON players.id = players_stats.players_id
                GROUP BY players.Name
                ORDER BY total_goals DESC
                LIMIT 10;
                """)
    
    scorers = {}
    
    for row in cur.fetchall():
        player_name, total_goals = row
        scorers[player_name] = total_goals

    fig, ax = plt.subplots(figsize=(12, 6))

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    plt.bar(range(len(scorers)), list(scorers.values()), align='center', width=0.5)

    plt.title('Top 10 Scorers in the Premier League from 2016/17 to 2022/23 Seasons')

    plt.ylabel('Number of Goals')

    plt.xlabel('Player')

    plt.xticks(range(len(scorers)), list(scorers.keys()))

    plt.show()

connection = create_connection("news_articles.db")

get_wins(connection)

get_teams_articles(connection)

get_average_number_goals_team(connection)

get_most_news_weeks(connection)

top10_scorers(connection)