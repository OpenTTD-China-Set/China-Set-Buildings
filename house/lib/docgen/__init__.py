import os
import shutil


def gen_docs(string_manager, houses):
    prefix = "docs/"
    os.makedirs(os.path.join(prefix, "img", "buildings"), exist_ok=True)

    # Generate individual building pages
    for house in houses:
        house_id = f"{house.id:04X}"
        # Try to get translated name from string manager, fallback to raw name
        try:
            house_name = string_manager[house.name]
        except KeyError:
            house_name = house.name

        # Copy the first sprite image from cache if available
        img_dest = os.path.join(prefix, "img", "buildings", f"{house_id}.png")
        has_image = False
        if house.sprites:
            try:
                # Get the voxel name from the LazyAlternativeSprites
                voxel_name = house.sprites[0].voxel.name
                cache_prefix = house.sprites[0].voxel.prefix
                # Use the 1x 32bpp rendered image (first angle)
                src_img = os.path.join(cache_prefix, f"{voxel_name}_1x_32bpp.png")
                if os.path.exists(src_img):
                    shutil.copy(src_img, img_dest)
                    has_image = True
            except Exception:
                pass

        # Generate individual building page
        with open(os.path.join(prefix, f"building_{house_id}.md"), "w") as f:
            print(f"# {house_name}\n", file=f)
            if has_image:
                print(f"![Building preview](img/buildings/{house_id}.png)\n", file=f)
            print(f"**ID:** {house_id}\n", file=f)
            print(f"**Name:** {house_name}\n", file=f)

    # Generate buildings index page with links to individual pages
    with open(os.path.join(prefix, "buildings.md"), "w") as f:
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
