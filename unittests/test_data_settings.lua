lu = require('externals/luaunit/luaunit')
require('scripts/data/data_settings')

function test_bow_range_not_nil()
  lu.assertNotEquals(nil, g_bow_range)
end


function test_art_range_not_nil()
  lu.assertNotEquals(nil, g_art_range)
end

function test_wwg_range_not_nil()
  lu.assertNotEquals(nil, g_wwg_range)
end

os.exit( lu.LuaUnit.run() )
