import sys


def solve(s):
    count = 0
    n = len(s)

    for i in range(0, n):
        freq_map = {s[i]: 1}
        max_freq = 1
        unique_count = 1

        # add for the case where the number is simply s[i] itself
        # which is always diverse
        count += 1

        for j in range(i + 1, n):
            c = s[j]

            # add a number
            if c not in freq_map:
                freq_map[c] = 0
                unique_count += 1
            freq_map[c] += 1
            max_freq = max(max_freq, freq_map[c])

            if max_freq > 10:
                break

            is_diverse = max_freq <= unique_count
            if is_diverse:
                count += 1

    return count


if __name__ == '__main__':
    input = sys.stdin
    output = sys.stdout

    num_of_tests = int(input.readline())

    for _ in range(num_of_tests):
        _ = input.readline()
        sol = solve(input.readline().strip())
        output.write(str(sol) + '\n')
