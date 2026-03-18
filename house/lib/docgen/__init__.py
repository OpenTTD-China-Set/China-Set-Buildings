import os
from pathlib import Path

from PIL import Image
import grf
from agrf.graphics import LayeredImage

from .builder import build_docs, LANGUAGES


def gen_docs(string_manager, houses, docs_dir=None):
    """Generate documentation content for buildings."""
    if docs_dir is None:
        docs_dir = Path("docs")
    else:
        docs_dir = Path(docs_dir)

    prefix = docs_dir
    os.makedirs(prefix / "img" / "buildings", exist_ok=True)

    # Create locale directories for all non-English languages
    for lang in LANGUAGES:
        if lang["code"] != "en":
            os.makedirs(prefix / "locale" / lang["code"] / "LC_MESSAGES", exist_ok=True)

    # Generate individual building pages
    for house in houses:
        house_id = f"{house.id:04X}"
        # Try to get translated name from string manager, fallback to raw name
        try:
            house_name = string_manager[house.name]
        except KeyError:
            house_name = house.name

        has_image = False
        for i, sprite in enumerate(house.sprites):
            img_dest = prefix / "img" / "buildings" / f"{house_id}_{i}.png"
            sprite.voxel.render()

            best_fit = sprite.get_sprite(zoom=grf.ZOOM_4X, bpp=32)
            img = LayeredImage.from_sprite(best_fit).crop().to_pil_image()
            img.save(img_dest)
            has_image = True

        with open(prefix / f"building_{house_id}.rst", "w") as f:
            print(f"{house_name}\n================\n", file=f)
            if has_image:
                for i in range(len(house.sprites)):
                    print(
                        f".. figure:: img/buildings/{house_id}_{i}.png\n"
                        f"   :width: 128\n"
                        f"   :figclass: inline-figure\n",
                        end="\n",
                        file=f,
                    )
                print("", file=f)
            print(f"**ID:** {house_id}\n", file=f)
            print(f"**Name:** {house_name}\n", file=f)

        # Generate translation files for all non-English languages
        for lang in LANGUAGES:
            if lang["code"] == "en":
                continue
            with open(
                prefix
                / "locale"
                / lang["code"]
                / "LC_MESSAGES"
                / f"building_{house_id}.po",
                "w",
            ) as f:
                print(
                    f"""# Translations for building {house_id} ({lang['name']})
msgid ""
msgstr ""
"Project-Id-Version: China Set Buildings 0.1.0\\n"
"Language: {lang['code']}\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "{house_name}"
msgstr "{house_name}"

msgid "**ID:** {house_id}"
msgstr "**ID:** {house_id}"

msgid "**Name:** {house_name}"
msgstr "**Name:** {house_name}"
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
            print(f"building_{house_id}.rst", file=f)
        print("```\n", file=f)

        for house in houses:
            house_id = f"{house.id:04X}"
            try:
                house_name = string_manager[house.name]
            except KeyError:
                house_name = house.name
            print(f"- [{house_name} (ID: {house_id})](building_{house_id}.rst)", file=f)


__all__ = ["gen_docs", "build_docs", "LANGUAGES"]
