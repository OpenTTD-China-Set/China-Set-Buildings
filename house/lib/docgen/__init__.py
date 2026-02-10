import os
import shutil


def gen_docs(string_manager, houses):
    prefix = "docs/"
    os.makedirs(os.path.join(prefix, "img", "buildings"), exist_ok=True)
    os.makedirs(os.path.join(prefix, "locale", "zh_CN", "LC_MESSAGES"), exist_ok=True)

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

        # Generate Chinese translation for this building
        with open(os.path.join(prefix, "locale", "zh_CN", "LC_MESSAGES", f"building_{house_id}.po"), "w") as f:
            print(f'''# Chinese translations for building {house_id}
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
''', file=f)

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

    # Generate Chinese translation for buildings index
    with open(os.path.join(prefix, "locale", "zh_CN", "LC_MESSAGES", "buildings.po"), "w") as f:
        print('''# Chinese translations for buildings page
msgid ""
msgstr ""
"Project-Id-Version: China Set Buildings 0.1.0\\n"
"Language: zh_CN\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "Buildings"
msgstr "建筑"

msgid "This page lists all the buildings included in this NewGRF."
msgstr "本页面列出本 NewGRF 中包含的所有建筑。"
''', file=f)

    # Generate Chinese translation for changelog
    with open(os.path.join(prefix, "locale", "zh_CN", "LC_MESSAGES", "changelog.po"), "w") as f:
        print('''# Chinese translations for changelog page
msgid ""
msgstr ""
"Project-Id-Version: China Set Buildings 0.1.0\\n"
"Language: zh_CN\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "Changelog"
msgstr "更新日志"

msgid "0.1.0 (Work in Progress)"
msgstr "0.1.0（开发中）"

msgid "Initial release. Adds Chinese-style buildings for OpenTTD."
msgstr "初始版本。为 OpenTTD 添加中式建筑。"
''', file=f)

    # Generate Chinese translation for index
    with open(os.path.join(prefix, "locale", "zh_CN", "LC_MESSAGES", "index.po"), "w") as f:
        print('''# Chinese translations for index page
msgid ""
msgstr ""
"Project-Id-Version: China Set Buildings 0.1.0\\n"
"Language: zh_CN\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "Languages / 语言:"
msgstr "语言 / Languages："
''', file=f)

    # Generate Chinese translation for readme
    with open(os.path.join(prefix, "locale", "zh_CN", "LC_MESSAGES", "readme.po"), "w") as f:
        print('''# Chinese translations for readme page
msgid ""
msgstr ""
"Project-Id-Version: China Set Buildings 0.1.0\\n"
"Language: zh_CN\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "China Set: Buildings"
msgstr "中国包：建筑"

msgid "0 Contents"
msgstr "0 目录"

msgid "1 About"
msgstr "1 关于"

msgid "2 General information"
msgstr "2 基本信息"

msgid "3 Credits"
msgstr "3 致谢"

msgid "4 Contact information"
msgstr "4 联系方式"

msgid "5 License"
msgstr "5 许可证"

msgid "6 Obtaining the source"
msgstr "6 获取源代码"

msgid "About"
msgstr "关于"

msgid "This NewGRF provides additional buildings for OpenTTD, focusing on Chinese architectural styles."
msgstr "本 NewGRF 为 OpenTTD 提供额外的建筑，专注于中式建筑风格。"

msgid "Minimum tested OpenTTD version: 12.0"
msgstr "最低测试通过的 OpenTTD 版本：12.0"

msgid "OpenTTD:"
msgstr "OpenTTD："

msgid "see https://wiki.openttd.org/NewGRF"
msgstr "请参阅 https://wiki.openttd.org/NewGRF"

msgid "This NewGRF is available from the in-game Online Content."
msgstr "本 NewGRF 可从游戏内在线内容下载。"

msgid "Graphics:"
msgstr "图形："

msgid "Code:"
msgstr "代码："

msgid "Special Thanks:"
msgstr "特别感谢："

msgid "Please report any bugs you find at"
msgstr "请在以下地址报告您发现的任何错误"

msgid "Always included a detailed description of the bug, preferrably with screenshot and savegame. Also state the exact game version you\'re using, as well as the version of this NewGRF."
msgstr "请始终包含错误的详细描述，最好附带截图和存档。同时请注明您使用的游戏版本以及本 NewGRF 的版本。"

msgid "If you have a savegame that includes NewGRFs not available on OpenTTD\'s Online Content, then please try to reproduce the bug in a new game which has all NewGRFs easily accessible."
msgstr "如果您的存档包含无法从 OpenTTD 在线内容获取的 NewGRF，请尝试在一个所有 NewGRF 都容易获取的新游戏中重现该错误。"

msgid "If you\'re using a patched version of the game, please try to reproduce the bug on an official game build. If you can\'t reproduce the bug, then don\'t report it here but in the forum topic of the patch(pack) instead."
msgstr "如果您使用的是修改版游戏，请尝试在官方版本上重现该错误。如果无法重现，请勿在此报告，而应在该修改版的论坛主题中报告。"

msgid "If you have any queries that cannot be asked in Github publicly, then contact Ahyangyi via Private Message at www.tt-forums.net."
msgstr "如果您有任何不能在 Github 上公开询问的问题，请通过私信联系 Ahyangyi，网址为 www.tt-forums.net。"

msgid "Visit [Github](https://github.com/OpenTTD-China-Set/China-Set-Buildings) and follow the general build instructions."
msgstr "访问 [Github](https://github.com/OpenTTD-China-Set/China-Set-Buildings) 并按照常规构建说明进行操作。"
''', file=f)
