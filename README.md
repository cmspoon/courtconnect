# courtconnect 🏀
    A Python CLI algorithm connecting any two NBA players through mutual teammates
  
> Input:  
> `Kobe Bryant, LeBron James`  
> Output:   
> `Kobe Bryant ➝ Shaquille O'Neal (LAL 2003–2004)`   
> `Shaquille O'Neal ➝ LeBron James (CLE 2009-2010)`

---

## Dataset

The dataset, `nba_players.csv`, currently covers **NBA seasons from 2003–04 to 2023–24**, totaling over 12,000 player-season-team entries: 
- Player 
- Team
- Season

---

## Known Challenges

- Players appearing on multiple teams in the same season
- Players who were on a roster but didn’t play due to injury
- Players with names containing accents or non-ASCII characters (e.g., Luka Dončić) may not import correctly

These are addressed as the dataset is cleaned.

---

## Future Implementations

- Path Caching - Store previously searched paths to avoid redundancy and improve performance.
- Dataset Expansion - Extend dataset coverage to include seasons prior to 2003–04.
- Weighted Connections - Prioritize more meaningful connections by weighting superstar status, longevity, and team relevance.
- GUI Makeover - Transition to a more polished display