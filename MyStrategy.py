import json
import math

# PRIVET VSEM KTO ETO CHITAET =)

tick = 0
_round = -1


def ButtonMin(pos):
    return min(pos[2][1], pos[3][1])


def RadianInDegree(rad):
    return rad * 180 / math.pi


def InverseCommand(cmd, side):
    if side == 1:
        return cmd
    else:
        return 'right' if cmd == 'left' else 'left'


def InverseX(x, side):
    if side == 1:
        return x
    else:
        return 1200 - x


def KeepAngle(angle, my_car, my_angle_prev, delta=10):
    if (angle - RadianInDegree(my_car[1]) * my_car[2]) > 180:
        angle -= 360
    if (angle - RadianInDegree(my_car[1]) * my_car[2]) < -180:
        angle += 360
    if my_angle + (my_angle - my_angle_prev) * delta > my_car[2] * (math.pi / 180 * angle):
        cmd = 'left'
    else:
        cmd = 'right'
    return cmd


def BusOn2ndFloor(tick, my_car):
    if tick < 30:
        return 'stop'
    if tick > 200:
        global rotate_bus
        rotate_bus = True
        return 'stop'
    if tick > 170:
        return InverseCommand('right', my_car[2])
    if tick > 140:
        return InverseCommand('left', my_car[2])

    if tick > 125:
        return 'stop'
    return InverseCommand('left', my_car[2])


def BusOnHill(tick, my_car):
    if tick < 50:
        return 'stop'
    if tick > 300:
        global rotate_bus
        rotate_bus = True
        return 'stop'
    if tick > 250:
        return 'right' if my_car[2] == 1 else 'left'
    if tick > 200:
        return 'stop'
    return "left" if my_car[2] == 1 else 'right'


def BusOnHubble(tick, my_car, delay=50):
    delay -= 50
    if tick < 50 + delay:
        return 'stop'
    if tick > 270 + delay:
        global rotate_bus
        rotate_bus = True
        return 'stop'
    if tick > 240 + delay:
        return InverseCommand('right', my_car[2])
    if tick > 155 + delay:
        return 'stop'
    return InverseCommand('left', my_car[2])


def BuggyIsland(tick, my_car, my_angle_prev):
    myx = my_pos[-1][0]
    enx = en_pos[-1][0]

    if tick < 44:
        return 'stop'
    cmd = KeepAngle(45, my_car, my_angle_prev)
    if myx < 250:
        cmd = KeepAngle(30, my_car, my_angle_prev)
    if myx > 1000 and myx > enx:
        cmd = KeepAngle(-30, my_car, my_angle_prev)
    return cmd


def BuggyFlatfloor(tick, my_car, my_angle_prev, my_pos, en_pos):
    global dbg
    myx = my_pos[-1][0]
    enx = en_pos[-1][0]
    if tick < 44:
        return 'stop'
    cmd = KeepAngle(45, my_car, my_angle_prev)
    if myx < 250:
        cmd = KeepAngle(30, my_car, my_angle_prev)
    return cmd


def BuggyOnHill(tick, my_car, my_angle_prev, my_pos, en_pos):
    myx = my_pos[-1][0]
    enx = en_pos[-1][0]

    if tick < 15:
        return InverseCommand('right', my_car[2])
    if tick < 66:
        return InverseCommand('left', my_car[2])
    if tick < 155:
        return InverseCommand('right', my_car[2])
    if tick < 270:
        return KeepAngle(-30, my_car, my_angle_prev)
    if tick > 820 and myx > 800 and ButtonMin(my_pos) < ButtonMin(en_pos):
        return InverseCommand('left', my_car[2])

    return KeepAngle(60, my_car, my_angle_prev, 5)


def SqBuggyOn2ndFloor(tick, my_car, my_angle_prev):
    if tick < 30:
        return 'stop'
    if tick < (130 if my_car[2] == 1 else 120):
        return InverseCommand('left', my_car[2])
    if tick > 1500:
        return KeepAngle(62, my_car, my_angle_prev)
    if tick > (180 if my_car[2] == 1 else 150):
        return KeepAngle(65, my_car, my_angle_prev)

    return 'stop'


