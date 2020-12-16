import pandas as pd
import pprint

from modul_nacteni_vstupu import nacti_studenty, nacti_lektory
# from modul_vytvoreni_hromadneho import create_schedule_hromadny


studenti = nacti_studenty("vstup_var2_studenti.csv")
# print("Celkový počet studentů: " + str(len(studenti)))
# print(studenti)


lektori = nacti_lektory("vstup_lektori.csv")
# print("Celkový počet lektorů: " + str(len(lektori)))
# print(lektori)

# novy_rozvrh_hromadny = create_schedule_hromadny()


# GENEROVANI ROZVRHU

def _make_dict_courses(studenti):
    """vrati slovnik, kde klicem je kurz a hodnotou seznam danych studentu"""
    slovnik_kurzu = {}
    for student in studenti:
        course = student.course
        if course not in slovnik_kurzu.keys():
            slovnik_kurzu[course] = [student]
        else:
            slovnik_kurzu.get(course).append(student)
    return slovnik_kurzu


def _make_dict_main(slovnik_kurzu):
    """ vrati slovnik, klicem je kurz, hodnoutou je slovnik
    v nested slovniku je klicem cas a hodnotou je seznam studentu z daneho kurzu, kteri muzou v dany cas"""
    slovnik_kurz_cas_studenti = {}
    for kurz, studenti in slovnik_kurzu.items():
        novy_slovnik = {}
        for student in studenti:
            for hodina, TF in student.mozne_hodiny.items():
                if TF == True:
                    if hodina not in novy_slovnik.keys():
                        novy_slovnik[hodina] = [student]
                    else:
                        novy_slovnik.get(hodina).append(student)
        slovnik_kurz_cas_studenti[kurz] = novy_slovnik
    return slovnik_kurz_cas_studenti


def _lektor_available(cas):
    """zkontroluje, jestli v dany cas alespon jeden z lektoru muze a vrati bool"""
    TF = False
    for lektor in lektori:
        TF = lektor.mozne_hodiny[cas]
        if TF:
            return True
    return TF


def _longest_in_dict(slovnik):
    """vstup - slovnik = hodina: seznam studentů co můžou"""
    """vrati slovnik casu, kdy muze nejvic studentu z daneho kurzu a seznam techto studentu"""
    nejdelsi = 0
    slovnik_casu_a_seznam_studentu = {}
    for key in slovnik.keys():
        TF = _lektor_available(key)
        if TF:
            podseznam_studenti = slovnik.get(key)
            if len(podseznam_studenti) > nejdelsi:
                nejdelsi = len(podseznam_studenti)
                slovnik_casu_a_seznam_studentu = {}
                slovnik_casu_a_seznam_studentu[key] = podseznam_studenti
            elif len(podseznam_studenti) == nejdelsi:
                slovnik_casu_a_seznam_studentu[key] = podseznam_studenti
    return slovnik_casu_a_seznam_studentu


def _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti):
    """vytvori slovnik, kde je klicem kurz a hodnotou slovnik, 
    kde je klic cas, ve ktery muze nejvic studentu, a hodnotou lektori, kteri muzou"""
    dict_of_courses_and_possible_times = {}
    for key, value in slovnik_kurz_cas_studenti.items():
        dict_of_times = _longest_in_dict(value)
        dict_of_courses_and_possible_times[key] = dict_of_times
    return dict_of_courses_and_possible_times


def rearrange_dict(dict):
    sorted_dict = {}
    pocet_klicu = len(dict)
    for i in range(pocet_klicu):
        for klic, hodnota in dict.items():
            if len(hodnota) == i:
                sorted_dict[klic] = hodnota
    print(sorted_dict)
    return sorted_dict


