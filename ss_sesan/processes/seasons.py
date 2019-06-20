# -*- coding: utf-8 -*-


def GetSeasonsRules():
    rules = {

        "Disponibilidad": {
            "opt1": {
                "name": "Opcion 1",
                "vals": [["Número de meses con reserva de maíz", 7.465],
                         ["Número de meses con reserva de frijol", 3.727],
                         ["Porcentaje de pérdida de cultivo de maíz", 4.353],
                         ["Porcentaje de pérdida de cultivo de frijól", 2.173],
                         ["No. de días sin lluvia por mes", "NA"],
                         ["Porcentaje de animales domésticos para consumo humano afectados por enfermedades",
                          1.882]]

            },
            "opt2": {
                "name": "Opcion 2",
                "vals": [["Número de meses con reserva de maíz", 7.465],
                         ["Número de meses con reserva de frijol", 3.727],
                         ["Porcentaje de pérdida de cultivo de maíz", 4.959],
                         ["Porcentaje de pérdida de cultivo de frijól", "NA"],
                         ["No. de días sin lluvia por mes", 2.587],
                         ["Porcentaje de animales domésticos para consumo humano afectados por enfermedades",
                          0.862]]

            },
            "opt3": {
                "name": "Opcion 3",
                "vals": [["Número de meses con reserva de maíz", 7.465],
                         ["Número de meses con reserva de frijol", 3.727],
                         ["Porcentaje de pérdida de cultivo de maíz", "NA"],
                         ["Porcentaje de pérdida de cultivo de frijól", 4.959],
                         ["No. de días sin lluvia por mes", 2.587],
                         ["Porcentaje de animales domésticos para consumo humano afectados por enfermedades", 0.862]]

            },
            "opt4": {
                "name": "Opcion 4",
                "vals": [["Número de meses con reserva de maíz", 9.805],
                         ["Número de meses con reserva de frijol", 4.895],
                         ["Porcentaje de pérdida de cultivo de maíz", "NA"],
                         ["Porcentaje de pérdida de cultivo de frijól", "NA"],
                         ["No. de días sin lluvia por mes", "NA"],
                         ["Porcentaje de animales domésticos para consumo humano afectados por enfermedades", 4.900]]

            },
            "opt5": {
                "name": "Opcion 5",
                "vals": [["Número de meses con reserva de maíz", 6.445],
                         ["Número de meses con reserva de frijol", 3.218],
                         ["Porcentaje de pérdida de cultivo de maíz", "NA"],
                         ["Porcentaje de pérdida de cultivo de frijól", 6.096],
                         ["No. de días sin lluvia por mes", "NA"],
                         ["Porcentaje de animales domésticos para consumo humano afectados por enfermedades", 3.842]]

            },
            "opt6": {
                "name": "Opcion 6",
                "vals": [["Número de meses con reserva de maíz", 7.060],
                         ["Número de meses con reserva de frijol", 3.524],
                         ["Porcentaje de pérdida de cultivo de maíz", 5.821],
                         ["Porcentaje de pérdida de cultivo de frijól", "NA"],
                         ["No. de días sin lluvia por mes", "NA"],
                         ["Porcentaje de animales domésticos para consumo humano afectados por enfermedades", 3.195]]

            },
            "opt7": {
                "name": "Opcion 7",
                "vals": [["Número de meses con reserva de maíz", 7.844],
                         ["Número de meses con reserva de frijol", 3.916],
                         ["Porcentaje de pérdida de cultivo de maíz", "NA"],
                         ["Porcentaje de pérdida de cultivo de frijól", "NA"],
                         ["No. de días sin lluvia por mes", 3.920],
                         ["Porcentaje de animales domésticos para consumo humano afectados por enfermedades", 3.920]]

            }

        }
    }

    return rules


def GetSeasonsRules_Vals():
    var_with_rules = ["por_de_per_de_cul_de_ma", "por_de_per_de_cul_de_fri", "no_de_d_sin_llu_por_mes"]

    rules = {

        "110": {
            "61": 7.465,
            "62": 3.727,
            "65": 4.353,
            "66": 2.173,
            "64": "NA",
            "63": 1.882

        },
        "101": {
            "61": 7.465,
            "62": 3.727,
            "65": 4.959,
            "66": "NA",
            "64": 2.587,
            "63": 0.862

        },
        "011": {
            "61": 7.465,
            "62": 3.727,
            "65": "NA",
            "66": 4.959,
            "64": 2.587,
            "63": 0.862

        },
        "000": {
            "61": 9.805,
            "62": 4.895,
            "65": "NA",
            "66": "NA",
            "64": "NA",
            "63": 4.900

        },
        "010": {
            "61": 6.445,
            "62": 3.218,
            "65": "NA",
            "66": 6.096,
            "64": "NA",
            "63": 3.842

        },
        "100": {
            "61": 7.060,
            "62": 3.524,
            "65": 5.821,
            "66": "NA",
            "64": "NA",
            "63": 3.195

        },
        "001": {
            "61": 7.844,
            "62": 3.916,
            "65": "NA",
            "66": "NA",
            "64": 3.920,
            "63": 3.920

        },
        "111": {
            "61": 7.844,
            "62": 3.916,
            "65": "NA",
            "66": "NA",
            "64": 3.920,
            "63": 3.920

        }

    }

    return rules
