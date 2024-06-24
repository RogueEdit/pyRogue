# V0.3.3

## Naming Convention
- Everything camelCase with prefixes
- Functions are prefixed with f_
- Fuction Helpers are prefixed with fh_
- "" for JSON and to make escaping easier, otherwise ''

## Bugfixes
- Fixed maxStacks in itemLogic
  - Berry Pouch from `(1)` to `(3)`
  - Vitamin Stacks from `(20)` to `(31)`

## Additions
- Added Autocompleter Bidirectional functionality
  - You can now type either ID or Name's
- Added Autocompleter to `f_editBiomes()`, `f_addCandies()`
- `f_addEggsGenerator`() full rewritten;
  - New save structure from game, we now use the first egg we find as sample and if we don't find one we provided a basic that testedly works
    - Added `isShiny` and `overrideHiddenAbility` flags
- Added (0: Cancel) everywhere aswell as you can type `cancel` or press `STRG+C` to escape from subMenus

- Added function helpers
  - `fh_getIntInput()`, `fh_getChoiceInput()`, `fh_getCompleterInput()`
    - Sanitizes input, allows to escape from submenus more consistently

## Rewrites
- Added functionality and decorators to handle error responses centralized
- Renamed  variable and function to comply with naming convention
- Rewritten input to use functionHelpers(`fh_`-definitions) to remove redundant code
- Affected Functions so far
    - `f_unlockAllCombined(tested:works)`
    - `f_editAccountStats()`
    - `f_editHatchWaves()`
    - `f_editMoney()`
    - `f_editPokeballs()`
    - `f_changeSaveSlot()`
    - `f_submenuEditor()`
    - `f_editBiome()`
    - `f_addCandies()`
    - `f_addEggsGenerator()`

