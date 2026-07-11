"""Fetch CC-licensed wildlife photos for demo seed content.

Source: iNaturalist taxa default photos (open-data S3 bucket). Every
photo carries a Creative Commons license_code and attribution string in
the API response; only CC-licensed photos are accepted and each one is
recorded in CREDITS.md.

Writes services/api/assets/demo/wild/<slug>.jpg (<=800px JPEG) + CREDITS.md.

Run:  python tools/fetch_demo_images.py
"""

from __future__ import annotations

import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "services" / "api" / "assets" / "demo" / "wild"
CREDITS = OUT_DIR / "CREDITS.md"

API = "https://api.inaturalist.org/v1/taxa"
UA = {"User-Agent": "PakimonGO-demo-seed/1.0 (educational demo content)"}

# (slug, iNaturalist query, expected common-name hint for sanity)
SPECIES = [
    ("house_sparrow", "Passer domesticus"),
    ("white_throated_kingfisher", "Halcyon smyrnensis"),
    ("golden_eagle", "Aquila chrysaetos"),
    ("markhor", "Capra falconeri"),
    ("himalayan_monal", "Lophophorus impejanus"),
    ("common_myna", "Acridotheres tristis"),
    ("hoopoe", "Upupa epops"),
    ("indian_peafowl", "Pavo cristatus"),
    ("gray_langur", "Semnopithecus entellus"),
    ("chital_deer", "Axis axis"),
    ("house_crow", "Corvus splendens"),
    ("great_egret", "Ardea alba"),
    ("red_vented_bulbul", "Pycnonotus cafer"),
    ("peacock_butterfly", "Aglais io"),
    ("red_fox", "Vulpes vulpes"),
    ("spotted_owlet", "Athene brama"),
    ("rose_ringed_parakeet", "Psittacula krameri"),
    ("indian_flapshell_turtle", "Lissemys punctata"),
    ("snow_leopard", "Panthera uncia"),
    ("himalayan_ibex", "Capra sibirica"),
    ("greater_flamingo", "Phoenicopterus roseus"),
    ("grey_heron", "Ardea cinerea"),
    # Expanded set for richer demo content.
    ("black_kite", "Milvus migrans"),
    ("cattle_egret", "Bubulcus ibis"),
    ("common_kingfisher", "Alcedo atthis"),
    ("purple_sunbird", "Cinnyris asiaticus"),
    ("indian_roller", "Coracias benghalensis"),
    ("little_egret", "Egretta garzetta"),
    ("black_drongo", "Dicrurus macrocercus"),
    ("green_bee_eater", "Merops orientalis"),
    ("red_wattled_lapwing", "Vanellus indicus"),
    ("jungle_babbler", "Argya striata"),
    ("indian_pond_heron", "Ardeola grayii"),
    ("wild_boar", "Sus scrofa"),
    ("golden_jackal", "Canis aureus"),
    ("mongoose", "Herpestes edwardsii"),
    ("monitor_lizard", "Varanus bengalensis"),
    ("painted_stork", "Mycteria leucocephala"),
    ("koel", "Eudynamys scolopaceus"),
    ("shikra", "Accipiter badius"),
]

ACCEPTED = {"cc0", "cc-by", "cc-by-sa", "cc-by-nc"}


def find_photo(query: str) -> dict | None:
    url = f"{API}?{urllib.parse.urlencode({'q': query, 'per_page': 3})}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    for taxon in data.get("results", []):
        photo = taxon.get("default_photo") or {}
        code = (photo.get("license_code") or "").lower()
        if code not in ACCEPTED:
            continue
        medium = photo.get("medium_url") or ""
        if not medium:
            continue
        return {
            "url": medium.replace("medium.", "large."),
            "fallback": medium,
            "license": code.upper().replace("CC-", "CC "),
            "artist": (photo.get("attribution_name")
                       or photo.get("attribution") or "Unknown")[:120],
            "name": taxon.get("preferred_common_name") or taxon.get("name"),
            "scientific": taxon.get("name", ""),
            "source": f"https://www.inaturalist.org/photos/{photo.get('id')}",
        }
    return None


def download_resize(urls: list[str], dest: Path) -> None:
    last: Exception | None = None
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read()
            img = Image.open(io.BytesIO(raw)).convert("RGB")
            img.thumbnail((800, 800))
            img.save(dest, "JPEG", quality=80, optimize=True)
            return
        except Exception as exc:
            last = exc
    raise last or RuntimeError("no url worked")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        "# Demo Image Credits",
        "",
        "Wildlife photos for demo/seed content, sourced from iNaturalist",
        "(Creative Commons licensed; attribution below).",
        "",
        "| File | Species | License | Author | Source |",
        "|---|---|---|---|---|",
    ]
    ok = 0
    for slug, query in SPECIES:
        dest = OUT_DIR / f"{slug}.jpg"
        try:
            found = find_photo(query)
            if not found:
                print(f"SKIP  {slug}: no CC-licensed default photo")
                continue
            download_resize([found["url"], found["fallback"]], dest)
            kb = dest.stat().st_size // 1024
            rows.append(
                f"| {slug}.jpg | {found['name']} (*{found['scientific']}*) "
                f"| {found['license']} | {found['artist']} "
                f"| [photo]({found['source']}) |"
            )
            print(f"OK    {slug}.jpg ({kb} KB, {found['license']}, {found['artist']})")
            ok += 1
        except Exception as exc:  # keep going; partial sets are fine
            print(f"FAIL  {slug}: {exc}")
    CREDITS.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"\n{ok}/{len(SPECIES)} images saved to {OUT_DIR}")
    return 0 if ok >= 12 else 1


if __name__ == "__main__":
    sys.exit(main())
