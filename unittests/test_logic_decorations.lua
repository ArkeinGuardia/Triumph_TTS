lu = require('externals/luaunit/luaunit')
JSON = require("lunajson")
require('scripts/logic_decorations')
require('scripts/utilities_lua')
require('scripts/utilities')

print_error = function(err)
  print("ERROR "  .. err)
  assert(false)
end

mock_objects = {}

function getObjectFromGUID(guid)
  if mock_objects[guid] == nil then
    mock_objects[guid] = {}
    mock_objects['getGUID'] = function () 
      return guid
    end
  end
  return mock_objects[guid]
end

function test_get_decoration_for_guid_returns_nil_if_object_not_recorded()
  mock_objects = {}
  g_decorations = {}
  local obj = { getGUID = function() return "ABCDEF" end }
  mock_objects[obj.getGUID()] = obj
  local result = get_decoration_for_guid("ABCDEF", "key")
  lu.assertEquals(result, nil)
end

function test_get_decoration_for_guid_returns_nil_if_key_not_recorded()
  mock_objects = {}
  g_decorations = {}
  local obj = { getGUID = function() return "ABCDEF" end }
  mock_objects[obj.getGUID()] = obj
  set_decoration_for_guid("ABCDEF", "something_else", 2)
  local result = get_decoration_for_guid("ABCDEF", "key")
  lu.assertEquals(result, nil)
end

function test_get_decoration_returns_value()
  mock_objects = {}
  g_decorations = {}
  local obj = { getGUID = function() return "ABCDEF" end }
  mock_objects[obj.getGUID()] = obj
  set_decoration_for_guid("ABCDEF", "key", 2)
  local result = get_decoration_for_guid("ABCDEF", "key")
  lu.assertEquals(result, 2)
end

function test_set_decoration_for_obj_uses_guid()
  mock_objects = {}
  g_decorations = {}
  local obj = { getGUID = function() return "ABCDEF" end }
  mock_objects[obj.getGUID()] = obj
  set_decoration_for_obj(obj, "key", 3)
  local result = get_decoration_for_guid("ABCDEF", "key")
  lu.assertEquals(result, 3)
end

function test_get_decoration_for_obj_uses_guid()
  mock_objects = {}
  g_decorations = {}
  local obj = { getGUID = function() return "ABCDEF" end }
  mock_objects[obj.getGUID()] = obj
  set_decoration_for_guid("ABCDEF", "key", 4)
  local result = get_decoration_for_obj(obj, "key")
  lu.assertEquals(result, 4)
end

function test_add_to_decoration_list_guid_creates_new_list()
  mock_objects = {}
  g_decorations = {}
  local obj = { getGUID = function() return "GHIJ" end }
  mock_objects[obj.getGUID()] = obj
  add_to_decoration_list_guid("GHIJ", "kay", 5)
  local result = get_decoration_for_guid("GHIJ", "kay")
  lu.assertEquals( #result, 1 )
  lu.assertEquals(5, result[1] )
end

function test_add_to_decoration_list_guid_appends_to_list()
  mock_objects = {}
  g_decorations = {}
  local obj = { getGUID = function() return "GHIJ" end }
  mock_objects[obj.getGUID()] = obj
  add_to_decoration_list_guid("GHIJ", "kay", 5)
  add_to_decoration_list_guid("GHIJ", "kay", 6)
  local result = get_decoration_for_guid("GHIJ", "kay")
  lu.assertEquals( #result, 2 )
  lu.assertEquals(5, result[1] )
  lu.assertEquals(6, result[2] )
end


function test_add_to_decoration_list_obj_uses_guid()
  mock_objects = {}
  g_decorations = {}
  local obj = { getGUID = function() return "KLM" end }
  mock_objects[obj.getGUID()] = obj
  add_to_decoration_list_obj(obj, "kay", 5)
  local result = get_decoration_for_guid("KLM", "kay")
  lu.assertEquals( #result, 1 )
  lu.assertEquals(5, result[1] )
end

function test_remove_decoration_for_guid()
  mock_objects = {}
  g_decorations = {}
  local guid = "ABCDEF"
  local obj = { getGUID = function() return guid end }
  mock_objects[obj.getGUID()] = obj
  set_decoration_for_obj(obj, "key", 3)
  remove_decorations_for_guid(guid)
  local result = get_decoration_for_guid(guid, "key")
  lu.assertEquals(result, nil)
end

function test_remove_decoration_for_guid_nil_harmless()
  mock_objects = {}
  g_decorations = {}
  remove_decorations_for_guid(nil)
end

function test_remove_decoration_for_obj()
  mock_objects = {}
  g_decorations = {}
  local guid = "ABCDEF"
  local obj = { getGUID = function() return guid end }
  mock_objects[obj.getGUID()] = obj
  set_decoration_for_obj(obj, "key", 3)
  remove_decorations_for_obj(obj)
  local result = get_decoration_for_guid(guid, "key")
  lu.assertEquals(result, nil)
end

function test_remove_decoration_for_obj_with_nil_harmless()
  mock_objects = {}
  g_decorations = {}
  remove_decorations_for_obj(nil)
end

os.exit( lu.LuaUnit.run() )
