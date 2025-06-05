# 🏀 courtconnect 
    An algorithm connecting any two NBA players through mutual teammates
  
> Input:  
> `Kobe Bryant, LeBron James`  
> Output:   
> `Kobe Bryant ➝ Shaquille O'Neal (LAL 2003–2004)`   
> `Shaquille O'Neal ➝ LeBron James (CLE 2009-2010)`

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


---

## 🛠️ Future Implementations

- Extend dataset to include more NBA seasons
- Fuzzy matching for misspelling and accents on user queries
- Weighted connection graph prioritzing more meaningful connections