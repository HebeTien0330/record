from line_profiler import LineProfiler
from copy import deepcopy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import time

# 二分查找法
class BinarySearchALG():

    def __init__(self, samepleSet):
        self.m_sampleSet = samepleSet
        self.m_result = []
        self.m_edge = 0
        self.m_start = 0
        self.m_end = 0
        self.m_maxNum = 0

    # 初始化二分查找数组
    def initSearchArray(self):
        edge = 0
        searchAarry = []
        for sampleId, weight in self.m_sampleSet.items():
            searchAarry.append([sampleId, range(edge, edge+weight)])
            edge += weight
        return searchAarry

    def initWeightedRandom(self):
        self.m_searchAarry = self.initSearchArray()
        self.m_edge = len(self.m_searchAarry)
        self.m_end = self.m_edge-1
        self.m_maxNum = self.m_searchAarry[-1][1][-1]

    def weightedRandom(self, count):
        for _ in range(count):
            self.initWeightedRandom()
            self.doWeightedRandom(self.m_start, self.m_end, self.m_maxNum)
        return self.m_result

    def doWeightedRandom(self, start, end, maxNum):
        randomNum = random.randint(0, maxNum)
        res = self.bindarySearch(randomNum, start, end)
        self.m_result.append(res)
        self.m_sampleSet.pop(res)

            
    def bindarySearch(self, target, start, end):
        length = end - start
        mid = length // 2
        idx = mid + start
        weightRange = self.m_searchAarry[idx][1]
        if target in weightRange:
            sampleId = self.m_searchAarry[idx][0]
            return sampleId
        if target > weightRange[-1]:
            return self.bindarySearch(target, idx+1, end)
        return self.bindarySearch(target, start, idx)


# A-Res算法
class A_RES_ALG():

    def __init__(self, samepleSet):
        self.m_sampleSet = samepleSet
        self.m_result = []

    def calcEigenValue(self):
        pool = {}
        for sampleId, weight in self.m_sampleSet.items():
            eigen = pow(random.random(), 1/weight)
            pool[sampleId] = eigen
        return pool
    
    # def weightedRandom(self, count):
    #     for _ in range(count):
    #         pool = self.calcEigenValue()
    #         pool = sorted(pool.items(), key=lambda x:x[1], reverse=True)
    #         self.m_result.append(pool[0][0])
    #     return self.m_result

    def weightedRandom(self, count):
        pool = self.calcEigenValue()
        pool = sorted(pool.items(), key=lambda x:x[1], reverse=True)
        self.m_result = [val[0] for val in pool[0: count]]
        return self.m_result


# 别名采样算法
class AliasSamplingALG():
    
    def __init__(self, sampleSet):
        self.m_sampleSet = sampleSet
        self.m_aliasTable = []
        self.m_littleQueue = []  # 存放面积小于1的图形的队列
        self.m_largeQueue = []  # 存放面积大于等于1的图形的队列
        self.m_result = []
        self.initQueue()

    def initQueue(self):
        demon = sum(self.m_sampleSet.values())
        total = len(self.m_sampleSet)
        for sampleId, weight in self.m_sampleSet.items():
            area = weight / demon * total
            if area > 1:
                self.m_largeQueue.append([sampleId, area])
            elif area < 1:
                self.m_littleQueue.append([sampleId, area])
            else:
                self.m_aliasTable.append([[sampleId, area]])

    def constructAliastable(self):
        while self.m_littleQueue and self.m_largeQueue:
            largeInfo = self.m_largeQueue.pop(0)
            littleInfo = self.m_littleQueue.pop(0)
            restArea = largeInfo[1] - (1 - littleInfo[1])
            self.m_aliasTable.append([[largeInfo[0], 1-littleInfo[1]], littleInfo])
            if restArea > 1:
                self.m_largeQueue.append([largeInfo[0], restArea])
            elif restArea < 1:
                self.m_littleQueue.append([largeInfo[0], restArea])
            else:
                self.m_aliasTable.append([[largeInfo[0], restArea]])

    def weightedRandom(self, count):
        for _ in range(count):
            self.constructAliastable()
            total = len(self.m_aliasTable)
            idx = random.randint(0, total)
            area = self.m_aliasTable[idx]
            rand = random.random()
            if rand < area[0][1]:
                self.m_result.append(area[0][0])
                continue
            self.m_result.append(area[1][0])
        return self.m_result

def genSampleSet():
    sampleSet = {}
    for sampleId in range(1, 100001):
        sampleSet[sampleId] = ((sampleId-1) // 20000 + 1) * 500
    return sampleSet

def statistic(result):
    match = {1: "第一类", 2: "第二类", 3: "第三类", 4: "第四类", 5: "第五类"}
    statisticData = {"第一类":0, "第二类": 0, "第三类": 0, "第四类": 0, "第五类": 0}
    for sampleId in result:
        dataType = sampleId // 20000 + 1
        newType = match[dataType]
        statisticData[newType] += 1
    return statisticData

# 柱状图
def getBarChart(BSA_res, ARA_res, ASA_res):
    mpl.rcParams['font.sans-serif']=['SimHei']
    mpl.rcParams['axes.unicode_minus']=False

    labels = ["第一类", "第二类", "第三类", "第四类", "第五类"]
    width = 0.2
    x = np.arange(len(labels)) 

    fig, ax = plt.subplots()
    ax.bar(x - width, list(BSA_res.values()), width, label='二分查找法')
    ax.bar(x, list(ARA_res.values()), width, label='A-RES算法')
    ax.bar(x + width, list(ASA_res.values()), width, label='别名采样算法')


    # 为y轴、标题和x轴等添加一些文本。
    ax.set_ylabel('采样次数', fontsize=16)
    ax.set_xlabel('样本类型', fontsize=16)
    ax.set_title('有放回抽取采样次数对比')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()

def calcTime(func):
    def execute(*args):
        startTime = time.time()
        res = func(*args)
        endTime = time.time()
        costTime = endTime - startTime
        print(f"function {func.__name__} run cost time {int(costTime * 1000)} ms")
        return res
    return execute


lp = LineProfiler()

# @calcTime
def analysisBSA(sampleSet):
    BSA = BinarySearchALG(sampleSet)
    lp_wrapper = lp(BSA.weightedRandom)
    BSA_res = lp_wrapper(500)
    lp.print_stats()
    BSA_res = statistic(BSA_res)
    return BSA_res

# @calcTime
def analysisARA(sampleSet):
    ARA = A_RES_ALG(sampleSet)
    lp_wrapper = lp(ARA.weightedRandom)
    ARA_res = lp_wrapper(500)
    lp.print_stats()
    ARA_res = statistic(ARA_res)
    return ARA_res

# @calcTime
def analysisASA(sampleSet):
    ASA = AliasSamplingALG(sampleSet)
    lp_wrapper = lp(ASA.weightedRandom)
    ASA_res = lp_wrapper(500)
    lp.print_stats()
    ASA_res = statistic(ASA_res)
    return ASA_res

def analysis():

    sampleSet = genSampleSet()

    # 二分查找法
    sampleSetBSA = deepcopy(sampleSet)
    BSA_res = analysisBSA(sampleSetBSA)
    print(BSA_res)

    # A-RES算法
    sampleSetARA = deepcopy(sampleSet)
    ARA_res = analysisARA(sampleSetARA)
    print(ARA_res)

    # 别名采样算法
    sampleSetASA = deepcopy(sampleSet)
    ASA_res = analysisASA(sampleSetASA)
    print(ASA_res)

    getBarChart(BSA_res, ARA_res, ASA_res)

if __name__ == "__main__":
    analysis()
