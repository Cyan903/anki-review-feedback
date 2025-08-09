.PHONY: prune lint run export clean

name := review-feedback
ui := config

Qt5 := $(foreach file,$(ui),addon/res/Qt5/$(file).py)
Qt6 := $(foreach file,$(ui),addon/res/Qt6/$(file).py)

addon/res/Qt5/%.py: addon/res/%.ui
	@pyuic5 $< -o $@

addon/res/Qt6/%.py: addon/res/%.ui
	@pyuic6 $< -o $@

# Rules
build: $(Qt5) $(Qt6)

prune:
	@rm -rf ./addon/res/Qt5/*.py
	@rm -rf ./addon/res/Qt6/*.py

lint:
	@mypy ./addon/src

run:
	@anki

export: clean
	@cp -r addon export/$(name)
	@find export -type d -name __pycache__ -exec rm -rf {} +
	@cd export/$(name) && zip -r ../$(name).ankiaddon ./*

clean:
	@find export -mindepth 1 ! -name .gitkeep -exec rm -rf {} +
