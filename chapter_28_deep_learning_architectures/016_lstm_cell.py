"""
文件意图：实现手写 LSTM 单元的门控状态递推和训练一步。
适用场景：需要比普通 RNN 更长记忆的序列建模。
核心思想：遗忘门、输入门、候选记忆和输出门共同更新 cell state 与 hidden state。
输入输出：输入 (batch,time,input) 序列，返回所有 hidden 与 cell 状态。
时间复杂度：O(batch*time*(input+hidden)*hidden)。空间复杂度：O(batch*time*hidden)。
关键边界：输入维度必须匹配；本基础版为单层、单向 LSTM。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class LSTMCell(torch.nn.Module):
    """将四个门合并为一次线性变换的手写 LSTM。"""

    def __init__(self, input_size: int, hidden_size: int) -> None:
        """初始化门控线性参数；维度必须为正。"""
        super().__init__()
        if input_size <= 0 or hidden_size <= 0:
            raise ValueError("LSTM 维度必须为正")
        self.hidden_size = hidden_size
        self.weight = torch.nn.Parameter(
            torch.randn(input_size + hidden_size, 4 * hidden_size) * 0.1
        )
        self.bias = torch.nn.Parameter(torch.zeros(4 * hidden_size))

    def forward(self, inputs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """展开 LSTM 并返回全部 hidden 与 cell 状态。

        参数：inputs 形状为 (batch,time,input_size)。返回：(hidden_sequence,cell_sequence)。
        边界情况：非三维或特征维不匹配抛出 ValueError。
        关键算法点：门顺序为 input、forget、output、candidate，cell 使用逐元素门控累积。
        """
        if (
            inputs.ndim != 3
            or inputs.shape[2] != self.weight.shape[0] - self.hidden_size
        ):
            raise ValueError("inputs 形状不匹配")
        batch, time, _ = inputs.shape
        hidden = torch.zeros((batch, self.hidden_size), dtype=inputs.dtype)
        cell = torch.zeros_like(hidden)
        hidden_states = []
        cell_states = []
        for index in range(time):
            gates = (
                torch.cat((inputs[:, index, :], hidden), dim=1) @ self.weight
                + self.bias
            )
            input_gate, forget_gate, output_gate, candidate = torch.chunk(
                gates, 4, dim=1
            )
            cell = torch.sigmoid(forget_gate) * cell + torch.sigmoid(
                input_gate
            ) * torch.tanh(candidate)
            hidden = torch.sigmoid(output_gate) * torch.tanh(cell)
            hidden_states.append(hidden)
            cell_states.append(cell)
        return torch.stack(hidden_states, 1), torch.stack(cell_states, 1)

    def training_step(
        self, inputs: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """以 hidden 序列 MSE 完成 BPTT 与手写 SGD 更新。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")
        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()
        hidden, _ = self.forward(inputs)
        if hidden.shape != target.shape:
            raise ValueError("target 形状不匹配")
        loss = torch.mean((hidden - target) ** 2)
        loss.backward()
        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad
        return float(loss.detach())


if __name__ == "__main__":
    cell = LSTMCell(2, 3)
    data = torch.randn((2, 4, 2))
    hidden, states = cell(data)
    assert hidden.shape == states.shape == (2, 4, 3)
    before = cell.weight.detach().clone()
    assert cell.training_step(data, torch.zeros_like(hidden), 0.01) >= 0.0
    assert not torch.equal(before, cell.weight.detach())
    print("016_lstm_cell: all examples passed")
