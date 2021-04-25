lu = require('externals/luaunit/luaunit')
require('scripts/logic_snapping')
require('scripts/utilities')
require('scripts/data/data_settings')

function test_identical_facings_allow_snapping()
  local actual = are_facings_degrees_close_enough_to_snap(38, 38)
  lu.assertTrue(actual)
end

function test_opposite_facings_allow_snapping()
    local actual = are_facings_degrees_close_enough_to_snap(38, 218)
    lu.assertTrue(actual)
  end
  
function test_front_left_facings_allow_snapping()
    local actual = are_facings_degrees_close_enough_to_snap(38, 128)
    lu.assertTrue(actual)
end

function test_front_right_facings_allow_snapping()
     local actual = are_facings_degrees_close_enough_to_snap(38, 308)
     lu.assertTrue(actual)
end

function test_facings_near_360_allow_snapping()
    local actual = are_facings_degrees_close_enough_to_snap(1, 359)
    lu.assertTrue(actual)
end

function test_large_differencs_disqualify_snapping()
    local actual = are_facings_degrees_close_enough_to_snap(1, 46)
    lu.assertFalse(actual)
end


os.exit( lu.LuaUnit.run() )