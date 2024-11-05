import sys
import heapq

input = sys.stdin
# input = open('/home/eugene/src/codeforces/1765/test.txt')

x0, y0 = [int(x) for x in input.readline().split(' ')]
x1, y1 = [int(x) for x in input.readline().split(' ')]
n = int(input.readline())
figures = []
for _ in range(n):
    type, x, y = input.readline().split(' ')
    figures.append((type, int(x), int(y)))

# overall idea is as follows
# find interesting ranges by "y"
# compress non intresting parts
# figure out which squares are beaten inside the all interesting places and
# compressed as well
# run reguar dijkstra to find the path

# spacing should probably be 16 or even 17
spacing = 16
interesting_x = [x for _, x, _ in figures] + [x0, x1]
ranges_heap = []
for x in interesting_x:
    heapq.heappush(ranges_heap, (x - spacing, False))
    heapq.heappush(ranges_heap, (x + spacing, True))

merged_interesting_ranges = []
counter = 0
start = None
while ranges_heap:
    x, is_end = heapq.heappop(ranges_heap)
    if not is_end:
        counter += 1
        start = x
    else:
        counter -= 1
        if counter == 0:
            merged_interesting_ranges.append((start, x))

# all x coordiates which are not interesting are join into a single column
# in the transofrmed board (compressed) and we need to capture how much they
# compress
real_x_to_compressed_map = {}
compressed = []  # column by column representaion of compressed field
last_x_end = None
speedline_x = {}  # compressed column index -> amount of compressed columns
for x_start, x_end in merged_interesting_ranges:
    if last_x_end is not None:
        # add special speedline column
        compressed_x = len(compressed)
        skip_counter = x_start - last_x_end - 1
        if skip_counter > 0:
            speedline_x[compressed_x] = skip_counter
            compressed.append([None] * 8)
    for x in range(x_start, x_end + 1):
        compressed_x = len(compressed)
        real_x_to_compressed_map[x] = compressed_x
        compressed.append([None] * 8)
    last_x_end = x_end

# put figures into the compressed board
figures_compressed = []
for type, x, y in figures:
    compressed_x = real_x_to_compressed_map[x]
    compressed[compressed_x][y - 1] = type
    figures_compressed.append((type, compressed_x, y - 1))

# convert the starting and target points
x_start, y_start = real_x_to_compressed_map[x0], y0 - 1
x_target, y_target = real_x_to_compressed_map[x1], y1 - 1

beaten = set()
k = len(compressed)

# traces ray until we either rach side of the field OR we hit another figure
def trace(x, y, dx, dy):
    xc, yc = x, y
    while True:
        xc, yc = xc + dx, yc + dy
        if xc < 0 or xc >= k:
            break
        if yc < 0 or yc >= 8:
            break
        if compressed[xc][yc] is not None:
            break
        beaten.add((xc, yc))

# trace beaten fields (compressed coordinates)
for type, x, y in figures_compressed:
    # consider place of the figure also beaten as we can not capture
    beaten.add((x, y))

    if type == 'K':
        for dx in range(-1, +2):
            for dy in range(-1, +2):
                beaten.add((x + dx, y + dy))
    elif type == 'B':
        trace(x, y, +1, +1)
        trace(x, y, +1, -1)
        trace(x, y, -1, +1)
        trace(x, y, -1, -1)
    elif type == "N":
        beaten.add((x + 1, y + 2))
        beaten.add((x + 1, y - 2))
        beaten.add((x - 1, y + 2))
        beaten.add((x - 1, y - 2))

        beaten.add((x + 2, y + 1))
        beaten.add((x + 2, y - 1))
        beaten.add((x - 2, y + 1))
        beaten.add((x - 2, y - 1))
    elif type == "R":
        trace(x, y, +1, 0)
        trace(x, y, -1, 0)
        trace(x, y, 0, +1)
        trace(x, y, 0, -1)
    elif type == "Q":
        trace(x, y, +1, 0)
        trace(x, y, -1, 0)
        trace(x, y, 0, +1)
        trace(x, y, 0, -1)
        trace(x, y, +1, +1)
        trace(x, y, +1, -1)
        trace(x, y, -1, +1)
        trace(x, y, -1, -1)
    else:
        assert False, "what?"

# now finally run dijkstra, considering speedlines can only be crossed w/o turns and they cost
# more than 1 but amount of skipped columns it encodes
visited = set()
# heap = [(0, x_start, y_start, None, None)]
heap = [(0, x_start, y_start)]
distance_map = {}
# prev = {}

while heap:
    # distance, x, y, prev_x, prev_y = heapq.heappop(heap)
    distance, x, y = heapq.heappop(heap)
    if (x, y) in visited:
        continue
    visited.add((x, y))
    distance_map[(x, y)] = distance
    # prev[(x, y)] = (prev_x, prev_y)
    if (x, y) == (x_target, y_target):
        break
    neighbor_candidates = [
        (x - 1, y - 1),
        (x - 1, y + 0),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y + 0),
        (x + 1, y + 1),
    ]
    for neighbor_x, neighbor_y in neighbor_candidates:
        if neighbor_x < 0 or neighbor_x >= k:
            continue
        if neighbor_y < 0 or neighbor_y >= 8:
            continue
        if (neighbor_x, neighbor_y) in visited:
            continue
        if (neighbor_x, neighbor_y) in beaten:
            continue
        cost = 1
        if neighbor_x in speedline_x:
            cost = speedline_x[neighbor_x]
        heapq.heappush(
            heap,
            # (distance + cost, neighbor_x, neighbor_y, x, y)
            (distance + cost, neighbor_x, neighbor_y)
        )

if (x_target, y_target) in distance_map:
    print(distance_map[(x_target, y_target)])

    # trace back
    # path = []
    # cur = (x_target, y_target)
    # while cur[0] is not None:
    #     path.append(cur)
    #     cur = prev[cur]
    # print('path: %s' % ' -> '.join('(%s, %s)' % (x, y) for x, y in reversed(path)))
else:
    print(-1)
