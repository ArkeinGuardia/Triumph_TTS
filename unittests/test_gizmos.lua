lu = require('Triumph_TTS/unittests/externals/luaunit/luaunit')
JSON = require("Triumph_TTS/unittests/externals/json/json")
require("Triumph_TTS/scripts/logic_gizmos")
require("Triumph_TTS/scripts/armies")


function test_has_archer_arc_returns_false_for_cavalry()
  -- Setup
  local base_obj = {
    getName = function()
      return "Elite Cavalry"
    end,

    getGUID = function()
      return "1234"
    end,
  }
  set_decoration_for_obj(base_obj, "base_definition_name", g_str_615351b603385c0016b88d45 )

  -- Exercise
  local actual = has_archer_shooting_arc(base_obj)

  -- Validate
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


function test_has_archer_arc_returns_false_for_when_mounted()
  local mounted_base_obj = {
    getName = function()
      return "Elite Cavalry #323"
    end,

    getGUID = function()
      return "1234"
    end,
  }
  set_decoration_for_obj(mounted_base_obj, "base_definition_name", g_str_615351b503385c0016b88b84_mounted)
  local mounted_actual = has_archer_shooting_arc(mounted_base_obj)
  lu.assertFalse(mounted_actual)
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
