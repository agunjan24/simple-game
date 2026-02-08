# Content Generation Pipeline

Automates adding new categories to the guessing game. Takes a config JSON (produced during brainstorming), generates images via Google Gemini API, creates the data JSON, and prints integration instructions.

## Setup

```bash
cd tools
npm install
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## Usage

```bash
node generate.mjs <config-file> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Validate config and print plan only (no API calls) |
| `--images-only` | Generate images but skip data JSON |
| `--data-only` | Write data JSON but skip image generation |
| `--force` | Re-generate images even if they already exist |
| `--concurrency N` | Parallel API calls (default: 2) |

### Examples

```bash
# Validate a config without generating anything
node generate.mjs configs/_example.json --dry-run

# Generate everything
node generate.mjs configs/_example.json

# Re-generate only images, overwriting existing ones
node generate.mjs configs/_example.json --images-only --force

# Only write the data JSON (images already generated)
node generate.mjs configs/_example.json --data-only
```

## Brainstorming Workflow

The config JSON is the bridge between brainstorming and automation. Use this workflow with Claude:

### 1. Concept
Decide what category to add. What's being guessed? What visual approach avoids real-person likenesses?

### 2. Item List
Claude generates 15-25 candidates with title, hint, category, and difficulty. You curate the list.

### 3. Image Prompts
Claude drafts an `imagePrompt` for each item. Review a few key ones to ensure the style is right.

### 4. Theme Design
Pick colors, team names, winner/loser phrases, labels. Decide where it fits in the category tree (new top-level category or subcategory of an existing one).

### 5. Config Assembly
Claude produces the final JSON. Save it to `tools/configs/<name>.json`.

### 6. Generation
```bash
node generate.mjs configs/<name>.json --dry-run   # Check the plan
node generate.mjs configs/<name>.json              # Generate everything
```

### 7. Integration
Follow the printed instructions to add the theme and data imports to `themes.js` and `gameStore.js`.

## Config JSON Schema

See `configs/_example.json` for a complete annotated example.

### Top-level fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | `1` | Schema version (must be 1) |
| `category` | object | Category metadata (key, concept, visualApproach) |
| `theme` | object | Full theme config matching the THEMES format in themes.js |
| `parentCategory` | object | Where to place in the category tree |
| `items` | array | List of items to generate |
| `imageDefaults` | object | Shared image generation settings |

### `parentCategory.action`

- `"create"` — New top-level category (like Movies, History). Requires `key`, `icon`, `name`, `color`, `colorDark`.
- `"add_subcategory"` — Add under existing category. Requires `existingCategoryKey`.

Both require `subcategoryKey` and `subcategoryName`.

### `items[]` fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID, used as filename (e.g. `jordan_last_shot`) |
| `title` | string | Display name (what the player guesses) |
| `hint` | string | Hint shown to the player |
| `category` | string | Sub-category label (e.g. "Basketball") |
| `difficulty` | string | `Easy`, `Medium`, or `Hard` |
| `imagePrompt` | string | Prompt for image generation (item-specific part) |

### `imageDefaults` fields

| Field | Type | Description |
|-------|------|-------------|
| `stylePrefix` | string | Prepended to every image prompt |
| `styleSuffix` | string | Appended to every image prompt |
| `model` | string | `imagen-3.0-generate-002` or `gemini-2.0-flash-exp` |

## Supported Models

| Model | Method | Notes |
|-------|--------|-------|
| `imagen-3.0-generate-002` | `generateImages()` | Dedicated image model, aspect ratio control |
| `gemini-2.0-flash-exp` | `generateContent()` | Fast, native image gen |

## Idempotency

The script is safe to re-run:
- Existing images are skipped (unless `--force`)
- Data JSON is overwritten with the current config
- Partial failures can be resumed by re-running

## Output

Generated files:
- Images: `mobile-app/public/<imageFolder>/<id>.webp` (1200x900, WebP quality 85)
- Data: `mobile-app/src/data/<category.key>.json`
