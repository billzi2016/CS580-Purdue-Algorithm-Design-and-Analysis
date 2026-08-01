"""文件意图：手写离线区间和查询。适用场景：全部查询已知且数组静态。核心思想：预处理前缀和，按输入批量回答半开区间。输入输出：返回每个查询的和。预处理 O(n)，总查询 O(q)。空间 O(n)。关键边界：空区间为零，非法范围拒绝。"""
def offline_range_sums(values:list[int],queries:list[tuple[int,int]])->list[int]:
    """批量返回半开区间查询和。
    参数：values 是静态数组，queries 是 (left,right)。返回与查询顺序对应的和；越界抛出 IndexError；前缀和将重复工作移到离线预处理阶段。"""
    prefix=[0]
    for value in values:prefix.append(prefix[-1]+value)
    result=[]
    for left,right in queries:
        if left<0 or left>right or right>len(values):raise IndexError("区间越界")
        result.append(prefix[right]-prefix[left])
    return result
if __name__=="__main__":
    assert offline_range_sums([3,1,4,1,5],[(0,5),(1,4),(2,2)])==[14,6,0]
    assert offline_range_sums([],[(0,0)])==[0]
    print("002_offline_queries: all examples passed")
