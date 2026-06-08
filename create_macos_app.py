#!/usr/bin/env python3
"""
Creates a native macOS .app launcher for Lutheran Lectionary.
Run once:  python3 create_macos_app.py

Double-click the resulting LutheranLectionary.app to start the server
and open the web interface. Drag it to your Dock or Applications
folder for quick access.
"""

import os
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
APP_NAME    = "LutheranLectionary"
SERVER_PORT = 5765
SCRIPT_DIR  = Path(__file__).parent.resolve()
SERVER_PY   = SCRIPT_DIR / "app.py"
PID_FILE    = Path.home() / ".lutheran-lectionary" / "server.pid"
LOG_FILE    = Path("/tmp/lutheran-lectionary.log")
GOLD        = (180, 140, 50)    # dark gold background
CROSS_WHITE = (255, 245, 220)   # warm white cross


# ── Icon generation ───────────────────────────────────────────────────────────

def _make_icon_pixels(size: int):
    """
    Returns an (size, size, 4) uint8 numpy RGBA array:
    dark gold circle with a white cross.
    """
    import numpy as np

    x = np.arange(size, dtype=np.float32)
    y = np.arange(size, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)

    cx, cy = size / 2.0, size / 2.0
    dx, dy = xx - cx, yy - cy
    dist   = np.hypot(dx, dy)
    radius = size / 2.0 - 1.0

    # Radial gradient background
    grad = np.clip(1.0 - 0.15 * (dx + dy) / size, 0.80, 1.0)
    bg   = np.clip(
        np.stack([np.full((size, size), c, dtype=np.float32) for c in GOLD], axis=2)
        * grad[:, :, np.newaxis],
        0, 255
    ).astype(np.uint8)

    # Cross dimensions
    arm_w  = size * 0.16        # width of each arm
    v_top  = cy - size * 0.35   # vertical bar top
    v_bot  = cy + size * 0.38   # vertical bar bottom
    h_left = cx - size * 0.30   # horizontal bar left
    h_right= cx + size * 0.30   # horizontal bar right
    h_cy   = cy - size * 0.05   # horizontal bar slightly above center

    in_vert  = (np.abs(xx - cx) <= arm_w / 2) & (yy >= v_top) & (yy <= v_bot)
    in_horiz = (np.abs(yy - h_cy) <= arm_w / 2) & (xx >= h_left) & (xx <= h_right)
    in_cross = in_vert | in_horiz

    # Compose RGBA
    aa = max(1.5, size * 0.002)
    circle_alpha = np.clip((radius + aa - dist) / aa * 255, 0, 255).astype(np.uint8)

    rgba = np.zeros((size, size, 4), dtype=np.uint8)
    rgba[:, :, :3] = bg
    rgba[in_cross, 0] = CROSS_WHITE[0]
    rgba[in_cross, 1] = CROSS_WHITE[1]
    rgba[in_cross, 2] = CROSS_WHITE[2]
    rgba[:, :, 3]     = circle_alpha
    rgba[dist > radius + aa] = 0

    return rgba


def _rgba_to_png(rgba) -> bytes:
    """Encode a numpy RGBA array as a PNG bytestring (no Pillow needed)."""
    import numpy as np

    size = rgba.shape[0]

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    rows = b"".join(b"\x00" + bytes(rgba[y].flatten()) for y in range(size))
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(rows, 6))
        + chunk(b"IEND", b"")
    )


def _make_png(size: int) -> bytes:
    return _rgba_to_png(_make_icon_pixels(size))


def _create_iconset(iconset_dir: Path):
    iconset_dir.mkdir(parents=True, exist_ok=True)

    entries = [
        (16,  16,  ""),   (16,  32,  "@2x"),
        (32,  32,  ""),   (32,  64,  "@2x"),
        (128, 128, ""),   (128, 256, "@2x"),
        (256, 256, ""),   (256, 512, "@2x"),
        (512, 512, ""),   (512, 1024,"@2x"),
    ]

    rendered: dict[int, bytes] = {}
    for _, px, _ in entries:
        if px not in rendered:
            print(f"    rendering {px}×{px}…", end=" ", flush=True)
            rendered[px] = _make_png(px)
            print("done")

    for logical, px, suffix in entries:
        fname = f"icon_{logical}x{logical}{suffix}.png"
        (iconset_dir / fname).write_bytes(rendered[px])


def _build_icns(iconset_dir: Path, icns_out: Path):
    subprocess.run(
        ["iconutil", "-c", "icns", str(iconset_dir), "-o", str(icns_out)],
        check=True, capture_output=True,
    )


# ── AppleScript launcher ──────────────────────────────────────────────────────

def _find_python() -> str:
    import shutil as _shutil
    candidates = [
        sys.executable,
        _shutil.which("python3") or "",
        "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3",
        "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3",
        "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3",
        "/Library/Frameworks/Python.framework/Versions/3.10/bin/python3",
        "/usr/local/bin/python3",
        "/opt/homebrew/bin/python3",
    ]
    for p in candidates:
        if p and Path(p).exists():
            return p
    return "/usr/bin/env python3"


def _launcher_sh(port: int, pid_file: Path, log_file: Path) -> str:
    python_bin = _find_python()
    return f'''\
#!/bin/sh
# Lutheran Lectionary server launcher — generated by create_macos_app.py
# SCRIPT_DIR is resolved at runtime so the app works from any location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH
mkdir -p "{pid_file.parent}"
nohup "{python_bin}" "$SCRIPT_DIR/app.py" \\
    </dev/null >>"{log_file}" 2>&1 &
echo $! > "{pid_file}"
sleep 0
'''


