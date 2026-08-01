"""
文件意图：实现基础版 Seq2Seq encoder-decoder 结构及其训练一步。
适用场景：序列到序列映射，如简单翻译、摘要或时间序列转写。
核心思想：编码器先把输入序列压缩为最终隐状态，解码器再以该状态为初始记忆逐步生成输出。
输入输出：输入源序列和目标序列均为 (batch,time,feature) 张量，输出预测序列。
时间复杂度：O(batch*(src_time+tgt_time)*(input_size+hidden_size)*hidden_size)。
空间复杂度：O(batch*(src_time+tgt_time)*hidden_size)。
关键边界情况：源序列和目标序列都必须是三维张量；本基础版仅实现单层单向 RNN。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class Seq2SeqEncoderDecoder(torch.nn.Module):
    """手写单层 RNN 编码器与解码器。"""

    def __init__(self, input_size: int, hidden_size: int, output_size: int) -> None:
        """初始化编码器、解码器及输出映射参数。"""
        super().__init__()
        if input_size <= 0 or hidden_size <= 0 or output_size <= 0:
            raise ValueError("所有维度都必须为正")

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.encoder_weight = torch.nn.Parameter(
            torch.randn(input_size + hidden_size, hidden_size) * 0.1
        )
        self.encoder_bias = torch.nn.Parameter(torch.zeros(hidden_size))

        self.decoder_weight = torch.nn.Parameter(
            torch.randn(output_size + hidden_size, hidden_size) * 0.1
        )
        self.decoder_bias = torch.nn.Parameter(torch.zeros(hidden_size))

        self.output_weight = torch.nn.Parameter(
            torch.randn(hidden_size, output_size) * 0.1
        )
        self.output_bias = torch.nn.Parameter(torch.zeros(output_size))

    def encode(self, source: torch.Tensor) -> torch.Tensor:
        """编码源序列，返回最终 hidden state。"""
        if source.ndim != 3 or source.shape[2] != self.input_size:
            raise ValueError("source 形状必须为 (batch,time,input_size)")

        batch_size = source.shape[0]
        hidden = torch.zeros(
            (batch_size, self.hidden_size), dtype=source.dtype, device=source.device
        )

        for step_index in range(source.shape[1]):
            combined = torch.cat((source[:, step_index, :], hidden), dim=1)
            hidden = torch.tanh(combined @ self.encoder_weight + self.encoder_bias)

        return hidden

    def decode(self, target_inputs: torch.Tensor, initial_hidden: torch.Tensor) -> torch.Tensor:
        """以 teacher forcing 方式解码目标序列。"""
        if target_inputs.ndim != 3 or target_inputs.shape[2] != self.output_size:
            raise ValueError("target_inputs 形状必须为 (batch,time,output_size)")
        if initial_hidden.shape != (target_inputs.shape[0], self.hidden_size):
            raise ValueError("initial_hidden 形状不匹配")

        hidden = initial_hidden
        predictions: list[torch.Tensor] = []

        for step_index in range(target_inputs.shape[1]):
            decoder_input = torch.cat((target_inputs[:, step_index, :], hidden), dim=1)
            hidden = torch.tanh(decoder_input @ self.decoder_weight + self.decoder_bias)
            predictions.append(hidden @ self.output_weight + self.output_bias)

        return torch.stack(predictions, dim=1)

    def forward(self, source: torch.Tensor, target_inputs: torch.Tensor) -> torch.Tensor:
        """先编码再解码，返回整个输出序列。"""
        context = self.encode(source)
        return self.decode(target_inputs, context)

    def training_step(
        self,
        source: torch.Tensor,
        target_inputs: torch.Tensor,
        expected_outputs: torch.Tensor,
        learning_rate: float,
    ) -> float:
        """执行一次 Seq2Seq 训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        predicted = self.forward(source, target_inputs)
        if predicted.shape != expected_outputs.shape:
            raise ValueError("expected_outputs 形状必须与预测输出一致")

        loss = torch.mean((predicted - expected_outputs) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(11)

    model = Seq2SeqEncoderDecoder(3, 5, 2)
    source_sequence = torch.randn((2, 4, 3))
    decoder_inputs = torch.randn((2, 3, 2))
    predictions = model(source_sequence, decoder_inputs)
    assert predictions.shape == (2, 3, 2)

    encoded = model.encode(torch.zeros((1, 2, 3)))
    assert encoded.shape == (1, 5)

    previous_output_weight = model.output_weight.detach().clone()
    loss_value = model.training_step(
        source_sequence,
        decoder_inputs,
        torch.zeros_like(predictions),
        0.01,
    )
    assert loss_value >= 0.0
    assert not torch.equal(previous_output_weight, model.output_weight.detach())

    print("018_seq2seq_encoder_decoder: all examples passed")
