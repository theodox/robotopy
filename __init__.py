from motors import left_front, right_front, left_rear, right_rear, FORWARD

import time


if __name__ == '__main__':
    for m in left_rear, right_rear, right_front, left_front:
        m.set_speed(0.5)
        m.run(FORWARD)

    time.sleep(4)
