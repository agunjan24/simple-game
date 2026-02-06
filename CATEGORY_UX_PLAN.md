# Category & Subcategory UX Plan

## Vision
Transform the welcome screen from a simple 3-theme selector into a scalable, engaging category browser inspired by slot machine drums. The UX should feel playful yet intuitive, making content discovery fun while supporting educational and entertainment use cases.

---

## 1. Category Taxonomy

### Proposed Structure

```
CATEGORIES
├── 🎬 Movies
│   ├── 🇮🇳 Bollywood
│   ├── 🎥 Hollywood
│   ├── 🎭 Tollywood (future)
│   └── 🎌 Anime Films (future)
│
├── 📚 History
│   ├── 🦅 American History (all ages)
│   ├── 🎒 History for Kids (K-5)
│   ├── 📖 History for Teens (6-12)
│   └── 🌍 World History (future)
│
├── 🔬 STEM
│   ├── 🧪 Science Discoveries
│   ├── 🔢 Math Moments
│   ├── 💻 Tech Pioneers
│   └── 🔧 Engineering Marvels
│
├── 🎨 Arts & Culture (future)
│   ├── 🖼️ Famous Paintings
│   ├── 🎵 Music Icons
│   └── 📚 Literary Classics
│
└── 🎲 YOLO (Random Mix)
    └── (no subcategories - pulls from everything)
```

### Data Structure

```python
CATEGORIES = {
    'movies': {
        'icon': '🎬',
        'name': 'Movies',
        'description': 'Guess the movie from the scene',
        'color': '#FFD700',  # Gold
        'subcategories': {
            'bollywood': { 'icon': '🇮🇳', 'name': 'Bollywood', ... },
            'hollywood': { 'icon': '🎥', 'name': 'Hollywood', ... },
        }
    },
    'history': {
        'icon': '📚',
        'name': 'History',
        'description': 'Identify historical moments',
        'color': '#8B4513',  # Saddle Brown
        'subcategories': {
            'american': { 'icon': '🦅', 'name': 'American', 'age_group': 'all' },
            'kids': { 'icon': '🎒', 'name': 'For Kids', 'age_group': 'K-5' },
        }
    },
    'stem': {
        'icon': '🔬',
        'name': 'STEM',
        'description': 'Science, Tech, Engineering & Math',
        'color': '#00CED1',  # Dark Turquoise
        'subcategories': { ... }
    },
    'yolo': {
        'icon': '🎲',
        'name': 'YOLO',
        'description': 'Random mix of everything!',
        'color': '#FF6B6B',  # Coral
        'subcategories': None  # No subcategories
    }
}
```

---

## 2. Slot Machine Drum UX

### The Concept

Imagine a **horizontal slot machine reel** that spins when you swipe or tap arrows. Each "slot" shows a category card. When the drum stops on a category, it "locks in" with a satisfying click/animation, and subcategories appear below.

```
    ◀ ─────────────────────────────────────────── ▶

         ╭─────────╮   ╭─────────╮   ╭─────────╮
         │   🎬    │   │   📚    │   │   🔬    │
         │ Movies  │   │ History │   │  STEM   │
         ╰─────────╯   ╰─────────╯   ╰─────────╯
              ↑             ↑             ↑
           faded        SELECTED        faded
                         glow
```

### Visual States

| State | Visual Treatment |
|-------|------------------|
| **Unselected** | 70% opacity, no glow, smaller scale (0.85) |
| **Hovered** | 90% opacity, subtle lift, scale (0.95) |
| **Selected** | 100% opacity, glowing border, scale (1.0), colored shadow |
| **Locked** | Checkmark badge, pulse animation, "locked in" sound |

### Interaction Patterns

#### Desktop
- **Click** on side cards to rotate drum
- **Arrow keys** (← →) for keyboard navigation
- **Scroll wheel** over drum area to spin
- **Click center** to select/lock current category

#### Mobile (Touch)
- **Swipe left/right** to spin drum
- **Tap side cards** to rotate one step
- **Tap center card** to select
- **Momentum scrolling** for satisfying spin feel

---

## 3. Complete Welcome Screen Flow

