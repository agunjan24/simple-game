<template>
  <div class="welcome-screen" :style="bgStyle">
    <div class="game-card">
      <div class="welcome-content">
        <!-- Film reel -->
        <div class="reel-icon">🎞️</div>

        <!-- Title -->
        <h1 class="main-title">{{ store.welcomeStep < 3 ? 'GUESS' : displayTitle }}</h1>
        <h1 class="main-title">FRAMES</h1>

        <p class="subtitle" :style="{ color: colors.textDark }">Guess • Learn • Play</p>

        <div class="stars" :style="{ color: colors.primary }">✦ ✦ ✦</div>

        <!-- Step dots -->
        <div class="step-dots">
          <div
            v-for="step in 3" :key="step"
            class="step-dot"
            :class="{
              'step-dot--completed': store.welcomeStep > step,
              'step-dot--active': store.welcomeStep === step,
            }"
            :style="stepDotStyle(step)"
          ></div>
        </div>

        <!-- ==================== STEP 1: Category Selection ==================== -->
        <template v-if="store.welcomeStep === 1">
          <div class="section-header">
            <div class="section-line" :style="{ background: `linear-gradient(90deg, transparent, ${colors.primary})` }"></div>
            <span class="section-label" :style="{ color: colors.textDark }">CHOOSE YOUR CATEGORY</span>
            <div class="section-line" :style="{ background: `linear-gradient(90deg, ${colors.primary}, transparent)` }"></div>
          </div>

          <div class="card-grid">
            <div
              v-for="(cat, catKey) in CATEGORIES" :key="catKey"
              class="category-card"
              :style="categoryCardStyle(cat)"
              @click="onCategoryClick(catKey)"
            >
              <span class="card-icon">{{ cat.icon }}</span>
              <span class="card-name">{{ cat.name }}</span>
              <span class="card-desc">{{ cat.description }}</span>
              <span class="card-count" v-if="cat.subcategories">{{ categoryTotalCount(catKey) }} items</span>
              <span class="card-count" v-else>Surprise!</span>
            </div>
          </div>

          <p class="tap-hint" :style="{ color: colors.textDark }">Tap to select</p>

          <span class="how-to-play-link" :style="{ color: colors.primaryDark }" @click="showHowToPlay = true">
            ? How to Play
          </span>
        </template>

        <!-- ==================== STEP 2: Subcategory Selection ==================== -->
        <template v-if="store.welcomeStep === 2">
          <div class="selected-badge" :style="badgeStyle">
            {{ CATEGORIES[store.selectedCategory].icon }}
            {{ CATEGORIES[store.selectedCategory].name }} ✓
          </div>

          <div class="section-header">
            <div class="section-line" :style="{ background: `linear-gradient(90deg, transparent, ${colors.primary})` }"></div>
            <span class="section-label" :style="{ color: colors.textDark }">CHOOSE SUBCATEGORY</span>
            <div class="section-line" :style="{ background: `linear-gradient(90deg, ${colors.primary}, transparent)` }"></div>
          </div>

          <div class="card-grid">
            <div
              v-for="(sub, subKey) in CATEGORIES[store.selectedCategory].subcategories" :key="subKey"
              class="subcategory-card"
              :style="subcategoryCardStyle(sub)"
              @click="onSubcategoryClick(subKey)"
            >
              <span class="card-icon">
                <img v-if="sub.iconImage" :src="sub.iconImage" class="card-icon-img" alt="" />
                <template v-else>{{ sub.icon }}</template>
              </span>
              <span class="card-name">{{ sub.name }}</span>
              <span class="card-count">{{ store.getItemCount(sub.themeKey) }} items</span>
            </div>
          </div>

          <span class="back-link" :style="{ color: colors.primaryDark }" @click="goBackToCategories">← Change Category</span>
        </template>

        <!-- ==================== STEP 3: Game Configuration ==================== -->
        <template v-if="store.welcomeStep === 3">
          <div class="selected-badge" :style="badgeStyle">
            <template v-if="store.selectedCategory === 'mashup'">
              🔀 Mashup Mode — {{ store.totalCount }} Frames
            </template>
            <template v-else>
              {{ CATEGORIES[store.selectedCategory].icon }}
              {{ CATEGORIES[store.selectedCategory].name }}
              <template v-if="store.selectedSubcategory">
                / {{ CATEGORIES[store.selectedCategory].subcategories[store.selectedSubcategory].name }}
              </template>
            </template>
          </div>

          <!-- Item count -->
          <p class="item-count" :style="{ color: colors.textDark }">
            <template v-if="store.isMashup">🔀 {{ store.totalCount }} Frames to Guess</template>
            <template v-else>🎬 {{ store.totalCount }} {{ store.themeConfig.categoryLabelPlural }} to Guess</template>
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

          <!-- Timer config -->
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

          <!-- Back link -->
          <span class="back-link" :style="{ color: colors.primaryDark }" @click="goBack">← Back</span>

          <!-- Timer info -->
          <p class="timer-info" :style="{ color: colors.accentDark }">
            ⏱️ {{ store.currentTimerDuration }} seconds per round
          </p>
        </template>
      </div>
    </div>

    <!-- How to Play modal -->
    <div v-if="showHowToPlay" class="modal-overlay" @click.self="showHowToPlay = false">
      <div class="modal-card help-card" :style="{ background: colors.textLight, borderColor: colors.primary }">
        <div class="modal-header">
          <span class="modal-title">How to Play</span>
          <button class="modal-close" @click="showHowToPlay = false">✕</button>
        </div>

        <div class="help-section-label" :style="{ color: colors.primaryDark }">The Basics</div>
        <p class="help-prose" :style="{ color: colors.textDark }">
          An image appears blurred and progressively clears as time runs down.
          Guess what's in the frame before the timer expires! A countdown appears for the last 10 seconds.
        </p>
        <p class="help-prose help-note" :style="{ color: colors.textDark }">
          Blurriness can be turned off with the Progressive Reveal toggle on the welcome screen.
        </p>

        <hr class="help-divider" :style="{ borderColor: colors.primary + '44' }" />
        <div class="help-section-label" :style="{ color: colors.primaryDark }">Tips &amp; Tricks</div>

        <div class="help-row">
          <span class="help-icon">🖼️</span>
          <span class="help-action" :style="{ color: colors.textDark }">Tap Image</span>
          <span class="help-arrow" :style="{ color: colors.primaryDark }">→</span>
          <span class="help-desc" :style="{ color: colors.textDark }">Clear blur early</span>
        </div>
        <div class="help-row">
          <span class="help-icon">⏱️</span>
          <span class="help-action" :style="{ color: colors.textDark }">Tap Timer</span>
          <span class="help-arrow" :style="{ color: colors.primaryDark }">→</span>
          <span class="help-desc" :style="{ color: colors.textDark }">Pause & clear blur</span>
        </div>
        <div class="help-row">
          <span class="help-icon">●</span>
          <span class="help-action" :style="{ color: colors.textDark }">Tap Dot</span>
          <span class="help-arrow" :style="{ color: colors.primaryDark }">→</span>
          <span class="help-desc" :style="{ color: colors.textDark }">Review past frames</span>
        </div>

        <hr class="help-divider" :style="{ borderColor: colors.primary + '44' }" />
        <div class="help-section-label" :style="{ color: colors.primaryDark }">Team Mode Scoring</div>
        <p class="help-prose" :style="{ color: colors.textDark }">
          100 pts in the first third of time, 75 in the middle, 50 in the last third.
          Using a hint costs 25 pts.
          Tapping the image or timer early locks scoring to 50 pts.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/gameStore.js'
