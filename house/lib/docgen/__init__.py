import os
import shutil
from pathlib import Path

from .builder import build_docs, LANGUAGES


def gen_docs(string_manager, houses, docs_dir=None):
    """Generate documentation content for buildings."""
    if docs_dir is None:
        docs_dir = Path("docs")
    else:
        docs_dir = Path(docs_dir)

    prefix = docs_dir
    os.makedirs(prefix / "img" / "buildings", exist_ok=True)
    os.makedirs(prefix / "locale" / "zh_CN" / "LC_MESSAGES", exist_ok=True)

    # Generate individual building pages
    for house in houses:
        house_id = f"{house.id:04X}"
        # Try to get translated name from string manager, fallback to raw name
        try:
            house_name = string_manager[house.name]
        except KeyError:
            house_name = house.name

        # Copy the first sprite image from cache if available
        img_dest = prefix / "img" / "buildings" / f"{house_id}.png"
        has_image = False
        if house.sprites:
            try:
                # Get the voxel name from the LazyAlternativeSprites
                voxel_name = house.sprites[0].voxel.name
                cache_prefix = house.sprites[0].voxel.prefix
                # Use the 1x 32bpp rendered image (first angle)
                src_img = Path(cache_prefix) / f"{voxel_name}_1x_32bpp.png"
                if src_img.exists():
                    shutil.copy(src_img, img_dest)
                    has_image = True
            except Exception:
                pass

        # Generate individual building page
        with open(prefix / f"building_{house_id}.md", "w") as f:
            print(f"# {house_name}\n", file=f)
            if has_image:
                print(f"![Building preview](img/buildings/{house_id}.png)\n", file=f)
            print(f"**ID:** {house_id}\n", file=f)
            print(f"**Name:** {house_name}\n", file=f)

        # Generate Chinese translation for this building
        with open(
            prefix / "locale" / "zh_CN" / "LC_MESSAGES" / f"building_{house_id}.po", "w"
        ) as f:
            print(
                f"""# Chinese translations for building {house_id}
msgid ""
msgstr ""
"Project-Id-Version: China Set Buildings 0.1.0\\n"
"Language: zh_CN\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "{house_name}"
msgstr "{house_name}"

msgid "**ID:** {house_id}"
msgstr "**ID：** {house_id}"

msgid "**Name:** {house_name}"
msgstr "**名称：** {house_name}"
""",
                file=f,
            )

    # Generate buildings index page with links to individual pages
    with open(prefix / "buildings.md", "w") as f:
        print("# Buildings\n", file=f)
        print("This page lists all the buildings included in this NewGRF.\n", file=f)
        print("```{toctree}\n:maxdepth: 1\n:hidden:\n", file=f)
        for house in houses:
            house_id = f"{house.id:04X}"
            print(f"building_{house_id}", file=f)
        print("```\n", file=f)

        for house in houses:
            house_id = f"{house.id:04X}"
            try:
                house_name = string_manager[house.name]
            except KeyError:
                house_name = house.name
            print(f"- [{house_name} (ID: {house_id})](building_{house_id}.md)", file=f)


__all__ = ["gen_docs", "build_docs", "LANGUAGES"]
