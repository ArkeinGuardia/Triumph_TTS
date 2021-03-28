
start:
	 python3 -m http.server 8000

# Get a local caopy of the Meshwesh JSON
.Phony: clone
clone:
	rm -rf armyLists
	mkdir armyLists
	curl -o armyLists/summary 'https://meshwesh.wgcwar.com/api/v1/armyLists?summary=true'
	python3 clone.py

# Generate the lua files needed for TTS
.PHONY: army_data
army_data:
	rm -rf army_data
	mkdir army_data
	python3 tts_army.py

