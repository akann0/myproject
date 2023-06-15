import random

class Stat:
    def __init__(self, symb, player, team = "o"):
        self.name = self.statsymbs[symb]
        self.player = player
        self.team = team

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.player != other.player:
            return False
        if self.team != other.team:
            return False
        return True

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

    #flip the keys and values of stat_symbs
    statsymbs = {
        "P": "Passes",
        "F": "Turnovers",
        "G": "Goals",
        "T": "Tackles",
        "D": "Dribbles",
        "C": "Clearances",
        "S": "Shots",
        "V": "Saves",
        "N": "Shots On Target",
        "s": "Shots Off Target",
        "PT": "Penalty Attempted",
        "PM": "Penalty Made",
        "CA": "Crosses Attempted",
        "CM": "Crosses Made",
    }

    def __repr__(self):
        return self.name + " by " + str(self.player)



class Result:
    def __init__(self, seconds, next_poss, stats, goal=False, change_of_poss = False):
        self.goal = goal
        self.change_of_possession = change_of_poss
        self.seconds = seconds
        self.next_poss = next_poss
        #list of Stat objects
        self.stats = stats
        self.odds = 0
        self.items = [self.goal, self.change_of_possession, self.seconds, self.next_poss, self.stats, self.odds]

    def add(self, seconds, stats):
        self.seconds += seconds
        self.stats += stats
        return self

    def add_stat(self, stat):
        self.stats.append(stat)
        return self

    def next_play(self, next_poss):
        #TODO: uncomment when other possessions are fixed
        if (self.next_poss not in  ["Buildup", "HalfSpace", "Recovery"]):
            self.next_poss = "Buildup"
        else:
            self.next_poss = next_poss
        return self#Result(self.seconds, next_poss, self.stats, self.goal, self.change_of_poss)

    def turnover(self, next_poss = "Buildup"):
        self.change_of_possession = True
        #TODO: uncomment when other possessions are fixed
        self.next_poss = next_poss
        return self#Result(self.seconds, self.next_poss, self.stats, self.goal, True)

    def add_goal(self):
        self.next_poss = "Buildup"
        self.goal = True
        self.change_of_possession = True
        return self #Result(self.seconds, "Buildup", self.stats, True, True)

    def set_odds(self, num):
        return Result(self.seconds, "Buildup", self.stats.copy(), True, True).set_odds_noCopy(num)

    def set_odds_noCopy(self, odds):
        self.odds = odds
        return self

    def chance_of(self, percent):
        self.odds /= percent
        return self

    def __eq__(self, other):
        for i in range(len(self.items)):
            if (self.items[i] != other.items[i]):
                return False
        return True
    
    def copy(self):
        return Result(self.seconds, self.next_poss, self.stats.copy(), self.goal, self.change_of_possession).set_odds_noCopy(self.odds)

#Result(10, "Buildup", [])