### ASCII Mockup - Step 1: Category Selection

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║                          🎞️ (spinning reel)                          ║
║                                                                       ║
║                    ╔═══════════════════════════╗                      ║
║                    ║    WELCOME TO FRAMES      ║                      ║
║                    ║    Guess • Learn • Play   ║                      ║
║                    ╚═══════════════════════════╝                      ║
║                                                                       ║
║     ════════════════════════════════════════════════════════════     ║
║                         CHOOSE YOUR CATEGORY                          ║
║     ════════════════════════════════════════════════════════════     ║
║                                                                       ║
║     ◀ ───────────────────────────────────────────────────────── ▶    ║
║                                                                       ║
║      ┌─────────┐    ╔═════════════╗    ┌─────────┐    ┌─────────┐    ║
║      │   🎬    │    ║     📚      ║    │   🔬    │    │   🎲    │    ║
║      │ Movies  │    ║   HISTORY   ║    │  STEM   │    │  YOLO   │    ║
║      │  (dim)  │    ║  (glowing)  ║    │  (dim)  │    │  (dim)  │    ║
║      └─────────┘    ╚═════════════╝    └─────────┘    └─────────┘    ║
║                            │                                          ║
║     ════════════════════════════════════════════════════════════     ║
║                                                                       ║
║                     Tap to select • Swipe to browse                   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### ASCII Mockup - Step 2: Subcategory Selection (After Category Lock)

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║                          🎞️ (spinning reel)                          ║
║                                                                       ║
║                    ╔═══════════════════════════╗                      ║
║                    ║       FRAMES GAME         ║                      ║
║                    ║    Guess • Learn • Play   ║                      ║
║                    ╚═══════════════════════════╝                      ║
║                                                                       ║
║     ═══════════════════════════════════════════════════════════      ║
║                         📚 HISTORY SELECTED                           ║
║                              ✓ LOCKED                                 ║
║     ═══════════════════════════════════════════════════════════      ║
║                                                                       ║
║                        Choose your subcategory:                       ║
║                                                                       ║
║       ╭───────────────╮  ╭───────────────╮  ╭───────────────╮        ║
║       │      🦅       │  │      🎒       │  │      📖       │        ║
║       │   American    │  │   For Kids    │  │   For Teens   │        ║
║       │   History     │  │    (K-5)      │  │    (6-12)     │        ║
║       │   10 items    │  │   8 items     │  │   12 items    │        ║
║       ╰───────────────╯  ╰───────────────╯  ╰───────────────╯        ║
║                                                                       ║
║                        [← Change Category]                            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### ASCII Mockup - Step 3: Game Configuration (After Subcategory)

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║                          🎞️ (spinning reel)                          ║
║                                                                       ║
║                    ╔═══════════════════════════╗                      ║
║                    ║   📚 HISTORY: American    ║                      ║
║                    ║      10 moments to ID     ║                      ║
║                    ╚═══════════════════════════╝                      ║
║                                                                       ║
║     ════════════════════════════════════════════════════════════     ║
║                          CONFIGURE YOUR GAME                          ║
║     ════════════════════════════════════════════════════════════     ║
║                                                                       ║
║               Game Mode:     ○ Solo    ● Team Battle                  ║
║                                                                       ║
║               Progressive Reveal:    [✓ ON ]                          ║
║                                                                       ║
║     ┌─────────────────────────────────────────────────────────┐      ║
║     │         🔴 Patriots  vs  Loyalists 🔵      🎲            │      ║
║     │                   ⏱️ 45 seconds                          │      ║
║     └─────────────────────────────────────────────────────────┘      ║
║                                                                       ║
║              ╔═══════════════════════════════════════╗               ║
║              ║       🎬 START THE SHOW 🎬            ║               ║
║              ╚═══════════════════════════════════════╝               ║
║                                                                       ║
║                   [← Back]           [? Help]                         ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 4. Drum Animation Details

### Spin Animation (CSS)

