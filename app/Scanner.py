import re
import os
import importlib.util

class Scanner:

    def __init__(self, programPath):
        self.programPath = programPath
        self.mainFilePath = os.path.dirname(self.programPath)

    def findDownloadEnv(self):
        envFilePaths = []
        for filepath, dirnames, filenames in os.walk(self.mainFilePath):
            for filename in filenames:
                # print(filename)
                if filename == 'requirements.txt' or filename == 'Pipfile.txt':
                    path = os.path.join(filepath, filename)
                    envFilePaths.append(path)
        return envFilePaths

    def findPackage(self):
        moduleList = []
        moduleNameList = []
        
        with open(self.programPath, 'r', encoding="utf-8") as f:
            contents = f.readlines()
        for line in contents:
            pattern_from = re.compile(r"from\s+(.+?)\s")
            pattern_import = re.compile(r"import\s+(.+?)[\n]")
            pattern_import_as = re.compile(r"import\s+(.+?)\sas")
            
            match_from = re.search(pattern_from, line)
            match_import = re.search(pattern_import, line)
            match_import_as = re.search(pattern_import_as, line)
            
            # print(match_from,match_import)
            if match_from != None:
                rex = match_from.group(1)
                rex = rex.replace(" ", '')
                moduleNameList.append(rex.split('.')[0])
                
            elif match_import_as != None:
                rex = match_import_as.group(1)
                rex = rex.replace(" ", '')
                moduleNameList.append(rex.split('.')[0])
                
            elif match_import != None:
                rex = match_import.group(1)
                rex = rex.replace(" ", '')
                temp = [s.split('.')[0] for s in rex.split(',')]
                moduleNameList.extend(temp)
                
        #print(moduleNameList)
        for moduleName in moduleNameList:
            module_specs = importlib.util.find_spec(moduleName)
            if module_specs:
                originPath = module_specs.origin
                if originPath:
                    if re.search("__init__.py", originPath):
                        moduleList.append(moduleName)
                else:
                    pass
        print(list(set(moduleList)))
        return list(set(moduleList))


# 在这里输入你想分析的py主文件
#scanner = Scanner(r'D:\study_notebook\作品赛\SJTU\main.py')
# 这个可以找到文件夹中的requirements.txt 和 pipfiles.txt文件地址
#scanner.findDownloadEnv()
# 这个可以找到主文件所有的module
#scanner.findPackage()