import { CATEGORIES } from '../themes/themes.js'

const store = useGameStore()
const router = useRouter()
const colors = computed(() => store.themeColors)
const showHowToPlay = ref(false)

function onEscape(e) {
  if (e.key === 'Escape') showHowToPlay.value = false
}
onMounted(() => window.addEventListener('keydown', onEscape))
onUnmounted(() => window.removeEventListener('keydown', onEscape))

const displayTitle = computed(() => {
  if (store.selectedCategory === 'mashup') return '🔀 MASHUP'
  if (store.selectedCategory && CATEGORIES[store.selectedCategory]) {
    return CATEGORIES[store.selectedCategory].name.toUpperCase()
  }
  return 'GUESS'
})

const bgStyle = computed(() => ({
  background: `
    radial-gradient(ellipse at top, ${colors.value.primary}1a 0%, transparent 50%),
    radial-gradient(ellipse at bottom, ${colors.value.accent}1a 0%, transparent 50%),
    linear-gradient(180deg, ${colors.value.bgDark} 0%, ${colors.value.bgMid} 50%, ${colors.value.bgLight} 100%)`,
  minHeight: '100vh',
}))

const startBtnStyle = computed(() => ({
  background: '#6495ED',
  color: '#fff',
}))

const badgeStyle = computed(() => ({
  background: colors.value.primary + '22',
  color: colors.value.textDark,
  border: `1px solid ${colors.value.primary}66`,
}))

