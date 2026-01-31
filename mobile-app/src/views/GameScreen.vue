<template>
  <div class="game-screen" :style="bgStyle">
    <div class="game-card">
      <!-- Film strip top -->
      <div class="film-strip" :style="filmStripStyle"></div>

      <div class="game-content">
        <!-- Header -->
        <div class="header-row">
          <div class="header-left">
            <h2 class="game-title">🎬 GUESS THE MOVIE</h2>
            <!-- Progress dots -->
            <div class="progress-dots">
              <span
                v-for="i in store.totalCount"
                :key="i"
                :class="['dot', i - 1 < store.shownCount - 1 ? 'completed' : '', i - 1 === store.shownCount - 1 ? 'current' : '']"
                :style="dotStyle(i - 1)"
              ></span>
            </div>
          </div>
          <div class="timer-circle">
            <div class="timer-inner">
              <span class="timer-text">{{ timerDisplay }}</span>
            </div>
          </div>
        </div>

        <!-- Team turn indicator -->
        <div v-if="store.teamMode" class="turn-indicator">
          <span class="turn-badge" :style="turnBadgeStyle">
            ✨ {{ store.currentTeamName }}'s Turn ✨
          </span>
        </div>

        <!-- Image area -->
        <div class="image-area">
          <img
            v-if="store.currentMovie"
            :src="imageSrc"
            :style="imageStyle"
            class="movie-image"
            @load="onImageLoad"
            @error="onImageError"
          />
          <!-- Countdown overlay -->
          <div v-if="countdownText" class="countdown-overlay" :class="{ clock: countdownText === '⏰' }">
            {{ countdownText }}
          </div>
        </div>

        <!-- Control buttons -->
        <div class="control-buttons">
          <button class="game-btn btn-hint" :style="hintBtnStyle" @click="showHint">💡 HINT</button>
          <button class="game-btn btn-reveal" :style="revealBtnStyle" @click="revealAnswer">🎬 REVEAL</button>
          <button class="game-btn btn-next" :style="nextBtnStyle" @click="nextMovie">
            {{ store.remainingCount > 0 ? '▶ NEXT' : '🏆 FINISH' }}
          </button>
        </div>

        <!-- Scoring buttons (team mode after reveal) -->
        <div v-if="store.teamMode && store.awaitingScore" class="scoring-buttons">
          <button class="score-btn correct" @click="scoreAnswer(true)">✓</button>
          <button class="score-btn wrong" @click="scoreAnswer(false)">✗</button>
        </div>

        <!-- Hint -->
        <div v-if="store.showHint && store.currentMovie" class="hint-box" :style="hintBoxStyle">
          💡 {{ store.hintText }}
        </div>

        <!-- Team scoreboard -->
        <div v-if="store.teamMode" class="scoreboard">
          <div
            :class="['team-score', store.currentTeam === 0 ? 'active' : '']"
            :style="store.currentTeam === 0 ? { border: '2px solid #E91E63', background: 'rgba(233,30,99,0.2)' } : {}"
          >
            <span class="team-label" style="color: #E91E63;">🔴 {{ store.teamNames[0] }}</span>
            <span class="team-points">{{ store.teamScores[0] }}</span>
          </div>
          <span class="vs-divider">vs</span>
          <div
            :class="['team-score', store.currentTeam === 1 ? 'active' : '']"
            :style="store.currentTeam === 1 ? { border: '2px solid #2196F3', background: 'rgba(33,150,243,0.2)' } : {}"
          >
            <span class="team-label" style="color: #2196F3;">🔵 {{ store.teamNames[1] }}</span>
            <span class="team-points">{{ store.teamScores[1] }}</span>
          </div>
        </div>
        <!-- Answer -->
        <div v-if="store.showAnswer && store.currentMovie" class="answer-box" :style="answerBoxStyle">
          🎬 {{ store.currentMovie.movie_name }}
        </div>
      </div>

      <!-- Film strip bottom -->
      <div class="film-strip" :style="filmStripStyle"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/gameStore.js'
import { useTimer } from '../composables/useTimer.js'
import { useAudio } from '../composables/useAudio.js'

const store = useGameStore()
const router = useRouter()
const { start, stop } = useTimer(store)
const { playTick } = useAudio()

const countdownText = ref('')
let countdownTimeout = null

const colors = computed(() => store.themeColors)
const config = computed(() => store.themeConfig)

const bgStyle = computed(() => ({
  background: `
    radial-gradient(ellipse at top, ${colors.value.primary}1a 0%, transparent 50%),
    radial-gradient(ellipse at bottom, ${colors.value.accent}1a 0%, transparent 50%),
    linear-gradient(180deg, ${colors.value.bgDark} 0%, ${colors.value.bgMid} 50%, ${colors.value.bgLight} 100%)`,
  minHeight: '100vh',
}))

