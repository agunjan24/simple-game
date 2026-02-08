/**
 * Config JSON validator for the content generation pipeline.
 * Validates structure, required fields, and value constraints.
 */

const REQUIRED_COLOR_KEYS = [
  'primary', 'primaryLight', 'primaryDark',
  'accent', 'accentDark', 'secondary',
  'bgDark', 'bgMid', 'bgLight',
  'textLight', 'textDark',
];

const VALID_DIFFICULTIES = ['Easy', 'Medium', 'Hard'];
const VALID_PARENT_ACTIONS = ['create', 'add_subcategory'];
const HEX_COLOR_RE = /^#[0-9A-Fa-f]{6}$/;

class ValidationError extends Error {
  constructor(errors) {
    super(`Config validation failed:\n  - ${errors.join('\n  - ')}`);
    this.name = 'ValidationError';
    this.errors = errors;
  }
}

export function validateConfig(config) {
  const errors = [];

  // Top-level version
  if (config.version !== 1) {
    errors.push(`"version" must be 1, got ${config.version}`);
  }

  // Category block
  if (!config.category) {
    errors.push('Missing "category" block');
  } else {
    if (!config.category.key || typeof config.category.key !== 'string') {
      errors.push('"category.key" is required and must be a string');
    }
    if (!config.category.concept) {
      errors.push('"category.concept" is required');
    }
  }

  // Theme block
  if (!config.theme) {
    errors.push('Missing "theme" block');
  } else {
    for (const field of ['name', 'titleText', 'categoryLabel', 'gameTitle', 'subtitle', 'imageFolder']) {
      if (!config.theme[field]) {
        errors.push(`"theme.${field}" is required`);
      }
    }

    // Colors
    if (!config.theme.colors) {
      errors.push('Missing "theme.colors"');
    } else {
      for (const key of REQUIRED_COLOR_KEYS) {
        const val = config.theme.colors[key];
        if (!val) {
          errors.push(`"theme.colors.${key}" is required`);
        } else if (!HEX_COLOR_RE.test(val)) {
          errors.push(`"theme.colors.${key}" must be a hex color (e.g. #FF0000), got "${val}"`);
        }
      }
    }

    // Team names
    if (!Array.isArray(config.theme.teamNames) || config.theme.teamNames.length < 2) {
      errors.push('"theme.teamNames" must be an array of at least 2 pairs');
    } else {
      for (let i = 0; i < config.theme.teamNames.length; i++) {
        const pair = config.theme.teamNames[i];
        if (!Array.isArray(pair) || pair.length !== 2) {
          errors.push(`"theme.teamNames[${i}]" must be a [name1, name2] pair`);
        }
      }
    }

    // Phrases
    if (!Array.isArray(config.theme.winnerPhrases) || config.theme.winnerPhrases.length < 1) {
      errors.push('"theme.winnerPhrases" must have at least 1 entry');
    }
    if (!Array.isArray(config.theme.loserPhrases) || config.theme.loserPhrases.length < 1) {
      errors.push('"theme.loserPhrases" must have at least 1 entry');
    }
  }

  // Parent category
  if (!config.parentCategory) {
    errors.push('Missing "parentCategory" block');
  } else {
    const pc = config.parentCategory;
    if (!VALID_PARENT_ACTIONS.includes(pc.action)) {
      errors.push(`"parentCategory.action" must be one of: ${VALID_PARENT_ACTIONS.join(', ')}`);
    }
    if (pc.action === 'add_subcategory' && !pc.existingCategoryKey) {
      errors.push('"parentCategory.existingCategoryKey" is required when action is "add_subcategory"');
    }
    if (pc.action === 'create') {
      for (const field of ['key', 'icon', 'name', 'color', 'colorDark']) {
        if (!pc[field]) {
          errors.push(`"parentCategory.${field}" is required when action is "create"`);
        }
      }
    }
    if (!pc.subcategoryKey) {
      errors.push('"parentCategory.subcategoryKey" is required');
    }
    if (!pc.subcategoryName) {
      errors.push('"parentCategory.subcategoryName" is required');
    }
  }

  // Items
  if (!Array.isArray(config.items) || config.items.length === 0) {
    errors.push('"items" must be a non-empty array');
  } else {
    const ids = new Set();
    for (let i = 0; i < config.items.length; i++) {
      const item = config.items[i];
      if (!item.id) {
        errors.push(`"items[${i}].id" is required`);
      } else if (ids.has(item.id)) {
        errors.push(`Duplicate item id: "${item.id}"`);
      } else {
        ids.add(item.id);
      }
      if (!item.title) errors.push(`"items[${i}].title" is required`);
      if (!item.hint) errors.push(`"items[${i}].hint" is required`);
      if (!item.category) errors.push(`"items[${i}].category" is required`);
      if (!VALID_DIFFICULTIES.includes(item.difficulty)) {
        errors.push(`"items[${i}].difficulty" must be one of: ${VALID_DIFFICULTIES.join(', ')}`);
      }
      if (!item.imagePrompt) errors.push(`"items[${i}].imagePrompt" is required`);
    }
  }

  // Image defaults
  if (!config.imageDefaults) {
    errors.push('Missing "imageDefaults" block');
  } else {
    if (!config.imageDefaults.model) {
      errors.push('"imageDefaults.model" is required');
    }
  }

  if (errors.length > 0) {
    throw new ValidationError(errors);
  }

  return true;
}

export { ValidationError };
