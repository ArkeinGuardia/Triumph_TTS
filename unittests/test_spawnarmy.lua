require('flatten')
lu = require('externals/luaunit/luaunit')

function test_get_a_model_definition_returns_plain_base()
    local base_def = g_base_definitions[g_str_5fb1ba44e1af06001770feb5]
    local model_def = get_a_model_definition(base_def)
    lu.assertEquals(model_def.base, 'tile_plain__Warband' )
    lu.assertEquals(n_models, nil )
end

function test_get_a_model_definition_returns_model_base()
    local base_def = g_base_definitions[g_str_5fb1b9dce1af06001770959d_camp]
    local model_def = get_a_model_definition(base_def)
    lu.assertEquals(model_def.base, 'tile_grass_40x40')
end

function test_get_a_model_definition_returns_plain_base_if_preferred()
    -- Setup
    local old = g_use_plain_bases
    g_use_plain_bases = true

    -- Exercise
    local base_def = g_base_definitions[g_str_5fb1ba34e1af06001770e186]
    local model_def = get_a_model_definition(base_def)

    -- Validate
    lu.assertEquals(model_def.base, 'tile_plain__Artillery')

    -- Cleanup
    g_use_plain_bases = old
end

-- Random model iterator will always return a non-nil figure to add to a base.
function test_random_model_iterator()
    local model_def = g_models[g_str_5fb1ba26e1af06001770c82a]
    local iter = random_model_iterator(model_def[1]['random_models'])
    for i=1,10 do
        local figure = iter()
        lu.assertTrue(figure ~= nil)
    end
end

function test_get_plain_model_tile_name_pack_trains()
    local base_def = g_base_definitions[g_str_5fb1b9d8e1af0600177092b3_camp_pack_train]
    local actual = get_plain_model_tile_name(base_def)
    lu.assertEquals(actual, 'tile_plain__Trains_And_Herds_Donkeys')
end

function test_get_plain_model_tile_name_fortified()
    local base_def = g_base_definitions[g_str_5fb1b9f6e1af06001770a458_camp_fortified]
    local actual = get_plain_model_tile_name(base_def)
    lu.assertEquals(actual, 'tile_plain__Fortified_Camp')
end

-- Verify that a mesh is not selected more than once if there are enough
-- meshes
function test_calculate_random_meshes()
  local input = {1,2,3,4}
  for trial=0,5 do
    math.randomseed(trial)
    local out = calculate_random_meshes(4,input)
    local total={0,0,0,0}
    for _,v in pairs(out) do
      total[v] = total[v] + 1
    end
    for _, v in ipairs(total) do
      if v ~=1 then
        print("seed ", trial, " ", v, " ", v)
        table_print(total)
        lu.assertTrue(false)
      end
    end
  end
end


os.exit( lu.LuaUnit.run() )
