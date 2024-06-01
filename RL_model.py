

class RL:

    def __init__(self):
        pass

    def action(self, j_state):
        """"
        dummy action, no trained module yet
        """

        comb_id = j_state["vehicle_in_combs"].index(max(j_state["vehicle_in_combs"]))

        return comb_id