```css
@keyframes drum-spin {
    0% { transform: translateX(0); }
    20% { transform: translateX(-150%); }  /* Overshoot */
    40% { transform: translateX(50%); }    /* Bounce back */
    60% { transform: translateX(-25%); }   /* Settle */
    80% { transform: translateX(10%); }    /* Final adjust */
    100% { transform: translateX(0); }     /* Lock in place */
}

@keyframes lock-pulse {
    0% { box-shadow: 0 0 0 0 rgba(gold, 0.7); }
    70% { box-shadow: 0 0 0 15px rgba(gold, 0); }
    100% { box-shadow: 0 0 0 0 rgba(gold, 0); }
}

.category-card.selected {
    animation: lock-pulse 0.6s ease-out;
}
```

### JavaScript Interaction

```javascript
class CategoryDrum {
    constructor(container) {
        this.categories = [...];
        this.currentIndex = 0;
        this.isSpinning = false;

        // Touch handling
        this.touchStartX = 0;
        this.touchEndX = 0;
    }

    spin(direction) {
        if (this.isSpinning) return;
        this.isSpinning = true;

        // Play slot machine "click" sound
        this.playSpinSound();

        // Animate rotation
        this.currentIndex += direction;
        this.render();

        setTimeout(() => {
            this.isSpinning = false;
            this.playLockSound();  // Satisfying "lock" click
        }, 300);
    }

    select() {
        // Trigger subcategory reveal with expansion animation
        this.showSubcategories(this.categories[this.currentIndex]);
    }
}
```

---

## 5. Mobile-First Considerations

### Touch Gestures

| Gesture | Action |
|---------|--------|
| **Swipe left** | Rotate drum right (next category) |
| **Swipe right** | Rotate drum left (previous category) |
| **Tap center** | Select category, show subcategories |
| **Tap side card** | Rotate drum to that card |
| **Swipe up** | Quick-select current (same as tap center) |

### Mobile Layout

```
┌─────────────────────────┐
│   🎞️ FRAMES GAME 🎞️    │
│   Guess • Learn • Play  │
├─────────────────────────┤
│                         │
│  CHOOSE CATEGORY        │
│                         │
│  ◀  ┌─────┐ ┌─────┐ ▶  │
│     │ 🎬  │ │ 📚  │     │
│     │     │ │     │     │
│     └─────┘ └─────┘     │
│       dim    GLOW       │
│                         │
│   ← Swipe to browse →   │
│                         │
├─────────────────────────┤
│   TAP TO SELECT         │
└─────────────────────────┘
```

On mobile, show **2-3 cards at a time** (vs 4 on desktop) with larger touch targets.

---

## 6. YOLO Mode Special Handling

When "YOLO" is selected:
1. Skip subcategory selection entirely
2. Show animated "mixing" effect (cards shuffling)
3. Display: "🎲 Random Mix - X items from all categories"
4. Pool items from ALL available subcategories
5. Each round could be from a different theme (with appropriate styling)

### Dynamic Theming in YOLO

When an item appears in YOLO mode, temporarily apply that item's theme colors:
- Bollywood movie → Gold/Magenta theme for that round
- History item → Parchment/Bronze theme for that round
- Creates visual variety and reinforces category identity

---

## 7. Subcategory Display Variants

### For 2-3 Subcategories: Simple Cards

```
    ╭───────────╮   ╭───────────╮   ╭───────────╮
    │    🇮🇳    │   │    🎥     │   │    🎭    │
    │ Bollywood │   │ Hollywood │   │ Tollywood │
    │  10 items │   │  12 items │   │  8 items  │
    ╰───────────╯   ╰───────────╯   ╰───────────╯
```

### For 4+ Subcategories: Mini Drum

```
    ◀ ─────────────────────────────────────── ▶

       ┌─────┐   ╔═══════╗   ┌─────┐   ┌─────┐
       │ 🧪  │   ║  🔢   ║   │ 💻  │   │ 🔧  │
       │Sci. │   ║ Math  ║   │Tech │   │ Eng │
       └─────┘   ╚═══════╝   └─────┘   └─────┘
```

### For 1 Subcategory: Auto-Select

If a category has only one subcategory, skip selection and go directly to game config.

---

## 8. Sound Design

| Action | Sound |
|--------|-------|
| **Drum spin** | Quick mechanical click (like slot machine) |
| **Card lock** | Satisfying "chunk" lock sound |
| **Category select** | Triumphant short chime |
| **Subcategory reveal** | Whoosh + sparkle |
| **YOLO shuffle** | Cards shuffling rapidly |
| **Start game** | Dramatic "showtime" flourish |

