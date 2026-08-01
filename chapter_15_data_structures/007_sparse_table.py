"""文件意图：手写静态 RMQ 稀疏表。适用场景：不可修改数组的区间最小值。核心思想：预处理所有 2 的幂长区间并重叠合并两块。输入输出：支持 range_min。构建 O(nlogn)，查询 O(1)，空间 O(nlogn)。关键边界：空数组无有效查询。"""
class SparseTable:
    """只读区间最小值稀疏表，min 的幂等性允许重叠块。"""
    def __init__(self, values:list[int])->None:
        """以 values 构建；空数组合法但不可查询非空范围。"""
        self.length=len(values);self.table=[values[:]] if values else []
        width=1
        while 2*width<=self.length:
            previous=self.table[-1];self.table.append([min(previous[i],previous[i+width]) for i in range(self.length-2*width+1)]);width*=2
    def range_min(self,left:int,right:int)->int:
        """返回闭区间 [left,right] 最小值；非法范围抛出 IndexError。"""
        if left<0 or left>right or right>=self.length:raise IndexError("区间越界")
        level=(right-left+1).bit_length()-1; width=1<<level;return min(self.table[level][left],self.table[level][right-width+1])
if __name__ == "__main__":
    table=SparseTable([4,6,1,5,7,3]);assert table.range_min(1,4)==1 and table.range_min(3,5)==3;print("007_sparse_table: all examples passed")
