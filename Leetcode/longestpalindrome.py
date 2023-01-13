class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        result = ''
        for ind in range(len(s)):
            left = ind
            right = ind
            while left > 0 and right < len(s) - 1:
                if s[left - 1] != s[right + 1]:
                    break
                left -= 1
                right += 1
            str = s[left:right + 1]
            if len(str) > len(result):
                result = str
            left = ind + 1
            right = ind
            while left > 0 and right < len(s) - 1:
                if s[left - 1] != s[right + 1]:
                    break
                left -= 1
                right += 1
            str = s[left:right + 1]
            if len(str) > len(result):
                result = str
        return result

news = Solution()
print(news.longestPalindrome('abba'))