function stepDotStyle(step) {
  if (store.welcomeStep > step) {
    return { background: colors.value.primary, borderColor: colors.value.primary }
  }
  if (store.welcomeStep === step) {
    return { background: colors.value.accent, borderColor: colors.value.accent, boxShadow: `0 0 8px ${colors.value.accent}88` }
  }
  return { background: 'transparent', borderColor: colors.value.primary + '66' }
}

function categoryCardStyle(cat) {
  return {
    background: `linear-gradient(145deg, ${cat.colorDark}, ${cat.color}33)`,
    borderColor: cat.color + '66',
  }
}

function subcategoryCardStyle(sub) {
  return {
    background: `linear-gradient(145deg, ${colors.value.bgMid}, ${colors.value.bgLight})`,
    borderColor: colors.value.primary + '66',
  }
}

function categoryTotalCount(catKey) {
  const cat = CATEGORIES[catKey]
  if (!cat.subcategories) return 0
  return Object.values(cat.subcategories).reduce(
    (sum, sub) => sum + store.getItemCount(sub.themeKey), 0
  )
}

function onCategoryClick(catKey) {
  store.selectCategory(catKey)
}

function onSubcategoryClick(subKey) {
  store.selectSubcategory(subKey)
}

function goBackToCategories() {
  store.resetToWelcome()
}

function goBack() {
  const cat = CATEGORIES[store.selectedCategory]
  if (!cat || !cat.subcategories || Object.keys(cat.subcategories).length <= 1) {
    // Go back to step 1 (mashup, or single-subcategory categories)
    store.resetToWelcome()
  } else {
    // Go back to step 2
    store.welcomeStep = 2
    store.selectedSubcategory = null
  }
}

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
  store.nextItem()
  store.resetWelcome()
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
  gap: 12px;
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

/* Step dots */
.step-dots {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0;
}

.step-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid;
  transition: all 0.3s ease;
}

.step-dot--completed {
  transform: scale(0.9);
}

.step-dot--active {
  transform: scale(1.2);
}

/* Section header with decorative lines */
.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  max-width: 500px;
  margin: 4px 0;
}

.section-line {
  flex: 1;
  height: 2px;
}

.section-label {
  font-family: 'Poppins', sans-serif;
  font-size: clamp(0.65rem, 2.5vw, 0.8rem);
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  white-space: nowrap;
}

/* Category and subcategory cards */
.card-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  width: 100%;
  max-width: 600px;
}

.category-card,
.subcategory-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 16px 24px;
  border-radius: 16px;
  border: 2px solid;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  min-width: 140px;
  flex: 1;
  max-width: 200px;
}

.category-card:hover,
.subcategory-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.category-card:active,
.subcategory-card:active {
  transform: translateY(0) scale(0.97);
}

.card-icon {
  font-size: clamp(1.5rem, 5vw, 2.2rem);
  display: flex;
  align-items: center;
  justify-content: center;
  height: clamp(1.5rem, 5vw, 2.2rem);
}

