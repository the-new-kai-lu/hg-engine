#!/usr/bin/env python3
"""Read-only checks for hg-engine sprite exports; this does not convert artwork.

Examples (from the repository root):
  .venv/bin/python scripts/validate_fakemon_graphics.py --kind battle path/front.png path/back.png
  .venv/bin/python scripts/validate_fakemon_graphics.py --kind icon path/icon.png
  .venv/bin/python scripts/validate_fakemon_graphics.py --kind follower path/overworld.png

Use --recolor-of only for two copies of the SAME pose sheet (normal and shiny),
never for front versus back sheets. Front/back color-role correspondence and
follower direction order require visual review. Passing these checks does not
verify artistic quality, sprite animation, species mappings, or ROM behavior.
"""

import argparse
import json
from pathlib import Path
import sys
import tempfile

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow is required; use the repository .venv/bin/python.")


REPO = Path(__file__).resolve().parents[1]
ICON_PALETTES = REPO / "documentation/wiki/resources/Editing-Pokemon-Data"


def bgr555(rgb):
    """Match tools/source/nitrogfx/gfx.c, including truncation (not rounding)."""
    red, green, blue = rgb
    return (red // 8) | ((green // 8) << 5) | ((blue // 8) << 10)


def palette_words(colors):
    return [bgr555(rgb) for rgb in colors]


def read_jasc(path):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if lines[:2] != ["JASC-PAL", "0100"]:
        raise ValueError("expected JASC-PAL / 0100 header")
    count = int(lines[2])
    colors = [tuple(map(int, line.split())) for line in lines[3:] if line.strip()]
    if len(colors) != count or any(len(rgb) != 3 or not all(0 <= v <= 255 for v in rgb) for rgb in colors):
        raise ValueError("palette count or RGB entries are invalid")
    return colors


def inspect_png(path, kind, recolor_of=None, check_sidecars=True, show_palette=False):
    errors, warnings, notes = [], [], []
    try:
        with Image.open(path) as source:
            source.load()
            image = source.copy()
            info = source.info.copy()
            file_format = source.format
    except (OSError, ValueError) as exc:
        return [str(exc)], warnings, notes

    if file_format != "PNG":
        errors.append("file is not PNG")
    width, height = image.size
    notes.append(f"{width}x{height}, mode {image.mode}")
    expected = {"battle": {(160, 80)}, "icon": {(32, 64)}, "follower": {(32, 256), (64, 512)}}[kind]
    if image.size not in expected:
        errors.append(f"expected dimensions {sorted(expected)}, got {image.size}")
    if image.mode != "P":
        errors.append("must be indexed PNG (mode P), not RGB/RGBA or grayscale")
        return errors, warnings, notes

    palette = image.getpalette("RGB") or []
    colors = [tuple(palette[i:i + 3]) for i in range(0, len(palette), 3)]
    if len(colors) != 16:
        errors.append(f"expected exactly 16 embedded palette entries, got {len(colors)}")
    pixels = image.tobytes()
    used = sorted(set(pixels))
    notes.append(f"{len(colors)} palette entries; {len([v for v in used if v])} used visible indices")
    if used and max(used) > 15:
        errors.append(f"pixel index {max(used)} exceeds 4bpp range 0..15")
    if not any(0 < value <= 15 for value in used):
        errors.append("sheet contains no visible sprite pixels")
    alpha = info.get("transparency")
    if isinstance(alpha, int) and alpha != 0:
        errors.append(f"PNG transparency must refer to palette index 0, got {alpha}")
    elif isinstance(alpha, bytes) and (not alpha or alpha[0] != 0 or any(v != 255 for v in alpha[1:])):
        errors.append("PNG transparency must make only index 0 transparent, with no partial alpha")
    # tRNS is optional: the game uses index 0 regardless of PNG transparency.
    words = palette_words(colors)
    if show_palette:
        notes.append("BGR555: " + " ".join(f"{word:04X}" for word in words))
    visible_words = [words[i] for i in used if 0 < i < len(words)]
    if len(set(visible_words)) < len(visible_words):
        warnings.append("some used visible palette indices become identical after BGR555 conversion")

    if kind == "battle":
        if pixels[:4] != bytes(4):
            errors.append("top-left four pixels must be index 0 (encryption-key storage)")
        if check_sidecars:
            key = Path(str(path) + ".key")
            if not key.is_file() or key.stat().st_size != 4:
                errors.append(f"missing or invalid 4-byte key sidecar: {key}")
        if image.size == (160, 80):
            if image.crop((0, 0, 80, 80)).tobytes() == image.crop((80, 0, 160, 80)).tobytes():
                warnings.append("battle animation frames are identical")
        notes.append("front.png supplies normal palette; back.png supplies shiny palette; review matching color roles visually")
    elif kind == "icon":
        matches = []
        for slot in range(3):
            try:
                reference = read_jasc(ICON_PALETTES / f"pal{slot}.pal")
                if words == palette_words(reference):
                    matches.append(slot)
            except (OSError, ValueError, IndexError) as exc:
                errors.append(f"cannot read icon palette {slot}: {exc}")
        if not matches:
            errors.append("embedded palette does not match fixed icon palette 0, 1, or 2 after BGR555 conversion")
        else:
            notes.append(f"fixed icon palette slot(s): {matches}; data/IconPaletteTable.c must use matching slot")
    elif check_sidecars:
        validate_follower_sidecars(path, image.size, words, errors, warnings)

    if recolor_of is not None:
        try:
            with Image.open(recolor_of) as partner:
                partner.load()
                if partner.mode != "P" or partner.size != image.size:
                    errors.append("recolor reference must be indexed and have identical dimensions")
                elif partner.tobytes() != pixels:
                    errors.append("normal/shiny copies of the same sheet must have identical pixel indices")
        except (OSError, ValueError) as exc:
            errors.append(f"cannot read recolor reference: {exc}")
    return errors, warnings, notes


def validate_follower_sidecars(path, size, png_words, errors, warnings):
    metadata_path = path.with_suffix(".json")
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        frames = metadata["frames"]
        palettes = metadata["palettes"]
        # Stock names differ: Bulbasaur uses .1,.10..16, Wailord uses .1..8.
        # Preserve a matching-size stock template; do not infer names from row.
        if len(frames) != 8 or [frame.get("frame") for frame in frames.values()] != list(range(8)):
            errors.append("follower metadata must contain eight ordered frame indices 0..7")
        for index, (name, frame) in enumerate(frames.items()):
            wanted = {"frame": index, "width": size[0], "height": size[0], "format": 3, "color0": 1}
            if any(frame.get(key) != value for key, value in wanted.items()):
                errors.append(f"follower metadata {name} must have {wanted}")
            if len(name.encode("ascii")) > 16:
                errors.append(f"follower frame name exceeds the 16-byte BTX field: {name}")
        for slot in range(2):
            name = f"tsure_poke{slot}"
            palette = palettes.get(name, {})
            if palette.get("offset") != slot or not isinstance(palette.get("fileName"), str):
                errors.append(f"follower palette {name} requires offset {slot} and fileName")
                continue
            palette_path = path.with_name(path.stem + "-" + palette["fileName"])
            colors = read_jasc(palette_path)
            if len(colors) != 16:
                errors.append(f"{palette_path} must have exactly 16 colors")
            if slot == 0 and palette_words(colors) != png_words:
                warnings.append("follower PNG palette differs from its normal JASC palette; BTX uses the JASC palette")
        if len(palettes) != 2:
            errors.append("follower template requires two palettes: normal and shiny")
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError) as exc:
        errors.append(f"invalid or missing follower sidecars: {exc}")


