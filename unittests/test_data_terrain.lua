lu = require('externals/luaunit/luaunit')
require("Triumph_TTS/assets/assets")
require('scripts/utilities_lua')
require('scripts/data/data_terrain')

os.exit( lu.LuaUnit.run() )
