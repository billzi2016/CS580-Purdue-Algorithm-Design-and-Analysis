"""
Early Stopping：在验证指标长期不提升时提前终止训练。
"""

from dataclasses import dataclass


@dataclass
class EarlyStopping:
    """跟踪最佳验证损失和耐心窗口。"""

    patience: int
    min_delta: float = 0.0
    best_score: float | None = None
    bad_epochs: int = 0

    def update(self, validation_loss: float) -> bool:
        """输入新验证损失；若应停止训练则返回 True。"""

        if self.patience < 0 or self.min_delta < 0:
            raise ValueError("patience 和 min_delta 不能为负数")
        if self.best_score is None or validation_loss < self.best_score - self.min_delta:
            self.best_score = validation_loss
            self.bad_epochs = 0
            return False
        self.bad_epochs += 1
        return self.bad_epochs > self.patience


if __name__ == "__main__":
    stopper = EarlyStopping(patience=2, min_delta=0.01)
    assert not stopper.update(1.0)
    assert not stopper.update(0.95)
    assert not stopper.update(0.951)
    assert not stopper.update(0.952)
    assert stopper.update(0.953)

    print("018_early_stopping: all examples passed")
