import pandas as pd
from collections import deque

def build_graph(df):
    graph = {}
    grouped = df.groupby(["Season", "Team"])
    for (season, team), group in grouped:
        players = group["Player Name"].unique().tolist()

        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                p1, p2 = players[i], players[j]

                if p1 not in graph:
                    graph[p1] = {}
                if p2 not in graph:
                    graph[p2] = {}

                if p2 not in graph[p1]:
                    graph[p1][p2] = set()
                if p1 not in graph[p2]:
                    graph[p2][p1] = set()

                graph[p1][p2].add((season, team))
                graph[p2][p1].add((season, team))

    print("CourtConnector built successfully!")
    return graph

def condense(seasons):
    years = sorted(int(season[:4]) for season in seasons)
    if not years:
        return []

    condensed = []
    start = prev = years[0]

    for year in years[1:]:
        if year == prev + 1:
            prev = year
        else:
            condensed.append(f"{start}–{prev+1 if prev > start else start+1}")
            start = year
        prev = year

    condensed.append(f"{start}–{prev+1 if prev > start else start+1}")
    return condensed

def find_path(graph, start, end):
    if start not in graph or end not in graph:
        return None
    
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        curr, path = queue.popleft()
        if curr == end:
            return path
        visited.add(curr)
        for neighbor in graph[curr]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None

def print_path(graph, path):
    if not path:
        print("No CourtConnection found.")
        return

    for i in range(len(path) - 1):
        player1 = path[i]
        player2 = path[i + 1]
        seasons = graph[player1][player2]

        team_to_years = {}
        for season, team in seasons:
            year = int(season[:4])
            if team not in team_to_years:
                team_to_years[team] = []
            if year not in team_to_years[team]:
                team_to_years[team].append(year)

        formatted = []
        for team in team_to_years:
            years = sorted(team_to_years[team])
            start = prev = years[0]
            for y in years[1:]:
                if y != prev + 1:
                    formatted.append(f"{team} {start}–{prev+1 if prev > start else start+1}")
                    start = y
                prev = y
            formatted.append(f"{team} {start}–{prev+1 if prev > start else start+1}")

        print(f"{player1} ➝  {player2} ({', '.join(formatted)})")

def main():
    print("Building CourtConnector...")
    df = pd.read_csv("nba_players.csv")
    graph = build_graph(df)

    player1 = input("Enter start player: ")
    player2 = input("Enter target player: ")

    path = find_path(graph, player1, player2)
    if path:
        print("\nCourtConnection:")
        print_path(graph, path)
    else:
        print("No CourtConnection found.")

if __name__ == "__main__":
    main()