class Possession:
    #self variables
    #team_obj = Team object
    #team = either home or away(opposition as well)
    
    def __init__(self, homeaway, team):
        self.team_obj = team
        self.team = homeaway
        self.gen_opposition()
        self.pos_results = []
        self.prob_list = []
        self.gen_pos_results()
        for item in self.pos_results:
            self.prob_list.append(item.odds)

    
    def gen_opposition(self):
        if (self.team == "home"):
            self.opposition = "away"
            return
        self.opposition = "home"

    def gen_pos_results(self):
        #self.pos_results = {
            #"goal?50": 1,
            #"turnover?10" : 99
        #}
        turnover = Result(10, "Buildup", []).set_odds(50)
        #print(turnover)
        goal = turnover.add(40, []).add_goal().set_odds(10)        
        self.pos_results = [turnover, goal]

    def stat(self, stat, player):
        return stat+str(player)+stat

    def add_shot(self, taker, result_so_far, chances_left, sotarg, gol, Pen = False):
        #get the class(for debugging purposes)
        #print(self.__class__.__name__)

        result = result_so_far
        total = chances_left
        sot = self.team_obj.number_by_rating(total, sotarg/total, 50)
        #print(sot)
        g = self.team_obj.number_by_rating(total, gol/total, 50)
        #print(g)
        if Pen:
            result.add_stat(Stat("PT", taker))
        #missed the target
        self.pos_results.append(
            result.set_odds(total-sot).turnover().add_stat(Stat("s", taker))
        )
        rebound = (sot - g) // 4
        result.add_stat(Stat("N", taker))
        #saved but not caught, rebound in play
        self.pos_results.append(
            result.set_odds(rebound).next_play("Rebound").add_stat(Stat("V", 1, "d"))
        )
        #touched goalie, went out of play, corner kick
        self.pos_results.append(
            result.set_odds(rebound).next_play("Corner").add_stat(Stat("V", 1, "d"))
        )
        
        #save, held onto
        self.pos_results.append(
            result.set_odds(sot - g - 2*rebound).turnover("GoalKick").add_stat(Stat("V", 1, "d")))
        
        #goal
        if Pen:
            result.add_stat(Stat("PM", taker))
        self.pos_results.append(
            result.set_odds(g).add_goal().add_stat(Stat("G", taker)))

    def addprob(self, rizz, odds, stats=[], turnover=False, np = "Buildup", goal=False):
        #have result be a deep copy of rizz
        result = rizz.copy()
        result.set_odds_noCopy(odds)
        for stat in stats:
            result.add_stat(stat)
        if turnover:
            result.turnover(np)
        if goal:
            result.goal()
        # to differentiate from the default parameter
        if np == "buildup":
            result.next_play("Buildup")
        self.pos_results.append(result)
        return

    def result(self):
        rizzult = random.choices(self.pos_results, weights=self.prob_list, k=1)[0]
        answer = {
            "team": self.team,
            "opposition": self.opposition
        }
        answer["result"] = rizzult.next_play
        if (rizzult.goal):
            answer["result"] = "goal"
        answer["seconds"] = rizzult.seconds
        answer["stats"] = rizzult.stats
        answer["possess"] = self.possess(rizzult)
        return answer

    def possess(self, resul):
        answer = self.team + " " + resul.next_poss
        if (resul.change_of_possession):
            return self.opposition + " " + resul.next_poss
        return answer
    
    
class Buildup(Possession):
    name = "Buildup"
    def gen_pos_results(self):
        buildup_patterns = self.team_obj.get_buildup_patterns()
        for buildup_pattern in buildup_patterns["halfspace"]:
            result = Result(3, "HalfSpace", [])
            chances = 10000
            for p in buildup_pattern:
                failure = chances - self.team_obj.number_by_rating(chances, 0.9, "shortpass?"+str(p))
                chances -= failure
                #print(result.stats)
                self.addprob(result, round(failure * 0.4),[Stat("F", p)], True)
                #print(result.stats)
                self.addprob(result, round(failure * 0.6),[Stat("F", p)], True, "Recovery")
                result.add(3, [Stat("P", p)])
            self.addprob(result, chances) 

        for bp in buildup_patterns["thruog"]:
            result = Result(5, "ThruOG", [])
            chances = 1000
            #self.addprob("turnover?"+str(seconds)+"?"+stats+"F"+ bp[0] +"F", 100)
            self.addprob(result, 500, [Stat("F", bp[0])], True)
            #self.addprob("orecovery?"+str(seconds)+"?"+stats+"F"+ bp[0]+"F", 300)
            self.addprob(result, 300, [Stat("F", bp[0])], True, "Recovery")
            #stats += self.stat("P", bp[0])
            result.add(4, [Stat("P", bp[0])])
            #seconds += 4
            #self.addprob("turnover?"+str(seconds)+"?"+stats+"F"+ bp[1]+"F", 300)
            self.addprob(result, 100, [Stat("F", bp[1])], True)
            self.add_shot(bp[1], result, 100, 50, 20)
            
        #print(self.pos_results)

class HalfSpace(Possession):
    name = "HalfSpace"
    def gen_pos_results(self):
        halfspace_patterns = self.team_obj.get_halfspace_patterns()
        for pattern in halfspace_patterns:
            result = Result(3, "HalfSpace", [])
            #seconds = 0
            for p in pattern:
                #seconds += 3
                #self.pos_results["turnover?"+str(seconds)+"?"+stats+"F"+ p+"F"] = 100
                self.addprob(result, 500, [Stat("F", p)], True)
                #stats += "P" + p + "P"
                result.add(3, [Stat("P", p)])
            shooter = random.choice(self.team_obj.formation.attackers)
            self.add_shot(shooter, result, 100, 40, 15)
        

class Recovery(Possession):
    name = "Recovery"

    def gen_pos_results(self):
        recovery_patterns = self.team_obj.get_recovery()
        for recoverer in recovery_patterns:
            #print(recoverer)
            #stats = ""
            #seconds = 5
            result = Result(5, "Recovery", [])
            chances = 9
            if (len(recoverer) == 2):
                result.add_stat(Stat("P", recoverer[1]))
                result.seconds += 2
            self.addprob(result, 5, [Stat("P", recoverer[0])], np="buildup")
            self.addprob(result, 3, [Stat("F", recoverer[0])], True)
            self.addprob(result, 1, [Stat("P", recoverer[0])])


      
class LeftFlank(Possession):
    name = "LeftFlank"

    def gen_pos_results(self):
        lflank = "7"
        defender_lflank= "5"

        seconds = 8
        #possibility one: check back
        result = Result(seconds, "LeftFlank", [])

        self.addprob(result, 5000, [Stat("P", lflank)], np="buildup")

        #possibility two: dribble and run 
        #gets tackled
        self.addprob(result, 1000, [Stat("T", defender_lflank, "d")], True)
        #gets past defender
        result.add_stat(Stat("D", lflank))
        #passes into the half space
        self.addprob(result, 900, [Stat("P", lflank)], True, "HalfSpace")
        #shoots
        #self.pos_results["goal?"+str(seconds)+"?"+stats+"G"+lflank+"G"] = 1
        self.add_shot(lflank, result, 100, 25, 8)
        #possibility three: whip a cross in
        #stats = "?P" + lflank + "P"
        result.add_stat(Stat("CA", lflank))

        #TODO: ADD CROSS LIKELY TO COME
        self.addprob(result, 900, [Stat("F", lflank)], True, "Recovery")
        result.add_stat(Stat("CM", lflank))
        self.add_shot("9", result, 100, 15, 5)
        
        
class Penalty(Possession):
    name = "Penalty"

    def gen_pos_results(self):
        seconds = 60
        taker = str(self.team_obj.get_pentaker())
        result = Result(seconds, "Penalty", [])
        self.add_shot(taker, result, 1000, 950, 760, True)

        


class Corner(Possession):
    name = "Corner"

    def gen_pos_results(self):
        seconds = 30
        #stats = self.stat("P", self.team_obj.corner_taker())
        result = Result(seconds, "Corner", [])
        result.add_stat(Stat("CA", self.team_obj.corner_taker()))
        chances = 10000
        chances_completed = 1600/len(self.team_obj.set_piece_offense())
        chances_on_target = 500/len(self.team_obj.set_piece_offense())
        chances_scored = 200/len(self.team_obj.set_piece_offense())
        #self.pos_results["obuildup?" + str(seconds) + "?"] = 840
        self.addprob(result, 8400, [], True)
        for taker in self.team_obj.set_piece_offense():
            self.add_shot(taker, result, chances_completed, chances_on_target, chances_scored)

class GoalKick(Possession):
    name = "Goal Kick"

    def gen_pos_results(self):
        seconds = 30
        result = Result(seconds, "Recovery", [])
        #self.pos_results["obuidup?"+str(seconds)+"?"+"F1F"] = 1
        self.addprob(result, 1000, [Stat("F", "1")], True)
        #self.pos_results["orecovery?"+str(seconds)+"?"+"P1PF" + "9" + "F"] = 1
        self.addprob(result, 1000, [Stat("P", "1"), Stat("F", "9")], True, "Recovery")
        #self.pos_results["recovery?"+str(seconds)+"?"+"P1PP" + "9" + "P"] = 1
        self.addprob(result, 1000, [Stat("P", "1"), Stat("P", "9")])

class Rebound(Possession):
    name = "Rebound"

    def gen_pos_results(self):
        seconds = 3
        result = Result(seconds, "Rebound", [])
        #shot_taker = self.team_obj.get_rebound()
        shot_taker = "9"

        self.addprob(result, 1000, [], True, "Recovery")
        self.addprob(result, 1000, [], True)
        self.addprob(result, 1000, [], np="HalfSpace")
        self.add_shot(shot_taker, result, 1000, 500, 200)

Possession("", "").result()
