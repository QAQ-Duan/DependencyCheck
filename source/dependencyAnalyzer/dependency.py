from enum import Enum
from dependencyAnalyzer.analyzer import Analyzer

class Dependency():
    EVIDENCE_CLASS = Enum('EVIDENCE_CLASS',('vendor','package','version'))
    dependency = {'file':'','evidence':'','language':'','analyzer':''}
    file = ''
    language = ''
    analyzer = ''
    def __init__(self,file,language):
        self.file = file
        self.language = language
        return {'file':file,'language':language}
        pass
    def gatherEvidence(self,type,description):
        '''为依赖添加证据'''
        pass
    def removeDependendcy():
        '''删除对应文件的依赖，可能没有用'''
        pass

