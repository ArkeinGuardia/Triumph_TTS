
.phony: check
check: 
	export "LUA_PATH=../../?.ttslua;../?.ttslua;?.lua;../../?.lua" && \
	  true $(foreach test,$(wildcard *.lua), && echo ${test} && lua ${test}) 

