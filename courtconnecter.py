import pandas as pd

def build_teammate_graph(df: pd.DataFrame):
    print("Building CourtConnector...")
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

                graph[p1][p2].add(season)
                graph[p2][p1].add(season)

    print("CourtConnector built successfully.")
    return graph

def condense_seasons(seasons: set[str]) -> list[str]:
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
            start = prev = year

    condensed.append(f"{start}–{prev+1 if prev > start else start+1}")
    return condensed

df = pd.read_csv("nba_players.csv")
graph = build_teammate_graph(df)

query = input("Enter any NBA player's name (First Last): ")
if query not in graph:
    print(f"No data found for {query}.")
    exit()
for teammate, seasons in graph[query].items():
    print(f"{teammate}: {', '.join(condense_seasons(seasons))}")

