import pandas as pd
from collections import defaultdict, deque
from rapidfuzz import process

def build(df):
    # builds a graph of players with seasons and teams
    graph = defaultdict(lambda: defaultdict(set))
    grouped = df.groupby(["Season", "Team"])
    
    for (season, team), group in grouped:
        players = group["Player Name"].dropna().str.strip().unique().tolist()
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                p1, p2 = players[i], players[j]
                graph[p1][p2].add((season, team))
                graph[p2][p1].add((season, team))
    
    print("CourtConnector built successfully!")
    return graph

def find(graph, start, end):
    # finds the shortest path from start to end in the graph
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
    # formats the seasons and teams
    team_to_years = defaultdict(set)
    formatted = []

    for season, team in seasons:
        year = int(season[:4])
        team_to_years[team].add(year)
    
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
    # prints the connection between players in the path
    if not path:
        return False
    for i in range(len(path) - 1):
        player1, player2 = path[i], path[i + 1]
        seasons = graph[player1][player2]
        print(f"{player1} ➝  {player2} ({format(seasons)})")

def fuzzymatch(input, players):
    # uses fuzzy matching to find the closest match to the input
    original_names = {p.lower(): p for p in players}
    matches = process.extract(input.lower(), original_names.keys(), limit=5, score_cutoff=60)
    if not matches:
        return None, []
    best_match = original_names[matches[0][0]]
    suggestions = [(original_names[name], score) for name, score, _ in matches]
    return best_match, suggestions

def inputprompt(prompt, player_names):
    # prompts the user for input and handles fuzzy matching
    name_lookup = {name.lower(): name for name in player_names}

    while True:
        raw = input(prompt).strip()
        if raw in player_names:
            return raw
        if raw.lower() in name_lookup:
            return name_lookup[raw.lower()]

        _, suggestions = fuzzymatch(raw, player_names)

        for name, score in suggestions:
            if score >= 100.0:
                return name

        if not suggestions:
            print(f"No close matches found for '{raw}'\n")
            continue

        print("\nDid you mean one of these?")
        for i, (name, score) in enumerate(suggestions[:3], 1):
            print(f"{i}. {name} ({score:.1f}%)")

        choice = input("Select 1-3 or retype a name: ").strip()
        if choice in {"1", "2", "3"}:
            return suggestions[int(choice) - 1][0]
        elif choice in player_names:
            return choice
        elif choice.lower() in name_lookup:    
            return name_lookup[choice.lower()]         
        else:
            raw = choice

def main():
    print("""\033[1m 
   ____                 _    ____                            _   
  / ___|___  _   _ _ __| |_ / ___|___  _ __  _ __   ___  ___| |_ 
 | |   / _ \| | | | '__| __| |   / _ \| '_ \| '_ \ / _ \/ __| __|
 | |__| (_) | |_| | |  | |_| |__| (_) | | | | | | |  __/ (__| |_ 
  \____\___/ \__,_|_|   \__|\____\___/|_| |_|_| |_|\___|\___|\__|                                                  
    \033[0m""")
    print("Loading NBA player data...")
    df = pd.read_csv("nba_players.csv")
    players = df["Player Name"].unique().tolist()
    graph = build(df)
    mode = input("Enter 'C' for CourtConnection or 'T' for Three-Man Weave: ").strip().upper()
    
    # CourtConnection Mode
    if mode == 'C':
        playerA = inputprompt("Enter Player A: ", players)
        playerB = inputprompt("Enter Player B: ", players)
        if not playerA or not playerB or playerA == playerB:
            print("Invalid player names provided.")
            return

        path = find(graph, playerA, playerB)
        if path:
            print("\nCourtConnection:")
            connection(graph, path)
        else:
            print(f"No CourtConnection between {playerA} and {playerB} found.")

    # Three-Man Weave Mode
    elif mode == 'T':
        playerA = inputprompt("Enter Player A: ", players)
        playerB = inputprompt("Enter Player B: ", players)
        playerC = inputprompt("Enter Player C: ", players)
        if not playerA or not playerB or not playerC or playerA == playerB or playerB == playerC or playerA == playerC:
            print("Invalid player names provided.")
            return
        
        path1 = find(graph, playerA, playerB)
        path2 = find(graph, playerB, playerC)
        if path1 and path2:
            print("\nThree-Man Weave:")
            connection(graph, path1)
            connection(graph, path2)
        else:
            print(f"No Three-Man Weave between {playerA}, {playerB}, and {playerC} found.")
            return
    else:
        print("Invalid mode selected. Please enter 'C' or 'T'.")
        return

if __name__ == "__main__":
    main()