def SqBuggyFlatFloor(my_car, my_angle_prev, my_pos, en_pos, d_my_pos):
    if tick < 19:
        cmd = 'stop'
    elif tick < 24:
        cmd = InverseCommand('left', my_car[2])
    elif tick < 50:
        cmd = InverseCommand('right', my_car[2])
    elif tick < 100:
        cmd = KeepAngle(10, my_car, my_angle_prev)
    else:
        if my_pos[-1][0] > en_pos[-1][0]:
            global dbg
            dbg += 'my_d_pos:' + str(d_my_pos[-1][0])
            if d_my_pos[-1][0] > 3:
                cmd = 'stop'
            else:
                cmd = KeepAngle(-30, my_car, my_angle_prev)
        else:
            cmd = KeepAngle(20, my_car, my_angle_prev)
    return cmd


def SqBuggyHubbleMap(tick, my_car, my_pos, en_pos, my_angle_prev):
    global dbg
    if tick < 19:
        cmd = 'stop'
    elif tick < 24:
        cmd = InverseCommand('left', my_car[2])
    elif tick < 50:
        cmd = InverseCommand('right', my_car[2])
    elif tick < 150:
        cmd = KeepAngle(10, my_car, my_angle_prev)
    else:
        if my_pos[-1][0] > en_pos[-1][0]:  # vrag pereletel menya
            cmd = KeepAngle(-60, my_car, my_angle_prev)
        else:  # vse norm
            if my_pos[-1][0] < 500:
                cmd = KeepAngle(30, my_car, my_angle_prev)
            elif my_pos[-1][0] > 700:
                if my_pos[-1][0] - en_pos[-1][0] > 200:
                    cmd = KeepAngle(-30, my_car, my_angle_prev)
                else:
                    cmd = KeepAngle(30, my_car, my_angle_prev)
            else:
                cmd = KeepAngle(65, my_car, my_angle_prev)
        if tick > 850 and min(my_pos[2][1], my_pos[3][1]) < min(en_pos[2][1], en_pos[3][1]):
            if my_pos[-1][0] < 600 and en_pos[-1][0] < 600 and my_pos[-1][0] < en_pos[-1][0]:  # mi vdvoem na moey polovine, ya levee
                cmd = KeepAngle(-30, my_car, my_angle_prev)
                dbg += 'deadline esc p1 '
            elif my_pos[-1][0] > 600 and en_pos[-1][0] > 600 and my_pos[-1][0] > en_pos[-1][0]:  # mi vdvoem na vrazheskoy polovine, ya pravee
                cmd = KeepAngle(30, my_car, my_angle_prev)
                dbg += 'deadline esc p2 '
            elif my_pos[-1][0] < 600 and en_pos[-1][0] < 600 and my_pos[-1][0] > en_pos[-1][0]:  # mi vdvoem na moey polovine, ya pravee
                cmd = KeepAngle(30, my_car, my_angle_prev)
                dbg += 'deadline esc p3 '
            elif my_pos[-1][0] > 600 and en_pos[-1][0] > 600 and my_pos[-1][0] < en_pos[-1][0]:  # mi vdvoem na vrazheskoy polovine, ya levee
                cmd = KeepAngle(-30, my_car, my_angle_prev)
                dbg += 'deadline esc p4 '
    return cmd


def SqBuggyIslholeeMap(tick, my_car):
    if my_car[2] == 1:
        if tick < 6:
            cmd = 'stop'
        elif tick < 17:
            cmd = InverseCommand('right', my_car[2])
        elif tick < 46:
            cmd = InverseCommand('left', my_car[2])
        elif tick < 79:
            cmd = InverseCommand('right', my_car[2])
        elif tick < 83:
            cmd = 'stop'
        elif tick < 105:
            cmd = InverseCommand('right', my_car[2])
        elif tick < 430:
            cmd = KeepAngle(63, my_car, my_angle_prev)
        else:
            cmd = KeepAngle(75, my_car, my_angle_prev)
        return cmd


