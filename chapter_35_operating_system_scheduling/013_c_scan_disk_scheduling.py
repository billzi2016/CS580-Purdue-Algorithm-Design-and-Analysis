"""
C-SCAN 循环扫描磁盘调度算法。

意图：
- 磁头只按一个方向服务请求，到达末端后跳回另一端继续。
- 相比 SCAN，C-SCAN 给请求更均匀的等待时间。
- 返回访问顺序和总移动距离，包含边界与回卷移动。
"""


def c_scan_disk_scheduling(
    requests: list[int],
    head: int,
    disk_size: int,
    direction: str = "up",
) -> tuple[list[int], int]:
    """执行 C-SCAN 调度。"""

    _validate(requests, head, disk_size, direction)
    lower = sorted(request for request in requests if request < head)
    higher = sorted(request for request in requests if request >= head)

    if direction == "up":
        order = higher + [disk_size - 1, 0] + lower
    else:
        order = list(reversed(lower)) + [0, disk_size - 1] + list(reversed(higher))

    return order, _movement_distance(head, order)


def _movement_distance(head: int, order: list[int]) -> int:
    """计算总移动距离。"""

    total = 0
    current = head
    for target in order:
        total += abs(target - current)
        current = target
    return total


def _validate(requests: list[int], head: int, disk_size: int, direction: str) -> None:
    """检查输入合法性。"""

    if disk_size <= 0:
        raise ValueError("disk_size 必须为正数")
    if not 0 <= head < disk_size:
        raise ValueError("head 必须在磁盘范围内")
    if direction not in {"up", "down"}:
        raise ValueError("direction 必须为 up 或 down")
    if any(request < 0 or request >= disk_size for request in requests):
        raise ValueError("request 超出磁盘范围")


if __name__ == "__main__":
    order, distance = c_scan_disk_scheduling(
        [82, 170, 43, 140, 24, 16, 190], 50, 200, "up"
    )
    assert order == [82, 140, 170, 190, 199, 0, 16, 24, 43]
    assert distance == 391

    down_order, _ = c_scan_disk_scheduling([10, 90], 50, 100, "down")
    assert down_order == [10, 0, 99, 90]

    print("013_c_scan_disk_scheduling: all examples passed")
