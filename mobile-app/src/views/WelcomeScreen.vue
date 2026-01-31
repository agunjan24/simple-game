<template>
  <div class="welcome-screen" :style="bgStyle">
    <div class="game-card">
      <div class="welcome-content">
        <!-- Film reel -->
        <div class="reel-icon">🎞️</div>

        <!-- Title -->
        <h1 class="main-title">{{ store.themeConfig.titleText }}</h1>
        <h1 class="main-title">FRAMES</h1>

        <p class="subtitle" :style="{ color: colors.textDark }">
          THE ULTIMATE MOVIE GUESSING GAME
        </p>

        <div class="stars" :style="{ color: colors.primary }">✦ ✦ ✦</div>

        <!-- Theme toggle -->
        <div class="theme-toggle">
          <button
            :class="['theme-btn', store.theme === 'bollywood' ? 'active' : 'inactive']"
            :style="store.theme === 'bollywood' ? activeBtnStyle : inactiveBtnStyle"
            @click="store.setTheme('bollywood')"
          >🎬 Bollywood</button>
          <button
            :class="['theme-btn', store.theme === 'hollywood' ? 'active' : 'inactive']"
            :style="store.theme === 'hollywood' ? activeBtnStyle : inactiveBtnStyle"
            @click="store.setTheme('hollywood')"
          >🎥 Hollywood</button>
        </div>

        <!-- Movie count -->
        <p class="movie-count" :style="{ color: colors.textDark }">
          🎬 {{ store.totalCount }} Movies to Guess
        </p>

        <!-- Game options -->
        <div class="options-section">
          <div class="option-row">
            <span :style="{ color: colors.textDark }">Game Mode:</span>
            <label class="toggle-switch">
              <input type="checkbox" v-model="store.teamMode" />
              <span class="toggle-slider" :style="store.teamMode ? { background: '#6495ED' } : {}"></span>
            </label>
            <span :style="{ color: colors.textDark }">{{ store.teamMode ? 'Team Battle' : 'Solo' }}</span>
          </div>

          <div class="option-row">
            <span :style="{ color: colors.textDark }">Progressive Reveal:</span>
            <label class="toggle-switch">
              <input type="checkbox" v-model="store.progressiveReveal" />
              <span class="toggle-slider" :style="store.progressiveReveal ? { background: '#6495ED' } : {}"></span>
            </label>
          </div>
        </div>

        <!-- Timer config (always visible) -->
        <div class="timer-config">
          <span :style="{ color: colors.textDark }">⏱️ Timer:</span>
          <input
            type="number"
            :value="store.teamMode ? store.timerDuration : store.soloDuration"
            @change="updateTimer($event)"
            min="15" max="120" step="5"
            class="timer-input"
          />
          <span :style="{ color: colors.textDark }">seconds</span>
        </div>

        <!-- Team options -->
        <div v-if="store.teamMode" class="team-options">
          <div class="team-names-row">
            <span class="team-names-label" :style="{ background: colors.primary + '33', color: colors.textDark }">
              🔴 {{ store.teamNames[0] }}  vs  🔵 {{ store.teamNames[1] }}
            </span>
            <button class="dice-btn" @click="store.randomizeTeamNames()">🎲</button>
          </div>
        </div>

        <!-- Start button -->
        <button class="start-btn" :style="startBtnStyle" @click="startGame">
          🎬 START THE SHOW
        </button>

        <!-- Timer info -->
        <p class="timer-info" :style="{ color: colors.accentDark }">
          ⏱️ {{ store.currentTimerDuration }} seconds per round
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/gameStore.js'

const store = useGameStore()
const router = useRouter()
const colors = computed(() => store.themeColors)

const bgStyle = computed(() => ({
  background: `
    radial-gradient(ellipse at top, ${colors.value.primary}1a 0%, transparent 50%),
    radial-gradient(ellipse at bottom, ${colors.value.accent}1a 0%, transparent 50%),
    linear-gradient(180deg, ${colors.value.bgDark} 0%, ${colors.value.bgMid} 50%, ${colors.value.bgLight} 100%)`,
  minHeight: '100vh',
}))

const activeBtnStyle = computed(() => ({
  background: '#6495ED',
  color: '#fff',
  borderColor: '#6495ED',
  boxShadow: '0 2px 10px rgba(100, 149, 237, 0.5)',
}))
const inactiveBtnStyle = computed(() => ({
  background: '#B0C4EE',
  color: '#fff',
  borderColor: '#B0C4EE',
}))

