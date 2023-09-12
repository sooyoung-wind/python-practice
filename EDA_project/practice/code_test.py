from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        stack = []
        answer = []
        nums.sort()
        
        for num in nums:
            if stack and stack[-1] == num:
                continue
            
            if stack and stack[-1]+1 != num:
                answer.append(len(stack))
                stack = []
                
            stack.append(num)
                
        return max(answer)
            
            
s = Solution()
# print(s.longestConsecutive(nums = [100,4,200,1,3,2]))

print(s.longestConsecutive(nums = [0,3,7,2,5,8,4,6,0,1]))