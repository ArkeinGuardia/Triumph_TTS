lu = require('externals/luaunit/luaunit')
require('flatten')


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

function test_get_army_builder_points_for_base_defintions_uses_points_from_tool_tip()
  local def = g_base_definitions[g_str_5fb1ba1ee1af06001770bd94] -- a rabble
  local actual = get_army_builder_points_for_base_definitions({def})
  lu.assertEquals(actual, 2)
end

function test_get_army_builder_points_for_base_defintions_does_not_use_victory_points()
  local def = g_base_definitions[g_str_5fb1b9d8e1af0600177092b3_camp]
  local actual = get_army_builder_points_for_base_definitions({def})
  lu.assertEquals(actual, 0)
end


function test_get_army_builder_points_for_base_defintion_uses_max_for_dismounting()
  local def = g_base_definitions[g_str_5fb1ba2fe1af06001770d99d_general_mounted]
  local actual = get_army_builder_points_for_base_definition(def)
  lu.assertEquals(actual, 4)
end


function test_get_army_builder_points_for_base_defintion_adds_1_point_for_any_deployment_dismounting()
  local def1 = g_base_definitions[g_str_5fb1ba2fe1af06001770d99d_general_mounted]
  local def2 = g_base_definitions[g_str_5fb1ba2fe1af06001770d99d_mounted]
  local actual = get_army_builder_points_for_base_definitions({def1, def2})
  lu.assertEquals(actual, 9)
end

function test_get_army_builder_points_for_base_defintion_adds_2_points_for_any_mid_battle_dismounting()
  local def1 = g_base_definitions[g_str_5fb1ba31e1af06001770dbd0_general_mounted]
  local def2 = g_base_definitions[g_str_5fb1ba31e1af06001770dbd0_general_mounted]
  local actual = get_army_builder_points_for_base_definitions({def1, def2})
  lu.assertEquals(actual, 10)
end

function test_get_army_builder_points_for_charging_camelry_1_point_less_than_normal()
  local def = g_base_definitions[g_str_5fb1ba32e1af06001770de42_charging_camelry]
  local actual = get_army_builder_points_for_base_definition(def)
  -- knights normally cost 4 points
  lu.assertEquals(actual, 3)
end

function test_get_army_builder_points_for_armored_camelry_1_point_less_than_normal()
  local def = g_base_definitions[g_str_5fb1ba2ae1af06001770cf87_armored_camelry]
  local actual = get_army_builder_points_for_base_definition(def)
  -- Cataphracts normally cost 4 points
  lu.assertEquals(actual, 3)
end

function test_get_army_builder_points_for_1_mobile_infantry()
  local def = g_base_definitions[g_str_5fb1ba22e1af06001770c30b_mounted_mobile_infantry]
  local actual = get_army_builder_points_for_base_definitions({def})
  -- same costs as normal
  lu.assertEquals(actual, 2)
end

function test_get_army_builder_points_for_3_mobile_infantry()
  local def = g_base_definitions[g_str_5fb1ba22e1af06001770c30b_mounted_mobile_infantry]
  local actual = get_army_builder_points_for_base_definitions({def,def,def})
  -- 1 extra for more than 1 mobile infranty
  lu.assertEquals(actual, 7)
end

function test_get_army_builder_points_plaustrella_one_point_per_stand()
  local def= g_base_definitions[g_str_5fb1ba35e1af06001770e449_plaustrella]
  local actual = get_army_builder_points_for_base_definitions({def})
  -- heavy foot are normally 3
  lu.assertEquals(actual, 4)
end

os.exit( lu.LuaUnit.run() )
