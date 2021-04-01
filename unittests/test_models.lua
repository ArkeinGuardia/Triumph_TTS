lu = require('externals/luaunit/luaunit')
require('flatten')

function test_models_have_base()
  for id,models in pairs(g_models) do
    for i,model in pairs(models) do
      local base = model['base']
      if base == nil then
        print("g_models['" .. id .. "'][" .. tostring(i) .. "] has no base.")
        table_print(model)
        lu.assertTrue(false)
      end
    end
  end
end

function test_models_with_fixed_figures_have_right_number()
  for id,models in pairs(g_models) do
    for i,model in pairs(models) do
      if model['fixed_models'] ~= nil then
        local n_models = model['n_models']
        if n_models == nil then
          n_models = 0
        end 
        local actual = tlen(model['fixed_models'])
        if n_models ~= actual then
          print("g_models['" .. id .. "'] has wrong number of models.")
        end
        lu.assertEquals(n_models, actual)
      end
    end
  end
end

os.exit( lu.LuaUnit.run() )