All sounds should be optional (mute toggle in corner).

---

## 9. Implementation Phases

### Phase 1: Data Structure
- Refactor THEMES → CATEGORIES with subcategory support
- Maintain backward compatibility with existing theme data
- Add `category` and `subcategory` fields to GameState

### Phase 2: Basic Category Selection
- Replace 3-button theme selector with category drum
- Implement horizontal scroll/swipe
- Add category cards with icons and descriptions

### Phase 3: Subcategory Flow
- Add subcategory reveal animation
- Implement card grid for 2-3 items
- Add mini-drum for 4+ items
- Handle single-subcategory auto-select

### Phase 4: YOLO Mode
- Implement random pool generation
- Add shuffling animation
- Handle dynamic theme switching per round

### Phase 5: Polish
- Add sound effects
- Refine animations
- Mobile touch optimization
- Accessibility (keyboard nav, screen readers)

---

## 10. Visual Theme for Category Selector

The category drum itself should have a **neutral casino/game show theme**:

| Element | Style |
|---------|-------|
| **Background** | Deep charcoal with subtle spotlight effect |
| **Drum track** | Metallic silver border with rivets |
| **Cards** | Slightly raised with drop shadow, rounded corners |
| **Arrows** | Glowing neon accent color |
| **Text** | Clean white with subtle text shadow |
| **Selection glow** | Golden spotlight from above |

This neutral base allows individual category/subcategory colors to pop when selected.

---

---

## 11. Mobile App Implementation (Vue 3 + Capacitor)

The mobile app (`mobile-app/`) uses a different tech stack but the same UX concepts apply. This section covers mobile-specific implementation details.

### Current Mobile Architecture

| Component | Technology |
|-----------|------------|
| Framework | Vue 3 (Composition API) |
| State | Pinia store (`gameStore.js`) |
| Routing | Vue Router (3 views) |
| Data | Static JSON files |
| Native | Capacitor 8 (Android/iOS) |
| Build | Vite |

### Key Files to Modify

```
mobile-app/src/
├── views/
│   └── WelcomeScreen.vue      # Main changes here
├── stores/
│   └── gameStore.js           # Add category/subcategory state
├── themes/
│   └── themes.js → categories.js  # Restructure
├── data/
│   ├── categories.json        # NEW: category index
│   ├── bollywood.json         # Existing (becomes subcategory)
│   ├── hollywood.json         # Existing (becomes subcategory)
│   └── history.json           # Existing (becomes subcategory)
└── components/
    └── CategoryDrum.vue       # NEW: reusable drum component
```

### Data Structure Changes

#### New: `categories.json` (Index File)

```json
{
  "movies": {
    "icon": "🎬",
    "name": "Movies",
    "description": "Guess the movie from the scene",
    "color": "#FFD700",
    "subcategories": {
      "bollywood": {
        "icon": "🇮🇳",
        "name": "Bollywood",
        "dataFile": "bollywood.json",
        "imageFolder": "images",
        "categoryLabel": "Movie",
        "categoryLabelPlural": "Movies"
      },
      "hollywood": {
        "icon": "🎥",
        "name": "Hollywood",
        "dataFile": "hollywood.json",
        "imageFolder": "images_hollywood",
        "categoryLabel": "Movie",
        "categoryLabelPlural": "Movies"
      }
    }
  },
  "history": {
    "icon": "📚",
    "name": "History",
    "description": "Identify historical moments",
    "color": "#C9A84C",
    "subcategories": {
      "american": {
        "icon": "🦅",
        "name": "American",
        "dataFile": "history.json",
        "imageFolder": "images_history",
        "categoryLabel": "Moment",
        "categoryLabelPlural": "Moments",
        "ageGroup": "all"
      }
    }
  },
  "yolo": {
    "icon": "🎲",
    "name": "YOLO",
    "description": "Random mix of everything!",
    "color": "#FF6B6B",
    "subcategories": null
  }
}
```

### Pinia Store Changes (`gameStore.js`)

