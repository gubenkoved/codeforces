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

    def pick(idx, s_offset):
        if idx == m:
            return 'YES'

        for c in range(l[idx], r[idx] + 1):
            # try to find it the "c" inside the database starting at given offset
            db_idx = s2[s_offset][c] if s_offset < len(s) else None

            if db_idx is None:
                return True

            # recursive dive
            sub_result = pick(idx + 1, db_idx + 1)

            if sub_result is True:
                return True

        return False

    found = pick(0, 0)

    return 'YES' if found else 'NO'


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