def Dobivka(cmd, my_pos, en_pos):
    myx = my_pos[-1][0]
    enx = en_pos[-1][0]
    myy = my_pos[-1][1]
    eny = en_pos[-1][1]
    global dbg
    if (abs(myx - enx) < 80  # mi na odnom x
            and myy > eny + 40  # ya nad vragom
            and myy - 280 < eny  # ya ne na drugom etazhe
            and 60 > RadianInDegree(my_car[2] * my_car[1]) > -45  # ya ne ubyus pri stope esli ya vverh nogami
    ):
        cmd = 'stop'
        dbg += 'dobivka'
    return cmd


def CoordShift(x0, y0, xi, yi, ang, ismy=True):
    if ismy:
        xin = x0 + xi * math.cos(ang) - yi * math.sin(ang)
        yin = y0 + xi * math.sin(ang) + yi * math.cos(ang)
    else:
        xin = x0 - xi * math.cos(ang) - (-yi) * math.sin(ang)
        yin = y0 - xi * math.sin(ang) - yi * math.cos(ang)
    return xin, yin


def CrushCheck(my_pos, d_my_pos, en_pos, d_en_pos, i, ind1, ind2):
    cr1 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                     my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                     en_pos[0][0], en_pos[0][1],
                     en_pos[0][0] + i * d_en_pos[0][0], en_pos[0][1] + i * d_en_pos[0][1]
                     )
    cr2 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                     my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                     en_pos[1][0], en_pos[1][1],
                     en_pos[1][0] + i * d_en_pos[1][0], en_pos[1][1] + i * d_en_pos[1][1]
                     )
    cr3 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                     my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                     en_pos[2][0], en_pos[2][1],
                     en_pos[2][0] + i * d_en_pos[2][0], en_pos[2][1] + i * d_en_pos[2][1]
                     )
    cr4 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                     my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                     en_pos[3][0], en_pos[3][1],
                     en_pos[3][0] + i * d_en_pos[3][0], en_pos[3][1] + i * d_en_pos[3][1]
                     )
    cr5 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                     my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                     en_pos[4][0], en_pos[4][1],
                     en_pos[4][0] + i * d_en_pos[4][0], en_pos[4][1] + i * d_en_pos[4][1]
                     )
    cr6 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                     my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                     en_pos[5][0], en_pos[5][1],
                     en_pos[5][0] + i * d_en_pos[5][0], en_pos[5][1] + i * d_en_pos[5][1]
                     )
    cr7 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                     my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                     en_pos[6][0], en_pos[6][1],
                     en_pos[6][0] + i * d_en_pos[6][0], en_pos[6][1] + i * d_en_pos[6][1]
                     )
    cr8 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                     my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                     en_pos[7][0], en_pos[7][1],
                     en_pos[7][0] + i * d_en_pos[7][0], en_pos[7][1] + i * d_en_pos[7][1]
                     )
    cr9 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                     my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                     en_pos[8][0], en_pos[8][1],
                     en_pos[8][0] + i * d_en_pos[8][0], en_pos[8][1] + i * d_en_pos[8][1]
                     )
    cr10 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                      my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                      en_pos[9][0], en_pos[9][1],
                      en_pos[9][0] + i * d_en_pos[9][0], en_pos[9][1] + i * d_en_pos[9][1]
                      )
    cr11 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                      my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                      en_pos[10][0], en_pos[10][1],
                      en_pos[10][0] + i * d_en_pos[10][0], en_pos[10][1] + i * d_en_pos[10][1]
                      )
    cr12 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                      my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                      en_pos[11][0], en_pos[11][1],
                      en_pos[11][0] + i * d_en_pos[11][0], en_pos[11][1] + i * d_en_pos[11][1]
                      )
    cr13 = CrossLines(my_pos[ind1][0] + i * d_my_pos[ind1][0], my_pos[ind1][1] + i * d_my_pos[ind1][1],
                      my_pos[ind2][0] + i * d_my_pos[ind2][0], my_pos[ind2][1] + i * d_my_pos[ind2][1],
                      en_pos[12][0], en_pos[12][1],
                      en_pos[12][0] + i * d_en_pos[12][0], en_pos[12][1] + i * d_en_pos[12][1]
                      )

    if cr1 or cr2 or cr3 or cr4 or cr5 or cr6 or cr7 or cr8 or cr9 or cr10 or cr11 or cr12 or cr13:
        return True
    return False


