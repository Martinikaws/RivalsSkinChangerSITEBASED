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

## Skyboxes

Since Roblox build cec3ad5 (October 2026) a sky made of images other than the
game's own crashes Rivals on the next map load. That covered every uploaded sky
and custom image id tried so far. So the changer only writes images the game's
own skies use: Blue, Station, Graveyard, Sudden Death, Space, Westown, Black and
Classic. Any other sky is turned down with a message, whether it comes as
`Preset=`, `All=` or per-face `BK=` ... `UP=` lines. Picking another sky, or
none, puts back what an earlier run wrote without a rejoin.

To try a sky anyway, add `Force=yes` to the `[Skybox]` section:

```
[Skybox]
Preset=cloudy 01
Force=yes
```

If it crashes, rejoin and remove the line.

The uploaded skies' images belong to the account that uploaded them. Two
scripts in [`tools`](tools) help get them working again (Python 3):

1. `open_use_skies.py` makes every uploaded sky image Open Use (needs an Open
   Cloud API key with the Asset Permissions API) and says whether they were
   Restricted, which would stop Rivals loading them. If some were, try one sky
   with `Force=yes`.
2. If they were Open Use already, `check_sky_faces.py` checks the prepared
   faces (`tools/skies/prepared` in the site repo) for faces that aren't
   square, the same size or plain RGB.
