# ROZVRH LEKTOR 1 - vytvoření zatím prázdného rozvrhu (nested dict: den - hodina - kurz)
# novy_rozvrh_lektor1 = {
#    "monday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    "tuesday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    "wednesday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    "thursday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    "friday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    }

days = ["monday", "tuesday", "wednesday", "thursday", "friday"]


# vytvoření (zatím) prázdného rozvrhu
def _create_nested_dict():
    """vytvoří slovník, kde klíčem je určitá hodina a hodnotou je prázdný string nachystaný pro kurz"""
    pole = {}
    for hour in range(13, 18):
        pole[hour] = ""
    return pole


def create_schedule():
    """vytvoří slovník, kde klíčem je den a hodnotou jiný slovník"""
    schedule_lektor = {}
    position_of_day = 0
    for i in range(len(days)):
        pole = _create_nested_dict()
        schedule_lektor[days[position_of_day]] = pole
        position_of_day += 1
    return schedule_lektor


def print_dict(schedule):
    """vytiskne slovnik"""
    for key, value in schedule.items():
        print(key, value)