"""文件意图：手写懒标记线段树。适用场景：区间加与区间和。核心思想：整段更新先记录 lazy，必要时才下推。输入输出：支持 range_add 与 range_sum。每操作 O(log n)，空间 O(n)。关键边界：半开区间，空区间可查询或更新。"""
class LazySegmentTree:
    """使用递归区间的区间加、区间和线段树。"""
    def __init__(self, values: list[int]) -> None:
        """按 values 构建；空数组合法。"""
        self.length = len(values); self.sum = [0] * max(1, 4 * self.length); self.lazy = [0] * max(1, 4 * self.length)
        if values: self._build(1, 0, self.length, values)
    def _build(self, node: int, left: int, right: int, values: list[int]) -> None:
        if right - left == 1: self.sum[node] = values[left]; return
        middle = (left + right) // 2; self._build(2*node,left,middle,values); self._build(2*node+1,middle,right,values); self.sum[node] = self.sum[2*node]+self.sum[2*node+1]
    def _apply(self,node:int,left:int,right:int,delta:int)->None: self.sum[node]+=delta*(right-left); self.lazy[node]+=delta
    def _push(self,node:int,left:int,right:int)->None:
        if self.lazy[node] and right-left>1:
            middle=(left+right)//2; self._apply(2*node,left,middle,self.lazy[node]); self._apply(2*node+1,middle,right,self.lazy[node]); self.lazy[node]=0
    def range_add(self, query_left: int, query_right: int, delta: int) -> None:
        """给半开区间加 delta；非法范围抛出 IndexError。"""
        self._check(query_left,query_right)
        def visit(node:int,left:int,right:int)->None:
            if query_right<=left or right<=query_left:return
            if query_left<=left and right<=query_right:self._apply(node,left,right,delta);return
            self._push(node,left,right); middle=(left+right)//2; visit(2*node,left,middle);visit(2*node+1,middle,right);self.sum[node]=self.sum[2*node]+self.sum[2*node+1]
        if self.length: visit(1,0,self.length)
    def range_sum(self, query_left: int, query_right: int) -> int:
        """返回半开区间和；非法范围抛出 IndexError。"""
        self._check(query_left,query_right)
        def visit(node:int,left:int,right:int)->int:
            if query_right<=left or right<=query_left:return 0
            if query_left<=left and right<=query_right:return self.sum[node]
            self._push(node,left,right);middle=(left+right)//2;return visit(2*node,left,middle)+visit(2*node+1,middle,right)
        return visit(1,0,self.length) if self.length else 0
    def _check(self,left:int,right:int)->None:
        if left<0 or left>right or right>self.length:raise IndexError("区间越界")
if __name__ == "__main__":
    tree=LazySegmentTree([1,2,3,4]);tree.range_add(1,4,2);assert tree.range_sum(0,4)==16 and tree.range_sum(1,3)==9
    tree.range_add(0,0,5);assert LazySegmentTree([]).range_sum(0,0)==0;print("006_lazy_segment_tree: all examples passed")
