lu = require('externals/luaunit/luaunit')
require('flatten')

function check_figure(figure)
  lu.assertEquals(type(figure.height_correction), 'number')
  lu.assertEquals(type(figure.scale), 'number')
  lu.assertEquals(type(figure.rotation), 'number')
  if figure.description ~= nil then
    lu.assertEquals(type(figure.description), 'string')
  end
  if figure.author ~= nil then
    lu.assertEquals(type(figure.author), 'string')
  end
  lu.assertFalse(figure.mesh == nil)
  lu.assertTrue(tlen(figure.mesh) > 0)
  for _,mesh in pairs(figure.mesh) do
    lu.assertEquals(type(mesh), "string")
  end
  lu.assertFalse(figure.player_red_tex == nil)
  lu.assertEquals(type(figure.player_red_tex), "string")
  lu.assertFalse(figure.player_blue_tex == nil)
  lu.assertEquals(type(figure.player_blue_tex), "string")
end

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
        for j,figure in pairs(model['fixed_models']) do
          if "string" == type(figure) then
            if nil == _G[figure] then
              print("No variable ", figure)
              lu.assertTrue(false)
            end
            if "table" ~= type(_G[figure]) then
              print(figure, " figure should be table")
              lu.assertTrue(false)
            end
            check_figure(_G[figure])
          else
            print("g_models['" .. id .. "'][" .. tostring(i) .. "][" .. tostring(j) .. "] should be string.")
            lu.assertTrue(false)
          end
        end
        lu.assertEquals(n_models, actual)
      end
    end
  end
end

os.exit( lu.LuaUnit.run() )
