<template>
  <div>
    <p>Bollywood Frames - Mobile App</p>
    <p>Theme: {{ store.theme }} | Movies: {{ store.totalCount }}</p>
  </div>
</template>

<script setup>
import { useGameStore } from '../stores/gameStore.js'
const store = useGameStore()
store.init()
</script>
