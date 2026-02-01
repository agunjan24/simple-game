<template>
  <div>
    <p>CineFrames - Mobile App</p>
    <p>Theme: {{ store.theme }} | {{ store.themeConfig.categoryLabelPlural }}: {{ store.totalCount }}</p>
  </div>
</template>

<script setup>
import { useGameStore } from '../stores/gameStore.js'
const store = useGameStore()
store.init()
</script>