def Escape(cmd, my_car, my_pos, d_my_pos, en_pos, d_en_pos, mapid=1):
    global dbg
    for i in range(50):
        if CrushCheck(my_pos, d_my_pos, en_pos, d_en_pos, i, 2, 3):
            dbg += 'CRUSH IN ' + str(i) + " TICKS!!!! "
            if i < 40:
                if my_pos[-1][0] > en_pos[-1][0]:
                    cmd = KeepAngle(10, my_car, my_angle_prev)
                else:
                    cmd = KeepAngle(-20 if mapid == 5 else -30, my_car, my_angle_prev)
            break
        if CrushCheck(my_pos, d_my_pos, en_pos, d_en_pos, i, 0, 1):
            break
        # if CrushCheck(my_pos,d_my_pos,en_pos,d_en_pos,i,1,2):
        #    break
        # if CrushCheck(my_pos,d_my_pos,en_pos,d_en_pos,i,3,4):
        #    break
        if CrushCheck(my_pos, d_my_pos, en_pos, d_en_pos, i, 4, 5):
            break
        if CrushCheck(my_pos, d_my_pos, en_pos, d_en_pos, i, 5, 8):
            break
        # if CrushCheck(my_pos,d_my_pos,en_pos,d_en_pos,i,8,0):
        #    break
    return cmd


def CrossLines(x1_1, y1_1, x1_2, y1_2, x2_1, y2_1, x2_2, y2_2):
    def point(x, y):
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2) and min(x2_1, x2_2) <= x <= max(x2_1, x2_2):
            return True
        else:
            return False

    A1 = y1_1 - y1_2
    B1 = x1_2 - x1_1
    C1 = x1_1 * y1_2 - x1_2 * y1_1
    A2 = y2_1 - y2_2
    B2 = x2_2 - x2_1
    C2 = x2_1 * y2_2 - x2_2 * y2_1

    if B1 * A2 - B2 * A1 and A1:
        y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        x = (-C1 - B1 * y) / A1
        return point(x, y)
    elif B1 * A2 - B2 * A1 and A2:
        y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        x = (-C2 - B2 * y) / A2
        return point(x, y)
    else:
        return False


