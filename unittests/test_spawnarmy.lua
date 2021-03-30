require('flatten')
lu = require('externals/luaunit/luaunit')

function test_get_a_model_definition_returns_plain_base()
    local base_def = g_base_definitions[g_str_5fb1ba44e1af06001770feb5]
    local model_def = get_a_model_definition(base_def)
    lu.assertEquals(model_def.base, 'tile_plain_40x20_Warband' )
    lu.assertEquals(n_models, 0 )
end

os.exit( lu.LuaUnit.run() )
