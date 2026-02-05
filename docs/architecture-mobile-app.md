# Mobile App — Implementation Status

## Progress

| Phase | Description | Status |
|-------|------------|--------|
| 1 | Project setup (Vue 3 + Vite + Pinia + Router) | Done |
| 2 | Core game logic (Pinia store, composables, data) | Done |
| 3 | UI components (Welcome, Game, GameOver screens) | Done |
| 4 | CSS/Styling (cinematic theme, animations, responsive) | Done |
| 5 | Capacitor integration (native Android/iOS shell) | Not started |
| 6 | App store prep (icons, splash, signing, metadata) | Not started |

## What's Built

### Project structure
```
mobile-app/
├── package.json              # vue, vue-router, pinia, vite
├── vite.config.js
├── index.html                # Google Fonts (Rozha One + Poppins)
├── public/
│   ├── images/               # 10 Bollywood screenshots (copied)
│   └── images_hollywood/     # 12 Hollywood screenshots (copied)
└── src/
    ├── main.js               # App bootstrap, Pinia init, global CSS import
    ├── App.vue               # <router-view />
    ├── router.js             # / → Welcome, /game → Game, /gameover → GameOver
    ├── assets/
    │   └── global.css        # Shared animations & keyframes
    ├── data/
    │   ├── bollywood.json    # 10 movies (from data.csv)
    │   └── hollywood.json    # 12 movies (from data_hollywood.csv)
    ├── themes/
    │   └── themes.js         # THEMES dict (colors, teamNames, phrases)
    ├── stores/
    │   └── gameStore.js      # Pinia store (full GameState port)
    ├── composables/
    │   ├── useTimer.js       # start/stop/reset with setInterval
    │   ├── useAudio.js       # playTick (last 10s), playVictory
    │   └── useConfetti.js    # DOM confetti burst
    └── views/
        ├── WelcomeScreen.vue # Theme toggle, solo/team, timer config, progressive reveal
        ├── GameScreen.vue    # Image + blur, timer, HINT/REVEAL/NEXT, scoring, scoreboard
        └── GameOverScreen.vue # Trophy, winner/tie, scores, confetti, play again
```

### Key decisions made
- **Timer default**: 25 seconds (solo), 45 seconds (team) — both configurable on welcome screen (15-120s range)
- **Styling**: Uses Vue `v-bind()` in `<style scoped>` for theme-reactive CSS (no CSS custom properties on `:root`)
- **Data**: Static JSON imports instead of CSV/Pandas — no image file validation needed (trusted data)
- **Node.js**: Installed as standalone extraction at `C:\nodejs\node-v22.13.1-win-x64` (not in system PATH)

### How to run
```bash
# Add Node to PATH for this session
set PATH=C:\nodejs\node-v22.13.1-win-x64;%PATH%

cd mobile-app
npm install      # first time only
npm run dev      # http://localhost:5173 (or next available port)
npm run build    # produces dist/
```

## What's Next — Phase 5: Capacitor Integration

### Steps
1. Install Capacitor: `npm install @capacitor/core @capacitor/cli`
2. Initialize: `npx cap init "Bollywood Frames" "com.bollywoodframes.app"`
3. Add Android: `npx cap add android`
4. Add iOS: `npx cap add ios` (requires macOS + Xcode)
5. Build + sync: `npm run build && npx cap sync`
6. Open in Android Studio: `npx cap open android`
7. Test on emulator or device

### Prerequisites
- **Android**: Android Studio installed with SDK
- **iOS**: macOS with Xcode (cannot build on Windows)

## Phase 6: App Store Prep (later)

- App icon (1024x1024 master, Capacitor generates all sizes)
- Splash screen
- Android signing key (`keytool` → `.keystore`)
- iOS provisioning profile (Apple Developer account)
- Store listing: screenshots, description, category, rating

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                  Distribution                    │
│  Browser (Web)  │  Google Play  │  App Store     │
└────────┬────────┴───────┬──────┴───────┬────────┘
         │           Capacitor Shell      │
         │        (Android / iOS WebView) │
         └────────────────┬───────────────┘
                          │
              Same Vue 3 App (all platforms)
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    WelcomeScreen    GameScreen     GameOverScreen
         │                │                │
         └────────────────┼────────────────┘
                          │
                    Pinia gameStore
                 (theme, movies, timer,
                  scoring, blur, teams)
                          │
              ┌───────────┼───────────┐
              │           │           │
         useTimer    useAudio    useConfetti
              │           │           │
         themes.js   bollywood.json   hollywood.json
```
