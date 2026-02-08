/**
 * Image writer with WebP conversion via sharp.
 * Converts raw image data to 1200x900 WebP and saves idempotently.
 */

import sharp from 'sharp';
import { existsSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';

const TARGET_WIDTH = 1200;
const TARGET_HEIGHT = 900;
const WEBP_QUALITY = 85;

/**
 * Save image buffer as a WebP file at the given path.
 * Resizes to 1200x900, converts to WebP quality 85.
 *
 * @param {Buffer} imageBuffer - Raw image data from API
 * @param {string} outputPath - Full path to write the .webp file
 * @param {boolean} force - Overwrite if file exists
 * @returns {{ written: boolean, path: string }}
 */
export async function writeImage(imageBuffer, outputPath, force = false) {
  if (!force && existsSync(outputPath)) {
    return { written: false, path: outputPath };
  }

  // Ensure output directory exists
  const dir = dirname(outputPath);
  mkdirSync(dir, { recursive: true });

  await sharp(imageBuffer)
    .resize(TARGET_WIDTH, TARGET_HEIGHT, { fit: 'cover' })
    .webp({ quality: WEBP_QUALITY })
    .toFile(outputPath);

  return { written: true, path: outputPath };
}

/**
 * Check if an image already exists at the given path.
 */
export function imageExists(outputPath) {
  return existsSync(outputPath);
}

/**
 * Build the output path for an item's image.
 */
export function buildImagePath(projectRoot, imageFolder, itemId) {
  return join(projectRoot, 'mobile-app', 'public', imageFolder, `${itemId}.webp`);
}
