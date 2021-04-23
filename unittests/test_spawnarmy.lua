require('flatten')
lu = require('externals/luaunit/luaunit')

function test_get_a_model_definition_returns_plain_base()
    local base_def = g_base_definitions[g_str_5fb1ba44e1af06001770feb5]
    local model_def = get_a_model_definition(base_def)
    lu.assertEquals(model_def.base, 'tile_plain_40x20_Warband' )
    lu.assertEquals(n_models, nil )
end

function test_get_a_model_definition_returns_model_base()
    local base_def = g_base_definitions[g_str_5fb1ba34e1af06001770e186]
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
    lu.assertEquals(model_def.base, 'tile_plain_40x40_Artillery')

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

os.exit( lu.LuaUnit.run() )