const startBtnStyle = computed(() => ({
  background: '#6495ED',
  color: '#fff',
}))

function updateTimer(e) {
  const val = Math.max(15, Math.min(120, +e.target.value || 25))
  if (store.teamMode) {
    store.timerDuration = val
  } else {
    store.soloDuration = val
  }
}

function startGame() {
  store.currentScreen = 'game'
  store.nextMovie()
  router.push('/game')
}
</script>

<style scoped>
.welcome-screen {
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
  max-width: 850px;
  width: 100%;
  overflow: hidden;
  animation: spotlightPulse 4s ease-in-out infinite;
}

.welcome-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 24px;
  gap: 16px;
  animation: floatUp 0.8s ease-out;
}

.reel-icon {
  font-size: clamp(1.5rem, 6vw, 3rem);
  animation: reelSpin 4s linear infinite;
}

.main-title {
  font-family: 'Rozha One', serif;
  font-size: clamp(1.8rem, 8vw, 3rem);
  margin: 0;
  line-height: 1.1;
  background: linear-gradient(
    90deg,
    v-bind('colors.primary') 0%,
    v-bind('colors.primaryLight') 25%,
    v-bind('colors.primary') 50%,
    v-bind('colors.primaryLight') 75%,
    v-bind('colors.primary') 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: primaryShimmer 3s linear infinite;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  text-align: center;
}

.subtitle {
  font-size: clamp(0.6rem, 2.5vw, 0.95rem);
  letter-spacing: 2px;
  text-transform: uppercase;
  opacity: 0.7;
  margin: 4px 0;
}

.stars {
  font-size: 1rem;
  letter-spacing: 12px;
  margin: 2px 0;
}

.theme-toggle {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.theme-btn {
  font-family: 'Poppins', sans-serif;
  padding: 8px 16px;
  border-radius: 20px;
  border: 2px solid transparent;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  touch-action: manipulation;
}

.theme-btn.active {
  border: 2px solid transparent;
}

.theme-btn.inactive {
  opacity: 0.85;
}

.theme-btn:hover {
  transform: scale(1.05);
}

.movie-count {
  font-size: clamp(0.9rem, 3vw, 1.1rem);
  font-weight: 600;
  margin-top: 2px;
}

.options-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option-row {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  font-size: 1rem;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 36px;
  height: 20px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: #ccc;
  border-radius: 20px;
  transition: 0.3s;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: 0.3s;
}

.toggle-switch input:checked + .toggle-slider::before {
  transform: translateX(16px);
}

.timer-config {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  color: v-bind('colors.textDark');
  margin-top: 4px;
}

.timer-input {
  width: 70px;
  padding: 6px 8px;
  border: 2px solid v-bind('colors.primary + "66"');
  border-radius: 8px;
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.8);
  transition: border-color 0.3s;
}

.timer-input:focus {
  outline: none;
  border-color: v-bind('colors.primary');
}

.team-options {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 100%;
  margin-top: 4px;
  animation: floatUp 0.4s ease-out;
}

.team-names-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.team-names-label {
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 700;
  font-size: clamp(0.85rem, 3.5vw, 1.3rem);
  white-space: nowrap;
}

.dice-btn {
  background: transparent;
  border: none;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 2px;
  transition: transform 0.2s;
}

.dice-btn:hover { transform: scale(1.2) rotate(15deg); }
.dice-btn:active { transform: scale(0.9); }

.start-btn {
  padding: 14px 36px;
  border: none;
  border-radius: 30px;
  font-family: 'Poppins', sans-serif;
  font-size: clamp(0.85rem, 2.5vw, 1.05rem);
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
  -webkit-touch-callout: none;
  user-select: none;
}

.start-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow:
    0 8px 25px rgba(0, 0, 0, 0.4),
    0 0 20px v-bind('colors.accent + "66"');
}

.start-btn:active {
  transform: translateY(0) scale(0.98);
}

.timer-info {
  font-size: clamp(0.75rem, 2.5vw, 0.9rem);
  margin-top: 8px;
}

@media (max-width: 640px) {
  .game-card {
    border-radius: 12px;
    animation: none;
  }

  .theme-btn {
    font-size: 0.75rem;
    padding: 6px 12px;
  }

  .start-btn {
    padding: 10px 28px;
  }
}
</style>
