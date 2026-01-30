export function useConfetti() {
  function createConfetti(colors) {
    const fallbackColors = ['#D4AF37', '#E91E63', '#00BFA5', '#F4D03F']
    const palette = colors || fallbackColors

    for (let i = 0; i < 50; i++) {
      const confetti = document.createElement('div')
      confetti.className = 'confetti'
      confetti.style.position = 'fixed'
      confetti.style.top = '-10px'
      confetti.style.left = Math.random() * 100 + 'vw'
      confetti.style.width = '10px'
      confetti.style.height = '10px'
      confetti.style.borderRadius = '50%'
      confetti.style.background = palette[Math.floor(Math.random() * palette.length)]
      confetti.style.animation = `confettiFall ${2 + Math.random() * 2}s ease-in ${Math.random() * 2}s forwards`
      confetti.style.zIndex = '9999'
      document.body.appendChild(confetti)

      setTimeout(() => confetti.remove(), 5000)
    }
  }

  return { createConfetti }
}
