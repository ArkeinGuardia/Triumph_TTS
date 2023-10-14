lu = require('externals/luaunit/luaunit')
require('scripts/utilities_lua')

function test_shallow_copy_on_number_returns_itself()
  local expected = 3.14
  local actual = shallow_copy(expected)
  lu.assertAlmostEquals(actual, expected, 1e-6)
end

function test_shallow_copy_on_table_returns_table_with_same_key_values()
  local expected = { a=1, b=2, c=3}
  local actual = shallow_copy(expected)
  lu.assertEquals(actual, expected)
end


function test_shallow_copy_on_table_returns_new_table()
  local expected = { a=1, b=2, c=3}
  local actual = shallow_copy(expected)
  expected['a'] = 4
  lu.assertEquals(actual['a'], 1)
end

function test_shallow_copy_does_not_copy_nested_tables()
  local expected = { a=1, b=2, c=3, d={e=4}}
  local actual = shallow_copy(expected)
  expected['d']['e'] = 6
  lu.assertEquals(actual['d']['e'], 6)
end

function test_deep_copy_on_number_returns_itself()
  local expected = 3.14
  local actual = deep_copy(expected)
  lu.assertAlmostEquals(actual, expected, 1e-6)
end

function test_deep_copy_on_table_returns_table_with_same_key_values()
  local expected = { a=1, b=2, c=3}
  local actual = deep_copy(expected)
  lu.assertEquals(actual, expected)
end


function test_deep_copy_on_table_returns_new_table()
  local expected = { a=1, b=2, c=3}
  local actual = deep_copy(expected)
  expected['a'] = 4
  lu.assertEquals(actual['a'], 1)
end

function test_deep_copy_does_copies_nested_tables()
  local expected = { a=1, b=2, c=3, d={e=4}}
  local actual = deep_copy(expected)
  expected['d']['e'] = 6
  lu.assertEquals(actual['d']['e'], 4)
end

function test_str_equals_case_insensitive_both_lower()
  lu.assertTrue( str_equals_case_insensitive("aa", "aa"))
end

function test_str_equals_case_insensitive_both_lower_false()
  lu.assertFalse( str_equals_case_insensitive("aa", "bb"))
end


function test_str_equals_case_insensitive_mixed_case()
  lu.assertTrue( str_equals_case_insensitive("aA", "Aa"))
end

function test_str_equals_case_insensitive_mixed_case_false()
  lu.assertFalse( str_equals_case_insensitive("ba", "Ab"))
end

function test_str_trim_returns_original_string()
  local expected = "abc      def"
  local actual = str_trim(expected)
  lu.assertEquals(actual, expected)
end

function test_str_trim_removes_leading_spaces()
  local expected = "abc      def"
  local actual = str_trim("  " .. expected)
  lu.assertEquals(actual, expected)
end

function test_str_trim_removes_trailing_spaces()
  local expected = "abc      def"
  local actual = str_trim("  " .. expected)
  lu.assertEquals(actual, expected)
end

function test_str_remove_prefix_returns_original_string()
  local actual=str_remove_prefix("something", "delta")
  lu.assertEquals(actual, "something")
end

function test_str_remove_prefix()
  local actual=str_remove_prefix("something", "some")
  lu.assertEquals(actual, "thing")
end

function test_str_remove_suffix_returns_original_string()
  local actual=str_remove_suffix("something", "delta")
  lu.assertEquals(actual, "something")
end

function test_str_remove_suffix()
  local actual=str_remove_suffix("4Bd  General", "  General")
  lu.assertEquals(actual, "4Bd")
end

function test_decimalize_number()
  local actual = decimalize(4.3763232)
  lu.assertEquals(tostring(actual), "4.4")
end

function test_decimalize_coords()
  local before = {}
  before['x'] = 1.21212121
  before['y'] = 2.3
  local actual = decimalize(before)
  expected = {x=1.2, y=2.3}
  lu.assertEquals(actual, expected)
end

function test_decimalize_vector()
  local expected = {1,2,3}
  local actual = decimalize(expected)
  lu.assertEquals(actual, expected)
end


function test_decimalize_line_segment()
  local point1 = {x=1.2, y=2.3}
  local point2 = {x=3.4, y=4.6}
  local expected = {point1, point2}
  local actual = decimalize(expected)
  lu.assertEquals(actual, expected)
end

os.exit( lu.LuaUnit.run() )
