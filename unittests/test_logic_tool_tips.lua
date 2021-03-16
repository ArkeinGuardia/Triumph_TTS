lu = require('externals/luaunit/luaunit')
armies = {}
require('scripts/data/data_armies_Medieval_Era')
require('scripts/utilities_lua')
require('scripts/utilities')
require('scripts/logic_tool_tips')
require('scripts/data/data_troops')
require('scripts/data/data_cheat_sheet')


function test_build_tool_tip_returns_empty_string_for_bad_type()
    local actual = build_tool_tip("Children")
    lu.assertEquals(actual, "")
end

function test_build_tool_tip_does_not_include_movement_for_camp()
    local tip = build_tool_tip("Camp")
    local actual = str_has_substr(tip, "MU")
    lu.assertFalse(actual)
end

function test_build_tool_tip_includes_movement()
    local tip = build_tool_tip("Archers")
    local actual = str_has_substr(tip, "3 MU")
    lu.assertTrue(actual)
end

function test_build_tool_tip_non_shooters()
    local tip = build_tool_tip("Bow Levy")
    local actual = str_has_substr(tip, "ranged combat: /")
    lu.assertTrue(actual)
end

function test_build_tool_tip_shooters()
    local tip = build_tool_tip("Archers")
    local actual = str_has_substr(tip, "ranged combat: 3/")
    lu.assertTrue(actual)
end

function test_build_tool_tip_target()
    local tip = build_tool_tip("Bow Levy")
    local actual = str_has_substr(tip, "ranged combat: /3")
    lu.assertTrue(actual)
end

function test_build_tool_tip_close_combat()
    local tip = build_tool_tip("Bow Levy")
    local actual = str_has_substr(tip, "close combat: 2/3")
    lu.assertTrue(actual)
end

function test_build_tool_tip_target_combat_factor_missing()
    local tip = build_tool_tip_string({})
    local actual = str_has_substr(tip, "ranged combat: /X")
    lu.assertTrue(actual)
end

function test_build_tool_tip_target_close_combat_vs_foot_missing()
    local tip = build_tool_tip_string({})
    local actual = str_has_substr(tip, "close combat: X/")
    lu.assertTrue(actual)
end

function test_build_tool_tip_target_close_combat_vs_mounted_missing()
    local tip = build_tool_tip_string({})
    local actual = str_has_substr(tip, "close combat: X/X")
    lu.assertTrue(actual)
end

function test_build_tool_tip_battle_card_added()
    -- setup
    local old_decorations = g_decorations
    g_decorations = {}

    local base = {
        getName = function() return "Archers_Mobile" end,
        getGUID = function() return "ABCDE" end,
        base_definition_name = "burgundian_ordannances_1471_to_1477_ad_knights_dd_mounted"
    }
    g_decorations[ base.getGUID() ] = {base_definition_name =  base.base_definition_name}

    -- Exercise
    local tip = get_tool_tip_for_base(base)

    -- Verify
    local actual = str_has_substr(tip, "Deployment Dismounting")
    lu.assertTrue(actual)

    -- Cleanup
    g_decorations = old_decorations
end

function test_get_tool_tip_returns_nil_if_tool_tips_not_enabled()
    -- setup
    local orig = g_tool_tips_enabled
    g_tool_tips_enabled = false

    -- exercise
    local actual = get_tool_tip("Bow Levy")

    -- validate
    lu.assertEquals(actual, nil)

    -- cleanup
    g_tool_tips_enabled = orig
end

function test_get_tool_tip_returns_tool_tip_if_tool_tips_enabled()
    -- setup
    local orig = g_tool_tips_enabled
    g_tool_tips_enabled = true

    -- exercise
    local tip = get_tool_tip("Bow Levy")

    -- validate
    local actual = str_has_substr(tip, "MU")
    lu.assertTrue(actual)

    -- cleanup
    g_tool_tips_enabled = orig
end

function test_get_tool_tip_returns_empty_string_for_proxy()
    -- setup
    local orig = g_tool_tips_enabled
    g_tool_tips_enabled = true

    -- exercise
    local actual = get_tool_tip_for_base_name("base Proxy 40x15 # 1")

    -- validate
    lu.assertEquals(actual, "")

    -- cleanup
    g_tool_tips_enabled = orig
end

function test_get_base_type_from_name_removes_base_and_serial_number()
    local actual = get_base_type_from_name("base Archers # 3")
    lu.assertEquals(actual, "Archers")
end

function test_get_base_type_from_name_removes_general()
    local actual = get_base_type_from_name("base Archers_Gen # 3")
    lu.assertEquals(actual, "Archers")
end

-- asterix is added to the name of a base to indicate that there
-- is something special about it, and the tool tips should
-- be consultex
function test_get_base_type_from_name_removes_asterix()
    local actual = get_base_type_from_name("base Archers_Gen* # 3")
    lu.assertEquals(actual, "Archers")
end

os.exit( lu.LuaUnit.run() )
