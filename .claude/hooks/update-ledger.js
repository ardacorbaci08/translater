#!/usr/bin/env node
/**
 * Auto-update CLAUDE.md ledger after file writes/edits.
 * Runs via PostToolUse hook when Write or Edit tools complete.
 * Logs changed files to the appropriate section based on directory (/frontend or /backend).
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const mdPath = path.join(__dirname, '../../CLAUDE.md');

try {
  // Get git status (staged and unstaged changes)
  const gitStatus = execSync('git status -s').toString().trim();

  if (!gitStatus) {
    process.exit(0); // No changes, exit silently
  }

  const date = new Date().toISOString().split('T')[0];
  const changedFiles = gitStatus
    .split('\n')
    .map(line => line.trim().split(/\s+/).slice(1).join(' '))
    .filter(Boolean);

  // Determine which section to update based on changed files
  const isFrontend = changedFiles.some(f => f.startsWith('frontend/'));
  const isBackend = changedFiles.some(f => f.startsWith('backend/'));

  let content = fs.readFileSync(mdPath, 'utf8');
  const fileList = changedFiles.join(', ');
  const newEntry = `- [${date}] Modified: ${fileList}\n`;

  if (isBackend) {
    content = content.replace(
      '### Backend State\n',
      `### Backend State\n${newEntry}`
    );
  }

  if (isFrontend) {
    content = content.replace(
      '### Frontend State\n',
      `### Frontend State\n${newEntry}`
    );
  }

  fs.writeFileSync(mdPath, content, 'utf8');
  console.log(`✅ Ledger updated: ${fileList.split(', ').length} file(s)`);

} catch (error) {
  // Silently fail if not in git repo or other issues
  process.exit(0);
}
