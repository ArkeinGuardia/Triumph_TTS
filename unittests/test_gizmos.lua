lu = require('externals/luaunit/luaunit')
JSON = require("lunajson")
require("Triumph_TTS/scripts/logic_gizmos")


function test_has_archer_arc_returns_false_for_cavalry()
  local base_obj = {
    getName = function()
      return "Elite Cavalry"
    end,

    getGUID = function()
      return "1234"
    end,
  }
  local actual = has_archer_shooting_arc(base_obj)
  lu.assertFalse(actual)
end

function test_has_archer_arc_returns_true_for_archers()
  local base_obj = {
    getName = function()
      return "Archers #323"
    end,

    getGUID = function()
      return "1234"
    end,
  }

  local actual = has_archer_shooting_arc(base_obj)
  lu.assertTrue(actual)
end

function test_has_archer_arc_returns_false_for_dismounting()
  -- Checking to see it is having a base definition is not sufficient
  local base_obj = {
    getName = function()
      return "Elite Cavalry #323"
    end,

    getGUID = function()
      return "1234"
    end,
  }
  set_decoration_for_obj(base_obj, "base_definition_name", g_str_5fb1ba41e1af06001770fb2b_dismounted)

  local actual = has_archer_shooting_arc(base_obj)
  lu.assertFalse(actual)
end

function test_shower_shooting_has_archer_arc()
  local base_obj = {
    getName = function()
      return "Elite Cavalry"
    end,

    getGUID = function()
      return "1234"
    end,
  }
  set_decoration_for_obj(base_obj, "base_definition_name", g_str_615351b203385c0016b88332_shower_shooting)
  local actual = has_archer_shooting_arc(base_obj)
  lu.assertTrue(actual)
end

os.exit( lu.LuaUnit.run() )
