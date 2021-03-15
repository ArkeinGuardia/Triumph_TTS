lu = require('externals/luaunit/luaunit')
function dofile (filename)
  local f = assert(loadfile(filename))
  return f()

end
armies={}
dofile("../scripts/data/data_armies_Biblical.ttslua")
dofile("../scripts/data/data_armies_Classical_Era.ttslua")
dofile("../scripts/data/data_armies_Dark_Ages.ttslua")
dofile("../scripts/data/data_armies_Medieval_Era.ttslua")

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
  name = remove_suffix(name, "_Gen")
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

-- page 7 lists the abbreviations for the bases.  Verify only the correct
-- abbreviations are used in the army lists.
function test_bases_are_in_list()
  local valid_names = get_valid_base_names_triumph()
  for book_name, book in pairs(armies) do
    for army_name, army in pairs(armies[book_name]) do
      for k,v in pairs(army) do
        if starts_with(k, "base") then
          local name = v.name
          assert_base_name_valid(name, army_name, valid_names)
        end
      end
    end
  end
end

os.exit( lu.LuaUnit.run() )
