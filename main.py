from math import sqrt, floor, ceil

files=['busy_day', 'mother_of_all_warehouses', 'redundancy']
for data_n in files:
    lines = [line.rstrip('\n') for line in open("{0}.in".format(data_n))]
    params = [int(we) for we in lines[0].split(' ')]
    r = params[0]
    c = params[1]
    dr_c = params[2]
    turns = params[3]
    max_pl = params[4]

    p_count = int(lines[1])
    w = [int(we) for we in lines[2].split(' ')]

    cords = {}
    avail = {}
    orders = {}
    orders_loc = {}
    drone_loc = {}
    drone_payload = {}
    cmd = []
    sim_count = {}
    drone_exceed = {}

    wh = int(lines[3])

    wh_c = 4
    for i in range(1, wh + 1):
        cords[i - 1] = [int(we) for we in lines[wh_c].split(' ')]
        wh_c += 1
        avail[i - 1] = [int(we) for we in lines[wh_c].split(' ')]
        wh_c += 1

    for d in range(0, dr_c):
        drone_loc[d] = cords[0]

    for d in range(0, dr_c):
        drone_payload[d] = 0
        sim_count[d] = 0

    ord_c = int(lines[wh_c])
    for i in range(1, ord_c + 1):
        orders[i - 1] = [0] * p_count
        wh_c += 1
        orders_loc[i - 1] = [int(we) for we in lines[wh_c].split(' ')]
        wh_c += 1
        ord_count = int(lines[wh_c])
        wh_c += 1
        order_pr = [int(we) for we in lines[wh_c].split(' ')]
        for pr in order_pr:
            orders[i - 1][pr] += 1

    # print(orders[0])
    while True:
        finish = True
        drone_avail = False
        for i in range(0, ord_c):
            # print(sum(orders[ord_c-1]))
            for idx in range(0, len(orders[i])):
                flights = {}
                pr = orders[i][idx]
                if pr > 0:
                    finish = False
                    close_wh = -1
                    dt = float("inf")
                    for wh_i in range(0, wh):
                        if avail[wh_i][idx] >= pr:
                            dt2 = sqrt(sum((a - b) ** 2 for a, b in zip(orders_loc[i], cords[wh_i])))
                            if dt2 < dt:
                                dt = dt2
                                close_wh = wh_i

                    if close_wh == -1:
                        continue

                    order_w = 0
                    order_prods = [0]*p_count
                    for idx2 in range(0,len(orders[i])):
                        if (avail[close_wh][idx2]<orders[i][idx2]):
                            continue
                        prod_idx2 = min(orders[i][idx2],int(floor(max_pl)/w[idx2]))
                        if (order_w+prod_idx2*w[idx2] <= max_pl ):
                            order_w += prod_idx2*w[idx2]
                            order_prods[idx2] += prod_idx2
                    close_dr = -1
                    # pr_c = 0
                    dt_dr = float("inf")
                    for d in range(0, dr_c):
                        if drone_payload[d] > 0:
                            continue
                        # pr_c = min(pr, int(floor(max_pl / w[idx])))
                        dt_dr2 = sqrt(sum((a - b) ** 2 for a, b in zip(drone_loc[d], cords[close_wh])))
                        if dt_dr2 < dt_dr:
                            close_dr = d
                            dt_dr = dt_dr2
                    if close_dr > -1 and sim_count[close_dr] <= (turns - (ceil(dt_dr) + ceil(dt) + 2*sum(order_prods))):
                        for idx3 in range(0,len(order_prods)):
                            if(order_prods[idx3]>0):
                                cmd.append("{0} L {1} {2} {3}".format(close_dr, close_wh, idx3, order_prods[idx3]))
                                avail[close_wh][idx3] -= order_prods[idx3]
                                drone_loc[close_dr] = cords[close_wh]
                        delivery = False
                        for idx3 in range(0,len(order_prods)):
                            if(order_prods[idx3]>0):
                                cmd.append("{0} D {1} {2} {3}".format(close_dr, i, idx3, order_prods[idx3]))
                                drone_loc[close_dr] = orders_loc[i]
                                orders[i][idx3] -= order_prods[idx3]
                                delivery = True
                        if delivery:
                            # print('dfd')
                            sim_count[close_dr] += ceil(dt_dr) + ceil(dt) + 2*sum(order_prods)
                            drone_avail = True

        if finish or (not drone_avail):
            break

    with open("{0}_out.in".format(data_n), 'w') as f:
        f.write("{0}\n".format(len(cmd)))
        for cm in cmd:
            f.write("{0}\n".format(cm))
        f.close()
