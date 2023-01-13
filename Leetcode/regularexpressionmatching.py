class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        return recur(s, p)

def recur(s, p):
    if not s and not p:
        return True
    if not s and len(p) >= 2 and p[1] == '*':
        return recur(s, p[2:])
    if not s or not p:
        return False
    if s[0] == p[0]:
        if len(p) == 1 or (len(p) >= 2 and p[1] != '*'):
            return recur(s[1:], p[1:])
        if recur(s, p[2:]):
            return True
        pointer = 0
        while pointer < len(s) and s[pointer] == p[0]:
            if recur(s[pointer + 1:], p[2:]):
                return True
            pointer += 1
        return False
    if s[0] != p[0] and p[0] != '.' and len(p) >= 2 and p[1] == '*':
        return recur(s, p[2:])
    if p[0] == '.':
        if len(p) == 1:
            if len(s) == 1:
                return True
            return False
        if p[1] != '*':
            return recur(s[1:], p[1:])
        for i in range(len(s) + 1):
            if recur(s[i:], p[2:]):
                return True
        return False
    return False


news = Solution()

print(news.isMatch('aab', 'c*a*b'))