const filmStripStyle = computed(() => ({
  background: `repeating-linear-gradient(90deg, ${colors.value.bgMid} 0px, ${colors.value.bgMid} 10px, ${colors.value.primary} 10px, ${colors.value.primary} 12px, ${colors.value.bgMid} 12px, ${colors.value.bgMid} 22px)`,
}))

const imageSrc = computed(() => {
  if (!store.currentMovie) return ''
  return `/${config.value.imageFolder}/${store.currentMovie.filename}`
})

const imageStyle = computed(() => {
  const blur = store.showAnswer ? 0 : store.currentBlur
  return {
    filter: `blur(${blur}px)`,
    transition: 'filter 0.3s ease-out',
  }
})

const timerDisplay = computed(() => {
  const m = Math.floor(store.timeLeft / 60)
  const s = store.timeLeft % 60
  return `${m}:${s.toString().padStart(2, '0')}`
})

const timerStyle = computed(() => ({
  borderColor: store.timeLeft <= 10 ? colors.value.accent : colors.value.primary,
}))

const turnBadgeStyle = computed(() => {
  const grad = store.currentTeam === 0
    ? 'linear-gradient(135deg, #E91E63, #C2185B)'
    : 'linear-gradient(135deg, #2196F3, #1565C0)'
  return { background: grad }
})

const btnStyle = computed(() => ({
  background: '#6495ED',
  color: '#fff',
  borderColor: '#6495ED',
}))
const hintBtnStyle = btnStyle
const revealBtnStyle = btnStyle
const nextBtnStyle = btnStyle
const hintBoxStyle = computed(() => ({
  background: 'rgba(255, 248, 231, 0.8)',
  color: colors.value.textDark,
}))
const answerBoxStyle = computed(() => ({
  background: '#E8F5E9',
  color: '#1A0A14',
  border: `2px solid ${colors.value.secondary}`,
}))

function dotStyle(i) {
  if (i < store.shownCount - 1) return { background: colors.value.primary }
  if (i === store.shownCount - 1) return { background: colors.value.accent }
  return {}
}

// Watch timer for countdown overlay and tick sounds
watch(() => store.timeLeft, (tl) => {
  if (!store.timerActive) return

  if (tl <= 10 && tl > 0) {
    countdownText.value = String(tl)
    playTick(tl)
  } else if (tl <= 0) {
    stop()
    store.showAnswer = true
    countdownText.value = '⏰'
    countdownTimeout = setTimeout(() => { countdownText.value = '' }, 2000)
  } else {
    countdownText.value = ''
  }
})

function onImageLoad() {
  if (!store.timerActive && !store.showAnswer && !store.gameOver) {
    start()
  }
}

function onImageError() {
  // Skip to next if image fails
  store.nextMovie()
}

function showHint() {
  store.showHint = true
  store.hintUsed = true
}

function revealAnswer() {
  store.showAnswer = true
  stop()
  countdownText.value = ''
  if (store.teamMode) {
    store.awaitingScore = true
  }
}

function scoreAnswer(correct) {
  store.awardPoints(correct)
  store.awaitingScore = false
  proceedToNext()
}

function proceedToNext() {
  if (store.teamMode) store.switchTeam()
  if (store.remainingCount > 0) {
    store.nextMovie()
    countdownText.value = ''
  } else {
    store.gameOver = true
    store.currentScreen = 'gameover'
    router.push('/gameover')
  }
}

function nextMovie() {
  if (store.teamMode && store.awaitingScore) return
  if (store.teamMode && !store.showAnswer) store.awardPoints(false)
  stop()
  proceedToNext()
}

onUnmounted(() => {
  stop()
  if (countdownTimeout) clearTimeout(countdownTimeout)
})
</script>

<style scoped>
.game-screen {
  display: flex;
  justify-content: center;
  padding: 8px;
  min-height: 100vh;
}

.game-card {
  background: linear-gradient(145deg, rgba(255, 248, 231, 0.98), rgba(255, 248, 231, 0.92));
  border-radius: 24px;
  box-shadow:
    0 25px 50px rgba(0, 0, 0, 0.4),
    0 0 100px v-bind('colors.primary + "33"'),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 2px solid v-bind('colors.primary + "4d"');
  max-width: 850px;
  width: 100%;
  overflow: hidden;
  align-self: flex-start;
}

.film-strip {
  height: 12px;
  width: 100%;
}

