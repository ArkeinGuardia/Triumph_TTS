lu = require('externals/luaunit/luaunit')
require('flatten')


local function starts_with(str, start)
   return str:sub(1, #start) == start
end

local function ends_with(str, ending)
   return ending == "" or str:sub(-#ending) == ending
end


function remove_suffix(s, suffix)
    return s:gsub("%" .. suffix, "")
end

function normalize_base_name(name)
  name = remove_suffix(name, "*")
  name = remove_suffix(name, " General")
  name = remove_suffix(name, "_Mobile")
  return name
end


-- Troop types as listed in appendix A
function get_valid_base_names_triumph()
  local valid= {}
  valid['Archers']=true
  valid['Bow Levy']=true
  valid['Light Foot']=true
  valid['Light Spear']=true
  valid['Rabble']=true
  valid['Raiders']=true
  valid['Skirmishers']=true
  valid['Warband']=true
  valid['Artillery']=true
  valid['Elite Foot']=true
  valid['Heavy Foot']=true
  valid['Horde']=true
  valid['Pavisiers']=true
   -- Appendix A uses "Pike"
  valid['Pikes']=true
  -- Appendix A uses "Spear"
  valid['Spears']=true
  valid['War Wagons']=true
  valid['Warriors']=true
  valid['Bad Horse']=true
  valid['Battle Taxi']=true
  valid['Chariots']=true
  valid['Elite Cavalary']=true
  valid['Horse Bow']=true
  valid['Javelin Cavalry']=true
  valid['Knights']=true
  valid['Cataphracts']=true
  valid['Elephants']=true
  valid['Camp']=true
  return valid
 end


 -- Assert that the name of a base matches the converntios of the game.
 -- Used to check the army lists to see that they have valid entries.
 -- name: name of the base
 -- army_name: name of the army, used for reporting errors
 -- valid_names: set of names that are valid in the game.
function assert_base_name_valid(name, army_name, valid_names)
  local n_name = normalize_base_name(name)
  if valid_names[n_name] then
    return
  end
  print("Invalid normalized name: ", n_name)
  print("name: ", name)
  print("army name: ", army_name)
  lu.assertTrue(false)
end

-- Appendix A lists the abbreviations for the bases.  Verify only the correct
-- abbreviations are used in the army lists.
function test_bases_types_are_in_list()
  local valid_names = get_valid_base_names_triumph()
  for book_name, book in pairs(armies) do
    for army_name, army in pairs(armies[book_name]) do
      for k,v in pairs(army) do
        if not starts_with(tostring(k), "data") then
          local base_definition = get_base_definition(v)
          if nil == base_definition then
            print("get_base_definition failed for ", v)
            lu.assertTrue(false)
          end
          local name = base_definition.name
          assert_base_name_valid(name, army_name, valid_names)
        end
      end
    end
  end
end

-- If a base has points override then verify that the points is a
-- reasonable value
function test_points_sane()
  for book_name, book in pairs(armies) do
    for army_name, army in pairs(armies[book_name]) do
      for k,v in pairs(army) do
        if not starts_with(tostring(k), "data") then
          local base_data = get_base_definition(v)
          if nil ~= base_data['points'] then
            lu.assertTrue(base_data.points >= 2)
            lu.assertTrue(base_data.points <= 5)
	        end
        end
      end
    end
  end
end

 -- Assert that the battle cards is valid
function assert_battle_card_valid(base_definition, army, key)
  if base_definition['battle_card'] == nil then
    return
  end
  if base_definition.battle_card == 'Deployment Dismounting' then
    return
  end
  if base_definition.battle_card == 'Mobile Infantry' then
    return
  end

  -- assertion failed
  print("army: ", army)
  print("base definition: ", key, ' ', base_definition.name)
  print("battle card: ", base_definition['battle_card'])
  lu.assertTrue(false)
end

-- If a base has a battle card check that it is valid
function test_battle_cards_valid()
  for book_name, book in pairs(armies) do
    for army_name, army in pairs(armies[book_name]) do
      for k,v in pairs(army) do
        if not starts_with(tostring(k), "data") then
          local base_data = get_base_definition(v)
          assert_battle_card_valid(base_data, army, k)
        end
      end
    end
  end
end

function assert_base_definitions_have_names(army_obj)
  for base_id,base_data  in pairs(army_obj) do
    if base_id ~= 'data' then
      local base_definition = get_base_definition(base_data)
      lu.assertTrue(nil ~= base_definition)
      local name = base_definition['name']
      lu.assertTrue(nil ~= name)
    end
  end
end

function test_base_definitions_have_names()
  for themes,armies_in_theme in pairs(armies) do
    for _,army_obj in pairs(armies_in_theme) do
      assert_base_definitions_have_names(army_obj)
    end
  end
  for _,army_obj in pairs(army) do
    assert_base_definitions_have_names(army_obj)
  end
end


function assert_base_definitions_have_depth(army_obj)
  for base_id,base_data  in pairs(army_obj) do
    if base_id ~= 'data' then
      local base_definition = get_base_definition(base_data)
      lu.assertTrue(nil ~= base_definition)
      local name = base_definition['name']
      lu.assertTrue(nil ~= name)
      local depth = get_base_depth(name)
      lu.assertTrue(nil ~= depth)
    end
  end
end

function test_base_definitions_have_depth()
  -- Setup
  local old_print_error = print_error
  print_error = function(message)
    print(message)
    assert(false)
  end

  -- Exercise
  for themes,armies_in_theme in pairs(armies) do
    for _,army_obj in pairs(armies_in_theme) do
      assert_base_definitions_have_depth(army_obj)
    end
  end

  -- Cleanup
  print_error = old_print_error
end



-- Any base whose name is "_Mobile" is on a square base.
-- See Battle Card "Mobile Infantry"
function test_get_base_depth_mobile()
  -- Setup
  local old_print_error = print_error
  print_error = function(message)
    print(message)
    assert(false)
  end

  -- Exercise
  local actual = get_base_depth('Archers_Mobile')
  lu.assertEquals(actual, 40)

  -- Cleanup
  print_error = old_print_error
end



function test_get_base_depth_camp()
  -- Setup
  local old_print_error = print_error
  print_error = function(message)
    print(message)
    assert(false)
  end

  -- Exercise
  local actual = get_base_depth('Camp')
  lu.assertEquals(actual, 40)

  -- Cleanup
  print_error = old_print_error
end

function test_get_base_depth_elite_foot()
  -- Exercise
  local old_print_error = print_error
  print_error = function(message)
    print(message)
    assert(false)
  end

  -- Exercise
  local actual = get_base_depth('Elite Foot')
  lu.assertEquals(actual, 15)

  -- Cleanup
  print_error = old_print_error
end

function test_get_base_depth_elite_foot_general()
  -- Exercise
  local old_print_error = print_error
  print_error = function(message)
    print(message)
    assert(false)
  end

  -- Exercise
  local actual = get_base_depth('Elite Foot General')
  lu.assertEquals(actual, 15)

  -- Cleanup
  print_error = old_print_error
end

-- A base that has important information in the tool top
-- gets an asterix in its name.
function test_get_base_depth_with_notes()
  -- Exercise
  local old_print_error = print_error
  print_error = function(message)
    print(message)
    assert(false)
  end

  -- Exercise
  local actual = get_base_depth('Elite Foot General*')
  lu.assertEquals(actual, 15)

  -- Cleanup
  print_error = old_print_error
end

-- Check that the armies could be spawned
function test_spawn_army(army_name)
  -- setup
  local old_spawn_base = spawn_base
  local old_spawn_note = spawn_note
  local old_print_error = print_error
  local old_print_important = print_important
  local old_print_info = print_info
  local old_update_tool_tips = update_tool_tips
  spawn_base = function() end
  spawn_note = function() end
  update_tool_tips = function() end
  print_important = function() end
  print_info = function() end
  print_error = function(message)
    print(message)
    assert(false)
  end

  -- Exercise
  for id,army_obj in pairs(army) do
    spawn_army(army_obj.data.name, army_obj, false, 'red')
  end

  -- Cleanup
  update_tool_tips = old_update_tool_tips
  print_info = old_print_info
  print_important = old_print_important
  print_error = old_print_error
  spawn_note = old_spawn_note
  spawn_base = old_spawn_base
end



os.exit( lu.LuaUnit.run() )
