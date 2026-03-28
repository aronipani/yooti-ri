#!/usr/bin/env node
// Yooti pre-flight checks — runs on Mac, Linux, and Windows
// Usage: node pipeline/scripts/preflight.js

import { existsSync, readFileSync } from 'fs'
import { execSync } from 'child_process'

const results = []

function check(name, fn) {
  try {
    const result = fn()
    results.push({ name, pass: result !== false, reason: typeof result === 'string' ? result : null })
  } catch (err) {
    results.push({ name, pass: false, reason: err.message })
  }
}

// 1. Git repository exists
check('Git repository exists', () => {
  execSync('git rev-parse --git-dir', { stdio: 'ignore' })
  return true
})

// 2. Working tree is clean
check('Working tree is clean', () => {
  const out = execSync('git status --porcelain', { encoding: 'utf8' }).trim()
  if (out.length > 0) throw new Error('Uncommitted changes found. Commit or stash before running.')
  return true
})

// 3. docker-compose.yml exists
check('docker-compose.yml exists', () => {
  if (!existsSync('docker-compose.yml')) throw new Error('docker-compose.yml not found in project root')
  return true
})

// 4. .claude/CLAUDE.md exists
check('.claude/CLAUDE.md exists', () => {
  if (!existsSync('.claude/CLAUDE.md')) throw new Error('.claude/CLAUDE.md not found — run yooti init')
  return true
})

// 5. yooti.config.json exists and is valid JSON
check('yooti.config.json is valid', () => {
  if (!existsSync('yooti.config.json')) throw new Error('yooti.config.json not found — run yooti init')
  try {
    JSON.parse(readFileSync('yooti.config.json', 'utf8'))
  } catch {
    throw new Error('yooti.config.json contains invalid JSON')
  }
  return true
})

// 6. Pipeline scripts exist
check('Pipeline scripts exist', () => {
  const required = [
    'pipeline/scripts/preflight.js',
    'pipeline/scripts/snapshot.py',
    'pipeline/scripts/regression-diff.py',
    'pipeline/scripts/generate-pr-body.py',
  ]
  const missing = required.filter(f => !existsSync(f))
  if (missing.length > 0) throw new Error('Missing: ' + missing.join(', '))
  return true
})

// 7. Example artifacts exist
check('Example artifacts exist', () => {
  if (!existsSync('.agent/examples')) throw new Error('.agent/examples not found — run yooti init')
  return true
})

// ── Results ──
const pass = results.filter(r => r.pass).length
const fail = results.filter(r => !r.pass).length

console.log('')
results.forEach(r => {
  const icon = r.pass ? '✓' : '✗'
  const color = r.pass ? '\x1b[32m' : '\x1b[31m'
  const reset = '\x1b[0m'
  console.log('  ' + color + icon + reset + ' ' + r.name)
  if (!r.pass && r.reason) console.log('    \x1b[2m→ ' + r.reason + '\x1b[0m')
})

console.log('')
console.log('  ' + pass + '/' + results.length + ' checks passed')

if (fail > 0) {
  const s = fail > 1 ? 's' : ''
  console.log('\n  \x1b[31m' + fail + ' check' + s + ' failed. Fix the issues above before continuing.\x1b[0m\n')
  process.exit(1)
} else {
  console.log('  \x1b[32mAll checks passed. Ready to start sprint.\x1b[0m\n')
  process.exit(0)
}