.game-content {
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.game-title {
  font-family: 'Rozha One', serif;
  font-size: clamp(1rem, 4vw, 1.5rem);
  margin: 0;
  letter-spacing: 1px;
  background: linear-gradient(
    90deg,
    v-bind('colors.primaryDark') 0%,
    v-bind('colors.primary') 25%,
    v-bind('colors.primaryDark') 50%,
    v-bind('colors.primary') 75%,
    v-bind('colors.primaryDark') 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: primaryShimmer 3s linear infinite;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
}

.progress-dots {
  display: flex;
  gap: 6px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: v-bind('colors.primary + "4d"');
  transition: all 0.3s ease;
}

.dot.completed {
  box-shadow: 0 0 8px v-bind('colors.primary + "80"');
}

.dot.current {
  box-shadow: 0 0 12px v-bind('colors.accent + "99"');
  animation: glowPulse 2s infinite;
}

.timer-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  padding: 3px;
  background: linear-gradient(145deg, v-bind('colors.primary'), v-bind('colors.primaryDark'));
  box-shadow: 0 4px 20px v-bind('colors.primary + "80"'), inset 0 2px 4px rgba(255, 255, 255, 0.3);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.timer-inner {
  width: 100%;
  height: 100%;
  background: linear-gradient(145deg, v-bind('colors.bgMid'), v-bind('colors.bgLight'));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timer-text {
  font-family: 'Poppins', sans-serif;
  font-size: 1.2rem;
  font-weight: 800;
  color: v-bind('colors.primary');
}

.turn-indicator {
  display: flex;
  justify-content: center;
}

.turn-badge {
  color: white;
  font-size: clamp(0.8rem, 3vw, 1rem);
  font-weight: 700;
  padding: 6px 16px;
  border-radius: 25px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.image-area {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 150px;
  padding: 4px 0 14px 0;
}

.movie-image {
  max-width: 100%;
  max-height: min(60vh, 500px);
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.countdown-overlay {
  position: absolute;
  font-family: 'Rozha One', serif;
  font-size: 6rem;
  font-weight: 400;
  color: v-bind('colors.accent');
  text-shadow:
    0 0 40px v-bind('colors.accent + "cc"'),
    0 0 80px v-bind('colors.accent + "66"'),
    0 4px 0 v-bind('colors.accentDark');
  z-index: 100;
  pointer-events: none;
  animation: countdownPulse 1s ease-in-out infinite;
}

.countdown-overlay.clock {
  font-size: 4rem;
  text-shadow: none;
}

.control-buttons {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.game-btn {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 0.75rem;
  padding: 8px 18px;
  border-radius: 25px;
  border: 2px solid;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  -webkit-touch-callout: none;
  user-select: none;
}

.game-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4), 0 0 20px v-bind('colors.primary + "66"');
}

.game-btn:active {
  transform: translateY(0) scale(0.98);
}

@media (pointer: coarse) {
  .game-btn:active { transform: scale(0.95); }
}

.scoring-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
  animation: floatUp 0.3s ease-out;
}

.score-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  font-size: 1.4rem;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  touch-action: manipulation;
  transition: transform 0.2s;
}

.score-btn:hover { transform: scale(1.1); }
.score-btn:active { transform: scale(0.9); }

.score-btn.correct {
  background: white;
  color: #2E7D32;
  border: 3px solid #4CAF50;
}

.score-btn.wrong {
  background: white;
  color: #C62828;
  border: 3px solid #F44336;
}

.hint-box {
  padding: 8px 16px;
  border-radius: 12px;
  text-align: left;
  font-size: clamp(0.8rem, 2.5vw, 1rem);
  border: 2px solid v-bind('colors.primary');
  animation: floatUp 0.5s ease-out;
}

.answer-box {
  padding: 12px 16px;
  border-radius: 12px;
  text-align: left;
  font-size: clamp(0.9rem, 3.5vw, 1.5rem);
  font-weight: 700;
  font-family: 'Rozha One', serif;
  animation: floatUp 0.5s ease-out;
}

.scoreboard {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.team-score {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: 6px;
  border: 2px solid transparent;
  background: rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.team-label {
  font-weight: 700;
  font-size: clamp(0.7rem, 2.5vw, 0.85rem);
  white-space: nowrap;
}

.team-points {
  font-size: clamp(0.9rem, 3vw, 1.1rem);
  font-weight: 700;
  color: #1A0A14;
}

.vs-divider {
  color: #888;
  font-weight: 700;
  font-size: 0.8rem;
}

@media (max-width: 640px) {
  .game-card { border-radius: 12px; }
  .game-content { padding: 6px 8px; }
  .game-btn {
    padding: 6px 10px;
    font-size: 0.7rem;
    border-radius: 20px;
    border-width: 1px;
    letter-spacing: 0;
  }
  .timer-circle { width: 48px; height: 48px; }
  .timer-text { font-size: 0.95rem; }
  .movie-image {
    max-height: 50vh;
  }
  .countdown-overlay { font-size: 4rem; }
  .film-strip { height: 6px; }
  .dot { width: 8px; height: 8px; }
  .progress-dots { gap: 4px; }
  .hint-box { padding: 4px 8px; border-radius: 6px; }
  .answer-box { padding: 8px 8px; }
}
</style>
