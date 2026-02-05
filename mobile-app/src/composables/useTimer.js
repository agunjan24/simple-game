import { ref, onUnmounted } from 'vue'

export function useTimer(store) {
  const intervalId = ref(null)

  function start() {
    stop()
    store.timerActive = true
    intervalId.value = setInterval(() => {
      if (store.timeLeft > 0) {
        store.timeLeft--
      } else {
        stop()
      }
    }, 1000)
  }

  function stop() {
    store.timerActive = false
    if (intervalId.value !== null) {
      clearInterval(intervalId.value)
      intervalId.value = null
    }
  }

  function reset(duration) {
    stop()
    store.timeLeft = duration
  }

  onUnmounted(() => stop())

  return { start, stop, reset }
}
