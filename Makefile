rebuild: clean all

all: building.grf

building: clean_building building.grf

clean_building:
	rm -f building.grf

clean:
	rm -f *.grf

doc.building:
	python3 -m house.gen doc
	cd docs; make html

building.grf:
	python3 -m house.gen gen
