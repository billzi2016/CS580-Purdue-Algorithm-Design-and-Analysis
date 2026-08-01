"""文件意图：手写离散稀疏表求静态区间和。适用场景：不可修改数组的 O(1) 区间和。核心思想：每层预处理跨中点的左后缀和与右前缀和。输入输出：支持 range_sum。构建 O(nlogn)，查询 O(1)，空间 O(nlogn)。关键边界：单点直接返回原值。"""
class DisjointSparseTable:
    """面向加法这一结合但非幂等运算的离散稀疏表。"""
    def __init__(self,values:list[int])->None:
        """以 values 构建；空数组合法。"""
        self.values=values[:];self.length=len(values);self.table=[];block=2
        while block//2<self.length:
            row=[0]*self.length;half=block//2
            for start in range(0,self.length,block):
                middle=min(start+half,self.length);end=min(start+block,self.length)
                if middle>start:
                    row[middle-1]=values[middle-1]
                    for index in range(middle-2,start-1,-1):row[index]=values[index]+row[index+1]
                if middle<end:
                    row[middle]=values[middle]
                    for index in range(middle+1,end):row[index]=row[index-1]+values[index]
            self.table.append(row);block*=2
    def range_sum(self,left:int,right:int)->int:
        """返回闭区间 [left,right] 和；非法范围抛出 IndexError。"""
        if left<0 or left>right or right>=self.length:raise IndexError("区间越界")
        if left==right:return self.values[left]
        level=(left^right).bit_length()-1;return self.table[level][left]+self.table[level][right]
if __name__ == "__main__":
    table=DisjointSparseTable([1,2,3,4,5]);assert table.range_sum(1,3)==9 and table.range_sum(0,4)==15 and table.range_sum(2,2)==3;print("008_disjoint_sparse_table: all examples passed")