```javascript
// New state properties
state: () => ({
  // Existing
  theme: 'bollywood',
  // New
  category: null,        // 'movies', 'history', 'stem', 'yolo'
  subcategory: null,     // 'bollywood', 'hollywood', 'american', etc.
  selectionStep: 1,      // 1=category, 2=subcategory, 3=config

  // Computed from category+subcategory
  activeThemeConfig: null,
  // ...existing state
}),

// New actions
actions: {
  selectCategory(categoryKey) {
    this.category = categoryKey;
    const cat = CATEGORIES[categoryKey];

    if (categoryKey === 'yolo') {
      this.prepareYoloMode();
      this.selectionStep = 3;
    } else if (Object.keys(cat.subcategories).length === 1) {
      // Auto-select single subcategory
      this.selectSubcategory(Object.keys(cat.subcategories)[0]);
    } else {
      this.selectionStep = 2;
    }
  },

  selectSubcategory(subcategoryKey) {
    this.subcategory = subcategoryKey;
    this.loadSubcategoryData();
    this.selectionStep = 3;
  },

  goBackToCategory() {
    this.subcategory = null;
    this.selectionStep = 1;
  },

  prepareYoloMode() {
    // Pool all items from all subcategories
    this.items = [...bollywoodData, ...hollywoodData, ...historyData];
    this.shuffleItems();
  }
}
```

### New Component: `CategoryDrum.vue`

```vue
<template>
  <div class="drum-container"
       @touchstart="onTouchStart"
       @touchend="onTouchEnd">

    <button class="arrow-btn left" @click="rotate(-1)">◀</button>

    <div class="cards-track" :style="trackStyle">
      <div
        v-for="(cat, key) in categories"
        :key="key"
        class="category-card"
        :class="{ selected: key === currentKey, dim: key !== currentKey }"
        :style="{ '--card-color': cat.color }"
        @click="onCardClick(key)"
      >
        <span class="card-icon">{{ cat.icon }}</span>
        <span class="card-name">{{ cat.name }}</span>
        <span class="card-count">{{ getItemCount(key) }} items</span>
      </div>
    </div>

    <button class="arrow-btn right" @click="rotate(1)">▶</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useGameStore } from '@/stores/gameStore';

const props = defineProps({
  categories: Object,
  modelValue: String
});

const emit = defineEmits(['update:modelValue', 'select']);

const currentIndex = ref(0);
const touchStartX = ref(0);

// Touch handling with momentum
function onTouchStart(e) {
  touchStartX.value = e.touches[0].clientX;
}

function onTouchEnd(e) {
  const diff = touchStartX.value - e.changedTouches[0].clientX;
  if (Math.abs(diff) > 50) {
    rotate(diff > 0 ? 1 : -1);
  }
}

function rotate(direction) {
  const keys = Object.keys(props.categories);
  currentIndex.value = (currentIndex.value + direction + keys.length) % keys.length;
  emit('update:modelValue', keys[currentIndex.value]);

  // Play click sound via useAudio composable
  playDrumClick();
}

function onCardClick(key) {
  const keys = Object.keys(props.categories);
  const targetIndex = keys.indexOf(key);

  if (targetIndex === currentIndex.value) {
    // Center card clicked - select it
    emit('select', key);
  } else {
    // Side card clicked - rotate to it
    currentIndex.value = targetIndex;
    emit('update:modelValue', key);
  }
}
</script>
```

### WelcomeScreen.vue Changes

