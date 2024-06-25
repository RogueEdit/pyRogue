Currently work in progres...
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
- Added Autocompleter to `f_editBiomes()`, `f_addCandies()`, `f_editAccountStats()`
- `f_addEggsGenerator`() full rewritten;
  - New save structure from game, we now use the first egg we find as sample and if we don't find one we provided a basic that testedly works
    - Added `isShiny` and `overrideHiddenAbility` flags

- Added function helpers
  - `fh_getIntInput()`, `fh_getChoiceInput()`, `fh_getCompleterInput()`
    - Sanitizes input, allows to escape from submenus more consistently

- When editing acc stats
  - Removed playtime due to a recent change
  - Added 2 more options; randomize all - manual type all - manual choose one

- Added 4th "login" option which is just edit locally existing json without server connection (for Offline)

## Rewrites
- Added functionality and decorators to handle error responses centralized
- Renamed  variable and function to comply with naming convention
- Rewritten input to use functionHelpers(`fh_`-definitions) to remove redundant code
- Added (0: Cancel) everywhere aswell as you can type `cancel` or press `STRG+C` to escape from subMenus
  - Menus that present multiple options before saving will allow to type 0 to cancel+save;
  - or type exit / cancel to Abort without saves
  - All rewrites affect mentioned above affect those functions so far:
    - `f_editAccountStats(retested:works)` <Can now either random all, set one by choice (With AutoComplete by ID or Name) or loop over all one by one>
    - `f_editPokeballs(tested:works)` <Can now skip pokes, edit single ones or all> <Can now also skip choices>
    - `f_restoreBackup(tested:works)`
    - `f_editMoney(tested:works)`
    - `f_editHatchWaves(tested:works)`
    - `f_changeSaveSlot(tested:works)` <Can now change Slots directly>
    - `f_submenuEditor(tested:works)` - <Can now use Autocomplete and 0Cancel>
    - `f_editBiome(tested:works)` <Can now type ID or Biome, case-insesitive, with autocompleter>
    - `f_addEggsGenerator(tested:works)`
    - `f_addCandies(tested:works)` - #Error in function f_addCandies(): type object 'PokemonEnum' has no attribute 'items'


