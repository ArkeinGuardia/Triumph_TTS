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

function test_snap_angle_change_same_facing()
  local actual = snap_angle_change(45, 45)
  lu.assertEquals(actual, 45)
end

function test_snap_angle_change_almost_same_facing()
  local actual = snap_angle_change(49, 45)
  lu.assertEquals(actual, 45)
end

function test_snap_angle_change_almost_opposite_facing()
  local actual = snap_angle_change(229, 45)
  lu.assertEquals(actual, 225)
end

function test_snap_angle_change_almost_orthogona_right_facing()
  local actual = snap_angle_change(139, 45)
  lu.assertEquals(actual, 135)
end

function test_snap_angle_change_almost_orthogona_left_facing()
  local actual = snap_angle_change(310, 45)
  lu.assertEquals(actual, 315)
end

os.exit( lu.LuaUnit.run() )