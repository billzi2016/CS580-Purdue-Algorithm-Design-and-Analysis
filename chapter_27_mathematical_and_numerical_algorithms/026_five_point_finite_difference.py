"""
五点有限差分：用对称五点模板近似一阶导数和二阶导数。

意图：展示高阶中心差分如何通过更多函数采样点降低截断误差。输入是单变量
函数、待求导位置和步长，输出该点的一阶或二阶导数近似值。

适用场景：函数在 x 附近足够光滑，并且可以计算 x - 2h 到 x + 2h 的函数值。
边界情况：步长必须为正；如果函数在采样点不可定义，应由调用方选择合适区间。

时间复杂度：O(1)，每次只评估固定 5 个采样点。
空间复杂度：O(1)。
"""


def five_point_first_derivative(function, x_value: float, step: float) -> float:
    """用五点中心差分近似一阶导数。

    参数：
        function: 单变量实函数。
        x_value: 求导位置。
        step: 正步长 h。

    返回：
        f'(x_value) 的四阶精度近似。

    关键算法点：
        模板 (-f(x+2h)+8f(x+h)-8f(x-h)+f(x-2h))/(12h) 会抵消
        Taylor 展开中的低阶误差项，因此比普通中心差分更精确。
    """

    if step <= 0:
        raise ValueError("step 必须为正数")
    return (
        -function(x_value + 2 * step)
        + 8 * function(x_value + step)
        - 8 * function(x_value - step)
        + function(x_value - 2 * step)
    ) / (12 * step)


def five_point_second_derivative(function, x_value: float, step: float) -> float:
    """用五点中心差分近似二阶导数。

    参数：
        function: 单变量实函数。
        x_value: 求二阶导的位置。
        step: 正步长 h。

    返回：
        f''(x_value) 的四阶精度近似。

    关键算法点：
        模板 (-f(x+2h)+16f(x+h)-30f(x)+16f(x-h)-f(x-2h))/(12h^2)
        使用对称采样抵消奇次误差项，并保留二阶导主项。
    """

    if step <= 0:
        raise ValueError("step 必须为正数")
    return (
        -function(x_value + 2 * step)
        + 16 * function(x_value + step)
        - 30 * function(x_value)
        + 16 * function(x_value - step)
        - function(x_value - 2 * step)
    ) / (12 * step * step)


if __name__ == "__main__":

    def cubic(x_value: float) -> float:
        return x_value**3

    def quartic(x_value: float) -> float:
        return x_value**4

    assert round(five_point_first_derivative(cubic, 2.0, 1e-3), 6) == 12.0
    assert round(five_point_second_derivative(cubic, 2.0, 1e-3), 6) == 12.0
    assert round(five_point_first_derivative(quartic, 1.5, 1e-3), 6) == 13.5
    assert round(five_point_second_derivative(quartic, 1.5, 1e-3), 6) == 27.0
    try:
        five_point_first_derivative(cubic, 1.0, 0.0)
        raise AssertionError("step=0 应触发异常")
    except ValueError:
        pass

    print("026_five_point_finite_difference: all examples passed")
