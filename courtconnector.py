import pandas as pd
from collections import defaultdict, deque
from rapidfuzz import process

def build(df):
    graph = defaultdict(lambda: defaultdict(set))
    grouped = df.groupby(["Season", "Team"])
    for (season, team), group in grouped:
        players = group["Player Name"].unique().tolist()
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                p1, p2 = players[i], players[j]
                graph[p1][p2].add((season, team))
                graph[p2][p1].add((season, team))
    print("CourtConnector built successfully!")
    return graph

def find(graph, start, end):
    if start not in graph or end not in graph:
        return None
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        curr, path = queue.popleft()
        if curr == end:
            return path
        for neighbor in graph[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

def format(seasons):
    team_to_years = defaultdict(set)
    for season, team in seasons:
        year = int(season[:4])
        team_to_years[team].add(year)
    formatted = []
    for team, years in team_to_years.items():
        years = sorted(years)
        start = prev = years[0]
        for y in years[1:]:
            if y != prev + 1:
                formatted.append(f"{team} {start}–{prev+1 if prev > start else start+1}")
                start = y
            prev = y
        formatted.append(f"{team} {start}–{prev+1 if prev > start else start+1}")
    return ', '.join(formatted)

def connection(graph, path):
    if not path:
        print("No CourtConnection found.")
        return
    for i in range(len(path) - 1):
        player1, player2 = path[i], path[i + 1]
        seasons = graph[player1][player2]
        print(f"{player1} ➝  {player2} ({format(seasons)})")

def fuzzymatch(input, players):
    matches = process.extract(input, players, limit=5, score_cutoff=60)
    if not matches:
        return None, []

    best_match = matches[0][0]
    suggestions = [(name, score) for name, score, _ in matches]
    return best_match, suggestions

def inputprompt(prompt, player_names):
    while True:
        raw = input(prompt).strip()
        if raw in player_names:
            return raw
        while True:
            _, suggestions = fuzzymatch(raw, player_names)
            if not suggestions:
                print(f"No close matches found for '{raw}'\n")
                raw = input(prompt).strip()
                if raw in player_names:
                    return raw
                continue
            print(f"\nDid you mean one of these?")
            for i, (name, score) in enumerate(suggestions[:3], 1):
                print(f"{i}. {name} ({score:.1f}%)")
            choice = input(f"Select 1 - 3 or retype a name: ").strip()
            if choice in {"1", "2", "3"}:
                idx = int(choice) - 1
                return suggestions[idx][0]
            elif choice in player_names:
                return choice
            else:
                raw = choice
        
def main():
    print("Loading NBA player data...")
    df = pd.read_csv("nba_players.csv")
    players = df["Player Name"].unique().tolist()
    graph = build(df)

    playerA = inputprompt("Enter Player A: ", players)
    playerB = inputprompt("Enter Player B: ", players)
    if not playerA or not playerB:
        print("Invalid player names provided.")
        return

    path = find(graph, playerA, playerB)
    if path:
        print("\nCourtConnection:")
        connection(graph, path)
    else:
        print("No CourtConnection found.")

if __name__ == "__main__":
    main()
