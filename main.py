import arc_synthesizer
import json
import time

result_file = open("result.txt", "w")
def dataReader(name):
    with open(name, 'r') as f:
        data = json.load(f)
    return data

arc_synthesizer.bfs_search(dataReader("arc-agi_challenges.json")["9d4f6a8e"]["train"], 2)
#arc_synthesizer.gbfs_search(trainningDataReader()["b6f3e8d7"]["train"], 5, arc_synthesizer.mismatched_cells)
#arc_synthesizer.a_star_search(trainningDataReader()["b6f3e8d7"]["train"], 5, arc_synthesizer.mismatched_cells)
#arc_synthesizer.testF.close()

def main():
    data = dataReader("arc-agi_challenges.json")
    solution = dataReader("arc-agi_solutions.json")

    bfs_accuracy = 0
    gfbs_accuracy = 0
    a_star_accuracy = 0

    total_num = len(data)
    for key in data:
        if (key == "d7a5c8b3"):
            continue
        print("Testing Task:", key)
        print("Testing Task:", key, file=result_file)

        # BFS Search
        #print("Beginning BFS Search")
        print("Beginning BFS Search", file=result_file)
        start = time.perf_counter()
        result = arc_synthesizer.bfs_search(data[key]["train"], 5)
        end = time.perf_counter()
        print ("BFS Program: ", result, "Time: ", round(end - start, 2))
        print ("BFS Program: ", result, "Time: ", round(end - start, 2), file=result_file)

        output = arc_synthesizer.apply_program(data[key]["test"][0]["input"], result) if result else None
        print ("Test Output: ", output)
        print ("Test Output: ", output, file=result_file)
        
        if (output == solution[key][0]):
            bfs_accuracy =+ 1

        # GBFS Search
        #print("Beginning BFS Search (Mismatched Cells)")
        print("Beginning BFS Search (Mismatched Cells)", file=result_file)
        start = time.perf_counter()
        result = arc_synthesizer.gbfs_search(data[key]["train"], 5, arc_synthesizer.mismatched_cells)
        end = time.perf_counter()
        print ("GBFS(MMC): ", result, "Time: ", round(end - start, 2))
        print ("GBFS(MMC): ", result, "Time: ", round(end - start, 2), file=result_file)

        output = arc_synthesizer.apply_program(data[key]["test"][0]["input"], result) if result else None
        print ("Test Output: ", output )
        print ("Test Output: ", output, file=result_file)

        if (output == solution[key][0]):
            gbfs_accuracy =+ 1
        
        # A* Search
        #print("Beginning BFS Search (Mismatched Cells)")
        print("Beginning BFS Search (Mismatched Cells)", file=result_file)
        start = time.perf_counter()
        result = arc_synthesizer.a_star_search(data[key]["train"], 5, arc_synthesizer.mismatched_cells)
        end = time.perf_counter()
        print ("A*(MMC): ", result, "Time: ", round(end - start, 2))
        print ("A*(MMC): ", result, "Time: ", round(end - start, 2), file=result_file)

        output = arc_synthesizer.apply_program(data[key]["test"][0]["input"], result) if result else None
        print ("Test Output: ", output )
        print ("Test Output: ", output, file=result_file)
        
        if (output == solution[key][0]):
            a_star_accuracy =+ 1

        print("Expected Outcome: ", solution[key][0])
        print("Expected Outcome: ", solution[key][0], file=result_file)
        print("")
        
    print("="*15)
    print("ACCURACY SUMMARY")
    print("="*15)
    print("="*15, file=result_file)
    print("ACCURACY SUMMARY", file=result_file)
    print("="*15, file=result_file)

    print("Total Tasks: ", total_num)
    print("BFS Accuracy: ", bfs_accuracy, "/", total_num, "(", (bfs_accuracy/total_num)*100, "%)")
    print("GFBS (Cell Mismatch)", gbfs_accuracy, "/", total_num, "(", (gbfs_accuracy/total_num)*100, "%)")
    print("A* (Cell Mismatch)", a_star_accuracy, "/", total_num, "(", (a_star_accuracy/total_num)*100, "%)")

    print("Total Tasks: ", total_num, file=result_file)
    print("BFS Accuracy: ", bfs_accuracy, "/", total_num, "(", (bfs_accuracy/total_num)*100, "%)", file=result_file)
    print("GFBS (Cell Mismatch)", gbfs_accuracy, "/", total_num, "(", (gbfs_accuracy/total_num)*100, "%)", file=result_file)
    print("A* (Cell Mismatch)", a_star_accuracy, "/", total_num, "(", (a_star_accuracy/total_num)*100, "%)", file=result_file)

    result_file.close
        

#main()