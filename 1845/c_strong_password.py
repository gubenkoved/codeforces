import sys


def solve_one(s, m, l, r):
    # preprocess s by creating an array of the same size
    # which contains array of size 10 corresponding to indexes of each number
    # after the

    s2 = [[None] * 10 for _ in range(len(s))]
    next_positions = [None] * 10

    for idx in range(len(s) - 1, -1, -1):
        x = int(s[idx])
        next_positions[x] = idx
        s2[idx] = list(next_positions)

    l = [int(x) for x in l]
    r = [int(x) for x in r]

    # greedily pick the number which cuts biggest amount of "database"
    db_offset = 0
    for idx in range(m):
        if db_offset >= len(s):
            return 'YES'
        max_db_offset = None
        for c in range(l[idx], r[idx] + 1):
            cur_db_offset = s2[db_offset][c]
            if cur_db_offset is None:
                return 'YES'
            max_db_offset = (
                max(max_db_offset, cur_db_offset)
                if max_db_offset is not None else cur_db_offset
            )
        db_offset = max_db_offset + 1

    return 'NO'


def solve():
    t = int(sys.stdin.readline())

    for _  in range(t):
        s = sys.stdin.readline().rstrip()
        m = int(sys.stdin.readline())
        l = sys.stdin.readline().rstrip()
        r = sys.stdin.readline().rstrip()

        sys.stdout.write(solve_one(s, m, l, r))
        sys.stdout.write('\n')


if __name__ == '__main__':
    solve()
