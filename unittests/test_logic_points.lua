lu = require('externals/luaunit/luaunit')
armies = {}
require('scripts/data/data_armies_Medieval_Era')
require('scripts/utilities_lua')
require('scripts/utilities')
require('scripts/logic_base_obj')
require('scripts/logic_dead')
require('scripts/logic_spawn_army')
require('scripts/data/data_troops')

g_decorations = {}

function test_all_bases_are_counted()
  local base1_obj = { getName = function() return "base Archers #48" end, getGUID = function() return "ABCDE" end }
  local base2_obj = { getName = function() return "base Horde #49" end, getGUID = function() return "A2345" end  }
  local bases = {base1_obj, base2_obj}
  local actual = calculate_dead_points(bases)
  lu.assertEquals(actual, 6)
end

function test_camp_is_worth_points_passed_in()
  local base_obj = { getName = function() return "base Camp #48" end, getGUID = function() return "ABCDE" end  }
  local actual = get_points_for_base(base_obj, 32)
  lu.assertEquals(actual, 32)
end

function test_camp_is_worth_eight_points_of_casualties()
  local base_obj = { getName = function() return "base Camp #48" end, getGUID = function() return "ABCDE" end  }
  local bases = {base_obj}
  local actual = calculate_dead_points(bases)
  lu.assertEquals(actual, 8)
end

function test_camp_is_worth_zero_points_in_army_builder()
  local base_obj = { getName = function() return "base Camp #48" end, getGUID = function() return "ABCDE" end  }
  local bases = {base_obj}
  local actual = calculate_army_builder_points(bases)
  lu.assertEquals(actual, 0)
end

-- Fortified camp battle card
function test_fortified_camp_is_worth_nine_points_of_casualties()
  local base_obj = { getName = function() return "base Fortified Camp #48" end, getGUID = function() return "ABCDE" end  }
  local bases = {base_obj}
  local actual = calculate_dead_points(bases)
  lu.assertEquals(actual, 9)
end

-- Fortified camp battle card
function test_fortified_camp_is_worth_one_points_in_army_builder()
  local base_obj = { getName = function() return "base Fortified Camp #48" end, getGUID = function() return "ABCDE" end  }
  local bases = {base_obj}
  local actual = calculate_army_builder_points(bases)
  lu.assertEquals(actual, 1)
end

function test_base_definition_overrides_points(base_obj)
  -- setup
  local old_fn = get_base_definition_from_base_obj
  get_base_definition_from_base_obj = function(base_obj)
    return {points=77}
  end

  -- exercise
  local base_obj = { getName = function() return "base Archer* #48" end, getGUID = function() return "ABCDE" end  }
  local bases = {base_obj}
  local actual = calculate_army_builder_points(bases)
  local bases = {base_obj}
  lu.assertEquals(actual, 77)

  -- cleanup
  get_base_definition_from_base_obj = old_fn
end

function test_algorithm_used_if_base_definition_does_not_define_points(base_obj)
  -- setup
  local old_fn = get_base_definition_from_base_obj
  get_base_definition_from_base_obj = function(base_obj)
    return {}
  end

  -- exercise
  local base_obj = { getName = function() return "base Archer* #48" end, getGUID = function() return "ABCDE" end  }
  local bases = {base_obj}
  local actual = calculate_army_builder_points(bases)
  local bases = {base_obj}
  lu.assertEquals(actual, 3)

  -- cleanup
  get_base_definition_from_base_obj = old_fn
end

function test_points_for_base_are_not_rounded()
  -- setup
  local old_fn = get_base_definition_from_base_obj
  get_base_definition_from_base_obj = function(base_obj)
    return {points=4.5}
  end

  -- exercise
  local base_obj = { getName = function() return "base Archer* #48" end, getGUID = function() return "ABCDE" end  }
  local actual = get_points_for_base(base_obj, 32)
  lu.assertEquals(actual, 4.5)

  -- cleanup
  get_base_definition_from_base_obj = old_fn
end

function test_total_points_are_not_rounded_up_for_army_builder()
  -- setup
  local old_fn = get_base_definition_from_base_obj
  get_base_definition_from_base_obj = function(base_obj)
    return {points=4.5}
  end

  -- exercise
  local base_obj = { getName = function() return "base Archer* #48" end, getGUID = function() return "ABCDE" end  }
  local bases = {base_obj}
  local actual = calculate_army_builder_points(bases)
  local bases = {base_obj}
  lu.assertEquals(actual, 4.5)

  -- cleanup
  get_base_definition_from_base_obj = old_fn
end

function test_total_points_are_rounded_up_for_casualties()
  -- setup
  local old_fn = get_base_definition_from_base_obj
  get_base_definition_from_base_obj = function(base_obj)
    return {points=4.5}
  end

  -- exercise
  local base_obj = { getName = function() return "base Archer* #48" end, getGUID = function() return "ABCDE" end  }
  local bases = {base_obj}
  local actual = calculate_dead_points(bases)
  local bases = {base_obj}
  lu.assertEquals(actual, 5)

  -- cleanup
  get_base_definition_from_base_obj = old_fn
end

os.exit( lu.LuaUnit.run() )
