
.phony: check
check: flatten
	export "LUA_PATH=../?.ttslua;?.lua" && \
	  true $(foreach test,$(wildcard *.lua), && lua ${test}) 

.phony: flatten
flatten:
	python3 flatten.py > flatten.lua
