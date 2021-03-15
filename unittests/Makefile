
check: 
	export "LUA_PATH=../?.ttslua;?.lua" && \
	  true $(foreach test,$(wildcard *.lua), && lua ${test}) 
