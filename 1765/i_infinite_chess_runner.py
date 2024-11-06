import random
import subprocess


for idx in range(100):
    print('round #%d' % idx)
    x0, y0 = random.randint(1, 10 ** 8), random.randint(1, 8)
    x1, y1 = random.randint(1, 10 ** 8), random.randint(1, 8)
    n = random.randint(1, 2000)
    print("n is %d" % n)
    figures = []
    for _ in range(n):
        figures.append(
            (random.choice('KBNRQ'), random.randint(1, 10 ** 8), random.randint(1, 8))
        )

    with open("test.txt", "w") as f:
        f.write("%s %s\n" % (x0, y0))
        f.write("%s %s\n" % (x1, y1))
        f.write("%s\n" % n)
        for t, x, y in figures:
            f.write("%s %s %s\n" % (t, x, y))

    retcode = subprocess.call([
        "bash",
        "-c",
        "cat test.txt | python i_infinite_chess.py"
    ])
    if retcode != 0:
        break
