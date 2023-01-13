def compare(a, b):
    if a[0] != b[0]:
        return a[0] < b[0]
    return a[1] < b[1]

def sort(lst):
    sort(lst, compare)

def binarysearch(lst, val):
    low = 0
    high = len(lst) - 1
    ans = -1
    while low <= high:
        mid = (low + high)//2
        if valid(mid):
            left = mid + 1
            ans = mid
        else:
            right = mid - 1
    return ans

def valid(val):
    return True

[True, True, True, True, False, False, False, False]