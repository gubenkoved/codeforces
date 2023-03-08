import sys


def solve(a, b, w, h, n):
    # go via all pairs and maintain possible shift of the belt to the left
    # and to the right side -- we will call it "left" and "right" respectively
    # every time we update left/right vars and solution exists if left <= right
    # and every next cake can be position using the allowed shifts

    # for the first cake position the dispenser on the center
    a_offset, b_offset = a[0], b[0]

    # we can now move belt in both directions equally
    delta = w - h
    left, right = -delta, +delta

    for idx in range(1, n):
        a_cur, b_cur = a[idx] - a_offset, b[idx] - b_offset

        # calculate distances from left side of the icing to the left side
        # of the cake, same for the right side
        # update possible left/right offsets
        left_cur = (a_cur - w) - (b_cur - h)
        right_cur = (a_cur + w) - (b_cur + h)

        left = max(left, left_cur)
        right = min(right, right_cur)

    return left <= right


if __name__ == '__main__':
    input = sys.stdin
    output = sys.stdout

    t = int(input.readline())

    for _ in range(t):
        n, w, h = [int(x) for x in input.readline().split(' ')]
        a = [int(x) for x in input.readline().split(' ')]
        b = [int(x) for x in input.readline().split(' ')]

        works = solve(a, b, w, h, n)
        output.write('YES' if works else 'NO')
        output.write('\n')
