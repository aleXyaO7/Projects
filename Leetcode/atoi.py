class Solution(object):
    def myAtoi(self, s):
        """
        :type s: str
        :rtype: int
        """
        t = s.strip()
        result = ''
        pointer = 0
        if t[0] == '-':
            result += '-'
            pointer += 1
        elif t[0] == '+':
            pointer += 1
        while pointer < len(t):
            if t[pointer] in '0123456789':
                result += t[pointer]
            else: break
            pointer += 1
        if not result or result[-1] == '-':
            return 0
        n = int(result)
        if n < -2147483648:
            return -2147483648
        if n > 2147483647:
            return 2147483647
        return n
        


news = Solution()
print(news.myAtoi('         -42'))