# Rivals Changer (site-based)

The changer itself, configured from the website:
**[martinikaws.github.io/rivals-skins](https://martinikaws.github.io/rivals-skins/)**

Pick your skins, swaps, wraps, finishers, charms, skybox and lighting there,
save `rivals_config.lua` into `C:\matcha\workspace`, then run `main.lua` in
Matcha. Put it in `C:\matcha\autoexec` to have it run on every join - one copy
there and no separate loader, or it starts twice and the second start is
refused by its own lock.

Only you see the changes. Nothing is sent to the server.

Prefer to choose everything in game? The same changer with a Matcha menu is in
[RivalsSkinChangerFULLMATCHA](https://github.com/Martinikaws/RivalsSkinChangerFULLMATCHA),
which reads the item lists from the running game instead of the website. Both
use the same `rivals_config.lua`, so you can switch between them freely.

## What it does

- **Skins** for every weapon, with their animations, offsets and hotbar icons.
- **Swaps**: equip a skin you own and it looks like another skin of the same
  weapon.
- **Wraps**, **finishers** and **charms**: the one you own looks like another,
  season charms down to the rank.
- **Skybox** and a darker **lighting** preset.

## When things apply

| Change | When you see it |
| --- | --- |
| Skins, swaps, wraps | Straight away; re-equip the weapon |
| Charms | Next time you equip the weapon |
| Finishers | The next time the finisher plays |
| Skybox | Next map or area load |
| Lighting | Straight away, and it survives map changes |

Run it once per server; a first run takes about three seconds. It stops quietly
in any game other than Rivals, and refuses to start a second run while one is
going.

## Roblox updates

The changer downloads the latest Roblox offsets list on each run, but uses it
only when it's for the Roblox build you're running: the version Matcha reports,
or, where it can't, a check that the list's pointers lead to this game. The list follows the newest
Roblox, and a bootstrapper can keep you on an older one. Every list is saved in
`rivals_offsets\` under its Roblox version, so an older build finds its own;
with none that fits, the built-in offsets are used. The console's `Offsets:`
line says which, and the sky, lighting, sound and name changes check their
fields in the game first and are skipped if they don't fit.

## Skyboxes

The changer writes the images of its own skies: the game's (Blue, Station,
Graveyard, Sudden Death, Space, Westown, Black) and the 91 uploaded
ones. Since Roblox build cec3ad5 (October 2026) a sky the game can't load
crashes Rivals on the next map load, so any other image id is turned down with
a message, whether it comes as `Preset=`, `All=` or per-face `BK=` ... `UP=`
lines. To try one anyway, add `Force=yes` to the `[Skybox]` section:

```
[Skybox]
All=123456789
Force=yes
```

Only image numbers (`rbxassetid://`) can be written, even with `Force=yes`.
Each sky face records which kind of address it holds, and the map skies hold
image numbers. The old Classic sky wrote Roblox's own `rbxasset://sky/...`
files over them; Roblox then read each path as a broken image number and
crashed. Classic is gone, and local files and links are turned down.

Picking another sky, or none, puts back what an earlier run wrote without a
rejoin, as long as Matcha hasn't restarted in between (otherwise rejoin).

The uploaded skies crashed the game on build cec3ad5, while the game's own
skies didn't. The changer used to rewrite the sky on screen as well as the map
templates; the next map load then freed that sky's textures under image ids the
game had never loaded, which is the likely cause (the game preloads its own sky
images, so those were found). It now rewrites only the templates, which is all
a map load reads. If an uploaded sky still crashes, rejoin, pick another sky,
and run the scripts in [`tools`](tools) (Python 3):

1. `open_use_skies.py` makes every uploaded sky image Open Use (needs an Open
   Cloud API key with the Asset Permissions API) and says whether they were
   Restricted, which would stop Rivals loading them.
2. If they were Open Use already, `check_sky_faces.py` checks the prepared
   faces (`tools/skies/prepared` in the site repo) for faces that aren't
   square, the same size or plain RGB.
