# courtconnect 🏀
    An algorithm connecting any two NBA players (past or present) through mutual teammates

> Example:  
> `Input: LeBron James, Kobe Bryant`  
> `Output: LeBron James ➝ Shaquille O'Neal ➝ Kobe Bryant`

---

## 📚 Dataset

The dataset currently covers **NBA seasons from 2003–04 to 2023–24**, totaling over 12,000 player-season-team entries. It is stored in `nba_players.csv` and includes:
- Player 
- Team
- Season

---

## 🚧 Known Challenges

- Players appearing on multiple teams in the same season
- Players who were on a roster but didn’t play due to injury
- Players with names containing accents or non-ASCII characters (e.g., Luka Dončić) may not import correctly

These are being addressed as the dataset is cleaned.
