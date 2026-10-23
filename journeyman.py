from os import path
import random
import pandas as pd
from collections import defaultdict
from courtconnector import build, find, format, inputprompt
from graph import display_graph

def matchup(graph, players, min_hops=2, max_hops=4):
    print("Generating matchup...", end="\r")
    while True:
        p1, p2 = random.sample(players, 2)
        path = find(graph, p1, p2)
        if path and min_hops <= (len(path) - 1) <= max_hops:
            return p1, p2, path


def game():
    print(r""" 
   __                                                            
   \ \  ___  _   _ _ __ _ __   ___ _   _ _ __ ___   __ _ _ __   
    \ \/ _ \| | | | '__| '_ \ / _ \ | | | '_ ` _ \ / _` | '_ \ 
 /\_/ / (_) | |_| | |  | | | |  __/ |_| | | | | | | (_| | | | |
 \___/ \___/ \__,_|_|  |_| |_|\___|\__, |_| |_| |_|\__,_|_| |_|
                                   |___/                        
    """)
    print("Loading NBA player data...")
    df = pd.read_csv("nba_players.csv")
    players = df["Player Name"].dropna().str.strip().unique().tolist()
    graph = build(df)
    
    start, target, optimal_path = matchup(graph, players)
    optimal_hops = len(optimal_path) - 1
    
    discovered_nodes = {start, target}
    board_graph = defaultdict(set)
    guesses = []
    
    print(f"\nConnect \033[1m{start}\033[0m -> \033[1m{target}\033[0m")
    print(f"Optimal Journey: {optimal_hops} links\n")

    # Initial graph render before first guess
    display_graph(board_graph, discovered_nodes, start, target)

    while True:
        completed_path = find(board_graph, start, target)
        if completed_path:
            user_hops = len(completed_path) - 1
            print(f"\nJourney complete in {len(guesses)} guesses!")
            for i in range(len(completed_path) - 1):
                p1, p2 = completed_path[i], completed_path[i+1]
                szns = format(graph[p1][p2])
                print(f"   {p1} -> {p2} ({szns})")
                
            if user_hops == optimal_hops:
                print(f"\nOptimal journey reached ({optimal_hops} hops)")
            else:
                print(f"\nOptimal Journey: {' -> '.join(optimal_path)}")
            break

        guess = inputprompt(f"[{len(guesses)+1}] Enter player or 'quit': ", players)

        if guess == "quit":
            print("Exiting game")
            print(f"Optimal Journey ({optimal_hops} hops): {' -> '.join(optimal_path)}")
            break
        
        if guess in discovered_nodes:
            print(f"{guess} has already been guessed")
            continue
            
        guesses.append(guess)
        discovered_nodes.add(guess)
        
        new_links = []
        for node in list(discovered_nodes):
            if node != guess and node in graph.get(guess, {}):
                seasons = graph[guess][node]
                board_graph[guess].add(node)
                board_graph[node].add(guess)
                new_links.append((node, format(seasons)))
        
        if new_links:
            print(f"\nLINK FOUND! {guess} connects to:")
            for connected_player, szns in new_links:
                print(f"   -> {connected_player} ({szns})")
        else:
            print(f"\n{guess} added, but has no teammates on the graph yet.")

        display_graph(board_graph, discovered_nodes, start, target)

if __name__ == "__main__":
    game()