def self_test():
    """Exercise rejection cases with synthetic fixtures, never project artwork."""
    with tempfile.TemporaryDirectory(prefix="hg-graphics-validator-") as directory:
        path = Path(directory) / "front.png"
        synthetic = Image.new("P", (160, 80), 0)
        synthetic.putpalette([v for n in range(16) for v in (n * 8, n * 8, n * 8)])
        synthetic.putpixel((20, 20), 1)
        synthetic.putpixel((101, 20), 2)
        synthetic.save(path, bits=4)
        Path(str(path) + ".key").write_bytes(bytes(4))
        assert not inspect_png(path, "battle")[0]
        synthetic.putpixel((0, 0), 1)
        synthetic.save(path, bits=4)
        assert any("top-left" in error for error in inspect_png(path, "battle")[0])
        synthetic.putpalette([v for n in range(256) for v in (n, n, n)])
        synthetic.putpixel((5, 5), 16)
        synthetic.save(path, bits=8)
        errors = inspect_png(path, "battle")[0]
        assert any("exceeds 4bpp" in error for error in errors)
        assert any("exactly 16" in error for error in errors)
        synthetic.convert("RGB").save(path)
        assert any("mode P" in error for error in inspect_png(path, "battle")[0])
        assert bgr555((255, 255, 255)) == 0x7FFF
        assert bgr555((7, 7, 7)) == 0
        assert bgr555((8, 0, 0)) == 1
    print("PASS: synthetic valid sheet, reserved pixels, >15 indices, oversized palette, RGB rejection, BGR555 packing")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", type=Path, nargs="*")
    parser.add_argument("--kind", choices=("battle", "icon", "follower"))
    parser.add_argument("--recolor-of", type=Path, help="compare one input with a recolored copy of the same pose sheet")
    parser.add_argument("--no-sidecars", action="store_true", help="check PNG only; not sufficient for an export")
    parser.add_argument("--show-palette", action="store_true", help="print the packed BGR555 palette")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.paths or not args.kind:
        parser.error("provide --kind and at least one PNG path")
    if args.recolor_of and len(args.paths) != 1:
        parser.error("--recolor-of requires exactly one input PNG")
    failed = False
    for path in args.paths:
        errors, warnings, notes = inspect_png(path, args.kind, args.recolor_of, not args.no_sidecars, args.show_palette)
        print(f"{'FAIL' if errors else 'PASS'}: {path}")
        for level, messages in (("INFO", notes), ("WARN", warnings), ("ERROR", errors)):
            for message in messages:
                print(f"  {level}: {message}")
        failed |= bool(errors)
    print("Format checks only. Visual review and an in-game check are still required.")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
