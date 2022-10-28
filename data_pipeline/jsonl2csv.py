"""
Input: a.jsonl, output: a.csv
1. rebalance
2. add prompt
"""
import re
import os, sys
import json, csv
from glob import glob

assert len(sys.argv) == 2, "Usage: python3 jsonl2csv.py <input.jsonl>"

INPUT_JSONL = sys.argv[1].strip()
assert INPUT_JSONL.endswith(".jsonl"), "Input must be .jsonl!"

OUTPUT_CSV = re.sub(r'.jsonl$', '.csv', INPUT_JSONL)
print("Output path:", OUTPUT_CSV)

def read_jsonl(path):
    ret = []
    with open(path) as f:
        for line in f:
            ret.append(json.loads(line))
    return ret

questions = read_jsonl(INPUT_JSONL)
for i, q in enumerate(questions):
    # Answer = B if even
    if i % 2 == 0 and q["answerKey"] == "A":
        q["question"]["choices"] = q["question"]["choices"][::-1]
        q["answerKey"] = "B"
    # Answer = A if odd
    if i % 2 == 1 and q["answerKey"] == "B":
        q["question"]["choices"] = q["question"]["choices"][::-1]
        q["answerKey"] = "A"
    
    q["question"]["choices"][0]["label"] = "A"
    q["question"]["choices"][1]["label"] = "B"

"""
,prompt,classes,answer_index
0,"Question: {Q}
A. {A1}
B. {A2}
Answer:","[' A', ' B']",0/1
1,"Question: {Q}
A. {A1}
B. {A2}
Answer:","[' A', ' B']",0/1
"""
with open(OUTPUT_CSV, "w") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(["", "prompt", "classes", "answer_index"])
    for i, q in enumerate(questions):
        Q = q["question"]["stem"].replace("\"", "``")
        A1 = q["question"]["choices"][0]["text"]
        A2 = q["question"]["choices"][1]["text"]
        prompt = f"""The following are multiple choice questions (with answers) about common sense.
        
Question: {Q}
A. {A1}
B. {A2}
Answer:"""
        classes = "[' A', ' B']"
        answer_index = (0 if q["answerKey"] == "A" else 1)
        csvwriter.writerow([i, prompt, classes, answer_index])