"""
SCAN 电梯磁盘调度算法。

意图：
- 磁头沿一个方向服务请求，直到边界后反向。
- 减少 FCFS 可能产生的大幅来回寻道。
- 返回访问顺序和总寻道距离。
"""


def scan_disk_scheduling(
    requests: list[int],
    head: int,
    disk_size: int,
    direction: str = "up",
) -> tuple[list[int], int]:
    """执行 SCAN 调度，direction 为 'up' 或 'down'。"""

    _validate(requests, head, disk_size, direction)
    lower = sorted(request for request in requests if request < head)
    higher = sorted(request for request in requests if request >= head)

    if direction == "up":
        order = higher + ([disk_size - 1] if higher else []) + list(reversed(lower))
    else:
        order = list(reversed(lower)) + ([0] if lower else []) + higher

    distance = _movement_distance(head, order)
    # 边界不是原始请求时只作为转向点保留；这符合 SCAN 的机械移动语义。
    return order, distance


def _movement_distance(head: int, order: list[int]) -> int:
    """计算磁头按 order 移动的总距离。"""

    distance = 0
    current = head
    for target in order:
        distance += abs(target - current)
        current = target
    return distance


def _validate(requests: list[int], head: int, disk_size: int, direction: str) -> None:
    """检查磁盘柱面输入。"""

    if disk_size <= 0:
        raise ValueError("disk_size 必须为正数")
    if not 0 <= head < disk_size:
        raise ValueError("head 必须在磁盘范围内")
    if direction not in {"up", "down"}:
        raise ValueError("direction 必须为 up 或 down")
    if any(request < 0 or request >= disk_size for request in requests):
        raise ValueError("request 超出磁盘范围")


if __name__ == "__main__":
    order, distance = scan_disk_scheduling([82, 170, 43, 140, 24, 16, 190], 50, 200, "up")
    assert order == [82, 140, 170, 190, 199, 43, 24, 16]
    assert distance == 332

    down_order, _ = scan_disk_scheduling([10, 90], 50, 100, "down")
    assert down_order == [10, 0, 90]

    print("012_scan_disk_scheduling: all examples passed")
