----
Branches
main -> need pull-request with author review and 1 approval+ passed workflow checks 
dev -> need pull-request force mergeable bypassing checks,
test -> nothing
----
Developing on test, when a feature/fix etc done PR to Dev with a nice Pull-Request title
then click ACtions > Build .exe to create a full /compiled/ suite for all OS
release drafter will reflect those PR in the draft
----
PR to Test -> Ruff & CodeQL (Security Analysis)
PR from Test to Dev -> automatic build of .exes in /compiled/ with bypassable checks on pull, but they will run afterwards
PR to Dev to Main -> automatic release since all checks have to be passed
---
Build Setup
deletes /compiled/ and all files
moves src/data/ to /compiled/data/
moves src/patch/game-data.ts to /compiled/patch/game-data.ts
builds .exes and places accordingly

Triggered from PR Test -> Dev
--- 
Release Setup
Bundles
 
SavefileConverter
respective .exe/.sh and /data/ of offlineEditor
respective .exe/.sh and game-data.ts of Patcher

Triggered by PR from Dev -> Main
---
All Pull-Requests and issues will be automatically labeled  based on keywords like
bugfix, enhance, workflow, feature, optimization, database 