.card-icon-img {
  height: clamp(1.1rem, 3.5vw, 1.5rem);
  width: auto;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.card-name {
  font-family: 'Poppins', sans-serif;
  font-size: clamp(0.9rem, 3vw, 1.1rem);
  font-weight: 700;
  color: #fff;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.card-desc {
  font-family: 'Poppins', sans-serif;
  font-size: clamp(0.65rem, 2vw, 0.78rem);
  color: rgba(0, 0, 0, 0.7);
  text-align: center;
}

.card-count {
  font-family: 'Poppins', sans-serif;
  font-size: clamp(0.6rem, 2vw, 0.72rem);
  color: rgba(255, 255, 255, 0.55);
}

.category-card .card-name {
  color: rgba(0, 0, 0, 0.85);
  text-shadow: none;
}

.category-card .card-count {
  color: rgba(0, 0, 0, 0.6);
}

.tap-hint {
  font-size: 0.78rem;
  opacity: 0.5;
  margin: 0;
}

/* Selected badge */
.selected-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  border-radius: 20px;
  font-family: 'Poppins', sans-serif;
  font-size: clamp(0.78rem, 2.5vw, 0.9rem);
  font-weight: 600;
}

/* Back link */
.back-link {
  font-family: 'Poppins', sans-serif;
  font-size: clamp(0.78rem, 2.5vw, 0.9rem);
  font-weight: 600;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
  touch-action: manipulation;
}

.back-link:hover {
  opacity: 1;
}

.item-count {
  font-size: clamp(0.9rem, 3vw, 1.1rem);
  font-weight: 600;
  margin: 0;
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
  white-space: nowrap;
}

@media (max-width: 640px) {
  .option-row {
    font-size: 0.85rem;
    gap: 8px;
  }
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
  margin: 0;
}

.how-to-play-link {
  font-family: 'Poppins', sans-serif;
  font-size: clamp(0.8rem, 2.5vw, 0.95rem);
  font-weight: 600;
  cursor: pointer;
  opacity: 0.7;
  margin-top: 4px;
  transition: opacity 0.2s;
}

.how-to-play-link:hover {
  opacity: 1;
}

/* Modal overlay */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.modal-card {
  border: 2px solid;
  border-radius: 16px;
  max-width: 460px;
  width: 92vw;
  padding: 24px 28px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.help-card {
  max-height: 85vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.modal-title {
  font-family: 'Rozha One', serif;
  font-size: 1.6rem;
  color: v-bind('colors.textDark');
}

.modal-close {
  background: transparent;
  border: none;
  font-size: 1.4rem;
  cursor: pointer;
  color: #888;
  padding: 4px;
}

.help-section-label {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 2px;
}

.help-prose {
  font-family: 'Poppins', sans-serif;
  font-size: 0.9rem;
  line-height: 1.45;
  margin: 2px 0;
}

.help-note {
  opacity: 0.65;
  font-size: 0.82rem;
}

.help-divider {
  border: none;
  border-top: 2px solid;
  margin: 6px 0 4px 0;
}

.help-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 3px 0;
}

.help-icon {
  font-size: 1.3rem;
  width: 32px;
  text-align: center;
  flex-shrink: 0;
}

.help-action {
  font-size: 1rem;
  font-weight: 700;
  font-family: 'Poppins', sans-serif;
  white-space: nowrap;
}

.help-arrow {
  font-size: 1rem;
  flex-shrink: 0;
}

.help-desc {
  font-size: 0.95rem;
  font-family: 'Poppins', sans-serif;
  opacity: 0.75;
}

/* Mobile overrides */
@media (max-width: 640px) {
  .game-card {
    border-radius: 12px;
    animation: none;
  }

  .category-card,
  .subcategory-card {
    padding: 12px 16px;
    min-width: 110px;
    border-radius: 12px;
  }

  .step-dot {
    width: 10px;
    height: 10px;
  }

  .start-btn {
    padding: 10px 28px;
  }

  .modal-card {
    padding: 16px 18px;
    max-height: 80vh;
  }

  .help-prose {
    font-size: 0.82rem;
    line-height: 1.35;
  }

  .help-section-label {
    font-size: 0.78rem;
    margin-top: 0;
  }

  .help-divider {
    margin: 4px 0 2px 0;
  }

  .help-row {
    gap: 8px;
    padding: 2px 0;
  }

  .help-icon {
    font-size: 1.1rem;
    width: 28px;
  }

  .help-action {
    font-size: 0.9rem;
  }

  .help-desc {
    font-size: 0.85rem;
  }
}
</style>
