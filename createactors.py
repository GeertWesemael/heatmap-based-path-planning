import actor
import random
import zone
from timefunct import random_time_between, random_time_between_, sec_to_hour_min_string


def actor_with_job(job, mapp, zones):
    wc = get_zone(zones, "wc")
    off1 = get_zone(zones, "office1")
    off2 = get_zone(zones, "office2")
    laun = get_zone(zones, "lounge")
    inbo = get_zone(zones, "inbound")
    outb = get_zone(zones, "outbound")
    stor = get_zone(zones, "storage")
    pack = get_zone(zones, "packing")
    door = get_zone(zones, "door")
    # all spots are equally possible => not ok
    all_zones = zone.Zone.combined_zones(zones)

    # work starts at 9 and stops at 17
    if job == "manager":

        # morning
        a = actor.Actor.actor_at_zone(door, random_time_between(8, 30, 9, 30), mapp)
        a.walk_to_zone(off1) if decision(0.5) else a.walk_to_zone(laun) and a.wait(60) and a.walk_to_zone(off1)
        a.wait_till(random_time_between(10, 30, 11, 00))
        a.walk_to_zone(get_random_zone(zones)) and a.wait(random_time_between_(20, 600)) if decision(0.8) else a.wait(1)
        a.walk_to_zone(get_random_zone(zones)) and a.wait(random_time_between_(20, 600)) if decision(0.2) else a.wait(1)
        a.walk_to_zone(off1)

        # noon
        a.wait_till(random_time_between(11, 55, 12, 15))
        a.walk_to_zone(laun)
        a.wait(random_time_between(0, 25, 0, 35))
        a.walk_to_zone(off1)
        a.wait(random_time_between(0, 5, 0, 10))

        # afternoon
        amount = random.randint(0, 10)
        while amount != 0:
            a.walk_to_zone(get_random_zone(zones))
            a.wait(random_time_between_(20, 600))
            a.walk_to_zone(off1) if decision(0.8) else a.walk_to_zone(get_random_zone(zones)) and a.wait(
                random_time_between_(20, 600)) and a.walk_to_zone(off1)
            amount = amount - 1
        a.wait_till(random_time_between(16, 30, 17, 30))
        a.walk_to_zone(door)

        return a

    else:
        active = True  # movement within zone
        if job == "receiver":
            profession_zone = inbo
        elif job == "packer":
            profession_zone = pack
            active = False
        elif job == "forklift":
            profession_zone = stor
        elif job == "shipper":
            profession_zone = outb
        else:
            raise Exception("unknown profession added")

        arrive_time = random_time_between(8, 45, 8, 58)
        start_time = random_time_between(8, 58, 9, 59)
        break_time_start = random_time_between(11, 55, 12, 10)
        # print("s: " + sec_to_hour_min_string(break_time_start))
        break_time_end = random_time_between(13, 0, 13, 10)
        # print("e: " + sec_to_hour_min_string(break_time_end))
        end_time = random_time_between(17, 00, 17, 10)

        # enter / coffee
        a = actor.Actor.actor_at_zone(door, arrive_time, mapp)
        a.walk_to_zone(laun)
        a.wait_till(start_time)
        a.walk_to_zone(profession_zone)

        # first work shift
        while a.path.get_end_time() <= break_time_start:
            a.walk_to_zone(profession_zone)
            r = random_time_between(0, 15, 0, 45)
            if active:
                r = random_time_between_(10, 300)
            a.wait(r)

        # lunch break
        a.walk_to_zone(laun)
        a.wait_till(break_time_end)
        a.walk_to_zone(profession_zone)

        # second work shift
        while a.path.get_end_time() <= end_time:
            a.walk_to_zone(profession_zone)
            r = random_time_between(0, 30, 1, 0)
            if active:
                r = random_time_between_(10, 300)
            a.wait(r)

        # end of working day
        a.walk_to_zone(door)

        return a


def decision(probability):
    return random.random() < probability


def get_zone(zones, name):
    for i in zones:
        if i.name == name:
            return i


def get_random_zone(zones):
    return random.choice(zones)