def _applescript(port: int, log_file: Path) -> str:
    url = f"http://localhost:{port}/"
    return f'''\
on run
    set theURL to "{url}"
    set theLog to "{log_file}"

    set appPosixPath to POSIX path of (path to me)
    set theLauncher to appPosixPath & "Contents/Resources/launcher.sh"

    try
        do shell script "curl -sf --max-time 1 " & theURL & " > /dev/null"
        open location theURL
        return
    end try

    do shell script "/bin/sh " & quoted form of theLauncher

    set maxWait to 20
    set waited to 0
    set ready to false
    repeat while waited < maxWait
        delay 1
        set waited to waited + 1
        try
            do shell script "curl -sf --max-time 1 " & theURL & " > /dev/null"
            set ready to true
            exit repeat
        end try
    end repeat

    if ready then
        open location theURL
            display notification "Server running at " & theURL with title "Lutheran Lectionary" subtitle "Ready"
    else
        display alert "Lutheran Lectionary failed to start" message ¬
            "Check the log at " & theLog & " for details." as critical
    end if
end run
'''


def _compile_app(app_path: Path, script_text: str):
    tmp = app_path.parent / "_tmp_launcher.applescript"
    tmp.write_text(script_text)
    try:
        if app_path.exists():
            shutil.rmtree(app_path)
        subprocess.run(
            ["osacompile", "-o", str(app_path), str(tmp)],
            check=True, capture_output=True,
        )
    finally:
        tmp.unlink(missing_ok=True)


def _apply_icon(app_path: Path, icns_path: Path):
    resources = app_path / "Contents" / "Resources"

    dest_icns = resources / f"{APP_NAME}.icns"
    shutil.copy(icns_path, dest_icns)

    plist = app_path / "Contents" / "Info.plist"
    text  = plist.read_text()
    text  = text.replace("<string>applet</string>", f"<string>{APP_NAME}</string>")
    plist.write_text(text)

    for f in resources.glob("applet.icns"):
        f.unlink()

    macos_dir  = app_path / "Contents" / "MacOS"
    applet_bin = macos_dir / "applet"
    named_bin  = macos_dir / APP_NAME
    if applet_bin.exists() and not named_bin.exists():
        shutil.copy(applet_bin, named_bin)

    subprocess.run(["touch", str(app_path)], check=False)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if sys.platform != "darwin":
        sys.exit("This script is macOS-only.")

    if not SERVER_PY.exists():
        sys.exit(f"Cannot find {SERVER_PY}\nRun this script from the liturgical-calendar directory.")

    app_path = SCRIPT_DIR / f"{APP_NAME}.app"
    tmp_dir  = SCRIPT_DIR / ".app_build"
    tmp_dir.mkdir(exist_ok=True)

    print(f"\n  ✝ Building {APP_NAME}.app\n")

    print("  [1/4] Generating icon…")
    iconset_dir = tmp_dir / f"{APP_NAME}.iconset"
    icns_path   = tmp_dir / f"{APP_NAME}.icns"
    _create_iconset(iconset_dir)
    _build_icns(iconset_dir, icns_path)
    print("        Icon built.\n")

    print("  [2/4] Compiling launcher…")
    resources_dir  = app_path / "Contents" / "Resources"
    launcher_sh    = resources_dir / "launcher.sh"
    bundled_server = resources_dir / "app.py"
    script = _applescript(SERVER_PORT, LOG_FILE)
    _compile_app(app_path, script)
    launcher_sh.write_text(_launcher_sh(SERVER_PORT, PID_FILE, LOG_FILE))
    launcher_sh.chmod(0o755)
    shutil.copy(SERVER_PY, bundled_server)
    # Also copy the package and supporting files into Resources
    import shutil as _sh
    for item in ["liturgical_calendar", "templates", "static", "pdf_gen.py", "requirements.txt"]:
        src = SCRIPT_DIR / item
        dst = resources_dir / item
        if src.is_dir():
            if dst.exists():
                _sh.rmtree(dst)
            _sh.copytree(src, dst)
        elif src.is_file():
            _sh.copy(src, dst)
    print("        App compiled.\n")

    print("  [3/4] Applying icon…")
    _apply_icon(app_path, icns_path)
    print("        Icon applied.\n")

    shutil.rmtree(tmp_dir, ignore_errors=True)

    print("  [4/4] Signing app…")
    subprocess.run(["find", str(app_path), "-name", "._*", "-delete"], check=False)
    subprocess.run(["xattr", "-cr", str(app_path)], check=False)
    subprocess.run(
        ["codesign", "--force", "--deep", "--sign", "-", str(app_path)],
        check=False, capture_output=True,
    )
    print("        Signed.\n")

    print(f"  ✓ Done:  {app_path}\n")
    print("  Next steps:")
    print(f"    • Double-click {APP_NAME}.app to start")
    print(f"    • Or drag it to your Applications folder:")
    print(f"        cp -r \"{app_path}\" /Applications/")
    print(f"    • Or drag it to the Dock from Applications")
    print(f"\n  Server log (if something goes wrong): {LOG_FILE}\n")

    answer = input("  Open folder in Finder? [Y/n]: ").strip().lower()
    if answer != "n":
        subprocess.run(["open", "-R", str(app_path)])


if __name__ == "__main__":
    main()
