"""
可存盘对象
当某个对象继承该对象时, 会变成可存盘对象
可存盘对象存在脏标记m_update, 0表示未存盘, 1表示已存盘
当存盘对象数据变更时脏标记会变成0, 执行update方法时会更新脏标记, 并加入存盘队列
每隔五分钟可存盘对象队列会自动存盘一次
数据持久化、序列化操作均基于pickle模块
对象名和pkl文件的对应关系存放在saveMatch.json
可存盘对象的属性必须是可序列化的
"""

from diff_timer import setTimeOut
import os
import json
import pickle
import copy


SAVE_MATCH = "saveMatch.json"

class SaveObject:

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        self.__dict__["m_update"] = 0

    def __init__(self):
        self.m_update = 0
        self.m_tag = "SaveObject"
        self.m_src = f"db/{SAVE_MATCH}"
        self.m_savePath = f"db/{self.m_tag}.pkl"

    def afterInit(self):
        self.refreshSavePath()
        saveMgr = getSaveMgr()
        saveMgr.addSaveObject(self)

    def refreshSavePath(self):
        # 加载对象时存储路径还是默认值，需要刷新
        self.m_savePath = f"db/{self.m_tag}.pkl"

    def update(self):
        self.m_update = 0
        saveMgr = getSaveMgr()
        saveMgr.addSaveObject(self)

    def save(self):
        if not os.path.exists(self.m_src):
            file = open(self.m_src, "w")
            file.close()
        saveMatch = {}
        with open(self.m_src, "r") as file:
            data = file.read()
            if data:
                saveMatch = json.loads(data)
        if self.m_tag not in saveMatch:
            saveMatch[self.m_tag] = self.m_savePath
            data = json.dumps(saveMatch)
            file = open(self.m_src, "w")
            file.write(data)
            file.close()

        with open(self.m_savePath, 'wb') as pkl:
            pickle.dump(self, pkl)

        print("save", f"update object {self}")
        self.m_update = 1

    def load(self):
        if not os.path.exists(self.m_src):
            return
        saveMatch = {}
        with open(self.m_src, "r") as file:
            data = file.read()
            if data:
                saveMatch = json.loads(data)
        if self.m_tag not in saveMatch:
            return
        self.refreshSavePath()
        if not os.path.exists(self.m_savePath):
            return
        with open(self.m_savePath, "rb") as pkl:
            self = pickle.load(pkl)
        self.m_update = 0
        print("save", f"load object {self}")
        return self


class SaveMgr:

    def __init__(self):
        self.m_saveMap = {}
        setTimeOut(self.allSave, 300, "allSave")

    def getSaveObject(self, tag):
        if tag not in self.m_saveMap:
            return
        return self.m_saveMap[tag]

    def addSaveObject(self, obj):
        tag = obj.m_tag
        if not tag:
            return
        if tag in self.m_saveMap:
            return
        self.m_saveMap[tag] = obj

    def removeSaveObject(self, tag):
        if tag not in self.m_saveMap:
            return
        del self.m_saveMap[tag]

    def allSave(self):
        for tag in copy.deepcopy(self.m_saveMap).keys():
            obj = self.getSaveObject(tag)
            if not obj:
                print("save", f"no such save object {tag}")
                continue
            obj.save()
            self.removeSaveObject(tag)
        print("save", "auto save success")
        setTimeOut(self.allSave, 300, "allSave")

    def allSaveWithoutTimer(self):
        for tag in copy.deepcopy(self.m_saveMap).keys():
            obj = self.getSaveObject(tag)
            if not obj:
                print("save", f"no such save object {tag}")
                continue
            obj.save()
            self.removeSaveObject(tag)
        print("save", "auto save success")


if "g_saveMgr" not in globals():
    g_saveMgr = SaveMgr()

def getSaveMgr():
    return g_saveMgr
