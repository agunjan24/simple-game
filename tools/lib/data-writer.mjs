/**
 * Data JSON file writer.
 * Maps config items to the game's data format and writes to mobile-app/src/data/.
 */

import { writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';

/**
 * Write the data JSON file for a category.
 *
 * @param {object} config - The full config object
 * @param {string} projectRoot - Root directory of the project
 * @returns {string} Path to the written file
 */
export function writeDataFile(config, projectRoot) {
  const data = config.items.map(item => ({
    filename: `${item.id}.webp`,
    title: item.title,
    hint: item.hint,
    category: item.category,
    difficulty: item.difficulty,
  }));

  const outputPath = join(projectRoot, 'mobile-app', 'src', 'data', `${config.category.key}.json`);
  const dir = dirname(outputPath);
  mkdirSync(dir, { recursive: true });

  writeFileSync(outputPath, JSON.stringify(data, null, 2) + '\n', 'utf-8');

  return outputPath;
}
