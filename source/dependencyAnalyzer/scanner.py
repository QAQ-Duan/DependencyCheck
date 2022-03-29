import os
from dependencyAnalyzer.dependency import Dependency

class Scanner():
    def __init__(self,path):
        self.path = path

    def runScan(self,dir,dependecies):
        '''扫描对应路径'''
        SUBFFIX = ['.py','.java']
        for root, _, files in os.walk(".", topdown=True,onerror=None,followlinks=False):
            for name in files:
                subffix = name.split('.')[-1]
                if subffix in SUBFFIX:
                    print(subffix)
                    dependecies.append(Dependency(name,subffix))