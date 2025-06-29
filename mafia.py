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
                        self.RT = RT(category_num[i], self.known_list[i], self.TI.options, self.TS.options, self.TP_TK.options, 'None')
                    else: 
                        self.RT = RT(category_num[i], self.known_list[i], self.TI.options, self.TS.options, self.TK.options, self.TP.options)
                case "//RM":
                    self.RM = RM(category_num[i],self.known_list[i])
                case "//NK":
                    self.NK = NK(category_num[i],self.known_list[i])
                case "//NE":
                    self.NE = NE(category_num[i],self.known_list[i])
                case "//NB":
                    self.NB = NB(category_num[i],self.known_list[i])
                case "//NE-NB":
                    self.NE_NB = NE_NB(category_num[i],self.known_list[i])
                # RN makes life harder and we usually don't have it so skipping for now and regretting it later
                #case "//RN":
                #   RN_options = self.NK.options + self.NB.options + self.NE.options
                #    self.RN = assignable_category(category_num[i],self.known_list[i], RN_options)
                case "//ANY":
                    ## if we have TP_TK, TP options will already be 'None' from RT.
                    if(hasattr(self,'NB-NE')): 
                        self.NB = category(0)
                        self.NE = category(0)
                    else:
                        self.NB_NE = category(0)
                    self.ANY = ANY(category_num[i], self.known_list[i], self.RT.TI_options, self.RT.TS_options, self.RT.TK_options, self.RT.TP_options,
                                self.RM.options, self.NK.options, self.NE.options, self.NB.options, self.NB_NE.options)                  
class category:
    def __init__(self, num):
        self.num = num
        self.options = 'None'

class assignable_category(category):
    def __init__(self, num, known, options):
        self.num = num
        self.options = []
        self.known = known
        self.roles = []
        self.options = options

        
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

class NE_NB(assignable_category):
    def __init__(self, num, known):
        options = ['Lifebinder', 'Witch', 'Amnesiac', 'Jester', 'Survivor']
        assignable_category.__init__(self, num, known, options)

class RT:
    def __init__(self, num, known, TI_options, TS_options, TK_options, TP_options):
        self.num = num
        self.known = known
        self.roles = []
        self.TI_options = TI_options
        self.TS_options = TS_options
        self.TK_options = TK_options
        self.TP_options = TP_options

        for i in range(len(known)):
            self.roles.append(known[i])
            if "[U]" in self.roles[i]:
                if(self.roles[i] in TK_options):
                    self.TK_options.remove(self.roles[i])
                elif (self.roles[i] in TS_options):
                    self.TS_options.remove(self.role[i])

        for i in range(int (num) - len(known)):
            if (self.TP_options == 'None'): ## combined TP-TK
                roll = random.randint(1,3)
            else:
                roll = random.randint(1,4)

            if roll == 1:
                self.roles.append(random.choice(TI_options))
            elif roll == 2:
                self.roles.append(random.choice(TS_options))
                if "[U]" in self.roles[i]:
                    self.TS_options.remove(self.roles[i]) 
            elif roll == 3:
                self.roles.append(random.choice(TK_options)) 
                if "[U]" in self.roles[i]:
                    self.TK_options.remove(self.roles[i]) 
            else:
                self.roles.append(random.choice(TP_options))

class ANY:
    def __init__(self, num, known, TI_options, TS_options, TK_options, TP_options,
                                RM_options, NK_options, NE_options, NB_options, NE_NB_options):
        self.num = num
        self.known = known
        self.roles = []

        for i in range(len(known)): ## there is most assuredly a better way to do this
            self.roles.append(known[i])
            if "[U]" in self.roles[i]:
                if(self.roles[i] in TK_options):
                    TK_options.remove(self.roles[i])
                elif (self.roles[i] in TS_options):
                    TS_options.remove(self.role[i])
                elif (self.roles[i] in NK_options):
                    NK_options.remove(self.role[i])
                elif (self.roles[i] in RM_options):
                    RM_options.remove(self.role[i])

        if(NB_options == 'None'):
            Other_options = RM_options + NK_options + NE_NB_options
        else:
            Other_options = RM_options + NK_options + NE_options + NB_options

        for i in range(int (num) - len(known)):
            roll = random.randint(1,2)
            if(roll == 1): ## Town 50% of the time
                if (TP_options == 'None'): ## combined TP-TK
                    roll2 = random.randint(1,3)
                else:
                    roll2 = random.randint(1,4)
                ## Town rolls for Town Category first
                if roll2 == 1:
                    self.roles.append(random.choice(TI_options))
                elif roll2 == 2:
                    self.roles.append(random.choice(TS_options))
                    if "[U]" in self.roles[i]:
                        TS_options.remove(self.roles[i]) 
                elif roll2 == 3:
                    self.roles.append(random.choice(TK_options)) 
                    if "[U]" in self.roles[i]:
                        TK_options.remove(self.roles[i]) 
                else:
                    self.roles.append(random.choice(TP_options))

            else: # Some other non-Town role 50% of the time
                ## Rolls randomly among all non-Town roles
                self.roles.append(random.choice(Other_options))
                if "[U]" in self.roles[i]:
                    Other_options.remove(self.roles[i])