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
          <h1 class="result-title">PICTURE PERFECT!</h1>
          <p class="result-sub">You've seen all {{ store.totalCount }} movies!</p>
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

const playAgainStyle = computed(() => ({
  background: `linear-gradient(135deg, ${colors.value.primary}, ${colors.value.primaryDark})`,
  color: colors.value.textDark,
}))

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

@media (max-width: 640px) {
  .game-card { border-radius: 12px; }
  .trophy { font-size: 4rem; }
}
</style>
