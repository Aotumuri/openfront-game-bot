import shutil
import subprocess

from player.rank.rank_svg import build_rank_svg


def build_rank_png(rank: str, progress: float) -> bytes:
    svg = build_rank_svg(rank, progress)
    converter = shutil.which("rsvg-convert")
    if not converter:
        raise RuntimeError("rsvg-convert is not installed")
    try:
        result = subprocess.run(
            [converter, "-f", "png", "-"],
            input=svg.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"rsvg-convert failed: {message}") from exc
    if not result.stdout:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"rsvg-convert produced empty output: {message}")
    return result.stdout
