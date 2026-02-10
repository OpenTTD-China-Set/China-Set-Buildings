rebuild: clean all

all: building.grf

building: clean_building building.grf

clean_building:
	rm -f building.grf

clean:
	rm -f *.grf

doc.building:
	python3 -m house.gen doc
	cd docs && make html
	cd docs && mv index.md index_en.md && mv index_zh.md index.md && \
		make -e SPHINXOPTS="-D language=zh_CN" html BUILDDIR=_build/zh_CN && \
		mv index.md index_zh.md && mv index_en.md index.md
	rm -rf docs/_build/html/zh_CN
	mkdir -p docs/_build/html/zh_CN
	cp -r docs/_build/zh_CN/html/* docs/_build/html/zh_CN/

building.grf:
	python3 -m house.gen gen
