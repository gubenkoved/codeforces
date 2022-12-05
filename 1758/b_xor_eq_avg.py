import sys


def solve(n):
    if n % 2 == 1:
        return [1] * n
    else:
        # [3, 1] -> 2
        # [5, 1, 5, 5] -> 4
        #   [1 + 4, 1, 1, 1] -> xor 4, avg 2
        # [6 + 1, 1, 1, 1, 1, 1] -> xor 6, avg 2,
        #   [7, 1, 7, 7, 7, 7]
        # [8 + 1, 1, 1, 1, 1, 1, 1, 1] -> xor 8, avg 2
        #   need to inc avg by (n - 2) * n via n - 2 members
        #   so every member starting with 3rd one should increase by
        #   (n - 2) * n / (n - 2) = n
        # so we have the sequence as follows:
        # [n + 1, 1, n + 1, n + 1, ..., n + 1]
        return [n + 1, 1] + [n + 1] * (n - 2)


if __name__ == '__main__':
    input = sys.stdin
    output = sys.stdout

    num_of_tests = int(input.readline())

    for _ in range(num_of_tests):
        a = solve(int(input.readline()))
        a = [str(x) for x in a]
        output.write(' '.join(a) + '\n')
