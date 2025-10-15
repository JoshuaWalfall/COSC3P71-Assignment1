import arc_synthesizer
import json
import time

result_file = open("result.txt", "w")
def dataReader(name):
    with open(name, 'r') as f:
        data = json.load(f)
    return data

#arc_synthesizer.bfs_search(dataReader("arc-agi_challenges.json")["9d4f6a8e"]["train"], 2)
#arc_synthesizer.gbfs_search(trainningDataReader()["b6f3e8d7"]["train"], 5, arc_synthesizer.mismatched_cells)
#arc_synthesizer.a_star_search(trainningDataReader()["b6f3e8d7"]["train"], 5, arc_synthesizer.mismatched_cells)
#arc_synthesizer.testF.close()

def main():
    data = dataReader("arc-agi_challenges.json")
    solution = dataReader("arc-agi_solutions.json")
    complexity = 5


    bfs_accuracy = 0
    bfs_timing = 0

    gbfs_accuracy = 0
    gbfs_timing = 0

    gbfs_accuracy_custom = 0
    gbfs_timing_custom = 0

    a_star_accuracy = 0
    a_star_timing = 0

    a_star_accuracy_custom = 0
    a_star_timing_custom = 0

    total_num = len(data)
    for key in data:
        
        print("Testing Task:", key)
        print("Testing Task:", key, file=result_file)

        # BFS Search
        
        print("Beginning BFS Search", file=result_file)
        start = time.perf_counter()
        result = arc_synthesizer.bfs_search(data[key]["train"], complexity)
        end = time.perf_counter()
        bfs_timing =+ round(end-start, 4)
        print ("BFS Program: ", result, "Time: ", round(end - start, 4))
        print ("BFS Program: ", result, "Time: ", round(end - start, 4), file=result_file)

        output = arc_synthesizer.apply_program(data[key]["test"][0]["input"], result)#if result else None
        print ("Test Output: ", output)
        print ("Test Output: ", output, file=result_file)
        
        if (output == solution[key][0]):
            bfs_accuracy =+ 1
        

        # GBFS Search
        #print("Beginning BFS Search (Mismatched Cells)")
        print("Beginning GBFS Search (Mismatched Cells)", file=result_file)
        start = time.perf_counter()
        result = arc_synthesizer.gbfs_search(data[key]["train"], complexity, arc_synthesizer.mismatched_cells)
        end = time.perf_counter()
        gbfs_timing =+ round(end-start, 4)
        print ("GBFS(MMC): ", result, "Time: ", round(end - start, 4))
        print ("GBFS(MMC): ", result, "Time: ", round(end - start, 4), file=result_file)

        output = arc_synthesizer.apply_program(data[key]["test"][0]["input"], result) #if result else None
        print ("Test Output: ", output )
        print ("Test Output: ", output, file=result_file)

        if (output == solution[key][0]):
            gbfs_accuracy =+ 1

        # GBFS Search CUSTOM
        #print("Beginning BFS Search (Mismatched Cells)")
        print("Beginning BFS Search (Custom Heurstic)", file=result_file)
        start = time.perf_counter()
        result = arc_synthesizer.gbfs_search(data[key]["train"], complexity, arc_synthesizer.heuristic_custom1)
        end = time.perf_counter()
        gbfs_timing_custom =+ round(end-start, 4)
        print ("GBFS(C): ", result, "Time: ", round(end - start, 4))
        print ("GBFS(C): ", result, "Time: ", round(end - start, 4), file=result_file)

        output = arc_synthesizer.apply_program(data[key]["test"][0]["input"], result) #if result else None
        print ("Test Output: ", output )
        print ("Test Output: ", output, file=result_file)

        if (output == solution[key][0]):
            gbfs_accuracy_custom =+ 1
        
        # A* Search
        #print("Beginning BFS Search (Mismatched Cells)")
        print("Beginning BFS Search (Mismatched Cells)", file=result_file)
        start = time.perf_counter()
        result = arc_synthesizer.a_star_search(data[key]["train"], complexity, arc_synthesizer.mismatched_cells)
        end = time.perf_counter()
        a_star_timing =+ round(end-start, 4)
        print ("A*(MMC): ", result, "Time: ", round(end - start, 4))
        print ("A*(MMC): ", result, "Time: ", round(end - start, 4), file=result_file)

        output = arc_synthesizer.apply_program(data[key]["test"][0]["input"], result)# if result else None
        print ("Test Output: ", output )
        print ("Test Output: ", output, file=result_file)
        
        if (output == solution[key][0]):
            a_star_accuracy =+ 1

        # A* Search CUSTOM
        #print("Beginning BFS Search (Mismatched Cells)")
        print("Beginning BFS Search (Custom)", file=result_file)
        start = time.perf_counter()
        result = arc_synthesizer.a_star_search(data[key]["train"], complexity, arc_synthesizer.heuristic_custom1)
        end = time.perf_counter()
        a_star_timing_custom =+ round(end-start, 4)

        print ("A*(C): ", result, "Time: ", round(end - start, 4))
        print ("A*(C): ", result, "Time: ", round(end - start, 4), file=result_file)

        output = arc_synthesizer.apply_program(data[key]["test"][0]["input"], result) #if result else None
        print ("Test Output: ", output )
        print ("Test Output: ", output, file=result_file)
        
        if (output == solution[key][0]):
            a_star_accuracy_custom =+ 1

        print("Expected Outcome: ", solution[key][0])
        print("Expected Outcome: ", solution[key][0], file=result_file)
        print("")
        print("", file=result_file)
        
        
    print("="*30)
    print("ACCURACY SUMMARY")
    print("="*30)
    print("="*30, file=result_file)
    print("ACCURACY SUMMARY", file=result_file)
    print("="*30, file=result_file)

    print("Total Tasks ( Complexity ", complexity, " ): ", total_num)
    print("BFS Accuracy: ", bfs_accuracy, "/", total_num, "(", (bfs_accuracy/total_num)*100, "%)")
    print("BFS Timing: ", round(bfs_timing/total_num, 4))
    print("")
    print("GFBS (Cell Mismatch) Accuracy: ", gbfs_accuracy, "/", total_num, "(", (gbfs_accuracy/total_num)*100, "%)")
    print("GBFS (Cell Mismatch) Timing :  ", round(gbfs_timing/total_num,4))
    print("")
    print("A* (Cell Mismatch) Accuracy: ", a_star_accuracy, "/", total_num, "(", (a_star_accuracy/total_num)*100, "%)")
    print("A* (Cell Mismatch) Timing : ", round(a_star_timing/total_num,4))
    print("")
    print("GFBS (Custom) Accuracy: ", gbfs_accuracy_custom, "/", total_num, "(", (gbfs_accuracy_custom/total_num)*100,"%)" )
    print("GFBS (Custom) Timing: ", round(gbfs_timing_custom/total_num,4))
    print("")
    print("A* (Custom) Accuracy: ", a_star_accuracy_custom, "/", total_num, "(", (a_star_accuracy_custom/total_num)*100, "%)")
    print("A* (Custom) Timing: ", round(a_star_timing_custom/total_num,4))

    print("Total Tasks ( Complexity ", complexity, " ): ", total_num, file=result_file)
    print("BFS Accuracy: ", bfs_accuracy, "/", total_num, "(", (bfs_accuracy/total_num)*100, "%)", file=result_file)
    print("BFS Timing: ", (bfs_timing/total_num), file=result_file)
    print("", file=result_file)
    print("GFBS (Cell Mismatch) Accuracy: ", gbfs_accuracy, "/", total_num, "(", (gbfs_accuracy/total_num)*100, "%)", file=result_file)
    print("GBFS (Cell Mismatch) Timing :  ", (gbfs_timing/total_num), file=result_file)
    print("", file=result_file)

    print("A* (Cell Mismatch) Accuracy: ", a_star_accuracy, "/", total_num, "(", (a_star_accuracy/total_num)*100, "%)", file=result_file)
    print("A* (Cell Mismatch) Timing : ", (a_star_timing/total_num), file=result_file)
    print("", file=result_file)

    print("GFBS (Custom) Accuracy: ", gbfs_accuracy_custom, "/", total_num, "(", (gbfs_accuracy_custom/total_num)*100,"%)", file=result_file)
    print("GFBS (Custom) Timing: ", (gbfs_timing_custom/total_num), file=result_file)
    print("", file=result_file)

    print("A* (Custom) Accuracy: ", a_star_accuracy_custom, "/", total_num, "(", (a_star_accuracy_custom/total_num)*100, "%)", file=result_file)
    print("A* (Custom) Timing: ", (a_star_timing_custom/total_num), file=result_file)

    result_file.close
        

main() 