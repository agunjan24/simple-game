# Bollywood Frames - Future Ideas

Party game improvement ideas for future development.

---

## Scoring & Competition

| Feature | Description | Priority |
|---------|-------------|----------|
| **Points system** | Award points based on speed: 100 pts if guessed in first 20s, 50 pts in next 20s, 25 pts in final 20s | High |
| **Streak bonus** | Consecutive correct guesses multiply points (2x, 3x...) | Medium |
| **Leaderboard** | Track high scores locally, show "Beat the high score!" | Medium |
| **Team mode** | Split into teams, alternate turns, track team scores | Low |

---

## Gameplay Enhancements

| Feature | Description | Priority |
|---------|-------------|----------|
| **"I Know It!" button** | Player claims to know answer → stops timer → if wrong, penalty | High |
| **Progressive reveal** | Image starts blurry/zoomed, gradually clears over 60s | Medium |
| **Lifelines** | "50/50" shows 2 choices, "Decade hint" shows release year | Medium |
| **Difficulty levels** | Easy (popular films), Medium (cult classics), Hard (obscure) | Low |

---

## Party Atmosphere

| Feature | Description | Priority |
|---------|-------------|----------|
| **Sound effects** | Tick-tock urgency, victory fanfare, wrong-answer buzzer | Medium |
| **Answer input** | Let players type guess (fuzzy match) instead of just reveal | High |
| **Round summary** | After each movie, show stats: "Guessed in 12s! +100 pts" | Medium |
| **Final scoreboard** | Animated results with rankings, "MVP" badge | Low |

---

## Quick Wins (Easy to Implement)

- [ ] **Add "SKIP" button** - forfeit points but move on (for stuck moments)
- [ ] **Show movie count** - "Movie 3 of 10" in header
- [ ] **Configurable game length** - "Quick (5)", "Standard (10)", "Marathon (all)"
- [ ] **Category filters** - Romance, Action, Comedy, 90s, 2000s, etc.

---

## Top 3 Recommendations

1. **Points + Speed bonus** - Creates urgency and competition
2. **"I Know It!" button** - Adds risk/reward excitement
3. **Movie progress indicator** - "3/10" gives pacing awareness

---

## Implementation Notes

- Points system requires adding `score` to `GameState` class
- Category filters require adding `category` column to `data.csv`
- Sound effects already have basic infrastructure (AudioContext in JS)
- Team mode would need significant UI changes

---

*Last updated: January 2026*
