# Affine Encryption/Decryption Implementation PoC

# Global Constants - capitalised to denote a constant and easily accessible in any part of the program.
ALPHABET_TO_NUM = { # Alphabetical to Numerical mappings - used for simple conversion. 
    "A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7,
    "I":8, "J":9, "K":10, "L":11, "M":12, "N":13, "O":14,
    "P":15, "Q":16, "R":17, "S":18, "T":19, "U":20, "V":21,
    "W":22, "X":23, "Y":24, "Z":25
} # This makes it easier to map alphabetic letters that the user entered to their numerical equivalents (0-25), without accidentally converting these to their ASCII representations instead (which Python does by default).

NUM_TO_ALPHABET = {value: key for key, value in ALPHABET_TO_NUM.items()} # Numeric to Alphabetic mappings. This reverses the Key:Value pairs in the above dictionary, saving more complex lines of code. ["A":0] -> [0:"A"]
 # Also note that these dictionaries don't contain special characters/symbols. Therefore, this automatically excludes any special characters or punctuation in input without any additional code to do so.

KEY_DOMAIN = [ # The range for which the key 'A' can reside in. 
    1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
] # If the user inputs a non-prime value for 'A', this can affect the correctness of the program. Therefore, this can catch any invalid integers and ensure the encryption/decryption process works as intended.

N = len(ALPHABET_TO_NUM) # Yields the value '26' for ease of access. This value will be required numerous times throughout different functions, and by having a global scope this can be accessed anywhere in any part of the program instead of being redeclared numerous times.

# Additional Functions - in order of relevance #
def encrypt(m_numeric, keys):
    (a, b) = (keys["A"], keys["B"])
    ciphertext = []
    for m_num in m_numeric:
        if m_num == ' ': # This accounts for any part of the text that contains whitespace.
            ciphertext.append(' ') # In doing this, spaces can be easily retained. For example, if a user wishes to encrypt a sentence, the separation between each word will be appended back into the ciphertext.
        else:
            c = ((a*m_num)+ b) % N
            ciphertext.append(c) 
    return ciphertext

def decrypt(c_numeric, keys):
    (a, b) = (keys["A"], keys["B"])
    plaintext = []
    for c_num in c_numeric:
        if c_num == ' ':
            plaintext.append(' ')
        else: 
            p = (c_num - b) * multInv(a, N) % N
            plaintext.append(p)
    return plaintext

def euclidGCD(a, m): # For simplicity, we have created a single-line implementation of the Euclidian Algorithm. Despite the simplicity, this function yields the correct result as per testing.
    return a if m == 0 else euclidGCD(m, (a % m)) # This is recursive, similar to that of the Euclidean Algorithm. This recursively performs 'a mod m' until the remainder equals to zero - in which case the previous remainder is returned. This is a very trivial implementation, but works with minimal code (in this case 1 LoC).

def multInv(a, m): # A very simple implementation of the Extended Euclidian Algorithm to calculate the modular multiplicative inverse of 'A'. 
    try:
        inv = pow(a, -1, m) # a^-1 mod m - usefully, the pow() function can calculate this without any need for addtional lines of code. This can reduce redundancy and additional complexty, but still maintains correctness and accuracy (as tried and tested).
        return inv
    except ValueError: # The pow() function throws a ValueError if no inverse exists for 'a' (that is, no inverse can be found under 'a * a^1 mod m')
        return False # In doing this, this returns False gracefully instead of raising a 'ValueError' exception and disrupting the correctness of the program.

def convert(list, type): # This is used to easily convert a string to its numerical equivalent and vice-versa seemlessly without complex, repeated code. For repeated use, I have implemented this as a function so that any conversion can be easily facilitated in any part of the program.
    if "STRING" in type: # String-to-Numerics conversion; note how this usefully maintains whitespace and eliminates special characters in the process. 
        str_to_num = [] # i.e. ["A", "B"] -> [0, 1]. 
        for char in list:
            if char in ALPHABET_TO_NUM:
                str_to_num.append(ALPHABET_TO_NUM[char]) # This is where each alphabet-to-numerical conversion is collated into an array/list, for simpler management of each individual character representation.
            if char == ' ':
                str_to_num.append(' ')
        return str_to_num        
    elif "INT" in type: # Numerics-to-String conversion: Once the Encryption/Decryption is carried out on the numerical values, these are then converted back to their alpabetic representations to be returned to the user. 
        int_to_str = [] # i.e. [0, 1] -> ["A", "B"].
        for num in list:
            if num == ' ':
                int_to_str.append(' ')
            else:
                int_to_str.append(NUM_TO_ALPHABET[num])
        return int_to_str    
    elif "LIST" in type: # The intention of this is to re-join characters from the array in to a more appropriate string format after Encryption/Decryption. This avoids repitition of code, also making this a suitable format to be easily returned to the user. 
        list_to_str = ''
        return(list_to_str.join(list))  # i.e. ["A", "B"] -> "AB".
    else:
        return False     

