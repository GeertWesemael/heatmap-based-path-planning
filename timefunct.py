import math

import numpy as np
import random
import datetime


def hour_min_to_sec(hour, min):
    return hour * 3600 + min * 60


def random_time_between(hour1, min1, hour2, min2):
    return random_time_between_(hour_min_to_sec(hour1, min1), hour_min_to_sec(hour2, min2))


def random_time_between_(sec1, sec2):
    if sec1 < sec2:
        return random.randint(sec1, sec2)
    else:
        return random.randint(sec2, sec1)


def sec_to_hour_min_string(sec):
    return str(datetime.timedelta(seconds=sec))

def sec_to_date_time(sec):
    return datetime.timedelta(seconds=sec)

def sec_to_min(sec):
    return sec/60

def sec_to_hour(sec):
    return sec/3600

def unifromly_dist_time_(begin,end,amount):
    return np.linspace(begin,end,num=amount+1,endpoint=False)[1:]
