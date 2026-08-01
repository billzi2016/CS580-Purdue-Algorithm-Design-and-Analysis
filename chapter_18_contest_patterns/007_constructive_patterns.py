"""文件意图：手写构造给定逆序对数的排列。适用场景：构造题中需要精确控制成对关系。核心思想：每次可把最大剩余数置前贡献 remaining-1 个逆序，最后处理剩余值。输入输出：返回 1..n 排列或 None。时间 O(n)，空间 O(n)。关键边界：超过 n(n-1)/2 无解。"""
def permutation_with_inversions(length:int,inversions:int)->list[int]|None:
    """构造长度 length、恰有 inversions 个逆序对的排列。
    参数：length 非负，inversions 非负。返回排列或 None；length 为零时只有零逆序可行；贪心每次贡献当前可取最大逆序数。"""
    if length<0 or inversions<0 or inversions>length*(length-1)//2:return None
    low=1;high=length;result=[]
    while low<=high:
        contribution=high-low
        if inversions>=contribution:result.append(high);high-=1;inversions-=contribution
        else:result.append(low);low+=1
    return result
if __name__=="__main__":
    assert permutation_with_inversions(4,0)==[1,2,3,4]
    assert permutation_with_inversions(4,6)==[4,3,2,1]
    assert permutation_with_inversions(4,3)==[4,1,2,3]
    assert permutation_with_inversions(3,4) is None
    print("007_constructive_patterns: all examples passed")
