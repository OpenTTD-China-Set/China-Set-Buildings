import os


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

        # Try to get the first sprite for the building preview
        if house.sprites:
            try:
                img = house.sprites[0].get_pil_image()
                img_path = f"img/buildings/{house_id}.png"
                img.save(os.path.join(prefix, img_path))
                has_image = True
            except Exception:
                has_image = False
        else:
            has_image = False

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
