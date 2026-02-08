const STOP_WORDS = new Set([
  'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'and', 'or', 'is', 'it',
  'ka', 'ki', 'ke', 'se', 'ko', 'hai', 'hain', 'ek', 'aur',
])

function normalize(str) {
  return str
    .toLowerCase()
    .trim()
    .replace(/[\u2018\u2019\u201C\u201D]/g, '') // smart quotes
    .replace(/\(.*?\)/g, '')                     // parentheticals
    .replace(/[^\w\s]/g, '')                     // punctuation
    .replace(/\s+/g, ' ')                        // collapse whitespace
    .trim()
}

function getWords(str) {
  return normalize(str).split(' ').filter((w) => w && !STOP_WORDS.has(w))
}

function levenshtein(a, b) {
  const m = a.length
  const n = b.length
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0))
  for (let i = 0; i <= m; i++) dp[i][0] = i
  for (let j = 0; j <= n; j++) dp[0][j] = j
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i - 1] === b[j - 1]
        ? dp[i - 1][j - 1]
        : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    }
  }
  return dp[m][n]
}

function levenshteinSimilarity(a, b) {
  const na = normalize(a)
  const nb = normalize(b)
  if (!na || !nb) return 0
  const dist = levenshtein(na, nb)
  return 1 - dist / Math.max(na.length, nb.length)
}

function diceCoefficient(a, b) {
  const wordsA = getWords(a)
  const wordsB = getWords(b)
  if (!wordsA.length || !wordsB.length) return 0
  const setA = new Set(wordsA)
  const setB = new Set(wordsB)
  let intersection = 0
  for (const w of setA) {
    if (setB.has(w)) intersection++
  }
  return (2 * intersection) / (setA.size + setB.size)
}

function containment(a, b) {
  const na = normalize(a)
  const nb = normalize(b)
  if (!na || !nb) return 0
  if (na.includes(nb) || nb.includes(na)) return 0.9
  return 0
}

export function fuzzyMatch(guess, answer, { threshold = 0.65 } = {}) {
  const ng = normalize(guess)
  const na = normalize(answer)

  if (!ng || !na) {
    return { match: false, score: 0, method: 'empty', transcription: guess }
  }

  // Exact match
  if (ng === na) {
    return { match: true, score: 1.0, method: 'exact', transcription: guess }
  }

  // Containment
  const cont = containment(guess, answer)
  if (cont >= threshold) {
    return { match: true, score: cont, method: 'containment', transcription: guess }
  }

  // Dice coefficient
  const dice = diceCoefficient(guess, answer)

  // Levenshtein similarity
  const lev = levenshteinSimilarity(guess, answer)

  const best = Math.max(cont, dice, lev)
  const method = best === dice ? 'dice' : best === lev ? 'levenshtein' : 'containment'

  return { match: best >= threshold, score: best, method, transcription: guess }
}
