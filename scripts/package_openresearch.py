"""Build a reproducible OpenResearch skill ZIP from the current skill folder."""

from argparse import ArgumentParser
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "research-workflow"


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", required=True, type=Path)
    args = parser.parse_args()

    output = args.output.resolve()
    if output.is_relative_to(SKILL_DIR.resolve()):
        parser.error("output must be outside the skill folder")

    files = sorted(
        (path for path in SKILL_DIR.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(SKILL_DIR).as_posix(),
    )
    if SKILL_DIR / "SKILL.md" not in files:
        parser.error("skills/research-workflow/SKILL.md is missing")

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w") as archive:
        for path in files:
            name = Path("research-workflow") / path.relative_to(SKILL_DIR)
            info = ZipInfo(name.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    print(output)


if __name__ == "__main__":
    main()