while True:
    z = input()
    state = json.loads(z)
    input_type = state['type']
    params = state['params']

    if input_type == 'new_match':
        my_lives = params["my_lives"]
        enemy_lives = params["enemy_lives"]
        map = params["proto_map"]
        map_id = map["external_id"]
        segments = map["segments"]
        for segment in segments:
            fp = segment[0]
            sp = segment[1]
            height = segment[2]
        proto_car = params['proto_car']
        proto_map = params['proto_map']
        _round += 1
        tick = 0
        rotate_bus = False
        special_action = False
        my_angle_prev = 0
        bus2delay = 800
    elif input_type == 'tick':
        cmd = ''
        dbg = ''
        my_car = params['my_car']
        en_car = params['enemy_car']
        my_pos = my_car[0]
        enemy_pos = en_car[0]
        d_my_pos = []
        d_en_pos = []

        if my_pos[0] > enemy_pos[0]:
            cmd = 'left'
        else:
            cmd = 'right'

        my_angle = my_car[1]
        en_angle = en_car[1]
        if abs(my_angle) > 10000 or abs(en_angle) > 10000:
            my_angle = 0
            en_angle = 0
        else:
            while my_angle > math.pi:
                my_angle -= 2 * math.pi
                my_car[1] = my_angle
            while my_angle < -math.pi:
                my_angle += 2 * math.pi
                my_car[1] = my_angle
            while en_angle > math.pi:
                en_angle -= 2 * math.pi
                en_car[1] = en_angle
            while en_angle < -math.pi:
                en_angle += 2 * math.pi
                en_car[1] = en_angle
        myx = InverseX(my_car[0][0], my_car[2])
        enx = InverseX(en_car[0][0], my_car[2])
        if proto_car['external_id'] in [1, 3]:
            mp1 = CoordShift(my_car[0][0], my_car[0][1], 0, 6, my_car[1])
            mp2 = CoordShift(my_car[0][0], my_car[0][1], 0, 25, my_car[1])
            mp3 = CoordShift(my_car[0][0], my_car[0][1], 33 * my_car[2], 42, my_car[1])
            mp4 = CoordShift(my_car[0][0], my_car[0][1], 85 * my_car[2], 42, my_car[1])
            mp5 = CoordShift(my_car[0][0], my_car[0][1], 150 * my_car[2], 20, my_car[1])
            mp6 = CoordShift(my_car[0][0], my_car[0][1], 150 * my_car[2], 0, my_car[1])
            mp7 = CoordShift(my_car[0][0], my_car[0][1], 122 * my_car[2], -17, my_car[1])
            mp8 = CoordShift(my_car[0][0], my_car[0][1], 29 * my_car[2], -17, my_car[1])
            mp9 = CoordShift(my_car[0][0], my_car[0][1], 20 * my_car[2], 0, my_car[1])
            mp10 = [(mp3[0] + mp4[0]) / 2, (mp3[1] + mp4[1]) / 2]
            mp11 = [(mp3[0] + mp4[0]) / 2, (mp3[1] + mp4[1]) / 2]
            mp12 = [(mp4[0] + mp5[0]) / 2, (mp4[1] + mp5[1]) / 2]
            mp13 = [(mp6[0] + mp9[0]) / 2, (mp6[1] + mp9[1]) / 2]
            mp_cen = [(mp1[0] + mp6[0]) / 2, (mp8[1] + mp3[1]) / 2]

            my_pos = [mp1, mp2, mp3, mp4, mp5, mp6, mp7, mp8, mp9, mp10, mp11, mp12, mp13, mp_cen]

            my_pos = [[InverseX(i[0], my_car[2]), i[1]] for i in my_pos]

            ep1 = CoordShift(en_car[0][0], en_car[0][1], 0, 6, en_car[1])
            ep2 = CoordShift(en_car[0][0], en_car[0][1], 0, 25, en_car[1])
            ep3 = CoordShift(en_car[0][0], en_car[0][1], 33 * en_car[2], 42, en_car[1])
            ep4 = CoordShift(en_car[0][0], en_car[0][1], 85 * en_car[2], 42, en_car[1])
            ep5 = CoordShift(en_car[0][0], en_car[0][1], 150 * en_car[2], 20, en_car[1])
            ep6 = CoordShift(en_car[0][0], en_car[0][1], 150 * en_car[2], 0, en_car[1])
            ep7 = CoordShift(en_car[0][0], en_car[0][1], 122 * en_car[2], -17, en_car[1])
            ep8 = CoordShift(en_car[0][0], en_car[0][1], 29 * en_car[2], -17, en_car[1])
            ep9 = CoordShift(en_car[0][0], en_car[0][1], 20 * en_car[2], 0, en_car[1])
            ep10 = [(ep3[0] + ep4[0]) / 2, (ep3[1] + ep4[1]) / 2]
            ep11 = [(ep3[0] + ep4[0]) / 2, (ep3[1] + ep4[1]) / 2]
            ep12 = [(ep4[0] + ep5[0]) / 2, (ep4[1] + ep5[1]) / 2]
            ep13 = [(ep6[0] + ep9[0]) / 2, (ep6[1] + ep9[1]) / 2]
            en_cen = [(ep1[0] + ep6[0]) / 2, (ep8[1] + ep3[1]) / 2]

            en_pos = [ep1, ep2, ep3, ep4, ep5, ep6, ep7, ep8, ep9, ep10, ep11, ep12, ep13, en_cen]

            en_pos = [[InverseX(i[0], my_car[2]), i[1]] for i in en_pos]
        else:
            mp1 = CoordShift(my_car[0][0], my_car[0][1], 76.5 * my_car[2], 31, my_car[1])
            my_pos = [mp1]
            my_pos = [[InverseX(i[0], my_car[2]), i[1]] for i in my_pos]

            ep1 = CoordShift(en_car[0][0], en_car[0][1], 76.5 * en_car[2], 31, en_car[1])
            en_pos = [ep1]
            en_pos = [[InverseX(i[0], my_car[2]), i[1]] for i in en_pos]

        if tick > 1:
            d_my_pos = []
            d_en_pos = []
            for lol in zip(my_pos, my_prev_pos):
                d_my_pos.append([lol[0][0] - lol[1][0], lol[0][1] - lol[1][1]])
            for lol in zip(en_pos, en_prev_pos):
                d_en_pos.append([lol[0][0] - lol[1][0], lol[0][1] - lol[1][1]])
        if proto_car['external_id'] == 1:
            if proto_map['external_id'] == 1:
                cmd = BuggyFlatfloor(tick, my_car, my_angle_prev, my_pos, en_pos)
            if proto_map['external_id'] == 4:
                if tick < 15:
                    cmd = InverseCommand('left', my_car[2])
                elif tick < 43:
                    cmd = InverseCommand('right', my_car[2])
                elif tick > 200:
                    cmd = KeepAngle(-80, my_car, my_angle_prev)
                else:
                    cmd = InverseCommand('left', my_car[2])
            elif proto_map['external_id'] == 5:
                cmd = BuggyIsland(tick, my_car, my_angle_prev)
            elif proto_map['external_id'] == 3:
                cmd = BuggyOnHill(tick, my_car, my_angle_prev, my_pos, en_pos)
            elif proto_map['external_id'] == 6:
                cmd = KeepAngle(60, my_car, my_angle_prev)
                if tick > 1050:
                    if abs(my_pos[-1][0] - en_pos[-1][0]) > 600:
                        cmd = InverseCommand('left', my_car[2])
            elif proto_map['external_id'] == 2:
                cmd = KeepAngle(45, my_car, my_angle_prev)
                if tick > 850 and en_pos[-1][0] > my_pos[-1][0] and en_car[0][1] > my_car[0][1]:
                    cmd = InverseCommand('left', my_car[2])
                    if 400 < my_pos[-1][0] < 600:
                        cmd = KeepAngle(0, my_car, my_angle_prev, 10)
                if my_pos[-1][0] < 150:
                    cmd = KeepAngle(35, my_car, my_angle_prev, 5)
            cmd = Dobivka(cmd, my_pos, en_pos)
            if tick > 1:
                cmd = Escape(cmd, my_car, my_pos, d_my_pos, en_pos, d_en_pos, proto_map['external_id'])
        elif proto_car['external_id'] == 3:
            if proto_map['external_id'] == 4:
                cmd = SqBuggyOn2ndFloor(tick, my_car, my_angle_prev)
            elif proto_map['external_id'] == 5:
                cmd = SqBuggyFlatFloor(my_car, my_angle_prev, my_pos, en_pos, d_my_pos)
            elif proto_map['external_id'] == 2:
                cmd = SqBuggyHubbleMap(tick, my_car, my_pos, en_pos, my_angle_prev)
            elif proto_map['external_id'] == 6:
                if my_car[2] == 1:
                    cmd = SqBuggyIslholeeMap(tick, my_car)
                else:
                    angle = 53
                    if abs(my_pos[-1][0] - en_pos[-1][0]) > 400:
                        if tick > 1085:
                            dbg += ' t3x:' + str(my_pos[2][1]) + " et3p" + str(en_pos[2][1])
                            angle = 30
                        if my_pos[0][-1] < 150:
                            angle = 40
                    cmd = KeepAngle(angle, my_car, my_angle_prev)
            else:
                if proto_map['external_id'] == 1:
                    angle = 60
                    if my_pos[-1][0] < 150:
                        angle = 50
                if proto_map['external_id'] == 2:
                    angle = 50
                    if my_pos[-1][0] < 150:
                        angle = 42
                if proto_map['external_id'] == 3:
                    angle = 56
                    if my_pos[-1][0] < 150:
                        angle = 48
                    if 450 < my_pos[-1][0] < 750:
                        angle = 60 if my_car[2] == 1 else 30
                    if my_pos[-1][0] > 500:
                        angle = 55
                    if my_pos[-1][0] > 700:
                        angle = 60
                    if my_pos[-1][0] > en_pos[-1][0]:
                        angle = -60
                    if tick > 820 and ButtonMin(my_pos) < ButtonMin(en_pos) and my_pos[-1][0] < 420:
                        angle = -30
                    if tick > 820 and ButtonMin(my_pos) < ButtonMin(en_pos) and my_pos[-1][0] > 850:
                        angle = -30
                cmd = KeepAngle(angle, my_car, my_angle_prev)
            cmd = Dobivka(cmd, my_pos, en_pos)
            if tick > 1:
                cmd = Escape(cmd, my_car, my_pos, d_my_pos, en_pos, d_en_pos, proto_map['external_id'])
        else:
            if rotate_bus:
                cmd = KeepAngle(68.55, my_car, my_angle_prev)
                if proto_map['external_id'] == 6:
                    cmd = 'stop'
                    delay = 200
                    if tick == delay:
                        if abs(my_pos[-1][0] - en_pos[-1][0]) > 400:
                            special_action = True
                            dbg += 'special action!!!,diff:' + str(abs(my_pos[-1][0] - en_pos[-1][0]))
                    if special_action:
                        if tick > (105 if my_car[2] == 1 else 100) + delay:
                            cmd = KeepAngle(-45, my_car, my_angle_prev)
                        if tick > 232 + delay:
                            cmd = 'stop'
                        if tick > (270 if my_car[2] == 1 else 260) + delay:
                            cmd = KeepAngle(68.55, my_car, my_angle_prev)
                    else:
                        cmd = KeepAngle(68.55, my_car, my_angle_prev)
                else:
                    cmd = KeepAngle(68.55, my_car, my_angle_prev)
            elif proto_map['external_id'] == 4:
                cmd = BusOn2ndFloor(tick, my_car)
            elif proto_map['external_id'] == 3:
                cmd = BusOnHill(tick, my_car)
            elif proto_map['external_id'] == 2:
                if bus2delay == 800:
                    if en_pos[-1][0] > 1000 or en_pos[-1][0] < 760:
                        bus2delay = tick
                cmd = BusOnHubble(tick, my_car, bus2delay)
            elif proto_map['external_id'] == 1:
                if tick < 45:
                    cmd = 'stop'
                elif tick < 100:
                    cmd = InverseCommand('left', my_car[2])
                elif tick < 130:
                    cmd = 'stop'
                elif tick < 170:
                    cmd = InverseCommand('left', my_car[2])
                else:
                    cmd = KeepAngle(85, my_car, my_angle_prev, 20)

            else:
                cmd = KeepAngle(60, my_car, my_angle_prev)
                rotate_bus = True

        print(json.dumps({"command": cmd, 'debug': str(cmd) + " t:" + str(tick) + " dbg:" + str(dbg) + " my_a:" + str(
            round(RadianInDegree(my_angle), 2)) + " en_a:"
                                                   + str(round(RadianInDegree(en_angle), 2)) +
                                                   ' my_c:[' + str(round(my_pos[-1][0], 2)) + ',' + str(
            round(my_pos[-1][1], 2)) +
                                                   "] en_c[:" + str(round(en_pos[-1][0], 2)) + ',' + str(
            round(en_pos[-1][1], 2)) + ']'}))
        tick += 1
        my_angle_prev = my_angle
        my_prev_pos = my_pos
        en_prev_pos = en_pos
    else:
        break
