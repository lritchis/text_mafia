import random

class game:
    def __init__(self, setup_file):
        file = open(setup_file, 'r')
        categories = []
        category_num = []
        known = []
        self.known_list = []

        while (True):
            current_line = file.readline() ## read next line in setup file
            if not current_line: ## break loop when file ends
                break
            if '//' not in current_line: 
                current_line = current_line.strip() ## remove \n character from line str
                if(current_line.isnumeric()): ## if line is a number, it is the number of players in current category
                    category_num.append(float (current_line))
                    total_categories = len(category_num)
                    self.known_list.append([])
                else:
                    known.append(current_line) ## if line is not a number, it is a known role within the category
                    self.known_list[total_categories - 1] = known

            else: ## all category lines begin with //
                known = []
                categories.append(current_line.strip())
        self.total_players = sum(category_num)

        self.known_players = 0
        for i in range(len(categories)):
            self.known_players = self.known_players + len(self.known_list[i])

        ## Instantiate all categories
        for i in range(len(categories)):
            match categories[i]:
                case "//JAL":
                    self.JAL = category(1)
                case "//GF":
                    self.GF = category(1)
                case "//TI":
                    self.TI = TI(category_num[i],self.known_list[i])
                case "//TS":
                    self.TS = TS(category_num[i],self.known_list[i])
                case "//TP":
                    self.TP = TP(category_num[i],self.known_list[i])
                case "//TK":
                    self.TK = TK(category_num[i],self.known_list[i])
                case '//TP-TK':
                    self.TP_TK = TP_TK(category_num[i],self.known_list[i])
                case "//RT":
                    if(hasattr(self,'TP_TK')): ## specifically handle case where we combine TP and TK
                        RT_options = self.TI.options + self.TS.options + self.TP_TK.options
                    else: 
                        RT_options = self.TI.options + self.TS.options + self.TP.options + self.TK.options
                    self.RT = assignable_category(category_num[i], self.known_list[i], RT_options)
                case "//RM":
                    self.RM = RM(category_num[i],self.known_list[i])
                case "//NK":
                    self.NK = NK(category_num[i],self.known_list[i])
                case "//NE":
                    self.NE = NE(category_num[i],self.known_list[i])
                case "//NB":
                    self.NB = NB(category_num[i],self.known_list[i])
                case "//NB-NE":
                    self.NB_NE = NB_NE(category_num[i],self.known_list[i])
                case "//RN":
                    RN_options = self.NK.options + self.NB.options + self.NE.options
                    self.RN = assignable_category(category_num[i],self.known_list[i], RN_options)
                case "//ANY": ## need to fix the ANY method, it is not just a random choice from role list
                    Town_options = self.RT.options 
                    if(hasattr(self,'RN')):
                        Other_options = self.RM.options + self.RN.options
                    elif (hasattr(self,'NB_NE')):
                        Other_options = self.RM.options + self.NK.options + self.NE_NB.options
                    else:
                        Other_options = self.RM.options + self.NK.options + self.NB.options + self.NE.options
                    self.ANY = ANY(category_num[i],self.known_list[i], Town_options, Other_options)                    
class category:
    def __init__(self, num):
        self.num = num

class assignable_category(category):
    def __init__(self, num, known, options):
        self.num = num
        self.options = []
        self.known = known
        self.roles = []
        self.options = options

        #print(len(known))
        for i in range(len(known)):
            self.roles.append(known[i])
            if "[U]" in self.roles[i]:
                self.options.remove(self.roles[i])

        for i in range(int (num) - len(known)):
            self.roles.append(random.choice(self.options))
            if "[U]" in self.roles[i]:
                self.options.remove(self.roles[i])

class TI(assignable_category):
    def __init__(self, num, known): 
        options = ['Lookout','Investigator','Scientist','Spy','Tracker']
        assignable_category.__init__(self, num, known, options)

class TS(assignable_category):
    def __init__(self, num, known):
        options = ['Escort','Mayor [U]','Medium [U]','Retributionist [U]','Transporter'] 
        assignable_category.__init__(self, num, known, options)

class TP(assignable_category):
    def __init__(self, num, known):
        options = ['Bodyguard', ' Doctor']
        assignable_category.__init__(self, num, known, options)

class TK(assignable_category):
    def __init__(self, num, known):
        options = ['Veteran [U]', 'Vigilante']
        assignable_category.__init__(self, num, known, options)

class TP(assignable_category):
    def __init__(self, num, known):
        options = ['Bodyguard', 'Doctor']
        assignable_category.__init__(self, num, known, options)

class TP_TK(assignable_category):
    def __init__(self, num, known):
        options = ['Bodyguard', 'Doctor', 'Veteran [U]', 'Vigilante']
        assignable_category.__init__(self, num, known, options)

class RM(assignable_category):
    def __init__(self, num, known):
        options = ['Blackmailer', 'Consigliere', 'Consort', 'Disguiser', 'Janitor [U]', 'Mafioso', 'Politician [U]']
        assignable_category.__init__(self, num, known, options)

class NK(assignable_category):
    def __init__(self, num, known):
        options = ['Arsonist', 'Serial Killer', 'Shaman [U]', 'Werewolf [U]']
        assignable_category.__init__(self, num, known, options)

class NE(assignable_category):
    def __init__(self, num, known):
        options = ['Lifebinder', 'Witch']
        assignable_category.__init__(self, num, known, options)

class NB(assignable_category):
    def __init__(self, num, known):
        options = ['Amnesiac', 'Jester', 'Survivor']
        assignable_category.__init__(self, num, known, options)

class NB_NE(assignable_category):
    def __init__(self, num, known):
        options = ['Lifebinder', 'Witch', 'Amnesiac', 'Jester', 'Survivor']
        assignable_category.__init__(self, num, known, options)

class ANY:
    def __init__(self, num, known, Town_options, Other_options):
        self.num = num
        self.known = known
        self.roles = []
        self.Town_options = Town_options
        self.Other_options = Other_options

        for i in range(len(known)):
            self.roles.append(known[i])

        for i in range(int (num) - len(known)):
            roll = random.randint(1,2)
            if(roll == 1): ## Town 50% of the time
                self.roles.append(random.choice(self.Town_options))
                if "[U]" in self.roles[i]:
                    self.Town_options.remove(self.roles[i])
            else: # Some other non-Town role 50% of the time
                self.roles.append(random.choice(self.Other_options))
                if "[U]" in self.roles[i]:
                    self.Other_options.remove(self.roles[i])