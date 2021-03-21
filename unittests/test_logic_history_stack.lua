lu = require('externals/luaunit/luaunit')
require('scripts/data/data_settings')
require('scripts/data/data_tables')
require('scripts/data/data_terrain')
require('scripts/data/data_troops')
require('scripts/base_cache')
require('scripts/log')
require('scripts/utilities_lua')
require('scripts/utilities')
require('scripts/logic_base_obj')
require('scripts/logic_terrain')
require('scripts/logic_gizmos')
require('scripts/logic_spawn_army')
require('scripts/logic_dead')
require('scripts/logic_dice')
require('scripts/logic_history_stack')
require('scripts/logic_history_snapshot')
require('scripts/logic')
require('scripts/uievents')



function test_current_equals_current()
    local sut = Stack.Create()
    lu.assertEquals(sut._current, sut._current)
end

function test_head_points_itself()
    local sut = Stack.Create()
    local head = sut._head
    local actual = head.after
    lu.assertEquals(head, actual)
end


function test_tail_points_itself()
    local sut = Stack.Create()
    local head = sut._head
    local tail = head.before
    local actual = tail.before
    lu.assertEquals(tail, actual)
end

function test_tail_points_head()
    local sut = Stack.Create()
    local head = sut._head
    local tail = head.before
    local actual = tail.after
    lu.assertEquals(head, actual)
end

function test_head_points_to_tail_on_empty_stack()
    local sut = Stack.Create()
    local head = sut._head
    lu.assertNotNil(head)
    local tail = sut._head.before
    lu.assertFalse(head == tail)
    local head_again = tail.after
    lu.assertEquals(head, head_again)
end


 function test_current_starts_at_top()
     local sut = Stack.Create()
     assert(sut._head ~= sut._head.before)
     local actual = sut:is_at_top()
     lu.assertTrue(actual)
end

function test_error_logged_at_go_back_when_at_bottom()
    -- setup
    local error_logged = false
    local old_print_important = print_important
    print_important = function() error_logged = true end
    -- exercise
    local sut = Stack.Create()
    sut:go_back()
    -- validate
    lu.assertTrue(error_logged)
    -- cleanup
    print_important = old_print_important
end

 function test_go_back_on_empty_stack_keeps_current_at_top()
    -- setup
    local old_print_important = print_important
    print_important = function()  end
    -- exercise
    local sut = Stack.Create()
    sut:go_back()
    -- validate
    local actual = sut:is_at_top()
    lu.assertTrue(actual)
    -- cleanup
    print_important = old_print_important
end

function test_push_inserts_into_list()
    local sut = Stack.Create()
    local head = sut._head
    local tail = sut._head.before
    local event1 = {type="1", apply=function() end}
    sut:push(event1)
    lu.assertEquals(head, sut._head)
    lu.assertTrue(head ~= sut._head.before)
    lu.assertTrue(tail ~= sut._head.before)
    local new_node = sut._head.before
    lu.assertEquals(new_node, head.before)
    lu.assertEquals(head, new_node.after)
    lu.assertEquals(tail, new_node.before)
    lu.assertEquals(new_node, tail.after)
end

function test_push_puts_new_node_as_current()
    local sut = Stack.Create()
    local head = sut._head
    local tail = sut._head.after
    local event1 = {type="1", apply=function() end}
    sut:push(event1)
    lu.assertTrue(sut._current ~= head)
    lu.assertTrue(sut._current ~= tail)
end

function test_no_longer_at_top_of_stack_after_go_back()
    local sut = Stack.Create()
    local event1 = {type="1", apply=function() end}
    local event2 = {type="2", apply=function() end}
    sut:push(event1)
    sut:push(event2)
    sut:go_back()
    local actual = sut:is_at_top()
    lu.assertFalse(actual)
end

function test_go_back_applies_the_event_before_the_current_event()
    local applied_event = nil
    local sut = Stack.Create()
    local event1 = {type="1", apply = function() applied_event = 1 end}
    local event2 = {type="2", apply = function() applied_event = 2 end}
    sut:push(event1)
    sut:push(event2)
    sut:go_back()
    lu.assertEquals(applied_event, 1)
end

function test_go_back_changes_current_event()
    local applied_event = nil
    local sut = Stack.Create()
local head = sut._head
local tail = sut._tail    
    local event1 = {type="1", apply = function() applied_event = 1 end}
    local event2 = {type="2", apply = function() applied_event = 2 end}
    local event3 = {type="3", apply = function() applied_event = 3 end}
    sut:push(event1)
 local one = sut._head.before
 lu.assertTrue(head == sut._head)
 lu.assertTrue(one == sut._head.before)
 lu.assertEquals(one, sut._current)
    sut:push(event2)
local two = sut._head.before
lu.assertFalse(head == sut._head.before)
lu.assertFalse(head == sut._head.before)
lu.assertEquals(two, sut._current)
sut:push(event3)
 local three = sut._head.before
 lu.assertEquals(three, sut._current)
    sut:go_back()
    lu.assertEquals(applied_event, 2)
