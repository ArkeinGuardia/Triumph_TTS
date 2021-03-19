lu = require('externals/luaunit/luaunit')
armies = {}
require('scripts/data/data_armies_Medieval_Era')
require('scripts/utilities_lua')
require('scripts/utilities')
require('scripts/logic_base_obj')
require('scripts/logic_dead')
require('scripts/data/data_troops')


function test_all_bases_are_counted()
  local base1_obj = { getName = function() return "base Archers #48" end }
  local base2_obj = { getName = function() return "base Horde #49" end }
  local bases = {base1_obj, base2_obj}
  local actual = calculate_dead_points(bases)
  lu.assertEquals(actual, 6)
end

function test_camp_is_worth_points_passed_in()
  local base_obj = { getName = function() return "base Camp #48" end }
  local actual = get_points_for_base(base_obj, 32)
    lu.assertEquals(actual, 32)
end

function test_camp_is_worth_eight_points_of_casualties()
  local base_obj = { getName = function() return "base Camp #48" end }
  local bases = {base_obj}
  local actual = calculate_dead_points(bases)
    lu.assertEquals(actual, 8)
end

function test_camp_is_worth_zero_points_in_army_builder()
  local base_obj = { getName = function() return "base Camp #48" end }
  local bases = {base_obj}
  local actual = calculate_army_builder_points(bases)
    lu.assertEquals(actual, 0)
end

-- Fortitified camp battle card
function test_fortified_camp_is_worth_nine_points_of_casualties()
  local base_obj = { getName = function() return "base Fortified Camp #48" end }
  local bases = {base_obj}
  local actual = calculate_dead_points(bases)
    lu.assertEquals(actual, 9)
end

-- Fortitified camp battle card
function test_fortified_camp_is_worth_one_points_in_army_builder()
  local base_obj = { getName = function() return "base Fortified Camp #48" end }
  local bases = {base_obj}
  local actual = calculate_army_builder_points(bases)
    lu.assertEquals(actual, 1)
end

os.exit( lu.LuaUnit.run() )