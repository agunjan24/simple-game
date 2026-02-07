<template>
  <div class="gameover-screen" :style="bgStyle">
    <div class="game-card">
      <div class="celebration">
        <!-- Trophy -->
        <div class="trophy">🏆</div>

        <!-- Team mode results -->
        <template v-if="store.teamMode">
          <template v-if="winner.tie">
            <h1 class="result-title">IT'S A TIE!</h1>
            <p class="result-sub">Both teams are winners!</p>
          </template>
          <template v-else>
            <h1 class="result-title" :style="{ color: winnerColor }">
              {{ winnerEmoji }} {{ store.teamNames[winner.index] }} WINS!
            </h1>
            <p class="winner-phrase">"{{ winnerPhrase }}"</p>
          </template>

          <div class="decorative-stars" :style="{ color: colors.primary }">✦ ✦ ✦</div>

          <!-- Final scores -->
          <div class="final-scores">
            <div class="final-team">
              <span :style="{ color: '#E91E63', fontWeight: winner.index === 0 ? 800 : 600 }">🔴 {{ store.teamNames[0] }}</span>
              <span class="final-points" :style="{ fontSize: winner.index === 0 ? '2rem' : '1.5rem' }">{{ store.teamScores[0] }}</span>
              <span class="points-label">points</span>
            </div>
            <div class="final-team">
              <span :style="{ color: '#2196F3', fontWeight: winner.index === 1 ? 800 : 600 }">🔵 {{ store.teamNames[1] }}</span>
              <span class="final-points" :style="{ fontSize: winner.index === 1 ? '2rem' : '1.5rem' }">{{ store.teamScores[1] }}</span>
              <span class="points-label">points</span>
            </div>
          </div>

          <p v-if="!winner.tie" class="loser-phrase">
            {{ loserEmoji }} {{ loserPhrase }}
          </p>
        </template>

        <!-- Solo mode results -->
        <template v-else>
          <h1 class="result-title">{{ soloTitle }}</h1>
          <p class="result-sub">{{ store.soloCorrectCount }} / {{ store.soloResults.length }} {{ store.themeConfig.categoryLabelPlural.toLowerCase() }} correct</p>

          <!-- Score display -->
          <div class="solo-score-display">
            <span class="solo-score-number">{{ store.soloTotalPoints }}</span>
            <span class="points-label">points</span>
          </div>

          <!-- Accuracy bar -->
          <div class="accuracy-bar-container">
            <div class="accuracy-bar-track">
              <div class="accuracy-bar-fill" :style="accuracyBarStyle"></div>
            </div>
            <span class="accuracy-label">{{ store.soloAccuracy }}% accuracy</span>
          </div>

          <!-- Per-item breakdown -->
          <div class="breakdown-list">
            <div
              v-for="(item, idx) in store.soloResults"
              :key="item.filename"
              class="breakdown-row"
              :class="item.correct ? 'row-correct' : 'row-wrong'"
            >
              <span class="breakdown-index">{{ idx + 1 }}</span>
              <span class="breakdown-icon">{{ item.correct ? '✓' : '✗' }}</span>
              <span class="breakdown-title">{{ item.title }}</span>
              <span class="breakdown-points" :class="item.correct ? 'pts-green' : 'pts-red'">{{ item.correct ? '+' + item.points : '0' }}</span>
              <span v-if="item.guessMethod === 'voice'" class="breakdown-badge">🎙️</span>
              <span v-if="item.hintUsed" class="breakdown-badge">💡</span>
            </div>
          </div>
        </template>

        <div class="star-row">⭐ 🌟 ⭐ 🌟 ⭐</div>

        <button class="play-again-btn" :style="playAgainStyle" @click="playAgain">
          🎬 PLAY AGAIN
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/gameStore.js'
import { useAudio } from '../composables/useAudio.js'
import { useConfetti } from '../composables/useConfetti.js'

const store = useGameStore()
const router = useRouter()
const { playVictory } = useAudio()
const { createConfetti } = useConfetti()

const colors = computed(() => store.themeColors)
const winner = computed(() => store.winner)

const bgStyle = computed(() => ({
  background: `
    radial-gradient(ellipse at top, ${colors.value.primary}1a 0%, transparent 50%),
    radial-gradient(ellipse at bottom, ${colors.value.accent}1a 0%, transparent 50%),
    linear-gradient(180deg, ${colors.value.bgDark} 0%, ${colors.value.bgMid} 50%, ${colors.value.bgLight} 100%)`,
  minHeight: '100vh',
}))

const winnerColor = computed(() => winner.value.index === 0 ? '#E91E63' : '#2196F3')
const winnerEmoji = computed(() => winner.value.index === 0 ? '🔴' : '🔵')
const loserEmoji = computed(() => winner.value.index === 0 ? '🔵' : '🔴')

const winnerPhrase = computed(() => {
  const phrases = store.themeConfig.winnerPhrases
  return phrases[Math.floor(Math.random() * phrases.length)]
})

