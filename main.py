import arc_synthesizer
import json

def trainningDataReader():
    with open('arc-agi_challenges.json', 'r') as f:
        data = json.load(f)
    return data

arc_synthesizer.bfs_search(trainningDataReader(), 5)
#arc_synthesizer.testF.close()
