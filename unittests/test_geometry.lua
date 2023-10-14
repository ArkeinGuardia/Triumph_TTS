lu = require('externals/luaunit/luaunit')
require 'scripts/geometry'

function test_lines_indentical()
    local line1 = {{x=30,z=20},{x=60,z=90}}
    local line2 = line1
    local actual = is_segment_contained(line1, line2)
    lu.assertTrue(actual)
  end

  function test_lines_reversed()
    local line1 = {{x=30,z=20},{x=60,z=90}}
    local line2 = {{x=60,z=90},{x=30,z=20}}
    local actual = is_segment_contained(line1, line2)
    lu.assertTrue(actual)
  end

  function test_lines_not_colinear()
    local line1 = {{x=30,z=20},{x=60,z=90}}
    local line2 = {{x=31,z=21},{x=61,z=91}}
    local actual = is_segment_contained(line1, line2)
    lu.assertFalse(actual)
  end

  function test_lines1_inside_line2()
    local line1 = {{x=30,z=30},{x=60,z=60}}
    local line2 = {{x=20,z=20},{x=70,z=70}}
    local actual = is_segment_contained(line1, line2)
    lu.assertTrue(actual)
  end

  function test_lines1_starts_before_line2()
    local line1 = {{x=20,z=20},{x=70,z=70}}
    local line2 = {{x=30,z=30},{x=70,z=70}}
    local actual = is_segment_contained(line1, line2)
    lu.assertFalse(actual)
  end

  function test_lines1_ends_after_line2()
    local line1 = {{x=30,z=30},{x=80,z=80}}
    local line2 = {{x=30,z=30},{x=70,z=70}}
    local actual = is_segment_contained(line1, line2)
    lu.assertFalse(actual)
  end

  os.exit( lu.LuaUnit.run() )

