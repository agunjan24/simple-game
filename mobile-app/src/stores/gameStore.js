import { defineStore } from 'pinia'
import { THEMES } from '../themes/themes.js'
import bollywoodData from '../data/bollywood.json'
import hollywoodData from '../data/hollywood.json'

const DEFAULT_DURATION = 25
const DEFAULT_THEME = 'bollywood'

const DATA_MAP = {
  bollywood: bollywoodData,
  hollywood: hollywoodData,
}

export const useGameStore = defineStore('game', {
  state: () => ({
    theme: DEFAULT_THEME,
    validMovies: [],
    shownMovies: [],
    currentMovie: null,
    timeLeft: DEFAULT_DURATION,
    timerActive: false,
    soloDuration: DEFAULT_DURATION,
    timerDuration: 45,
    showHint: false,
    showAnswer: false,
    hintUsed: false,
    awaitingScore: false,
    gameOver: false,
    score: 0,
    currentScreen: 'welcome',
    teamMode: false,
    currentTeam: 0,
    teamScores: [0, 0],
    teamNames: ['Team A', 'Team B'],
    progressiveReveal: true,
  }),

  getters: {
    themeConfig: (state) => THEMES[state.theme],
    themeColors: (state) => THEMES[state.theme].colors,
    remainingCount: (state) => state.validMovies.length - state.shownMovies.length,
    totalCount: (state) => state.validMovies.length,
    shownCount: (state) => state.shownMovies.length,

    currentBlur: (state) => {
      if (!state.progressiveReveal) return 0
      const total = state.teamMode ? state.timerDuration : state.soloDuration
      if (state.timeLeft <= 10) return 0
      const ratio = (state.timeLeft - 10) / (total - 10)
      return Math.round(ratio * 100) / 10 // max 10px
    },

    hintText: (state) => {
      if (!state.currentMovie) return ''
      const hint = state.currentMovie.hint
      if (!hint || hint === 'No hint') {
        const name = state.currentMovie.movie_name
        return `Starts with '${name[0]}' \u2022 ${name.length} characters`
      }
      return hint
    },

    currentTeamName: (state) => state.teamNames[state.currentTeam],

    winner: (state) => {
      if (state.teamScores[0] > state.teamScores[1]) return { index: 0, tie: false }
      if (state.teamScores[1] > state.teamScores[0]) return { index: 1, tie: false }
      return { index: -1, tie: true }
    },

    currentTimerDuration: (state) => {
      return state.teamMode ? state.timerDuration : state.soloDuration
    },
  },

  actions: {
    _loadThemeData() {
      this.validMovies = DATA_MAP[this.theme] || []
    },

    init() {
      this._loadThemeData()
      this.randomizeTeamNames()
    },

    setTheme(name) {
      if (!(name in THEMES)) return
      this.theme = name
      this._loadThemeData()
      this.randomizeTeamNames()
      this.shownMovies = []
    },

    nextMovie() {
      const available = this.validMovies.filter(
        (m) => !this.shownMovies.includes(m.filename)
      )
      if (available.length > 0) {
        this.currentMovie = available[Math.floor(Math.random() * available.length)]
        this.shownMovies.push(this.currentMovie.filename)
        this.timeLeft = this.teamMode ? this.timerDuration : this.soloDuration
        this.showHint = false
        this.showAnswer = false
        this.hintUsed = false
        this.awaitingScore = false
        this.gameOver = false
        this.timerActive = false
        return true
      } else {
        this.gameOver = true
        this.currentMovie = null
        this.timerActive = false
        this.currentScreen = 'gameover'
        return false
      }
    },

    resetGame() {
      this.shownMovies = []
      this.gameOver = false
      this.score = 0
      this.currentScreen = 'game'
      if (this.teamMode) {
        this.teamScores = [0, 0]
        this.currentTeam = 0
      }
      this.nextMovie()
    },

    randomizeTeamNames() {
      const pairs = THEMES[this.theme].teamNames
      this.teamNames = [...pairs[Math.floor(Math.random() * pairs.length)]]
    },

    switchTeam() {
      this.currentTeam = 1 - this.currentTeam
    },

    calculatePoints(correct) {
      if (!correct) return 0
      const duration = this.teamMode ? this.timerDuration : this.soloDuration
      const timeRatio = this.timeLeft / duration

      let points
      if (timeRatio > 0.66) points = 100
      else if (timeRatio > 0.33) points = 75
      else points = 50

      if (this.hintUsed) points = Math.max(0, points - 25)
      return points
    },

    awardPoints(correct) {
      const points = this.calculatePoints(correct)
      if (this.teamMode) {
        this.teamScores[this.currentTeam] += points
      } else {
        this.score += points
      }
      return points
    },
  },
})
