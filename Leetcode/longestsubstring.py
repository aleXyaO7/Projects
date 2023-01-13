class Solution(object):
    def lengthOfLongestSubstring(self, s):
        maximum = 0
        cur = ''
        for i in s:
            if i in cur:
                ind = cur.index(i)
                if len(cur) > maximum:
                    maximum = len(cur)
                cur = cur[ind + 1:]
            cur = ''.join([cur, i])
        if len(cur) > maximum:
            maximum = len(cur)
        return maximum

news = Solution()
print(news.lengthOfLongestSubstring(' '))