import random
from copy import deepcopy
import json
import os


with open("cfg.json") as f:
    CFG = json.load(f)
TYPEEFFECTIVENESS = CFG["type"]


def rnd():
    return random.random()

def rndc(choose4m, k=1):
    if not isinstance(choose4m, list):
        choose4m = list(choose4m)
    return random.choice(choose4m) if k == 1 else random.sample(choose4m, k)

def randomize(x):
    return int(int(x * (100 - random.randrange(0, 16))) / 100)

def n2f(n):
    return n.replace("-", "").replace(" ", "_")


def read_json(filename):
    with open(filename) as f:
        content = json.load(f)
    return content
def write_json(content, filename):
    with open(filename, "w") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
def read(filename):
    with open(filename) as f:
        contet = f.read().strip()
    return contet
def write(content, filename):
    with open(filename, "w") as f:
        f.write(content.strip())
        f.write("\n")
def read_jsonl(filename):
    content = []
    with open(filename) as f:
        for line in f:
            content += [json.loads(line.strip())]
    return content
def write_jsonl(content, filename, mode="w"):
    with open(filename, mode) as f:
        for line in content:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

def rndstr(k=3):
    code = ""
    for i in range(k):
        code += chr(random.randint(97, 122))
    return code

def get_keys(content):
    if isinstance(content, dict):
        return list(content.keys())
    
def get_values(content):
    if isinstance(content, dict):
        return list(content.values())

class mdict(dict):
    def __eq__(self, value):
        return value == list(self.keys())[0]
    
    def key(self):
        return list(self.keys())[0]
