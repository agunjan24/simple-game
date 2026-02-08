/**
 * Prints copy-pastable integration code for themes.js and gameStore.js.
 */

/**
 * Print all integration instructions for a generated category.
 */
export function printIntegrationSteps(config) {
  const key = config.category.key;
  const themeKey = key;

  console.log('\n' + '='.repeat(70));
  console.log('  INTEGRATION INSTRUCTIONS');
  console.log('='.repeat(70));

  // Step 1: themes.js — THEMES entry
  console.log('\n--- Step 1: Add theme to THEMES in mobile-app/src/themes/themes.js ---');
  console.log('Add this entry inside the THEMES object (before the closing brace):\n');

  const t = config.theme;
  const themeCode = `  ${themeKey}: {
    name: '${t.name}',
    titleText: '${t.titleText}',
    colors: {
${Object.entries(t.colors).map(([k, v]) => `      ${k}: '${v}',`).join('\n')}
    },
    categoryLabel: '${t.categoryLabel}',
    categoryLabelPlural: '${t.categoryLabelPlural || t.categoryLabel + 's'}',
    gameTitle: '${t.gameTitle}',
    mashupGameTitle: '${t.mashupGameTitle || t.gameTitle}',
    subtitle: '${t.subtitle}',
    imageFolder: '${t.imageFolder}',
    teamNames: [
${t.teamNames.map(pair => `      ['${pair[0]}', '${pair[1]}'],`).join('\n')}
    ],
    winnerPhrases: [
${t.winnerPhrases.map(p => `      '${escapeQuotes(p)}',`).join('\n')}
    ],
    loserPhrases: [
${t.loserPhrases.map(p => `      '${escapeQuotes(p)}',`).join('\n')}
    ],
  },`;

  console.log(themeCode);

  // Step 2: themes.js — CATEGORIES entry
  console.log('\n--- Step 2: Update CATEGORIES in mobile-app/src/themes/themes.js ---');

  const pc = config.parentCategory;
  if (pc.action === 'create') {
    console.log(`Add this entry inside the CATEGORIES object (before mashup):\n`);
    const catCode = `  ${pc.key}: {
    icon: '${pc.icon}',
    name: '${pc.name}',
    description: '${escapeQuotes(pc.description || '')}',
    color: '${pc.color}',
    colorDark: '${pc.colorDark}',
    subcategories: {
      ${pc.subcategoryKey}: { icon: '${pc.subcategoryIcon || ''}', name: '${pc.subcategoryName}', themeKey: '${themeKey}' },
    },
  },`;
    console.log(catCode);
  } else {
    console.log(`Add this subcategory to the "${pc.existingCategoryKey}" category's subcategories:\n`);
    const subCode = `      ${pc.subcategoryKey}: { icon: '${pc.subcategoryIcon || ''}', name: '${pc.subcategoryName}', themeKey: '${themeKey}' },`;
    console.log(subCode);
  }

  // Step 3: gameStore.js — import + DATA_MAP
  console.log('\n--- Step 3: Update mobile-app/src/stores/gameStore.js ---');
  console.log('Add this import at the top with the other data imports:\n');
  console.log(`import ${key}Data from '../data/${key}.json'`);
  console.log('\nAdd this entry to the DATA_MAP object:\n');
  console.log(`  ${themeKey}: ${key}Data,`);

  // Step 4: mashup theme (optional)
  console.log('\n--- Step 4 (optional): Add to mashup ---');
  console.log('If you want this category included in Mashup mode, update the');
  console.log('mashup data loading in gameStore.js to include the new data.\n');

  console.log('='.repeat(70));
  console.log('  Done! Run the mobile app to verify: cd mobile-app && npm run dev');
  console.log('='.repeat(70) + '\n');
}

function escapeQuotes(str) {
  return str.replace(/'/g, "\\'");
}
