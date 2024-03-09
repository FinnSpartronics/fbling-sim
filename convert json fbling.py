import json

with open('show.json') as f:
    show = json.load(f)

data = ""
for seg in show:
    data = f"{data}-{seg['time']}\n   {seg['function']['r']}\n   {seg['function']['g']}\n   {seg['function']['b']}\n"
    if seg["function"]["wrapping"]: data = f"{data}   wrap\n"

f = open("show.fbling", "w")
f.write(data)
f.close()