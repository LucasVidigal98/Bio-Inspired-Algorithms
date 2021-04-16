from mapping import mapping as mp_food


class pdcr:
    def __init__(self):
        self.mp = mp_food()
        self.total_nutirents = self.calculate_bj()
        self.pi = (0.5, 3.0)

    def calculate_bj(self):
        total_nutirents = 0
        for nutrients_key in self.mp.nutrients.keys():
            if nutrients_key == 'kcal':
                continue
            total_nutirents += self.mp.nutrients[nutrients_key]

        return total_nutirents

    # Verfica equação (2)
    def check_restriction(self, proportion, ids):
        left_side_eqation = 0
        for i in range(len(proportion)):
            p = proportion[i]
            id_food = ids[i]
            info_food = self.mp.get_food_info(id_food)
            for nutrients_key in info_food.keys():
                if nutrients_key == 'kcal':
                    continue
                left_side_eqation += info_food[nutrients_key] * p

            if left_side_eqation >= self.total_nutirents:
                return True

            return False

    def get_fo(self, proportion, ids):
        # Verfica se houve violação
        fo = 0
        if self.check_restriction(proportion, ids):
            #print('Não violou')
            total = 0
            for i in range(len(proportion)):
                p = proportion[i]
                kcal = self.mp.get_food_info_test(ids[i])["kcal"]
                total += kcal*p
            fo = 1200 - total
        else:
            # print('Violou')
            for i in range(len(proportion)):
                total = 0
                info_food = self.mp.get_food_info_test(ids[i])
                p = proportion[i]
                for nutrients_key in info_food.keys():
                    if nutrients_key == 'kcal':
                        continue
                    x = abs(info_food[nutrients_key] * p -
                            self.mp.nutrients[nutrients_key])
                    x = x / self.mp.nutrients[nutrients_key]
                    total += x
                diff_kcal = abs(info_food['kcal'] - 1200)

                fo = diff_kcal + total * 300

        return fo
