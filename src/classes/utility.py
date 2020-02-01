import json

from deepdiff import DeepDiff


class CompareFile:

    def __init__(self, file1, file2):
        with open(file1, 'r') as f:
            self.json1 = json.load(f)
        with open(file2, 'r') as f:
            self.json2 = json.load(f)

    def difference(self):
        print(DeepDiff(self.json1, self.json2, ignore_order=True))
