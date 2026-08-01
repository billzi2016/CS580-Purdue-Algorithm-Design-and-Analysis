"""文件意图：手写坐标压缩。适用场景：值域很大而相对顺序重要的数组或端点。核心思想：手写归并排序、去重后映射到连续秩。输入输出：返回压缩坐标和有序唯一值。时间 O(nlogn)，空间 O(n)。关键边界：空输入返回两个空列表。"""
def _merge(values:list[int])->list[int]:
    if len(values)<=1:return values[:]
    mid=len(values)//2;left=_merge(values[:mid]);right=_merge(values[mid:]);out=[];i=j=0
    while i<len(left) and j<len(right):
        if left[i]<=right[j]:out.append(left[i]);i+=1
        else:out.append(right[j]);j+=1
    return out+left[i:]+right[j:]
def coordinate_compress(values:list[int])->tuple[list[int],list[int]]:
    """压缩 values。
    参数：任意整数列表。返回：(各元素从零开始秩，升序唯一原值)。空输入合法；映射只依赖大小关系。"""
    unique=[]
    for value in _merge(values):
        if not unique or unique[-1]!=value:unique.append(value)
    rank={value:index for index,value in enumerate(unique)}
    return [rank[value] for value in values],unique
if __name__=="__main__":
    assert coordinate_compress([100,-5,100,7])==([2,0,2,1],[-5,7,100])
    assert coordinate_compress([])==([],[])
    print("001_coordinate_compression: all examples passed")
