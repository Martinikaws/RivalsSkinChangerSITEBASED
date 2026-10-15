"""Make the uploaded sky images Open Use, and find out whether they were.

Since Roblox build cec3ad5 (Oct 2026) the uploaded skies crash RIVALS on the
next map load, so the changer turns them down. Images are created Open Use
unless the account opted into Asset Privacy (Creator Dashboard > Settings >
Advanced); a Restricted image can only load in games its owner can edit, and
RIVALS isn't one. This script asks Roblox to make every uploaded sky image
Open Use and reports what each one was:

- "made Open Use": it was Restricted, so RIVALS was never allowed to load it.
  Try one sky in game with Force=yes (see the README).
- "already Open Use": privacy isn't the cause. Run check_sky_faces.py on the
  prepared faces next.

Open Use can't be undone: anyone may then use these images in their games.

Needs an Open Cloud API key from create.roblox.com (Open Cloud > API Keys)
with the Asset Permissions API, write access, set in your own terminal:
    set ROBLOX_API_KEY=...        (Windows cmd)
    $env:ROBLOX_API_KEY="..."     (PowerShell)

    python open_use_skies.py            ask before changing anything
    python open_use_skies.py --yes      don't ask
    python open_use_skies.py --dry-run  only list the images

The image ids come from the uploaded entries of SKYBOX_PRESETS in ../main.lua.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CHANGER = os.path.join(HERE, "..", "main.lua")
API = "https://apis.roblox.com/asset-permissions-api/v1/assets/permissions"
GAME_SKIES = {"blue", "station", "graveyard", "sudden death", "space", "westown", "black", "classic"}
BATCH = 50


def uploaded_ids(path):
    """{asset id: sky name} for every uploaded sky in the changer's SKYBOX_PRESETS."""
    src = open(path, encoding="utf-8").read()
    start = src.index("local SKYBOX_PRESETS = {")
    block = src[start:src.index("\n}", start)]
    ids = {}
    for name, faces in re.findall(r'\["([^"]+)"\]\s*=\s*\{([^}]*)\}', block):
        if name not in GAME_SKIES:
            for asset in re.findall(r'"(\d+)"', faces):
                ids.setdefault(int(asset), name)
    return ids


def grant_open_use(key, batch):
    body = json.dumps({"subjectType": "All", "action": "Use",
                       "requests": [{"assetId": a} for a in batch]}).encode()
    req = urllib.request.Request(API, data=body, method="PATCH",
                                 headers={"x-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        raise RuntimeError("HTTP %d: %s" % (e.code, detail)) from None


def main(argv):
    ids = uploaded_ids(CHANGER)
    skies = sorted(set(ids.values()))
    print("%d uploaded sky images in %d skies" % (len(ids), len(skies)))
    if "--dry-run" in argv:
        for asset, name in sorted(ids.items(), key=lambda kv: (kv[1], kv[0])):
            print("  %-20s %d" % (name, asset))
        return 0
    key = os.environ.get("ROBLOX_API_KEY")
    if not key:
        print("Set ROBLOX_API_KEY first (see the top of this file).")
        return 1
    if "--yes" not in argv:
        answer = input("Make all %d images Open Use? This can't be undone. [y/N] " % len(ids))
        if answer.strip().lower() not in ("y", "yes"):
            print("Nothing changed.")
            return 1

    opened, already, failed = [], [], {}
    assets = sorted(ids)
    for i in range(0, len(assets), BATCH):
        batch = assets[i:i + BATCH]
        try:
            result = grant_open_use(key, batch)
        except Exception as e:
            print("Roblox refused the request: %s" % e)
            print("Check that the key has the Asset Permissions API with write access and belongs to")
            print("the account that uploaded the skies.")
            return 1
        opened += [int(a) for a in result.get("successAssetIds") or []]
        for err in result.get("errors") or []:
            code, asset = str(err.get("code")), int(err.get("assetId") or 0)
            (already if code == "PublicAssetCannotBeGrantedTo" else failed.setdefault(code, [])).append(asset)
        print("  %d/%d done" % (min(i + BATCH, len(assets)), len(assets)))
        time.sleep(1)  # the API allows 100 requests a minute

    print()
    print("made Open Use:    %d" % len(opened))
    print("already Open Use: %d" % len(already))
    for code, bad in sorted(failed.items()):
        names = sorted({ids.get(a, "?") for a in bad})
        print("failed (%s): %d - %s" % (code, len(bad), ", ".join(names[:12]) + (" ..." if len(names) > 12 else "")))
    print()
    if opened:
        print("Some images were Restricted, so RIVALS couldn't load them. Try one sky in game:")
        print("  [Skybox]")
        print("  Preset=%s" % ids[opened[0]])
        print("  Force=yes")
        print("If the next map shows it without crashing, the uploaded skies can be turned back on.")
    elif already and not failed:
        print("Every image was Open Use already, so privacy isn't why the skies crash.")
        print("Next: python check_sky_faces.py <path to rivals-skins/tools/skies/prepared>")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
