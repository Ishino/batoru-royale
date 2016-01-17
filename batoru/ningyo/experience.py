class Experience:
    @staticmethod
    def calculate_experience_need(level, experience_modifier):

        calculate_experience_need = 0

        for i in range(int(level)):
            calculate_experience_need += ((int(i + 1) + int(experience_modifier)) * (int(i + 1) ** 2))

        return calculate_experience_need

    @staticmethod
    def calculate_experience_gain(level, opponent_level):
        experience_gain = opponent_level * opponent_level + opponent_level * opponent_level - level * level

        if experience_gain < 0:
            experience_gain = 0

        return experience_gain
