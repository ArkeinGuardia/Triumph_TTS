
lu = require('externals/luaunit/luaunit')
json = require('externals/json/json')

require('scripts/meshwesh')
require('scripts/utilities')
require('scripts/utilities_lua')


function readAll(file)
    local f = assert(io.open(file, "rb"))
    local content = f:read("*all")
    f:close()
    return content
end

function print_error(message)
  print("ERROR " .. message)
  assert(false)
end

warring_states_text = readAll("../fake_meshwesh/armyLists/5fb1b9f1e1af06001770a195")
warring_states_json = json.decode(warring_states_text)

function test_meshwesh_to_lua_army()
  meshwesh_to_lua_army(warring_states_json)
end

os.exit( lu.LuaUnit.run() )