def validateA(a): # This is also used to minimise repitition. If 'A' is not coprime with 26, Decryption is infeasible and the program's correctness is affected. Therefore, the invalid value returns an error message to the user.  
    return True if (euclidGCD(a, N) == 1) and (a < N) else False   # In this case, the program checks to see if 'A' is coprime with 26 and within the modulo space, by utilising the euclidGCD function to check if this results to 1.

def validateB(b):
    return True if b < N else False

def exitProgram(): # This function causes the program to exit gracefully. This is to minimise repition of the same code in several parts of the program; instead making this invokable in any part of the program in only one line (LoC).
    try:
        input('\nPress ENTER to exit')
        exit(1)
    except KeyboardInterrupt:
        print("\n")
        exit(1)

# Main Function #
def main():
    try:
        # Dialogue Menu # 
        print("""Affine Cipher Implementation\n\nOptions:
        1. Encrypt
        2. Decrypt
        3. Simple Brute Force 
        4. Advanced Brute Force
        5. Kasiski Analysis
        99. Exit\n""")
        # User Input #
        choice = input("[+] Please enter your choice of operation [1/2/3/4/5/99]: ")
        if int(choice) == 1:
            # Option 1: Encryption #
            print("\nYou selected: Encryption")
            m_str = input("[+] Please enter a string: ").upper() # This converts the inputted string to uppercase, to be properly compared with the ALPHABET_TO_NUM dictionary.
            exitProgram() if m_str == '' else None
            m_numeric = [] # This will store the 0-23 mappings of the inputted string 'm_str'. i.e. "HELLO" -> [7, 4, 11, 11, 14], so that Encryption/Decryption can be carried out on each letter.
            m_numeric = convert(m_str, "STRING") # This converts the string into numerics from 0-25 via a function named 'convert()' so that the Encryption function can be computed on each character accordingly. 

            a = int(input("[+] Please enter Key A: "))
            if validateA(a): # Validation check to ensure that 'a' is coprime with 'N'(26). If it is, this will be assigned; if not, an error will return - with the program exiting gracefully.
                keys = {"A":a}
            else:
                print("[!] Please choose a key in the accepted range: {}".format(KEY_DOMAIN))
                exitProgram()

            b = int(input("[+] Please enter Key B: "))
            if validateB(b): # Validation check to ensure that 'b' will not go outside of the expected range 0-26; otherwise this may yield undesirable behaviours and incorrect results.
                keys["B"] = b
            else: 
                print("[!] Please choose acceptable key in range 0-25")
                exitProgram()

            ciphertext = encrypt(m_numeric, keys)
            ciphertext = convert(ciphertext, "INT") 
            ciphertext = convert(ciphertext, "LIST")
            print("\nYour ciphertext is {}".format(ciphertext) + "\nand your keys are: {}\n".format(keys))
        if int(choice) == 2:
            # Option 2: Decryption #
            print("\nYou selected: Encryption")
            c_str = input("[+] Please enter ciphertext: ").upper()
            exitProgram() if c_str == '' else None
            c_numeric = []
            c_numeric = convert(c_str, "STRING")

            dec_a = int(input("[+] Please enter Key A: "))
            if validateA(dec_a):
                keys = {"A":dec_a}
            else:
                print("[!] Please choose a key in the accepted range: {}".format(KEY_DOMAIN))
                exitProgram()

            dec_b = int(input("[+] Please enter Key B: "))
            if validateB(dec_b): 
                keys["B"] = dec_b
            else: 
                print("[!] Please choose acceptable key in range 0-25")
                exitProgram()

            plaintext = decrypt(c_numeric, keys)
            plaintext = convert(plaintext, "INT") 
            plaintext = convert(plaintext, "LIST")
            print("\nYour plaintext is {}\n".format(plaintext))
        if int(choice) == 3:
            # Option 3: Simple Brute Force Mode #
            print("\nYou selected: Simple Brute Force")
            c_str = input("[+] Please supply the ciphertext to brute force: ").upper() 
            exitProgram() if c_str == '' else None
            c_numeric = [] 
            c_numeric = convert(c_str, "STRING") 
            plaintexts = []
            print("312 Possible Combinations.\n")
            input("Press ENTER to continue.")
            try:
                for a in KEY_DOMAIN: # O(N^2) time complexity 
                    for b in range(0,N): # For every A, For every B - this will exercise each possible combination of both A and B (312).
                        keys = {"A":a, "B":b}
                        plaintext = decrypt(c_numeric, keys)
                        plaintext = convert(plaintext, "INT") 
                        plaintext = convert(plaintext, "LIST")
                        print("-" * 15)
                        print("[*] Trying keys " + str(a) + " and " + str(b) + " on '" + c_str + "':" + "\n{}".format(plaintext))
                        plaintexts.append(plaintext)
                print("\nBrute Force Completed.")
            except KeyboardInterrupt:
                print("\nBrute Force Attack Interrupted.\n")
                exitProgram()    
            choice = input("\n[+] Would you like to output results to a file? [Y/N]: ").upper() # Due to there being 312 results in the output, the option to save this to a file is offered to the user (for further analysis). 
            if choice == 'Y':                                                                   # Additionally, this will be included in the Advanced Brute Force mode.
                output_file = open("affine_results.txt", "w")
                for line in plaintexts:
                    output_file.write("-"*len(line) + "\n" + line + "\n")
                print("Output sent to affine_results.txt\n")   
                exitProgram() 
            else:
                exitProgram()
        if int(choice) == 4:
            # Option 4: Advanced Brute Force Mode #
            print("\nYou selected: Advanced Brute Force") # This is an additional feature that attempts to refine the brute force results and find a more specific plaintext. This is more suitable compared to displaying 312 results. 
            c_str = input("[+] Please supply the ciphertext to brute force: ").upper() 
            exitProgram() if c_str == '' else None
            c_numeric = [] 
            c_numeric = convert(c_str, "STRING") 
            plaintexts = {}
            plaintext_keys = {}
            letter_frequency_scores = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 
                                    'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 
                                    'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 
                                    'Q': 0.10, 'Z': 0.07} # The Kasiski Analysis will be discussed in more depth in Choice 5, as to the reasoning for using this dictionary.
            # This utilises a combination of a Dictionary-Attack and Kasiski Analysis in order to find a more sensical, English word from the plaintexts produced.
            
            print("312 Possible Combinations.\nPress Ctrl+C to stop.\n")
            input("Press ENTER to continue.")
            try:
                for a in KEY_DOMAIN: # O(N^2) time complexity 
                    for b in range(0,N):
                        keys = {"A":a, "B":b}
                        plaintext = decrypt(c_numeric, keys)
                        plaintext = convert(plaintext, "INT") 
                        plaintext = convert(plaintext, "LIST")

                        letter_scores = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0, "G":0, "H":0,
                        "I":0, "J":0, "K":0, "L":0, "M":0, "N":0, "O":0,
                        "P":0, "Q":0, "R":0, "S":0, "T":0, "U":0, "V":0,
                        "W":0, "X":0, "Y":0, "Z":0} # This is a function of the Kasiski Analysis method. This is to assist in calculating the commonality of each English letter in the plaintext.
                        # The theory here is that the more common English letters are contained within a plaintext, the more likely the plaintext resembles an English word. 

                        dictionary = ["ABILITY", "ABLE", "ABOUT", "ABOVE", "ACCEPT", "ACCORDING", "ACCOUNT", "ACROSS", "ACT", "ACTION", "ACTIVITY", "ACTUALLY", "ADD", "ADDRESS", "ADMINISTRATION", "ADMIT", "ADULT", "AFFECT", "AFTER", "AGAIN", "AGAINST", "AGE", "AGENCY", "AGENT", "AGO", "AGREE", "AGREEMENT", "AHEAD", "AIR", "ALGORITHM", "ALL", "ALLOW", "ALMOST", "ALONE", "ALONG", "ALREADY", "ALSO", "ALTHOUGH", "ALWAYS", "AMERICAN", "AMONG", "AMOUNT", "ANALYSIS", "AND", "ANIMAL", "ANOTHER", "ASSUME", "ANSWER", "ANY", "ANYONE", "ANYTHING", "APPEAR", "APPLY", "APPROACH", "AREA", "ARGUE", "ARM", "AROUND", "ARRIVE", "ART", "ARTICLE", "ARTIST", "ASK", "ASSUME", "ATTACK", "ATTENTION", "ATTORNEY", "AUDIENCE", "AUTHOR", "AUTHORITY", "AVAILABLE", "AUTHENTIC", "AVOID", "AWAY", "BABY", "BACK", "BAD", "BAG", "BALL", "BANK", "BAR", "BASE", "BEAT", "BEAUTIFUL", "BECAUSE", "BECOME", "BED", "BEFORE", "BEGIN", "BEHAVIOR", "BEHIND", "BELIEVE", "BENEFIT", "BEST", "BETTER", "BETWEEN", "BEYOND", "BIG", "BILL", "BILLION", "BIT", "BLACK", "BLOCK", "BLOOD", "BLUE", "BOARD", "BODY", "BOOK", "BORN", "BOTH", "BOX", "BOY", "BREAK", "BRING", "BROTHER", "BUDGET", "BUILD", "BUILDING", "BUSINESS", "BUT", "BUY", "CALL", "CAMERA", "CAMPAIGN", "CAN", "CANCER", "CANDIDATE", "CAPITAL", "CAR", "CARD", "CARE", "CAREER", "CARRY", "CASE", "CATCH", "CAUSE", "CELL", "CENTER", "CENTRAL", "CENTURY", "CERTAIN", "CERTAINLY", "CHAIN", "CHAIR", "CHALLENGE", "CHANCE", "CHANGE", "CHARACTER", "CHARGE", "CHECK", "CHILD", "CHOICE", "CHOOSE", "CHURCH", "CITIZEN", "CITY", "CIVIL", "CLAIM", "CLASS", "CLEAR", "CLEARLY", "CLOSE", "COACH", "COLD", "COLLECTION", "COLLEGE", "COLOR", "COME", "COMMERCIAL", "COMMON", "COMMUNITY", "COMPANY", "COMPARE", "COMPUTER", "CONCERN", "CONDITION", "CONFERENCE", "CONFIDENTIAL", "CONGRESS", "CONSIDER", "CONSUMER", "CONTAIN", "CONTINUE", "CONTROL", "COST", "COULD", "COUNTRY", "COUPLE", "COURSE", "COURT", "COVER", "CREATE", "CRIME", "CRYPT", "CULTURAL", "CULTURE", "CUP", "CURRENCIES", "CURRENT", "CUSTOMER", "CRYPT", "CUT", "DARK", "DATA", "DAUGHTER", "DAY", "DEAD", "DEAL", "DEATH", "DEBATE", "DECADE", "DECIDE", "DECISION", "DECRYPT", "DEEP", "DEFENSE", "DEGREE", "DEMOCRAT", "DEMOCRATIC", "DESCRIBE", "DESIGN", "DESPITE", "DETAIL", "DETERMINE", "DEVELOP", "DEVELOPMENT", "DIE", "DIFFERENCE", "DIFFERENT", "DIFFICULT", "DINNER", "DIRECTION", "DIRECTOR", "DISCOVER", "DISCRETE", "DISCUSS", "DISCUSSION", "DISEASE", "DOCTOR", "DOG", "DOOR", "DOWN", "DRAW", "DREAM", "DRIVE", "DROP", "DRUG", "DURING", "EACH", "EARLY", "EAST", "EASY", "EAT", "ECONOMIC", "ECONOMY", "EDGE", "EDUCATION", "EFFECT", "EFFORT", "EIGHT", "EITHER", "ELECTION", "ELSE", "EMPLOYEE", "ENCRYPT", "END", "ENERGY", "ENJOY", "ENOUGH", "ENTER", "ENTIRE", "ENVIRONMENT", "ENVIRONMENTAL", "ESPECIALLY", "ESTABLISH", "EVEN", "EVENING", "EVENT", "EVER", "EVERY", "EVERYBODY", "EVERYONE", "EVERYTHING", "EVIDENCE", "EXACTLY", "EXAMPLE", "EXECUTIVE", "EXIST", "EXPECT", "EXPERIENCE", "EXPERT", "EXPLAIN", "EYE", "FACE", "FACT", "FACTOR", "FAIL", "FALL", "FAMILY", "FAR", "FAST", "FATHER", "FEAR", "FEDERAL", "FEEL", "FEELING", "FEW", "FIELD", "FIGHT", "FIGURE", "FILL", "FILM", "FINAL", "FINALLY", "FINANCIAL", "FIND", "FINE", "FINGER", "FINISH", "FIRE", "FIRM", "FIRST", "FISH", "FIVE", "FLOOR", "FLY", "FOCUS", "FOLLOW", "FOOD", "FOOT", "FOR", "FORCE", "FOREIGN", "FORGET", "FORM", "FORMER", "FORWARD", "FOUR", "FREE", "FRIEND", "FROM", "FRONT", "FULL", "FUNCTION", "FUND", "FUTURE", "GAME", "GARDEN", "GAS", "GENERAL", "GENERATION", "GET", "GIRL", "GIVE", "GLASS", "GOAL", "GOOD", "GOVERNMENT", "GREAT", "GREEN", "GROUND", "GROUP", "GROW", "GROWTH", "GUESS", "GUN", "GUY", "HAIR", "HALF", "HAND", "HANG", "HAPPEN", "HAPPY", "HARD", "HAVE", "HEAD", "HEALTH", "HEAR", "HEART", "HEAT", "HEAVY", "HELLO", "HELP", "HER", "HERE", "HERSELF", "HIGH", "HIM", "HIMSELF", "HIS", "HISTORY", "HIT", "HOLD", "HOME", "HOPE", "HOSPITAL", "HOT", "HOTEL", "HOUR", "HOUSE", "HOW", "HOWEVER", "HUGE", "HUMAN", "HUNDRED", "HUSBAND", "IDEA", "IDENTIFY", "IMAGE", "IMAGINE", "IMPACT", "IMPORTANT", "IMPROVE", "INCLUDE", "INCLUDING", "INCREASE", "INDEED", "INDICATE", "INDIVIDUAL", "INDUSTRY", "INFORMATION", "INFRASTRUCTURE", "INSIDE", "INSTEAD", "INSTITUTION", "INTEGRITY", "INTEREST", "INTERESTING", "INTERNATIONAL", "INTERVIEW", "INTO", "INVESTMENT", "INVOLVE", "ISSUE", "ITEM", "ITS", "ITSELF", "JOB", "JOIN", "JUST", "KEEP", "KEY", "KID", "KILL", "KIND", "KITCHEN", "KNOW", "KNOWLEDGE", "LAND", "LANGUAGE", "LARGE", "LAST", "LATE", "LATER", "LAUGH", "LAW", "LAWYER", "LAY", "LEAD", "LEADER", "LEARN", "LEAST", "LEAVE", "LEFT", "LEG", "LEGAL", "LESS", "LET", "LETTER", "LEVEL", "LIE", "LIFE", "LIGHT", "LIKE", "LIKELY", "LINE", "LIST", "LISTEN", "LITTLE", "LIVE", "LOCAL", "LONG", "LOOK", "LOSE", "LOSS", "LOT", "LOVE", "LOW", "MACHINE", "MAGAZINE", "MAIN", "MAINTAIN", "MAJOR", "MAJORITY", "MAKE", "MAN", "MANAGE", "MANAGEMENT", "MANAGER", "MANY", "MARKET", "MARRIAGE", "MATERIAL", "MATTER", "MAY", "MAYBE", "MEAN", "MEASURE", "MEDIA", "MEDICAL", "MEET", "MEETING", "MEMBER", "MEMORY", "MENTION", "MESSAGE", "METHOD", "MIDDLE", "MIGHT", "MILITARY", "MILLION", "MIND", "MINUTE", "MISS", "MISSION", "MODEL", "MODERN", "MOMENT", "MONEY", "MONTH", "MORE", "MORNING", "MOST", "MOTHER", "MOUTH", "MOVE", "MOVEMENT", "MOVIE", "MRS", "MUCH", "MUSIC", "MUST", "MYSELF", 
                        "NAME", "NATION", "NATIONAL", "NATURAL", "NATURE", "NEAR", "NEARLY", "NECESSARY", "NEED", "NETWORK", "NEVER", "NEW", "NEWS", "NEWSPAPER", "NEXT", "NICE", "NIGHT", "NONE", "NOR", "NORTH", "NOT", "NOTE", "NOTHING", "NOTICE", "NOW", "N'T", "NUMBER", "OCCUR", "OFF", "OFFER", "OFFICE", "OFFICER", "OFFICIAL", "OFTEN", "OIL", "OLD", "ONCE", "ONE", "ONLY", "ONTO", "OPEN", "OPERATION", "OPPORTUNITY", "OPTION", "ORDER", "ORGANIZATION", "OTHER", "OTHERS", "OUR", "OUT", "OUTSIDE", "OVER", "OWN", "OWNER", "PAGE", "PAIN", "PAINTING", "PAPER", "PARENT", "PART", "PARTICIPANT", "PARTICULAR", "PARTICULARLY", "PARTNER", "PARTY", "PASS", "PAST", "PATIENT", "PATTERN", "PAY", "PEACE", "PEOPLE", "PER", "PERFORM", "PERFORMANCE", "PERHAPS", "PERIOD", "PERSON", "PERSONAL", "PHONE", "PHYSICAL", "PICK", "PICTURE", "PIECE", "PLACE", "PLAN", "PLANT", "PLAY", "PLAYER", "POINT", "POLICE", "POLICY", "POLITICAL", "POLITICS", "POOR", "POPULAR", "POPULATION", "POSITION", "POSITIVE", "POSSIBLE", "POWER", "PRACTICE", "PREPARE", "PRESENT", "PRESIDENT", "PRESSURE", "PRETTY", "PREVENT", "PRICE", "PRIVATE", "PROBABLY", "PROBLEM", "PROCESS", "PRODUCE", "PRODUCT", "PRODUCTION", "PROFESSIONAL", "PROFESSOR", "PROGRAM", "PROJECT", "PROOF", "PROPERTY", "PROTECT", "PROVE", "PROVIDE", "PUBLIC", "PULL", "PURPOSE", "PUSH", "PUT", "QUALITY", "QUESTION", "QUICKLY", "QUITE", "RACE", "RADIO", "RAISE", "RANGE", "RATE", "RATHER", "REACH", "READ", "READY", "REAL", "REALITY", "REALIZE", "REALLY", "REASON", "RECEIVE", "RECENT", "RECENTLY", "RECOGNIZE", "RECORD", "RED", "REDUCE", "REFLECT", "REGION", "RELATE", "RELATIONSHIP", "RELIGIOUS", "REMAIN", "REMEMBER", "REMOVE", "REPORT", "REPRESENT", "REPUBLICAN", "REQUIRE", "RESEARCH", "RESOURCE", "RESPOND", "RESPONSE", "RESPONSIBILITY", "REST", "RESULT", "RETURN", "REVEAL", "RICH", "RIGHT", "RISE", "RISK", "ROAD", "ROCK", "ROLE", "ROOM", "RULE", "RUN", "SAFE", "SAME", "SAVE", "SAY", "SCENE", "SCHOOL", "SCIENCE", "SCIENTIST", "SCORE", "SEA", "SEASON", "SEAT", "SECOND", "SECRECY", "SECRET", "SECTION", "SECURITY", "SEE", "SEEK", "SEEM", "SELL", "SEND", "SENIOR", "SENSE", "SERIES", "SERIOUS", "SERVE", "SERVICE", "SET", "SEVEN", "SEVERAL", "SEX", "SEXUAL", "SHAKE", "SHARE", "SHE", "SHIFT", "SHOOT", "SHORT", "SHOT", "SHOULD", "SHOULDER", "SHOW", "SIDE", "SIGN", "SIGNIFICANT", "SIMILAR", "SIMPLE", "SIMPLY", "SINCE", "SING", "SINGLE", "SISTER", "SIT", "SITE", "SITUATION", "SIX", "SIZE", "SKILL", "SKIN", "SMALL", "SMILE", "SOCIAL", "SOCIETY", "SOLDIER", "SOME", "SOMEBODY", "SOMEONE", "SOMETHING", "SOMETIMES", "SON", "SONG", "SOON", "SORT", "SOUND", "SOURCE", "SOUTH", "SOUTHERN", "SPACE", "SPEAK", "SPECIAL", "SPECIFIC", "SPEECH", "SPEND", "SPORT", "SPRING", "STAFF", "STAGE", "STAND", "STANDARD", "STAR", "START", "STATE", "STATEMENT", "STATION", "STAY", "STEP", "STILL", "STOCK", "STOP", "STORE", "STORY", "STRATEGY", "STREET", "STRONG", "STRUCTURE", "STUDENT", "STUDY", "STUFF", "STYLE", "SUBJECT", "SUCCESS", "SUCCESSFUL", "SUCH", "SUDDENLY", "SUFFER", "SUGGEST", "SUMMER", "SUPPORT", "SURE", "SURFACE", "SYSTEM", "SYMMETRIC", "TABLE", "TAKE", "TALK", "TASK", "TAX", "TEACH", "TEACHER", "TEAM", "TECHNOLOGY", "TELEVISION", "TELL", "TEN", "TEND", "TERM", "TEST", "THAN", "THANK", "THAT", "THE", "THEIR", "THEM", "THEMSELVES", "THEN", "THEORY", "THERE", "THESE", "THEY", "THING", "THINK", "THIRD", "THIS", "THOSE", "THOUGH", "THOUGHT", "THOUSAND", "THREAT", "THREE", "THROUGH", "THROUGHOUT", "THROW", "THUS", "TIME", "TODAY", "TOGETHER", "TONIGHT", "TOO", "TOP", "TOTAL", "TOUGH", "TOWARD", "TOWN", "TRADE", "TRADITIONAL", "TRAINING", "TRAVEL", "TREAT", "TREATMENT", "TREE", "TRIAL", "TRIP", "TROUBLE", "TRUE", "TRUTH", "TRY", "TURN", "TWO", "TYPE", "UNDER", "UNDERSTAND", "UNIT", "UNTIL", "UPON", "USE", "USUALLY", "VALUE", "VARIOUS", "VERY", "VICTIM", "VIEW", "VIOLENCE", "VISIT", "VOICE", "VOTE", "WAIT", "WALK", "WALL", "WANT", "WAR", "WATCH", "WATER", "WAY", "WEAPON", "WEAR", "WEEK", "WEIGHT", "WELL", "WEST", "WESTERN", "WHAT", "WHATEVER", "WHEN", "WHERE", "WHETHER", "WHICH", "WHILE", "WHITE", "WHO", "WHOLE", "WHOM", "WHOSE", "WHY", "WIDE", "WIFE", "WILL", "WIN", "WIND", "WINDOW", "WISH", "WITH", "WITHIN", "WITHOUT", "WOMAN", "WONDER", "WORD", "WORK", "WORKER", "WORLD", "WORRY", "WOULD", "WRITE", "WRITER", "WRONG", "YARD", "YEAH", "YEAR", "YES", "YET", "YOU", "YOUNG", "YOUR", "YOURSELF"];
                        # This is an assortment of English words from A-Z in the form of an array. Each plaintext will be interrogated to identify if any of the above words are found in the results.
                        count = 0 # Count is used to identify how often the above English words are found in the plaintext - this will be used to rank the results according to the most likely correct plaintext result.

                        for x in dictionary:
                            if (x in plaintext or plaintext in x): # This searches in the above dictionary, identifying if any of the items are found in the plaintext.
                                count += len(x) # If so, a score is added. 
                                for m in plaintext:
                                    if m in letter_frequency_scores:
                                        letter_scores[m] += letter_frequency_scores[m]
                                score = sum(letter_scores.values())
                                if len(plaintext) < 6: # In the results, the frequency scores may be varied based upon the length of the plaintext. This accounts for this margin of error, broadening the results if the plaintext is a shorter word.
                                    if score > (len(plaintext) * 6):
                                        plaintexts.update({plaintext:[score, count]}) # The reasoning for this, is because it is desirable to display the plaintext and its corresponding keys in the output. However, because we are also calculating the frequency, this cannot be stored within the same data structure at the risk of overlap and access. 
                                        # As a result, we will use two separate dictionaries; one for storing the plaintext and keys (A, B), and one for storing the plaintext and its frequency score.
                                        plaintext_keys.update({plaintext:[a, b]})
                                        break
                                else: 
                                    if score > (len(plaintext) * 8):
                                        plaintexts.update({plaintext:[score, count]})
                                        plaintext_keys.update({plaintext:[a, b]})
                                        break
                            else:
                                pass         
                        plaintexts_sorted = sorted(zip(plaintexts.values(), plaintexts.keys()), reverse=True) # This efficiently stores each result in descending order, placing the most likely correct plaintext at the top of the results.

                for key, value in plaintexts_sorted:
                    print("-" * 15)
                    print("[*] Trying keys " + str(plaintext_keys[value][0]) + " and " + str(plaintext_keys[value][1]) + " on '" + c_str + "':" + "\n{}".format(value))

                print("\nBrute Force Completed.")
            except KeyboardInterrupt:
                print("\n[!] Brute Force Attack Interrupted.\n")
                exitProgram()    
            choice = input("\n[+] Would you like to output results to a file? [Y/N]: ").upper()
            if choice == 'Y':
                output_file = open("affine_results.txt", "w")
                for line in plaintexts:
                    output_file.write("-"*len(line) + "\n" + line + "\n")
                print("Output sent to affine_results.txt\n")   
                exitProgram() 
            else:
                exitProgram()      
        if int(choice) == 5:
            # Option 5: Frequency Analysis #
            print("\nYou selected: Kasiski Method")
            c_str = input("[+] Please supply the ciphertext to analyse: ").upper() 
            exitProgram() if c_str == '' else None
            c_numeric = [] 
            c_numeric = convert(c_str, "STRING") 
            plaintexts = {}
            letter_frequency_scores = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 
            'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 
            'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 
            'Q': 0.10, 'Z': 0.07} # This table contains a frequency score, based upon empirical data. 
            # This will help calculate a weighted score, based upon the frequency of occuring letters of a plaintext. The more common letters appear, the higher the score will be. By doing this, an English word is more likely to be extracted as a result.
            # http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html 
            try:
                for a in KEY_DOMAIN: # O(N^2) time complexity 
                    for b in range(1,N):
                        keys = {"A":a, "B":b}
                        plaintext = decrypt(c_numeric, keys)
                        plaintext = convert(plaintext, "INT") 
                        plaintext = convert(plaintext, "LIST")

                        letter_scores = {"A":0, "B":0, "C":0, "D":0, "E":0, "F":0, "G":0, "H":0,
                                        "I":0, "J":0, "K":0, "L":0, "M":0, "N":0, "O":0,
                                        "P":0, "Q":0, "R":0, "S":0, "T":0, "U":0, "V":0,
                                        "W":0, "X":0, "Y":0, "Z":0}
                        # Each plaintext's score will begin at 0. Each letter is compared to its empirical frequency scores, and added in this dictionary based upon which word is contained in the plaintext.
                        # For example, 'E' in the plaintext will score as 12.70; and will be added into this score (keeping in mind E is one of the most common letters in the English language).
                        # In theory, the more common letters are in the plaintext, the higher the score this will have - this will help to sort the results.

                        for m in plaintext:
                            if m in letter_frequency_scores:
                                letter_scores[m] += letter_frequency_scores[m]
                        # If a letter in the plaintext is found in the list of common letters, then the Frequency score of the lettter (in letter_frequency_scores) is added to letter_scores.

                        score = sum(letter_scores.values()) # The score of each letter is summated. This helps rank each plaintext decrypted according to the frequency of commonly occuring letters. 
                        plaintexts.update({plaintext:score})
                plaintexts_sorted = sorted(zip(plaintexts.values(), plaintexts.keys()), reverse=True)
                # As discussed previously, the results will be sorted in descending order. This will display the most probable plaintext first; for convenience.

                length = len(plaintext)
                print("\nFreq. Score | Plaintext")
                if length < 6: # If the text is shorter, say "HELLO", there is a chance of error in the results if the output is limited. Therefore, this will display every plaintext in order in case the word is shorter.
                    for key, value in plaintexts_sorted:
                        print("-" * len(value) + "\n[*] " + str(int(key)), value)
                else:
                    for key, value in plaintexts_sorted[:30]: # If the word is longer, this limits the result to only 30 plaintexts, as opposed to 312. This also makes the output shorter and more readable. Additionally, it is likely that the correct plaintext will be within the results; as more frequent letters are found in larger texts.
                        print("-" * len(value) + "\n[*] " + str(int(key)), value)
                print("\nAnalysis Completed.")
            except KeyboardInterrupt:
                print("\n[!] Analysis Interrupted.\n")
                exitProgram()    
            choice = input("\n[+] Would you like to output results to a file? [Y/N]: ").upper()
            if choice == 'Y':
                output_file = open("affine_results.txt", "w")
                output_file.write("Freq. Score | Plaintext\n")
                for key, value in plaintexts_sorted:
                    output_file.write("-"*len(value) + "\n" + str(int(key)) + " " + value + "\n")
                print("Output sent to affine_results.txt\n")   
                exitProgram() 
        if int(choice) == 99:
            exitProgram() 
        else:
            exitProgram()      
    except Exception as e:
        print("\n[!] Sorry, something went wrong.\n{}".format(e))
        exitProgram()
    except KeyboardInterrupt:
        print("\n")
        exitProgram()

main()
input('\nPress ENTER to exit') # Addresses minor issue in Windows where if opened in the Python application instead of the terminal, it abruptly exits without prompt.