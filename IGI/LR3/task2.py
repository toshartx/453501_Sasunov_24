def solve_task2(nums) -> int:
    nums_in_range: int = 0
    for num in nums:
        if num in range(5, 25):
            nums_in_range += 1
    return nums_in_range
