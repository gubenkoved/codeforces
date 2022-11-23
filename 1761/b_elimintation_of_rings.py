import sys

f = sys.stdin
output = sys.stdout

n = int(f.readline())


def solve(a):
    if len(a) <= 2:
        return len(a)

    counts = {}
    for x in a:
        if x not in counts:
            counts[x] = 0
        counts[x] += 1

    if len(counts) > 2:
        return len(a)
    return len(a) // 2 + 1


for _ in range(n):
    k = int(f.readline())
    ans = solve([int(x) for x in f.readline().split(' ')])
    output.write(str(ans) + '\n')

f.close()
output.close()
