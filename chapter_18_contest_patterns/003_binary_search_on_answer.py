"""文件意图：手写答案二分解决最小化最大连续分段和。适用场景：答案具单调可行性的优化问题。核心思想：二分最大允许和，用贪心检查给定界是否可分成至多 k 段。输入输出：返回最优最大段和。时间 O(nlog(sum))，空间 O(1)。关键边界：仅支持非负数。"""
def minimum_largest_partition_sum(values:list[int],parts:int)->int:
    """把非负 values 分为至多 parts 个非空连续段，返回最小可能最大段和。
    参数：values 非空非负，parts 在 1..len(values)。返回最优界；非法输入抛出 ValueError；可行性随界增大单调。"""
    if not values or parts<=0 or parts>len(values) or any(value<0 for value in values):raise ValueError("需要非空非负数组和有效 parts")
    def feasible(limit:int)->bool:
        used=1;current=0
        for value in values:
            if current+value>limit:used+=1;current=value
            else:current+=value
        return used<=parts
    low=max(values);high=sum(values)
    while low<high:
        middle=(low+high)//2
        if feasible(middle):high=middle
        else:low=middle+1
    return low
if __name__=="__main__":
    assert minimum_largest_partition_sum([7,2,5,10,8],2)==18
    assert minimum_largest_partition_sum([1,1,1],3)==1
    print("003_binary_search_on_answer: all examples passed")
