lu = require('externals/luaunit/luaunit')
require('scripts/data/data_settings')
require('scripts/base_cache')
require('scripts/logic')
require('scripts/utilities')
require('scripts/utilities_lua')

if g_bases == nil then
  g_bases = {}
end

-- Create a fake base that can be used for
-- testing
function build_base(base_name, tile)
  if tile == nil then
    tile="tile_plain_Archers"
  end

  local base = {
    name=base_name,
    position={
      x=1.0057,
      y=1.2244,
      z=2.1356
    },
    rotation={
      x=0,
      y=0,
      z=0
    },
  }

  base['getName']=function()
    return base.name
  end

  base['getPosition']=function()
    return deep_copy(base.position)
  end

  base['setPosition']=function(new_value)
    base.position = new_value
  end

  base['getRotation']=function()
    return deep_copy(base.rotation)
  end

  base['setRotation']=function(new_value)
    base.rotation = new_value
  end

  g_bases[ base_name] = {
    tile=tile,
    is_red_player=true
  }

  if _G [tile] == nil then
    _G[tile]={ depth=20  }
  end

  return base
end

function test_get_base()
  local expected = build_base("base 4Bw # 16")
  local actual = build_base_cache(expected)
  lu.assertEquals(actual.getBase(), expected)
end

function test_is_wwg()
  local expected = build_base("base 4Bw # 16")
  local sut = build_base_cache(expected)
  lu.assertFalse( sut['is_wwg'] )
end

function test_is_wwg()
  local expected = build_base("base 4Bw # 16")
  local sut = build_base_cache(expected)
  lu.assertFalse( sut['is_large_base'] )
end

function test_get_name()
  local expected = "base 4Bw # 16"
  local base = build_base(expected)
  local sut = build_base_cache(base)
  local actual = sut.getName()
  lu.assertEquals(actual, expected)
end

function test_get_position()
  local base = build_base("base 4Bw # 16")
  local sut = build_base_cache(base)
  lu.assertEquals(sut.getPosition(), base.getPosition())
end

function test_get_rotation()
  local base = build_base("base 4Bw # 16")
  local sut = build_base_cache(base)
  lu.assertEquals(sut.getRotation(), base.getRotation())
end

function test_get_size()
  local name="base 4Bw # 16"
  local base = build_base(name)
  local sut = build_base_cache(base)
  local expected = get_size(name)
  local actual = sut.getSize()
  lu.assertEquals(actual, expected)
end

function test_get_transform()
  local expected_base = build_base("base 4Bw # 16")
  local sut = build_base_cache(expected_base)
  local expected_transform = calculate_transform(expected_base)
  local actual = sut.getTransform()
  lu.assertEquals(actual, expected_transform)
end

function test_get_corners()
  local expected_base = build_base("base 4Bw # 16")
  local sut = build_base_cache(expected_base)
  local expected_transform = calculate_transform(expected_base)
  local expected_corners = expected_transform['corners']
  local actual = sut.getCorners()
  lu.assertEquals(actual, expected_corners)
end

function test_get_shape()
  local expected_base = build_base("base 4Bw # 16")
  local sut = build_base_cache(expected_base)
  local expected_transform = calculate_transform(expected_base)
  local expected_shape = transform_to_shape( expected_transform )
  local actual = sut.getShape()
  lu.assertEquals(actual, expected_shape)
end

function test_intersects_with()
  local other_name = "base 4Bw # 16"
  local other_base = build_base(other_name)
  local other = build_base_cache(other_base)
  local name = "base 4Bw # 15"
  local base = build_base(name)
  local sut = build_base_cache(base)
  local actual = sut.intersectsWith(other)
  lu.assertTrue(actual)
end

function test_set_position_changes_position()
  -- Setup
  local base = build_base("base 4Bw # 16")
  local sut = build_base_cache(base)
  local original_position = deep_copy( sut.getPosition())

  -- Exercise
  local new_pos = sut.getPosition()
  new_pos['x'] = new_pos['x'] + 5
  sut.setPosition(new_pos)

  -- Verify
  local new_position = sut.getPosition()
  lu.assertNotEquals(original_position['x'], new_position['x'])
  lu.assertEquals(new_pos['x'], new_position['x'])
end  


function test_set_position_recalculates_transform()
  -- Setup
  local base = build_base("base 4Bw # 16")
  local sut = build_base_cache(base)
  local original_tansform = deep_copy( sut.getTransform())

  -- Exercise
  local new_pos = sut.getPosition()
  new_pos['x'] = new_pos['x'] + 5
  sut.setPosition(new_pos)

  -- Verify
  local new_transform = sut.getTransform()
  lu.assertNotEquals(original_tansform.position.x, new_transform.position.x)
end  

function test_set_position_recalculates_shape()
  -- Setup
  local base = build_base("base 4Bw # 16")
  local sut = build_base_cache(base)
  local original_shape = deep_copy( sut.getShape())

  -- Exercise
  local new_pos = sut.getPosition()
  new_pos['x'] = new_pos['x'] + 5
  sut.setPosition(new_pos)

  -- Verify
  local new_shape = sut.getShape()
  lu.assertNotEquals(original_shape[1]['x'], new_shape[1]['x'])
end  


function test_set_rotation_changes_rotation()
  -- Setup
  local base = build_base("base 4Bw # 16")
  local sut = build_base_cache(base)
  local original_rotation = deep_copy( sut.getRotation())

  -- Exercise
  local new_rot = sut.getRotation()
  new_rot['y'] = new_rot['y'] + 0.1
  sut.setRotation(new_rot)

  -- Verify
  local new_rotation = sut.getRotation()
  lu.assertNotEquals(original_rotation['y'], new_rotation['y'])
  lu.assertEquals(new_rot['y'], new_rotation['y'])
end  


function test_set_position_recalculates_transform()
  -- Setup
  local base = build_base("base 4Bw # 16")
  local sut = build_base_cache(base)
  local original_tansform = deep_copy( sut.getTransform())

  -- Exercise
  local new_rot = sut.getRotation()
  new_rot['x'] = new_rot['x'] + 3
  new_rot['y'] = new_rot['y'] + 3
  new_rot['z'] = new_rot['z'] + 3
  sut.setRotation(new_rot)

  -- Verify
  local new_transform = sut.getTransform()
  lu.assertNotEquals(original_tansform.corners.topright.x, new_transform.corners.topright.x)
end  

function test_set_position_recalculates_shape()
  -- Setup
  local base = build_base("base 4Bw # 16")
  local sut = build_base_cache(base)
  local original_shape = deep_copy( sut.getShape())

  -- Exercise
  local new_rot = sut.getRotation()
  new_rot['x'] = new_rot['x'] + 3
  new_rot['y'] = new_rot['y'] + 3
  new_rot['z'] = new_rot['z'] + 3
  sut.setRotation(new_rot)

  -- Verify
  local new_shape = sut.getShape()
  lu.assertNotEquals(original_shape[1]['x'], new_shape[1]['x'])
end  

--function test_table_print()
--  local expected_base = build_base("base 4Bw # 16")
--  local sut = build_base_cache(expected_base)
--  sut.getTransform()
--  table_print(sut)
--end


os.exit( lu.LuaUnit.run() )