```vue
<template>
  <div class="welcome-screen">
    <!-- Header (unchanged) -->
    <header>...</header>

    <!-- Step Indicator -->
    <div class="step-dots">
      <span :class="{ active: step >= 1, completed: step > 1 }"></span>
      <span :class="{ active: step >= 2, completed: step > 2 }"></span>
      <span :class="{ active: step >= 3 }"></span>
    </div>

    <!-- Step 1: Category Selection -->
    <section v-if="step === 1" class="category-section">
      <h2>Choose Your Category</h2>
      <CategoryDrum
        :categories="categories"
        v-model="selectedCategory"
        @select="onCategorySelect"
      />
      <p class="hint">Swipe to browse • Tap to select</p>
    </section>

    <!-- Step 2: Subcategory Selection -->
    <Transition name="slide-up">
      <section v-if="step === 2" class="subcategory-section">
        <div class="selected-badge">
          {{ categories[selectedCategory].icon }}
          {{ categories[selectedCategory].name }}
          <span class="checkmark">✓</span>
        </div>

        <h3>Choose Subcategory</h3>

        <div class="subcategory-grid">
          <button
            v-for="(sub, key) in currentSubcategories"
            :key="key"
            class="subcategory-card"
            @click="onSubcategorySelect(key)"
          >
            <span class="sub-icon">{{ sub.icon }}</span>
            <span class="sub-name">{{ sub.name }}</span>
            <span class="sub-count">{{ sub.itemCount }} items</span>
          </button>
        </div>

        <button class="back-link" @click="step = 1">
          ← Change Category
        </button>
      </section>
    </Transition>

    <!-- Step 3: Game Config (existing, mostly unchanged) -->
    <Transition name="slide-up">
      <section v-if="step === 3" class="config-section">
        <!-- Existing game mode, timer, team config -->
      </section>
    </Transition>
  </div>
</template>
```

### Mobile-Specific CSS Considerations

```css
/* Drum optimizations for touch */
.drum-container {
  touch-action: pan-x;  /* Allow horizontal swipe only */
  -webkit-overflow-scrolling: touch;
  user-select: none;
}

.category-card {
  /* Prevent iOS tap delay */
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;

  /* Larger touch targets on mobile */
  min-width: 100px;
  min-height: 120px;
}

/* Reduce animations on mobile for performance */
@media (max-width: 640px) {
  .category-card {
    transition: transform 0.2s, opacity 0.2s;
  }

  /* Disable complex animations */
  .drum-spin-animation {
    animation: none;
  }
}

/* Handle notch/safe areas */
.welcome-screen {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
}
```

### Capacitor Native Enhancements

```javascript
// In WelcomeScreen.vue or a composable

import { Haptics, ImpactStyle } from '@capacitor/haptics';
import { StatusBar, Style } from '@capacitor/status-bar';

// Haptic feedback on drum rotation
async function playDrumClick() {
  await Haptics.impact({ style: ImpactStyle.Light });
}

// Haptic feedback on selection
async function playSelectFeedback() {
  await Haptics.impact({ style: ImpactStyle.Medium });
}

// Update status bar color based on selected category
async function updateStatusBarColor(color) {
  await StatusBar.setBackgroundColor({ color });
}
```

### Implementation Order for Mobile

1. **Create `categories.json`** - Define category structure
2. **Update `gameStore.js`** - Add category/subcategory state and actions
3. **Create `CategoryDrum.vue`** - Reusable drum component
4. **Refactor `WelcomeScreen.vue`** - 3-step flow with transitions
5. **Add haptic feedback** - Capacitor Haptics plugin
6. **Test touch gestures** - iOS Safari and Android Chrome
7. **Polish animations** - Ensure 60fps on older devices

### Shared vs Platform-Specific Code

| Aspect | Shared | Platform-Specific |
|--------|--------|-------------------|
| Category data structure | ✅ Same JSON schema | |
| UX flow (3 steps) | ✅ Same concept | |
| Drum interaction | ✅ Same gestures | |
| Animation CSS | | ✅ Lighter on mobile |
| Sound effects | | ✅ Web Audio (web) vs native (mobile) |
| Haptics | | ✅ Capacitor only |
| Status bar | | ✅ Capacitor only |

---

## Summary

This UX design:
- ✅ Scales to unlimited categories and subcategories
- ✅ Feels playful (slot machine inspiration) yet intuitive
- ✅ Works great on mobile (swipe gestures) and desktop (click/keys)
- ✅ Supports educational use cases (age-based filtering, STEM)
- ✅ Maintains entertainment value (YOLO mode, satisfying animations)
- ✅ Preserves existing theme system (colors, team names, etc.)
- ✅ Progressive disclosure (category → subcategory → config → play)
- ✅ **Mobile-native enhancements** (haptics, status bar, touch optimization)
- ✅ **Reusable components** (CategoryDrum works in both NiceGUI JS and Vue)
