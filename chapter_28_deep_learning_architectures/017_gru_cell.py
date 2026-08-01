"""
文件意图：实现手写 GRU 单元的门控递推与训练一步。
适用场景：需要比普通 RNN 更稳定地保留长期信息的序列建模任务。
核心思想：用更新门控制旧状态保留比例，用重置门控制候选状态对历史信息的读取强度。
输入输出：输入形状为 (batch,time,input_size) 的序列，输出所有时间步的 hidden state。
时间复杂度：O(batch*time*(input_size+hidden_size)*hidden_size)。
空间复杂度：O(batch*time*hidden_size)。
关键边界情况：输入必须是三维张量；本基础版只支持单层单向 GRU。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class GRUCell(torch.nn.Module):
    """手写展开的单层 GRU。"""

    def __init__(self, input_size: int, hidden_size: int) -> None:
        """初始化更新门、重置门和候选状态参数。"""
        super().__init__()
        if input_size <= 0 or hidden_size <= 0:
            raise ValueError("GRU 维度必须为正")

        self.input_size = input_size
        self.hidden_size = hidden_size

        self.gate_weight = torch.nn.Parameter(
            torch.randn(input_size + hidden_size, 2 * hidden_size) * 0.1
        )
        self.gate_bias = torch.nn.Parameter(torch.zeros(2 * hidden_size))
        self.candidate_input_weight = torch.nn.Parameter(
            torch.randn(input_size, hidden_size) * 0.1
        )
        self.candidate_hidden_weight = torch.nn.Parameter(
            torch.randn(hidden_size, hidden_size) * 0.1
        )
        self.candidate_bias = torch.nn.Parameter(torch.zeros(hidden_size))

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """展开整个 GRU 序列并返回所有 hidden state。

        参数：`inputs` 的形状为 `(batch, time, input_size)`。
        返回值：形状为 `(batch, time, hidden_size)` 的 hidden state 序列。
        边界情况：当输入维度不匹配时抛出 `ValueError`。
        关键算法点：先算更新门与重置门，再用重置门筛选旧 hidden 后构造候选状态。
        """
        if inputs.ndim != 3:
            raise ValueError("inputs 必须是三维张量")
        if inputs.shape[2] != self.input_size:
            raise ValueError("inputs 的最后一维必须等于 input_size")

        batch_size, time_steps, _ = inputs.shape
        hidden = torch.zeros(
            (batch_size, self.hidden_size), dtype=inputs.dtype, device=inputs.device
        )
        hidden_states: list[torch.Tensor] = []

        for step_index in range(time_steps):
            current_input = inputs[:, step_index, :]

            # 门控线性项依赖当前输入和上一时刻 hidden。
            gate_input = torch.cat((current_input, hidden), dim=1)
            gate_values = gate_input @ self.gate_weight + self.gate_bias
            update_gate, reset_gate = torch.chunk(torch.sigmoid(gate_values), 2, dim=1)

            # 候选状态只允许被重置门筛选后的历史信息参与。
            candidate = torch.tanh(
                current_input @ self.candidate_input_weight
                + (reset_gate * hidden) @ self.candidate_hidden_weight
                + self.candidate_bias
            )

            # 更新门越大，越倾向于直接保留旧状态。
            hidden = update_gate * hidden + (1.0 - update_gate) * candidate
            hidden_states.append(hidden)

        return torch.stack(hidden_states, dim=1)

    def training_step(
        self, inputs: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """执行一次 BPTT 和手写 SGD 更新。

        参数：`inputs` 为输入序列，`target` 为目标 hidden 序列，`learning_rate` 为学习率。
        返回值：当前批次的均方误差损失。
        边界情况：学习率非正或 target 形状不匹配时抛出 `ValueError`。
        关键算法点：使用 autograd 计算跨时间步梯度，但参数更新步骤显式手写。
        """
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        predicted = self.forward(inputs)
        if predicted.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")

        loss = torch.mean((predicted - target) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(7)

    gru = GRUCell(3, 4)
    example_inputs = torch.randn((2, 5, 3))
    outputs = gru(example_inputs)
    assert outputs.shape == (2, 5, 4)

    zero_outputs = GRUCell(3, 4)(torch.zeros((1, 3, 3)))
    assert zero_outputs.shape == (1, 3, 4)

    previous_gate_weight = gru.gate_weight.detach().clone()
    previous_candidate_weight = gru.candidate_input_weight.detach().clone()
    loss_value = gru.training_step(example_inputs, torch.zeros_like(outputs), 0.01)
    assert loss_value >= 0.0
    assert not torch.equal(previous_gate_weight, gru.gate_weight.detach())
    assert not torch.equal(
        previous_candidate_weight, gru.candidate_input_weight.detach()
    )

    print("017_gru_cell: all examples passed")
