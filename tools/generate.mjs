#!/usr/bin/env node

/**
 * Content generation pipeline CLI.
 *
 * Usage:
 *   node generate.mjs <config-file> [options]
 *
 * Options:
 *   --dry-run       Validate config and print plan only
 *   --images-only   Skip data JSON generation
 *   --data-only     Skip image generation
 *   --force         Re-generate existing images
 *   --concurrency N Parallel API calls (default: 2)
 */

import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import dotenv from 'dotenv';

import { validateConfig } from './lib/config-schema.mjs';
import { ImageGenerator } from './lib/image-generator.mjs';
import { writeImage, imageExists, buildImagePath } from './lib/image-writer.mjs';
import { writeDataFile } from './lib/data-writer.mjs';
import { printIntegrationSteps } from './lib/integration-printer.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '..');

// --- Argument parsing ---

function parseArgs(argv) {
  const args = argv.slice(2);
  const opts = {
    configFile: null,
    dryRun: false,
    imagesOnly: false,
    dataOnly: false,
    force: false,
    concurrency: 2,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--dry-run') {
      opts.dryRun = true;
    } else if (arg === '--images-only') {
      opts.imagesOnly = true;
    } else if (arg === '--data-only') {
      opts.dataOnly = true;
    } else if (arg === '--force') {
      opts.force = true;
    } else if (arg === '--concurrency') {
      const val = parseInt(args[++i], 10);
      if (isNaN(val) || val < 1) {
        console.error('Error: --concurrency must be a positive integer');
        process.exit(1);
      }
      opts.concurrency = val;
    } else if (arg.startsWith('-')) {
      console.error(`Unknown option: ${arg}`);
      printUsage();
      process.exit(1);
    } else {
      opts.configFile = arg;
    }
  }

  if (!opts.configFile) {
    printUsage();
    process.exit(1);
  }

  return opts;
}

function printUsage() {
  console.log(`
Usage: node generate.mjs <config-file> [options]

Options:
  --dry-run       Validate config and print plan only
  --images-only   Skip data JSON generation
  --data-only     Skip image generation
  --force         Re-generate existing images
  --concurrency N Parallel API calls (default: 2)
`);
}

// --- Concurrency limiter ---

async function runWithConcurrency(tasks, concurrency) {
  const results = [];
  let index = 0;

  async function worker() {
    while (index < tasks.length) {
      const i = index++;
      results[i] = await tasks[i]();
    }
  }

  const workers = Array.from({ length: Math.min(concurrency, tasks.length) }, () => worker());
  await Promise.all(workers);
  return results;
}

// --- Main ---

async function main() {
  const opts = parseArgs(process.argv);

  // Load .env
  dotenv.config({ path: resolve(__dirname, '.env') });

  // Load config
  const configPath = resolve(opts.configFile);
  let config;
  try {
    const raw = readFileSync(configPath, 'utf-8');
    config = JSON.parse(raw);
  } catch (err) {
    console.error(`Error reading config: ${err.message}`);
    process.exit(1);
  }

  // Validate
  console.log(`Validating config: ${configPath}`);
  try {
    validateConfig(config);
    console.log('Config is valid.\n');
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }

  // Plan summary
  const imageFolder = config.theme.imageFolder;
  const itemCount = config.items.length;
  const existingCount = config.items.filter(item =>
    imageExists(buildImagePath(PROJECT_ROOT, imageFolder, item.id))
  ).length;
  const toGenerate = opts.force ? itemCount : itemCount - existingCount;

  console.log('Plan:');
  console.log(`  Category:     ${config.category.key}`);
  console.log(`  Items:        ${itemCount}`);
  console.log(`  Images exist: ${existingCount}`);
  console.log(`  To generate:  ${toGenerate}`);
  console.log(`  Model:        ${config.imageDefaults.model}`);
  console.log(`  Image folder: mobile-app/public/${imageFolder}/`);
  console.log(`  Data file:    mobile-app/src/data/${config.category.key}.json`);

  if (opts.dryRun) {
    console.log('\n--dry-run: stopping here.');
    printIntegrationSteps(config);
    return;
  }

  // Image generation
  let generated = 0;
  let skipped = 0;
  let failed = 0;

  if (!opts.dataOnly) {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      console.error('\nError: GEMINI_API_KEY not set. Create tools/.env with your key.');
      process.exit(1);
    }

    const generator = new ImageGenerator(apiKey);
    const model = config.imageDefaults.model;
    const stylePrefix = config.imageDefaults.stylePrefix || '';
    const styleSuffix = config.imageDefaults.styleSuffix || '';

    console.log(`\nGenerating images (concurrency: ${opts.concurrency})...\n`);

    const tasks = config.items.map((item, idx) => async () => {
      const outputPath = buildImagePath(PROJECT_ROOT, imageFolder, item.id);

      if (!opts.force && imageExists(outputPath)) {
        console.log(`  [${idx + 1}/${itemCount}] Skipping ${item.id}.webp (exists)`);
        skipped++;
        return;
      }

      const fullPrompt = [stylePrefix, item.imagePrompt, styleSuffix]
        .filter(Boolean)
        .join(' ');

      console.log(`  [${idx + 1}/${itemCount}] Generating ${item.id}.webp...`);

      try {
        const imageBuffer = await generator.generate(fullPrompt, model);
        const result = await writeImage(imageBuffer, outputPath, opts.force);
        if (result.written) {
          generated++;
          console.log(`  [${idx + 1}/${itemCount}] Saved ${item.id}.webp`);
        }
      } catch (err) {
        failed++;
        console.error(`  [${idx + 1}/${itemCount}] FAILED ${item.id}: ${err.message}`);
      }
    });

    await runWithConcurrency(tasks, opts.concurrency);
  }

  // Data JSON
  if (!opts.imagesOnly) {
    console.log('\nWriting data JSON...');
    const dataPath = writeDataFile(config, PROJECT_ROOT);
    console.log(`  Written: ${dataPath}`);
  }

  // Summary
  console.log('\nSummary:');
  if (!opts.dataOnly) {
    console.log(`  Images generated: ${generated}`);
    console.log(`  Images skipped:   ${skipped}`);
    console.log(`  Images failed:    ${failed}`);
  }
  if (!opts.imagesOnly) {
    console.log(`  Data JSON:        written`);
  }

  // Integration instructions
  printIntegrationSteps(config);

  if (failed > 0) {
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
