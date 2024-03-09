import json

with open('show.json') as f:
    show = json.load(f)

data = f"#{show['title']}\n#{show['description']}\n#{show['version']}\n"
for seg in show["segments"]:
    data = f"{data}-{seg['time']}\n   {seg['function']['r']}\n   {seg['function']['g']}\n   {seg['function']['b']}\n"
    if "wrapping" in seg["function"] and seg["function"]["wrapping"]: data = f"{data}   wrap\n"

f = open("show.fbling", "w")
f.write(data)
f.close()