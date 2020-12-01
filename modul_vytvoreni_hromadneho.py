from modul_vytvoreni_slovniku import days

# ROZVRH HROMADNÝ - možná zbytečné - místo str v hodnotě pro kurz je list (více kurzů)
# novy_rozvrh_hromadny = {
#    "pondeli": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    "utery": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    "streda": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    "ctvrtek": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    "patek": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    }


def _create_nested_dict_hromadny():
    """vytvoří slovník, kde klíčem je určitá hodina a hodnotou je prázdné pole nachystané pro kurzy"""
    pole = {}
    for hour in range(13, 18):
        pole[hour] = []
    return pole


def create_schedule_hromadny():
    """vytvoří slovník, kde klíčem je den a hodnotou jiný slovník"""
    schedule_hromadny = {}
    position_of_day = 0
    for i in range(len(days)):
        pole = _create_nested_dict_hromadny()
        schedule_hromadny[days[position_of_day]] = pole
        position_of_day += 1
    return schedule_hromadny