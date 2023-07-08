
.phony: check
check:  submodules
	export "LUA_PATH=../../?.ttslua;../?.ttslua;?.lua;../../?.lua;../submodules/lunajson/src/?.lua" && \
	  true $(foreach test,$(wildcard *.lua), && echo ${test} && lua ${test}) 

.phony: submodules
submodules:
	cd .. && git submodule update --init

