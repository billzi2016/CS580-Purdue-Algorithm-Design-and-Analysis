"""手写整体二分：求每个查询首次满足单调谓词的时间。"""

def parallel_binary_search(events: list[int], thresholds: list[int]) -> list[int | None]:
    """返回每个阈值首次被事件前缀和达到的时间；真正按中点分桶扫描。"""
    if any(value < 0 for value in events): raise ValueError("事件增量必须非负以保证单调性")
    total=sum(events); low=[0]*len(thresholds); high=[len(events)]*len(thresholds)
    for i,value in enumerate(thresholds):
        if value <= 0: high[i]=0
        elif value > total: low[i]=len(events)+1
    while True:
        buckets=[[] for _ in range(len(events)+1)]; pending=False
        for i in range(len(thresholds)):
            if low[i] < high[i]:
                middle=(low[i]+high[i])//2; buckets[middle].append(i); pending=True
        if not pending: break
        prefix=0
        for time in range(len(events)+1):
            if time: prefix += events[time-1]
            for i in buckets[time]:
                if prefix >= thresholds[i]: high[i]=time
                else: low[i]=time+1
    return [None if low[i]>len(events) else low[i] for i in range(len(thresholds))]

if __name__ == "__main__":
    assert parallel_binary_search([2, 0, 3, 1], [0, 2, 5, 6, 7]) == [0, 1, 3, 4, None]
    print("004_parallel_binary_search: all examples passed")
