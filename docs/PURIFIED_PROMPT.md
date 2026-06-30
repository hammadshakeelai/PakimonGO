# Purified Product Prompt

Build PakimonGO, a large-scale mobile app inspired by location-based creature collection games, but focused on real-life animals photographed by users.

The app should launch on Android first as an installable APK, with a later path to iOS distribution. Users can log in with Google, email/password, and account recovery through email and phone. The app uses the phone camera and location to let users capture animal photos, submit details, earn points, save photos, share posts, and compete with friends and wider communities.

Users earn points from a server-side scoring system. Scoring should consider animal species, rarity, image quality, artistic/aesthetic value, distance and safety, whether the user is petting or near the animal, whether the animal is wild or someone else's pet, whether the owner is tagged, and whether the user provides a real name or cute name. Users should not know the exact score until after submission.

Zoo photos must be saved but should not produce normal score. If users honestly mark an animal as a zoo animal, they may receive a small limited participation point, but repeated zoo uploads should quickly stop giving points. The same animal should not count repeatedly unless it has clearly changed or there is a valid reason. Duplicate and spam behavior should reduce score or trigger review.

The app should include four leaderboard scopes: global, country, local, and friends. Low-score and new users should have catch-up opportunities, while high-score users should face harder progression and diminishing returns.

Social features should include public/private/friends-only visibility, chosen-friends visibility, captions, likes, comments, reposts, shares, hashtags, groups, collections, and map discovery. Users should be able to view what kinds of animals have been posted in an area. The map should feel game-like and polished, with realistic location data where possible, and include a simple GTA-style waypoint route feature.

The system must be built using a full SDLC and Agile process. Before coding, the team should think deeply, research options, derive requirements, write an Agile SRS, plan architecture, and define quality gates. The repository must support future AI-agent handoff by storing current task, current thinking, next task, backlog, technical debt, bugs, risks, decisions, and process notes.

The codebase should be modular, deeply organized, and designed for a large future project. Files should usually stay around 200-300 lines so AI models and humans can read, test, and modify them easily. Use context-preserving comments and references in code where helpful, while avoiding noisy comments.

Integrate a knowledge workflow using OKF-style structured knowledge files, Obsidian-friendly Markdown, and later Graphify/code-graph tooling so future agents can understand the codebase, decisions, requirements, and relationships without losing context.