lu.assertEquals(two, sut._current)
    sut:go_back()
lu.assertEquals(one, sut._current)
    lu.assertEquals(applied_event, 1)
end

function test_go_forwared_applies_the_event_after_the_current_event()
    -- setup
    local applied_event = nil
    local sut = Stack.Create()
    local event1 = {type="1", apply = function() applied_event = 1 end}
    local event2 = {type="2", apply = function() applied_event = 2 end}
    sut:push(event1)
    sut:push(event2)
    sut:go_back()
    lu.assertEquals(applied_event, 1)
    -- Exercise
    sut:go_forward()
    -- validate
    lu.assertEquals(applied_event, 2)
end



function test_go_forwared_moves_the_current_event()
    -- setup
    local applied_event = nil
    local sut = Stack.Create()
    local event1 = {type="1", apply = function() applied_event = 1 end}
    local event2 = {type="2", apply = function() applied_event = 2 end}
    local event3 = {type="3", apply = function() applied_event = 3 end}
    sut:push(event1)
    sut:push(event2)
    sut:push(event3)
    sut:go_back()
    lu.assertEquals(applied_event, 2)
    sut:go_back()
    lu.assertEquals(applied_event, 1)
    -- Exercise
    sut:go_forward()
    lu.assertEquals(applied_event, 2)
    sut:go_forward()
    -- validate
    lu.assertEquals(applied_event, 3)
end

function test_delete_node_updates_links()
    -- setup
    local sut = Stack.Create()
    local head = sut._head
    local tail = sut._head.before
    local event1 = {apply = function()  end}
    sut:push(event1)
    -- exercise
    sut:_delete_node(sut._head.before)
    -- validate
    lu.assertEquals(tail, sut._head.before)
    lu.assertEquals(head, sut._head.before.after)
end


function test_push_erases_all_above_current()
    -- setup
    local applied_event = nil
    local sut = Stack.Create()
    local event1 = {apply = function() applied_event = 1 end}
    local event2 = {apply = function() applied_event = 2 end}
    local event3 = {apply = function() applied_event = 3 end}
    local event4 = {apply = function() applied_event = 4 end}
    sut:push(event1)
    sut:push(event2)
    sut:push(event3)
    sut:go_back()
    lu.assertEquals(applied_event, 2)
    sut:go_back()
    lu.assertEquals(applied_event, 1)
    -- Exercise
    sut:push(event4)
    -- Validate
    sut:go_back()
    lu.assertEquals(applied_event, 1)
    sut:go_forward()
    lu.assertEquals(applied_event, 4)
end

function test_empty_stack_size_is_zero()
  local sut = Stack.Create()
  local actual = sut:size()
  lu.assertEquals(0, actual)
end

function test_push_adds_to_size()
    local event1 = {apply = function() applied_event = 1 end}
    local sut = Stack.Create()
    sut:push(event1)
    local actual = sut:size()
    lu.assertEquals(actual, 1)
end

function test_push_eraseing_decreases_size()
    -- setup
    local applied_event = nil
    local sut = Stack.Create()
    local event1 = {apply = function() applied_event = 1 end}
    local event2 = {apply = function() applied_event = 2 end}
    local event3 = {apply = function() applied_event = 3 end}
    local event4 = {apply = function() applied_event = 4 end}
    sut:push(event1)
    sut:push(event2)
    sut:push(event3)
    sut:go_back()
    lu.assertEquals(applied_event, 2)
    sut:go_back()
    lu.assertEquals(applied_event, 1)
    -- Exercise
    sut:push(event4)
    local actual = sut:size()
    -- Validate
    lu.assertEquals(actual, 2)
end

function test_pushing_past_capacity_erases_oldest_event()
    -- setup
    local applied_event = nil
    local sut = Stack.Create()
    sut._capacity = 3
    local tail = sut._head.before
    local event1 = {apply = function() applied_event = 1 end}
    local event2 = {apply = function() applied_event = 2 end}
    local event3 = {apply = function() applied_event = 3 end}
    local event4 = {apply = function() applied_event = 4 end}
    sut:push(event1)
    sut:push(event2)
    sut:push(event3)
    lu.assertEquals(sut:size(), 3)
    -- Exercise
    sut:push(event4)
    local actual = sut:size()
    -- Validate
    lu.assertEquals(actual, 3)
end

function test_top_returns_null_for_empty_stack()
    local sut = Stack.Create()
    local actual = sut.top()
    lu.assertEquals(actual, nil)
end

function test_top_returns_most_recent_event()
    -- setup
    local applied_event = nil
    local sut = Stack.Create()
    local event1 = {apply = function() applied_event = 1 end}
    local event2 = {apply = function() applied_event = 2 end}
    sut:push(event1)
    sut:push(event2)
    -- exercise
    local top = sut:top()
    -- validate
    top.apply()
    lu.assertEquals(applied_event, 2)
end
  
os.exit( lu.LuaUnit.run() )
