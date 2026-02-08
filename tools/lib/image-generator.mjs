/**
 * Gemini/Imagen API wrapper for image generation.
 * Supports both Gemini native image gen and Imagen dedicated model.
 */

import { GoogleGenAI } from '@google/genai';

export class ImageGenerator {
  constructor(apiKey, opts = {}) {
    this.client = new GoogleGenAI({ apiKey });
    this.maxRetries = opts.maxRetries ?? 3;
    this.baseDelay = opts.baseDelay ?? 5000;
  }

  /**
   * Generate a single image from a prompt using the specified model.
   * Returns a Buffer of the raw image data (PNG from API).
   */
  async generate(prompt, model) {
    const isImagen = model.startsWith('imagen-');
    let lastError;

    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      if (attempt > 0) {
        const delay = this.baseDelay * Math.pow(2, attempt - 1);
        console.log(`    Retry ${attempt}/${this.maxRetries} after ${delay / 1000}s...`);
        await sleep(delay);
      }

      try {
        if (isImagen) {
          return await this._generateImagen(prompt, model);
        } else {
          return await this._generateGemini(prompt, model);
        }
      } catch (err) {
        lastError = err;
        const status = err.status || err.code;
        if (status === 429 || status === 500 || status === 503) {
          continue; // Retryable
        }
        throw err; // Non-retryable
      }
    }

    throw lastError;
  }

  async _generateImagen(prompt, model) {
    const response = await this.client.models.generateImages({
      model,
      prompt,
      config: {
        numberOfImages: 1,
        aspectRatio: '4:3',
        personGeneration: 'dont_allow',
      },
    });

    if (!response.generatedImages || response.generatedImages.length === 0) {
      throw new Error('Imagen returned no images');
    }

    const imageData = response.generatedImages[0].image;
    if (imageData.imageBytes) {
      return Buffer.from(imageData.imageBytes, 'base64');
    }
    throw new Error('Imagen response missing image bytes');
  }

  async _generateGemini(prompt, model) {
    const response = await this.client.models.generateContent({
      model,
      contents: prompt,
      config: {
        responseModalities: ['IMAGE'],
      },
    });

    const parts = response.candidates?.[0]?.content?.parts;
    if (!parts) {
      throw new Error('Gemini returned no content parts');
    }

    for (const part of parts) {
      if (part.inlineData) {
        return Buffer.from(part.inlineData.data, 'base64');
      }
    }

    throw new Error('Gemini response contained no image data');
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
