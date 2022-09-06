lu = require('externals/luaunit/luaunit')
require("Triumph_TTS/scripts/stack")


if nil == printToAll then
  -- Replace TTS framework function
  printToAll = print
end

function test_starts_empty()
    local sut = Stack.Create()
    lu.assertEquals(sut:size(), 0)
end

function test_push_increases_size()
  data = {x=4}
  local sut = Stack.Create()
  sut:push(data)
  lu.assertEquals(sut:size(), 1)
end

function test_push_adds_item()
  data = {x=4}
  local sut = Stack.Create()
  sut:push(data)
  actual = sut:top()
  lu.assertEquals(data, actual)
end

function test_push_places_item_at_top()
  local sut = Stack.Create()
  data1 = {x=4}
  sut:push(data1)
  data2 = {x=5}
  sut:push(data2)
  actual = sut:top()
  lu.assertEquals(actual, data2)
end

function test_clear_removes_all_items()
  data = {x=4}
  local sut = Stack.Create()
  sut:push(data)
  actual = sut:clear()
  lu.assertEquals(0, sut:size())
end

function test_pop_removes_last_item()
  local sut = Stack.Create()
  data1 = {x=4}
  sut:push(data1)
  data2 = {x=5}
  sut:push(data2)
  sut:pop()
  actual = sut:top()
  lu.assertEquals(data1, actual)
end

function test_pop_returns_top_value()
  local sut = Stack.Create()
  data1 = {x=4}
  sut:push(data1)
  data2 = {x=5}
  sut:push(data2)
  actual = sut:pop()
  lu.assertEquals(actual, data2)
end

function test_apply_calls_all_data()
  incr = function(d) 
    d.x = d.x + 1
  end
  local sut = Stack.Create()
  data1 = {x=4}
  sut:push(data1)
  data2 = {x=5}
  sut:push(data2)
  sut:apply(incr)

  lu.assertEquals(data1.x, 5)
  lu.assertEquals(data2.x, 6)
end

function test_pop_front_removes_one_item()
  local sut = Stack.Create()
  data1 = {x=4}
  sut:push(data1)
  data2 = {x=5}
  sut:push(data2)
  sut:pop_front()
  lu.assertEquals(1, sut:size())
end

function test_pop_front_removes_first_item()
  local sut = Stack.Create()
  data1 = {x=4}
  sut:push(data1)
  data2 = {x=5}
  sut:push(data2)
  sut:pop_front()
  actual = sut:top()
  lu.assertEquals(data2, actual)
end

function test_pop_front_returns_oldest_item()
  local sut = Stack.Create()
  data1 = {x=4}
  sut:push(data1)
  data2 = {x=5}
  sut:push(data2)
  actual = sut:pop_front()
  lu.assertEquals(actual, data1)
end




os.exit( lu.LuaUnit.run() )
