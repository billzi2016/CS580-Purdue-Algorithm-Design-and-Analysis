"""
文件意图：实现手写 Elman RNN 单元与跨时间步训练一步。
适用场景：序列特征建模，理解隐藏状态递推和通过时间反向传播（BPTT）。
核心思想：每一步计算 h_t=tanh(x_t W_x+h_{t-1} W_h+b)，最后按目标计算损失并反传。
输入输出：输入 (batch,time,input) 序列和初始状态，返回全部隐藏状态。
时间复杂度：O(batch*time*(input*hidden+hidden^2))。空间复杂度：O(batch*time*hidden)。
关键边界：输入维度必须匹配；本基础单元不含门控、层归一化或截断 BPTT。
"""

import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class RNNCell(torch.nn.Module):
    """使用显式输入与隐藏线性变换的 Elman RNN 单元。"""
    def __init__(self,input_size:int,hidden_size:int)->None:
        """初始化 RNN 参数；两个维度必须为正。"""
        super().__init__()
        if input_size<=0 or hidden_size<=0:raise ValueError("RNN 维度必须为正")
        self.input_weight=torch.nn.Parameter(torch.randn(input_size,hidden_size)*0.1)
        self.hidden_weight=torch.nn.Parameter(torch.randn(hidden_size,hidden_size)*0.1)
        self.bias=torch.nn.Parameter(torch.zeros(hidden_size))
    def forward(self,inputs:torch.Tensor,initial_state:torch.Tensor|None=None)->torch.Tensor:
        """展开序列并返回每个时间步隐藏状态。

        参数：inputs 为 (batch,time,input_size)，initial_state 可为 (batch,hidden_size)。
        返回：(batch,time,hidden_size) 隐藏状态。
        边界情况：空时间维返回对应空输出；形状不匹配抛出 ValueError。
        关键算法点：当前状态依赖前一状态，因此计算图自然连接所有时间步以供 BPTT。
        """
        if inputs.ndim!=3 or inputs.shape[2]!=self.input_weight.shape[0]:raise ValueError("inputs 形状不匹配")
        batch,time,_=inputs.shape
        state=torch.zeros((batch,self.bias.numel()),dtype=inputs.dtype,device=inputs.device) if initial_state is None else initial_state
        if state.shape!=(batch,self.bias.numel()):raise ValueError("initial_state 形状不匹配")
        states=[]
        for index in range(time):
            state=torch.tanh(inputs[:,index,:]@self.input_weight+state@self.hidden_weight+self.bias)
            states.append(state)
        return torch.stack(states,dim=1) if states else torch.empty((batch,0,self.bias.numel()),dtype=inputs.dtype,device=inputs.device)
    def training_step(self,inputs:torch.Tensor,target:torch.Tensor,learning_rate:float)->float:
        """对全部隐藏状态 MSE 执行 BPTT 与手写 SGD。"""
        if learning_rate<=0:raise ValueError("learning_rate 必须为正")
        for parameter in self.parameters():
            if parameter.grad is not None:parameter.grad.zero_()
        output=self.forward(inputs)
        if output.shape!=target.shape:raise ValueError("target 形状不匹配")
        loss=torch.mean((output-target)**2);loss.backward()
        with torch.no_grad():
            for parameter in self.parameters():parameter-=learning_rate*parameter.grad
        return float(loss.detach())

if __name__=="__main__":
    cell=RNNCell(2,3);data=torch.randn((2,4,2));output=cell(data)
    assert output.shape==(2,4,3)
    before=cell.input_weight.detach().clone();assert cell.training_step(data,torch.zeros_like(output),0.01)>=0.0
    assert not torch.equal(before,cell.input_weight.detach())
    print("015_rnn_cell: all examples passed")
