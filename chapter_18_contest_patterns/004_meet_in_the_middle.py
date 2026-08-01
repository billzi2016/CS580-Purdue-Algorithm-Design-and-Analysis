"""文件意图：手写折半搜索解决子集和。适用场景：n 约为 40、无法枚举全部 2^n 子集时。核心思想：分半枚举两侧子集和，再搜索互补和。输入输出：判断目标是否可达。时间 O(2^(n/2) log 2^(n/2))，空间 O(2^(n/2))。关键边界：空集可达目标零。"""
def subset_sum_exists(values:list[int],target:int)->bool:
    """判断是否存在子集和等于 target。
    参数：整数列表与目标。返回布尔值；空列表仅能构成零；左右各枚举所有掩码避免全量指数枚举。"""
    middle=len(values)//2
    def sums(part:list[int])->set[int]:
        result={0}
        for value in part:result|={old+value for old in result}
        return result
    left=sums(values[:middle]);right=sums(values[middle:])
    return any(target-value in right for value in left)
if __name__=="__main__":
    assert subset_sum_exists([3,34,4,12,5,2],9)
    assert not subset_sum_exists([3,34,4,12,5,2],30)
    assert subset_sum_exists([],0)
    print("004_meet_in_the_middle: all examples passed")
