import os
from pathlib import Path

from PIL import Image
import grf
from agrf.graphics import LayeredImage

from .builder import build_docs, LANGUAGES

# Map language codes to OpenTTD language IDs
LANG_ID_MAP = {"en": 0x7F, "zh_CN": 0x56}  # English (US)  # Chinese (Simplified)

# Map language codes to file suffixes
LANG_SUFFIX_MAP = {"en": "", "zh_CN": "_zh"}

# Language-specific UI strings
LANG_UI = {
    "en": {
        "buildings_title": "Buildings",
        "buildings_intro": "This page lists all the buildings included in this NewGRF.",
        "id_label": "ID",
        "name_label": "Name",
    },
    "zh_CN": {
        "buildings_title": "建筑",
        "buildings_intro": "此页面列出了此 NewGRF 中的所有建筑。",
        "id_label": "编号",
        "name_label": "名称",
    },
}


def _get_house_name(string_manager, house, lang_id):
    """Return the translated house name for the given language ID."""
    house_name = house.name
    try:
        string_ref = string_manager[house.name]
        translations = {
            lid: (
                text.decode("utf-8").replace("Þ", "")
                if isinstance(text, bytes)
                else text
            )
            for lid, text in string_ref.get_pairs()
        }
        house_name = translations.get(lang_id, translations.get(0x7F, house.name))
    except (KeyError, AttributeError):
        pass
    return house_name


def gen_docs(string_manager, houses, docs_dir=None):
    """Generate documentation content for buildings."""
    if docs_dir is None:
        docs_dir = Path("docs")
    else:
        docs_dir = Path(docs_dir)

    prefix = docs_dir
    img_prefix = prefix / "img" / "buildings"
    os.makedirs(img_prefix, exist_ok=True)

    # Build language list including English
    all_langs = [{"code": "en", "name": "English"}] + LANGUAGES

    # Generate images once (shared across all languages)
    for house in houses:
        house_id = f"{house.id:04X}"
        for i, sprite in enumerate(house.sprites):
            img_dest = img_prefix / f"{house_id}_{i}.png"
            sprite.voxel.render()

            best_fit = sprite.get_sprite(zoom=grf.ZOOM_4X, bpp=32)
            img = LayeredImage.from_sprite(best_fit).crop().to_pil_image()
            img.save(img_dest)

    # Generate building RST files and buildings index for each language
    for lang in all_langs:
        lang_code = lang["code"]
        suffix = LANG_SUFFIX_MAP[lang_code]
        lang_id = LANG_ID_MAP.get(lang_code, 0x7F)
        ui = LANG_UI[lang_code]

        # Building detail pages
        for house in houses:
            house_id = f"{house.id:04X}"
            house_name = _get_house_name(string_manager, house, lang_id)

            with open(prefix / f"building_{house_id}{suffix}.rst", "w") as f:
                print(f"{house_name}\n================\n", file=f)
                for i in range(len(house.sprites)):
                    print(
                        f".. figure:: /img/buildings/{house_id}_{i}.png\n"
                        f"   :width: 128\n"
                        f"   :figclass: inline-figure\n",
                        end="\n",
                        file=f,
                    )
                print("", file=f)
                print(f"**{ui['id_label']}:** {house_id}\n", file=f)
                print(f"**{ui['name_label']}:** {house_name}\n", file=f)

        # Buildings index page
        with open(prefix / f"buildings{suffix}.md", "w") as f:
            print(f"# {ui['buildings_title']}\n", file=f)
            print(f"{ui['buildings_intro']}\n", file=f)
            print("```{toctree}\n:maxdepth: 1\n:hidden:\n", file=f)
            for house in houses:
                house_id = f"{house.id:04X}"
                print(f"building_{house_id}", file=f)
            print("```\n", file=f)

            for house in houses:
                house_id = f"{house.id:04X}"
                house_name = _get_house_name(string_manager, house, lang_id)
                print(
                    f"- [{house_name} (ID: {house_id})](building_{house_id}.rst)",
                    file=f,
                )


__all__ = ["gen_docs", "build_docs", "LANGUAGES"]
