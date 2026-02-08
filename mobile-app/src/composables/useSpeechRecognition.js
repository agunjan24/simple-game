import { ref } from 'vue'
import { Capacitor } from '@capacitor/core'

let capacitorPlugin = null
let webRecognition = null

export function useSpeechRecognition() {
  const isAvailable = ref(false)
  const isListening = ref(false)
  const transcript = ref('')
  const error = ref(null)
  const unavailableReason = ref('')

  let timeoutId = null

  async function checkAvailability() {
    // Native platform: try Capacitor plugin
    if (Capacitor.isNativePlatform()) {
      try {
        const mod = await import('@capacitor-community/speech-recognition')
        capacitorPlugin = mod.SpeechRecognition
        const { available } = await capacitorPlugin.available()
        if (available) {
          const perm = await capacitorPlugin.requestPermissions()
          isAvailable.value = perm.speechRecognition === 'granted'
          if (!isAvailable.value) unavailableReason.value = 'Microphone permission denied'
          return
        }
      } catch {
        // Plugin not installed or not available
      }
    }

    // Web fallback: check for Web Speech API
    const SpeechAPI = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechAPI) {
      unavailableReason.value = 'Browser does not support speech recognition'
      return
    }

    // Web Speech API requires secure context (HTTPS or localhost)
    if (!window.isSecureContext) {
      unavailableReason.value = 'Mic requires HTTPS or localhost'
      return
    }

    isAvailable.value = true
  }

  async function startListening(language = 'en-US') {
    if (!isAvailable.value || isListening.value) return
    transcript.value = ''
    error.value = null
    isListening.value = true

    // Safety timeout: 5 seconds
    timeoutId = setTimeout(() => {
      stopListening()
    }, 5000)

    if (capacitorPlugin) {
      try {
        const result = await capacitorPlugin.start({
          language,
          maxResults: 1,
          partialResults: false,
          popup: false,
        })
        clearTimeout(timeoutId)
        isListening.value = false
        if (result?.matches?.length) {
          transcript.value = result.matches[0]
        }
      } catch (e) {
        clearTimeout(timeoutId)
        isListening.value = false
        error.value = e.message || 'Speech recognition failed'
      }
      return
    }

    // Web Speech API fallback
    const SpeechAPI = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechAPI) {
      isListening.value = false
      error.value = 'Speech recognition not supported'
      return
    }

    webRecognition = new SpeechAPI()
    webRecognition.lang = language
    webRecognition.interimResults = false
    webRecognition.maxAlternatives = 1

    webRecognition.onresult = (event) => {
      const result = event.results[0]
      if (result?.length) {
        transcript.value = result[0].transcript
      }
    }

    webRecognition.onerror = (event) => {
      error.value = event.error
      isListening.value = false
      clearTimeout(timeoutId)
    }

    webRecognition.onend = () => {
      isListening.value = false
      clearTimeout(timeoutId)
    }

    webRecognition.start()
  }

  function stopListening() {
    clearTimeout(timeoutId)
    isListening.value = false

    if (capacitorPlugin) {
      capacitorPlugin.stop().catch(() => {})
      return
    }

    if (webRecognition) {
      webRecognition.abort()
      webRecognition = null
    }
  }

  return { isAvailable, isListening, transcript, error, unavailableReason, checkAvailability, startListening, stopListening }
}