const loserPhrase = computed(() => {
  const phrases = store.themeConfig.loserPhrases
  return phrases[Math.floor(Math.random() * phrases.length)]
})

const soloTitle = computed(() => {
  const acc = store.soloAccuracy
  if (acc >= 80) return 'PICTURE PERFECT!'
  if (acc >= 50) return 'WELL PLAYED!'
  return 'KEEP TRYING!'
})

const accuracyBarStyle = computed(() => {
  const acc = store.soloAccuracy
  let color
  if (acc >= 70) color = '#4CAF50'
  else if (acc >= 40) color = '#FF9800'
  else color = '#F44336'
  return {
    width: `${acc}%`,
    background: color,
    transition: 'width 1s ease-out',
  }
})

const playAgainStyle = computed(() => {
  const p = colors.value.primary
  const r = parseInt(p.slice(1, 3), 16)
  const g = parseInt(p.slice(3, 5), 16)
  const b = parseInt(p.slice(5, 7), 16)
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
  return {
    background: `linear-gradient(135deg, ${colors.value.primary}, ${colors.value.primaryDark})`,
    color: luminance > 0.5 ? colors.value.textDark : colors.value.textLight,
  }
})

onMounted(() => {
  playVictory()
  const c = colors.value
  createConfetti([c.primary, c.accent, c.secondary, c.primaryLight])
})

function playAgain() {
  store.resetGame()
  router.push('/game')
}
</script>

<style scoped>
.gameover-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px;
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
  max-width: 500px;
  width: 100%;
}

.celebration {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 16px;
  gap: 8px;
  animation: floatUp 0.8s ease-out;
}

.trophy {
  font-size: 6rem;
  animation: glowPulse 2s infinite, trophyBounce 1.5s ease-in-out infinite;
}

.result-title {
  font-family: 'Rozha One', serif;
  font-size: clamp(1.3rem, 6vw, 2.2rem);
  margin: 0;
  text-align: center;
  white-space: nowrap;
}

.result-sub {
  color: #1A0A14;
  font-size: 1.3rem;
  opacity: 0.8;
  margin: 0;
}

.winner-phrase {
  color: #1A0A14;
  font-size: clamp(0.8rem, 3vw, 1rem);
  font-style: italic;
  opacity: 0.8;
  text-align: center;
  max-width: 300px;
  margin: 0;
}

.decorative-stars {
  font-size: 1rem;
  letter-spacing: 12px;
  margin: 8px 0;
}

.final-scores {
  display: flex;
  gap: 32px;
}

.final-team {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.final-points {
  color: #1A0A14;
  font-weight: 700;
}

.points-label {
  color: #666;
  font-size: 0.8rem;
}

.loser-phrase {
  color: #666;
  font-size: 0.85rem;
  font-style: italic;
  margin-top: 8px;
}

.star-row {
  font-size: 2rem;
  margin: 16px 0;
}

.play-again-btn {
  font-family: 'Poppins', sans-serif;
  padding: 18px 48px;
  border: none;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

.play-again-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4), 0 0 20px v-bind('colors.primary + "66"');
}

.play-again-btn:active {
  transform: translateY(0) scale(0.98);
}

/* Solo score display */
.solo-score-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}

.solo-score-number {
  font-family: 'Rozha One', serif;
  font-size: 3rem;
  font-weight: 700;
  color: #1A0A14;
  line-height: 1;
}

/* Accuracy bar */
.accuracy-bar-container {
  width: 100%;
  max-width: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.accuracy-bar-track {
  width: 100%;
  height: 10px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  overflow: hidden;
}

.accuracy-bar-fill {
  height: 100%;
  border-radius: 5px;
  min-width: 2px;
}

.accuracy-label {
  font-family: 'Poppins', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  color: #666;
}

/* Breakdown list */
.breakdown-list {
  width: 100%;
  max-width: 400px;
  max-height: 240px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 4px;
}

.breakdown-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 8px;
  font-family: 'Poppins', sans-serif;
  font-size: 0.8rem;
}

.row-correct {
  background: rgba(76, 175, 80, 0.1);
}

.row-wrong {
  background: rgba(244, 67, 54, 0.1);
}

.breakdown-index {
  font-weight: 700;
  color: #888;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}

.breakdown-icon {
  font-weight: 900;
  font-size: 1rem;
  flex-shrink: 0;
}

.row-correct .breakdown-icon { color: #2E7D32; }
.row-wrong .breakdown-icon { color: #C62828; }

.breakdown-title {
  flex: 1;
  font-weight: 600;
  color: #1A0A14;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.breakdown-points {
  font-weight: 700;
  flex-shrink: 0;
}

.pts-green { color: #2E7D32; }
.pts-red { color: #C62828; }

.breakdown-badge {
  font-size: 0.9rem;
  flex-shrink: 0;
}

@media (max-width: 640px) {
  .game-card { border-radius: 12px; }
  .trophy { font-size: 4rem; }
  .solo-score-number { font-size: 2.5rem; }
  .breakdown-list { max-height: 200px; }
  .breakdown-row { padding: 4px 8px; font-size: 0.75rem; }
}
</style>
