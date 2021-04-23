
.phony: check
check: 
	python3 flatten.py > flatten.lua
	export "LUA_PATH=../?.ttslua;?.lua" && \
	  true $(foreach test,$(wildcard *.lua), && echo ${test} && lua ${test}) 

.phony: flatten
flatten:
	python3 flatten.py > flatten.lua
