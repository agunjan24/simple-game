let audioCtx = null

function getCtx() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)()
  return audioCtx
}

export function useAudio() {
  function playTick(timeLeft) {
    const ctx = getCtx()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()

    const freq = 880 + (10 - timeLeft) * 44
    osc.type = 'sine'
    osc.frequency.value = freq

    const duration = 0.08 + (timeLeft / 10) * 0.12

    gain.gain.setValueAtTime(0, ctx.currentTime)
    gain.gain.linearRampToValueAtTime(0.2, ctx.currentTime + 0.01)
    gain.gain.setValueAtTime(0.2, ctx.currentTime + duration - 0.02)
    gain.gain.linearRampToValueAtTime(0, ctx.currentTime + duration)

    osc.connect(gain)
    gain.connect(ctx.destination)

    osc.start()
    osc.stop(ctx.currentTime + duration)
  }

  function playVictory() {
    const ctx = getCtx()
    const notes = [523, 659, 784, 1047]
    const now = ctx.currentTime

    notes.forEach((freq, i) => {
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()

      osc.type = 'sine'
      osc.frequency.value = freq

      const startTime = now + i * 0.1
      gain.gain.setValueAtTime(0, startTime)
      gain.gain.linearRampToValueAtTime(0.15, startTime + 0.05)
      gain.gain.setValueAtTime(0.15, startTime + 0.3)
      gain.gain.linearRampToValueAtTime(0, startTime + 0.6)

      osc.connect(gain)
      gain.connect(ctx.destination)

      osc.start(startTime)
      osc.stop(startTime + 0.7)
    })
  }

  return { playTick, playVictory }
}
