from collections import Counter

def get_inputs(file):
    with open(f"2021/day14-extended-polymerization/{file}.txt") as f:
        lines =  [line.strip("\n") for line in f]
        polymer = lines[0]
        instructions = [rule.split(" -> ") for rule in lines[2:]]
        
        rules = {}
    for instruction in instructions:
        rules[instruction[0]] = instruction[1]

    return polymer, rules

def processStep(polymer, days, rules):
    if days == 0:
        return polymer
    else: 
        new_polymer = ""
        for i in range(len(polymer) - 1):
            curr_polymer = polymer[i:i+2]
            ins = rules[curr_polymer]
            new_polymer += curr_polymer[0] + ins 
        new_polymer += curr_polymer[1] #off by 1 

        return processStep(new_polymer, days - 1, rules)

def get_code(file, days):
    polymer, rules = get_inputs(file)
    polymer_count = Counter(processStep(polymer, days, rules))

    return polymer_count.most_common(1)[0][1] - polymer_count.most_common()[-1][1]

print(get_code("input", 10))