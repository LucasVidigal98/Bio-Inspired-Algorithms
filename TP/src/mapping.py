import json
import pandas as pd


class mapping:
    def __init__(self):
        self.food_interval = {
            "B": (1, 21),
            "S": (22, 32),
            "F": (33, 94),
            "L": (95, 113),
            "C1": (114, 134),
            "C2": (135, 146),
            "G": (147, 158),
            "V": (159, 199),
            "P": (200, 294)
        }

        self.diet_scope = {
            "length": 17,
            "n_meals": 6,
            "meals": ["breakfast", "snack_1", "lunch", "snack_2", "dinner", "supper"],
            "breakfast": (0, 2),
            "snack_1": (3, 3),
            "lunch": (4, 9),
            "snack_2": (10, 11),
            "dinner": (12, 15),
            "supper": (16, 16),
            "composition": ["B", "F", "C1", "F", "C2", "G", "V", "V", "P", "S", "B", "C1", "C2", "G", "V", "P", "L"]
        }

        self.nutrients = {
            "Df": 25,
            "C": 300,
            "Pt": 75,
            # / 1000 Trnasformar mg -> g
            "Ca": 1000/1000,
            "Mn": 2.3/1000,
            "Fe": 14/1000,
            "Mg": 260/1000,
            "P": 700/1000,
            "Zn": 7/1000,
            "Na": 2400/1000
        }

        self.info_food = ""

        self.info_food_test = pd.read_csv("./dataset_formatado.csv")

        with open("TACO_formatted.json", "r") as json_file:
            self.info_food = json.load(json_file)

    def get_food_info(self, id_food):
        info = dict()

        for food in self.info_food:
            if food["id"] == id_food:
                try:
                    info["kcal"] = float(food["energy_kcal"])
                except:
                    info["kcal"] = 200.0

                try:
                    info["Df"] = float(food["fiber_g"])
                except:
                    info["Df"] = float(self.nutrients["Df"])

                try:
                    info["C"] = float(food["carbohydrate_g"])
                except:
                    info["C"] = float(self.nutrients["C"])

                    try:
                        info["Pt"] = float(food["protein_g"])
                    except:
                        info["Pt"] = float(self.nutrients["Pt"])

                    # / 1000 Trnasformar mg -> g
                    try:
                        info["Ca"] = float(food["calcium_mg"])/1000
                    except:
                        info["Ca"] = float(self.nutrients["C"])

                    try:
                        info["Mn"] = float(food["manganese_mg"])/1000
                    except:
                        info["Mn"] = float(self.nutrients["Mn"])

                    try:
                        info["Fe"] = float(food["iron_mg"])/1000
                    except:
                        info["Fe"] = float(self.nutrients["Fe"])

                    try:
                        info["Mg"] = float(food["magnesium_mg"])/1000
                    except:
                        info["Mg"] = float(self.nutrients["Mg"])

                    try:
                        info["P"] = float(food["phosphorus_mg"])/1000
                    except:
                        info["P"] = float(self.nutrients["P"])

                    try:
                        info["Zn"] = float(food["zinc_mg"])/1000
                    except:
                        info["Zn"] = float(self.nutrients["Zn"])

                return info

    def get_food_info_test(self, id_food):
        info = dict()
        line = self.info_food_test.loc[id_food-1]
        info["kcal"] = line["kcal"]
        info["Df"] = line["Df"]
        info["C"] = line["C"]
        info["Pt"] = line["Pt"]
        # /1000 mg -> m
        info["Ca"] = line["Ca"] / 1000
        info["Mn"] = line["Mn"] / 1000
        info["Fe"] = line["Fe"] / 1000
        info["Mg"] = line["Mg"] / 1000
        info["P"] = line["P"] / 1000
        info["Na"] = line["Na"] / 1000
        info["Zn"] = line["Zn"] / 1000

        return info

        '''
            file = open('dataset_formatado.csv', 'r')
            lines = file.readlines()
            file.close()

            info = dict()

            count_id = 1
            for line in lines:
                if id_food == count_id:
                    parsed_line = line.split(',')

                    for parse in parsed_line:
                        if '"' in parse or "'" in parse or ' ' in parse or ' "' in parse:
                            del(parsed_line[parse.index(parse)])

                    info["kcal"] = float(parsed_line[12])
                    info["Pt"] = float(parsed_line[2])
                    info["C"] = float(parsed_line[3])
                    info["Df"] = float(parsed_line[4])
                    # / 1000 Trnasformar mg -> g
                    info["Ca"] = float(parsed_line[5]) / 1000
                    info["Mg"] = float(parsed_line[6]) / 1000
                    info["Mn"] = float(parsed_line[7]) / 1000
                    info["P"] = float(parsed_line[8]) / 1000
                    info["Fe"] = float(parsed_line[9]) / 1000
                    info["Na"] = float(parsed_line[10]) / 1000
                    info["Zn"] = float(parsed_line[11]) / 1000
                    return info

                count_id += 1
                '''
