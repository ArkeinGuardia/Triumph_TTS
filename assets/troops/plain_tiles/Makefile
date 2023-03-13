
LUA_PATH=../../../../?.ttslua;../../../../Triumph_TTS/submodules/lunajson/src/?.lua


.PHONY: all
all: svg

../../../../Triumph_TTS/submodules/lunajson/src/lunajson.lua:
	cd ../../../../Triumph_TTS && \
	  git submodule init && \
	  git submodule update

data.json: ../../../scripts/data/data_cheat_sheet.ttslua
data.json: ../../../../Triumph_TTS/submodules/lunajson/src/lunajson.lua
data.json: get_data.lua 
	LUA_PATH="${LUA_PATH}" lua get_data.lua > $@

plain_army.ttslua: svg


.PHONY: svg
svg: data.json generate_plain_tiles.py
	python3 ./generate_plain_tiles.py

.PHONY: clean
clean:


.DELETE_ON_ERROR:

