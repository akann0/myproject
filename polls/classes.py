import random, math
import names
import itertools
from .possessions import Possession


class Player:
    next_pid_to_be_assigned = 1
    stats = []
    
    def choosename(self):
        self.pid = Player.next_pid_to_be_assigned
        if self.pid == 1:
            Player.stats = Game.stat_symbs.keys()
        Player.next_pid_to_be_assigned += 1
        self.name = names.get_full_name(gender="male")

    def gen_positions(self):
        self.position = random.randint(1, 11)

    def gen_ratings(self):
        self.ratings = {
            "OF": random.gauss(50, 1),
            "GK": 50
        }

    def __init__(self):
        self.age = 20
        self.rating = 50
        self.ratings = {
        "OF": 50,
        "GK": 30
        }
        self.game_stats = {}
        self.choosename()
        self.gen_positions()
        self.gen_ratings()
    
    def clear_game_stats(self):
        self.game_stats = {}
        for stat in self.stats:
            self.game_stats[stat] = 0

    def add_game_stat(self, stat):
        self.game_stats[stat] += 1

    def print_game_stats(self):
        print(self.name)
        print(self.game_stats)


class Formation:
    name = "4-2-3-1"
    defenders = ["2", "3", "4", "5"]
    midfielders = ["6", "8", "10"]
    attackers = ["7", "10", "11", "9"]
    bu = ["2", "6", "8", "5"]

    def listed(self, list, count=1):
        answer = []
        for i in range(count):
            for item in list:
                answer.append([item])
        return answer

    def __init__(self, name):
        self.name = name

    def get_buildup(self):
        buildup = {}
        buildup["halfspace"] = self.get_bu_to_hs()
        buildup["thruog"] = self.get_thruog()
        return buildup

    def all_different(self, tup):
        if len(tup) != 4:
            return False
        if tup[0] == tup[1] or tup[0] == tup[2] or tup[0] == tup[3] or tup[1] == tup[2] or tup[1] == tup[3] or tup[2] == tup[3]:
            return False
        return True
    
    def get_bu_to_hs(self):
        answer = []
        fanswer = itertools.product(self.defenders, self.bu, self.bu, self.midfielders)
        for tup in fanswer:
            if self.all_different(tup):
                answer.append(tup)
        return answer

        
    def get_thruog(self):
        answer = []
        for defender in self.defenders:
            for attacker in self.attackers:
                answer.append([defender, attacker])
        return answer
        

    def get_halfspace(self):
        return itertools.permutations(self.attackers, 3)

    def get_recovery(self):
        return (list)(itertools.permutations(self.midfielders, 2)) + self.listed(self.midfielders, 3) + self.listed(self.attackers, 2) + self.listed(self.defenders)
        

class Team:
    name = "Manchester United"
    roster = []
    formation = "4-2-3-1"
    stats=[]

    def __init__(self, name, form):
        self.name = name
        Team.stats = Game.stat_symbs.keys()
        self.game_stats = {}
        self.set_lifetime_stats()
        self.formation = Formation(form)
        self.pentaker = self.set_pentaker()

    def set_lifetime_stats(self):
        self.lifetime_stats = {}
        for stat in self.stats:
            self.lifetime_stats[stat] = 0

    def set_pentaker(self):
        return 10

    def add_to_roster(self, player):
        self.roster.append(player)

    def gen_random_team(self):
        self.roster = []
        for i in range(11):
            self.roster.append(Player())

    def get_buildup_patterns(self):
        return self.formation.get_buildup()

    def get_halfspace_patterns(self):
        return self.formation.get_halfspace()

    def get_recovery(self):
        return self.formation.get_recovery()

    def get_pentaker(self):
        return self.pentaker

    def corner_taker(self):
        return "5"

    def set_piece_offense(self):
        return ["3", "4", "9", "7", "8"]

    def get_player_rating(self, player, rating):
        return self.roster[int(player)-1].ratings[rating]

    def number_by_rating(self, total, percentage, rating):
        mean_rating = self.get_rating(rating)
        change_over_expected = mean_rating-50 
        x = self.percentage_change(percentage, change_over_expected)
        #print(x)
        return round(x * total)

    def get_rating(self, rating):
        if rating == 50:
            return 50
        if "shortpass" in rating:
            return int(self.get_player_rating(rating.split("?")[1], "OF"))
        
    def percentage_change(self, percent, change_over_expected):
        #print((1/percent) - 1)
        x = (-50) * math.log((1/percent) - 1)
        y = math.exp((-1/50)*(x - change_over_expected))
        return 1/(1+y)

    def clear_game_stats(self):
        self.game_stats = {}
        for stat in self.stats:
            self.game_stats[stat] = 0

    def add_game_stat(self, stat):
        self.game_stats[stat] += 1

    def print_game_stats(self):
        print(self.name)
        print(self.game_stats)

    def start_game(self, opponent):
        self.current_opponent = opponent
        self.clear_game_stats()
        
    

class Game:
    home = Team
    away = Team
    homeScore = 0
    awayScore = 0
    minute = 0
    second = 0
    possessions= {}
    stat_symbs = {
        "Passes": "P",
        "Turnovers":"F",
        "Goals": "G",
        "Tackles": "T",
        "Dribbles": "D",
        "Clearances": "C",
        "Shots": "S",
        "Saves": "V",
        "Shots On Target": "N",
        "Shots Off Target": "s",
        "Penalty Attempted": "PT",
        "Penalty Made": "PM",
        "Crosses Attempted": "CA",
        "Crosses Made": "CM",
    }
    defstats = ["Saves", "Clearances", "Tackles", "Interceptions", "Blocked Shots", "Dribbled Past"]

    def __init__(self, home, away):
        self.home = home
        self.away = away
        self.gen_poss()

    def gen_poss(self):
        for cls in Possession.__subclasses__():
            print(cls.__name__)
            self.possessions["home "+ cls.__name__] = cls("home", self.home)
            self.possessions["away "+ cls.__name__] = cls("away", self.away)
        print(self.possessions.keys())
        print(self.possessions["home HalfSpace"].name)

    def play_game(self):
        #let teams know the game has started
        self.home.start_game(self.away)
        self.away.start_game(self.home)
        #reset the player stats
        for team in [self.home, self.away]:
            for player in team.roster:
                player.clear_game_stats()
        possess = "home Buildup"
        while self.minute < 96:
            while self.second < 60:
                #print("Minute: " + str(self.minute) + " Second: " + str(self.second))
                #print(possess)
                #print(self.possessions[possess].pos_results)
                result = self.possessions[possess].result()
                #print(result["result"])
                if (result["result"] == "goal"):
                    print(possess + " goal!")
                    if "home" in possess:
                        self.homeScore += 1
                    else:
                        self.awayScore += 1
                #print(result["stats"])
                possess = result["possess"]
                self.second += result["seconds"]
                #TODO: add stats to player
                self.digest_stats(result["stats"], result["team"], result["opposition"])
                #end second loop
            self.second -= 60
            self.minute += 1
            #end minute loop
        return self.postgame()
    

    def postgame(self):
        print(self.home.name + ": " + str(self.homeScore))
        print(self.away.name + ": " + str(self.awayScore))
        print("----------")
        self.print_player_stats()
        return self.home.name + ": " + str(self.homeScore) + " " + self.away.name + ": " + str(self.awayScore)

    def print_team_stats(self):
        self.home.print_game_stats()
        self.away.print_game_stats()

    def print_player_stats(self):
        for player in self.home.roster:
            player.print_game_stats()
        print("----------")
        for player in self.away.roster:
            player.print_game_stats()
    
    def digest_stats(self, stats, offense, defense):
        for stat in stats:
            stat.player = int(stat.player)
            if (offense == "home"):
                if (stat.team == 'o'):
                    self.home.add_game_stat(stat.name)
                    self.home.roster[stat.player - 1].add_game_stat(stat.name)
                else:
                    self.away.add_game_stat(stat.name)
                    self.away.roster[stat.player - 1].add_game_stat(stat.name)
            else:
                if (stat.team == 'o'):
                    self.away.add_game_stat(stat.name)
                    self.away.roster[stat.player - 1].add_game_stat(stat.name)
                else:
                    self.home.add_game_stat(stat.name)
                    self.home.roster[stat.player - 1].add_game_stat(stat.name)
            



            

        




    
    

        



    
    
