.PHONY: lint stop start log

# res/*.ui
ui := config
logs := /tmp/anki-plugin-debug.log

Qt5 := $(foreach file,$(ui),addon/res/Qt5/$(file).py)
Qt6 := $(foreach file,$(ui),addon/res/Qt6/$(file).py)

addon/res/Qt5/%.py: addon/res/%.ui
	@pyuic5 $< -o $@

addon/res/Qt6/%.py: addon/res/%.ui
	@pyuic6 $< -o $@

# Rules
build: $(Qt5) $(Qt6)

clean:
	@rm -rf ./addon/res/Qt5/*.py
	@rm -rf ./addon/res/Qt6/*.py

lint:
	@mypy src

stop:
	@pgrep -f anki > /dev/null && kill $(shell pgrep -f anki) 2> /dev/null || echo "Not running"

start: stop
	@nohup ./.venv/bin/anki > $(logs) 2>&1 &

log:
	@tail -n +1 -f $(logs)