def make_schedule():
    # zatim zde neni zahrnut pocet 6 studentu na kurz
    slovnik_kurzu = _make_dict_courses(studenti)
    # print(slovnik_kurzu)

    # print("Počet studentů v kurzu")
    # for keys, values in slovnik_kurzu.items():
        # print((str(keys)) + ": " + str(len(values)))

    slovnik_kurz_cas_studenti = _make_dict_main(slovnik_kurzu)
    print(slovnik_kurz_cas_studenti)

    dict_of_courses_and_possible_times = _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti)
    pprint.pprint(dict_of_courses_and_possible_times)

    dict_of_courses_and_possible_times = rearrange_dict(dict_of_courses_and_possible_times)

    for kurz, cas_studenti in dict_of_courses_and_possible_times.items():           # cas_studenti je vnořený slovník, proto ho rozvíjím o řádek níž
        for cas, studenti_konkr_kurz in cas_studenti.items():                       # je v něm čas a seznam studentu napr. "pondeli 13:00": [Student 1, Student 2, ...]
            for i in range(len(lektori)):
                if kurz not in lektori[i].schedule.values() and kurz not in lektori[i-1].schedule.values():            # pokud kurz ještě není v rozvrhu lektora --> aby se nevypsal dvakrát, !limitováno 2 lektory - pokud kurz nebyl zapsán u předchozího lektora --> vymyslet jinak
                    if lektori[i].mozne_hodiny[cas]:                # if True (jestli lektor v dany cas muze, je uprednostnen lektor 1)
                        if lektori[i].schedule[cas] == "":          # pokud čas v rozvrhu ještě není obsazený
                            lektori[i].schedule[cas] = kurz         # pridej do schedule lektora kurz
                            for student in studenti_konkr_kurz:
                                student.cas_kurzu = cas
                                student.jeho_lektor = lektori[i]             # pridat cas kurzu do atributu tridy Student
        if kurz not in lektori[i].schedule.values() and kurz not in lektori[i-1].schedule.values():  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není: - u mych dat pro pet
            # najdi jiný termín pro kurz, který je v tomto čase a do tohoto času dej tento kurz
            print(kurz)

    for lektor in lektori:
        print(lektor)
        pprint.pprint(lektor.schedule)


    # VYPSANI DO HTML

    # data = []
    # dat = lektor.schedule
    # df = pd.DataFrame(data, index=[""])
    # df = df.fillna('').T
    # df.to_html("vystup.html")
        
make_schedule()



# poznamky
    # vzít první a umístit
    # vzít druhý a umístit, pokud nejde, najít jiný termín druhého, jinak najít druhý termín toho, se kterým se to kryje

    # for klic, hodnota in dict_of_courses_and_possible_times.items():      # klicem je kurz
        # najdi studenty, kteri maji ve slovnik_kurz_cas_studenti dany klic
        # najdi studenty, kteri NEmaji v dany cas cas a hledej, jestli maji nejaky spolecny
        # pro key, value in hodnota.items():
            # 


# najdi ostatní studenty pro první, jestli mají společný termín a může v něm lektor
# pokud ano, zapiš je do rozvrhu lektora
# najdi ostatní studenty pro druhý kurz


    # preskladej kurzy ve slovniku podle delky hodnoty
    # vezmi prvni den a dej ho do výsledného rozvrhu prvniho lektora, ktery muze
    # vezmi dalsi a dalsi den a dej ho do vysledneho rozvrhu lektora
        # pokud je tam uz obsazeno
            # zjisti, jestli je moznost u druheho lektora a dej ho druhemu lektorovi
            # pokud lektor nemuze, zjisti dalsi casovou moznost pro kurz
            # pokud dany kurz nema dalsi moznost, pro kterou by bylo volno
                # vrat se k obsazenemu policku a zjisti, jestli kurz v dany cas nema jinou casovou moznost a presun jej
    # pokud neni jina casovy moznost, najdi cas, kdy muze druhy nejvyssi pocet studentu


# rozdelit podle poctu v kurzu
# menší než 7
    # if len(studenti) < 7:
# existuje moznost dat je po 6? --> dělitelný 6?
    # if len(studenti) % 6 == 0: