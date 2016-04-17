class Actions:

    def __init__(self, combat_calc):
        self.actionList = None
        self.combat_calc = combat_calc

    def get_action(self, action_name):
        action_list = {'heal': self.heal_action,
                       'boost': self.boost_action,
                       'bash': self.bash_action}
        callback = None

        try:
            callback = action_list[action_name]
        except KeyError:
            # if we get an unknown callback we just ignore it
            print('action does not exist')

        return callback

    def run_action(self, player_one, player_two, action_name):
        action = self.get_action(action_name)

        if action is not None:
            player_one = action(player_one, player_two)

        return player_one

    @staticmethod
    def heal_action(player_one, player_two):
        player_one.hitPoints = player_one.hitPointsBase * player_one.stamina
        return player_one

    def boost_action(self, player_one, player_two):
        skill_modifier = self.combat_calc.calc_modifier(player_one.typeStat, player_two.typeStat, 0.2)
        player_one.fightSkill += skill_modifier
        return player_one

    @staticmethod
    def bash_action(player_one, player_two):
        player_one.hitPoints = player_one.hitPointsBase * player_one.stamina
        return player_one
