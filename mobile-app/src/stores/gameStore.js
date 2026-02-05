import { defineStore } from 'pinia'
import { Capacitor } from '@capacitor/core'
import { StatusBar, Style } from '@capacitor/status-bar'
import { THEMES } from '../themes/themes.js'
import bollywoodData from '../data/bollywood.json'
import hollywoodData from '../data/hollywood.json'
import historyData from '../data/history.json'

function updateStatusBar(themeName) {
  if (!Capacitor.isNativePlatform()) return
  const colors = THEMES[themeName].colors
  StatusBar.setStyle({ style: Style.Dark })
  StatusBar.setBackgroundColor({ color: colors.bgDark })
}

const DEFAULT_DURATION = 25
const DEFAULT_THEME = 'bollywood'

const DATA_MAP = {
  bollywood: bollywoodData,
  hollywood: hollywoodData,
  history: historyData,
}

export const useGameStore = defineStore('game', {
  state: () => ({
    theme: DEFAULT_THEME,
    validItems: [],
    shownItems: [],
    currentItem: null,
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
    // Feature 1: History navigation (review mode)
    reviewingItem: null,
    savedTimeLeft: null,
    savedTimerActive: false,
    // Feature 2: Timer pause
    timerPaused: false,
    // Feature 3: Image click to clear blur
    imageRevealed: false,
  }),

  getters: {
    themeConfig: (state) => THEMES[state.theme],
    themeColors: (state) => THEMES[state.theme].colors,
    remainingCount: (state) => state.validItems.length - state.shownItems.length,
    totalCount: (state) => state.validItems.length,
    shownCount: (state) => state.shownItems.length,

    currentBlur: (state) => {
      if (!state.progressiveReveal) return 0
      // Feature 2 & 3: Instant clear when timer paused or image revealed
      if (state.timerPaused || state.imageRevealed) return 0
      const total = state.teamMode ? state.timerDuration : state.soloDuration
      if (state.timeLeft <= 10) return 0
      const ratio = (state.timeLeft - 10) / (total - 10)
      return Math.round(ratio * 100) / 10 // max 10px
    },

    // Feature 1: Check if in review mode
    isReviewing: (state) => state.reviewingItem !== null,

    hintText: (state) => {
      if (!state.currentItem) return ''
      const hint = state.currentItem.hint
      if (!hint || hint === 'No hint') {
        const name = state.currentItem.title
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
      this.validItems = DATA_MAP[this.theme] || []
    },

    init() {
      this._loadThemeData()
      this.randomizeTeamNames()
      updateStatusBar(this.theme)
    },

    setTheme(name) {
      if (!(name in THEMES)) return
      this.theme = name
      this._loadThemeData()
      this.randomizeTeamNames()
      this.shownItems = []
      updateStatusBar(name)
    },

    nextItem() {
      const available = this.validItems.filter(
        (m) => !this.shownItems.includes(m.filename)
      )
      if (available.length > 0) {
        this.currentItem = available[Math.floor(Math.random() * available.length)]
        this.shownItems.push(this.currentItem.filename)
        this.timeLeft = this.teamMode ? this.timerDuration : this.soloDuration
        this.showHint = false
        this.showAnswer = false
        this.hintUsed = false
        this.awaitingScore = false
        this.gameOver = false
        this.timerActive = false
        // Reset Feature 2 & 3 state for new item
        this.timerPaused = false
        this.imageRevealed = false
        return true
      } else {
        this.gameOver = true
        this.currentItem = null
        this.timerActive = false
        this.currentScreen = 'gameover'
        return false
      }
    },

    resetGame() {
      this.shownItems = []
      this.gameOver = false
      this.score = 0
      this.currentScreen = 'game'
      if (this.teamMode) {
        this.teamScores = [0, 0]
        this.currentTeam = 0
      }
      this.nextItem()
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
      // Feature 2 & 3: Timer paused or image revealed locks to last-third rate (50 points)
      if (this.timerPaused || this.imageRevealed) {
        points = 50
      } else if (timeRatio > 0.66) {
        points = 100
      } else if (timeRatio > 0.33) {
        points = 75
      } else {
        points = 50
      }

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

    // Feature 1: Enter review mode to view a previously shown item
    enterReview(index) {
      if (index < 0 || index >= this.shownItems.length - 1) return // Can't review current or future
      const filename = this.shownItems[index]
      const item = this.validItems.find((m) => m.filename === filename)
      if (!item) return

      // Save current game state
      this.savedTimeLeft = this.timeLeft
      this.savedTimerActive = this.timerActive
      this.reviewingItem = item
      // Pause timer while reviewing
      this.timerActive = false
    },

    // Feature 1: Exit review mode and return to current game
    exitReview() {
      if (!this.reviewingItem) return
      this.reviewingItem = null
      // Restore saved time but keep timer paused (user must click timer to resume)
      if (this.savedTimeLeft !== null) {
        this.timeLeft = this.savedTimeLeft
        this.savedTimeLeft = null
      }
      // Timer stays paused - user clicks timer to resume (consistent with Feature 2)
      this.savedTimerActive = false
    },
  },
})
