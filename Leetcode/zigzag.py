class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        if numRows == 1: return s
        result = ''
        zigzag = []
        for i in range(numRows):
            zigzag.append([])
        dire = True
        pointer = 0
        for i in s:
            zigzag[pointer].append(i)
            if dire == True: pointer += 1
            else: pointer -= 1
            if pointer == 0 or pointer == numRows - 1:
                dire = not dire
        for i in zigzag:
            result += ''.join(i)
        return result

news = Solution()
print(news.convert("PAYPALISHIRING", 3))