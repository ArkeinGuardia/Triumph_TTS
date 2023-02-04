# Generate JSON containing the troop details

require("Triumph_TTS/scripts/data/data_cheat_sheet")
lunajson = require("lunajson")

t = lunajson.encode(base_tool_tips)
print(t)
