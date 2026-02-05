from house.lib import AHouse
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet


houses = []
for i, x in enumerate(
    ["rural_north01", "rural_north02", "rural_north03", "town_north01"]
):
    vox = LazyVoxel(
        x,
        prefix=f".cache/render/house/{x}",
        voxel_getter=lambda: f"house/voxels/{x}.vox",
        load_from="house/files/gorender.json",
    )
    vox.render()
    rotated_voxels = [LazySpriteSheet([vox], [(0, i)]) for i in range(8)]
    houses.append(
        AHouse(
            substitute=0x06,
            id=0x80 + i,
            name="Building",
            sprites=[s for v in rotated_voxels for s in v.spritesheet()],
            flags=0x1,
            availability_mask=0xF81F,
        )
    )
