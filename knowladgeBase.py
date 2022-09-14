from experta import *
from navigator import Navigator

def ask_question(question: str):
    print(question) 
    flag = False
    while(not(flag)):
        userInput = ''
        userInput = input(" --> ")
        try:
            answer = int(userInput)
            if(answer < 1 or answer > 3):
                raise Exception()
            flag = True
        except (ValueError, Exception) as ex:
            print("Errore! Risposta non valida. La risposta deve essere un INTERO compreso tra 1 e 3\n")
    return answer

def ask_question2(question: str):
    print(question) 
    flag = False
    while(not(flag)):
        userInput = ''
        userInput = input(" --> ")
        try:
            answer = int(userInput)
            if(answer < 1 or answer > 4):
                raise Exception()
            flag = True
        except (ValueError, Exception) as ex:
            print("Errore! Risposta non valida. La risposta deve essere un INTERO compreso tra 1 e 4\n")
    return answer


def expert_system():
    print("=======================================================================")
    print("|Benvenuto nel sistema esperto di diagnostica per problemi al veicolo.|")
    print("|                                                                     |")
    print("|Rispondi alle domande proposte dal sistema a seconda dei sintomi     |")
    print("|riscontrati durante il tentativo di accensione del veicolo.          |")
    print("=======================================================================")
    runex()
   
def runex():
    engine = DiagnosticsES()
    engine.reset()
    engine.run()

class DiagnosticsES(KnowledgeEngine):

    @DefFacts()
    def _initial_action(self):
        yield Fact(question=True)
        yield Fact(orderQuestion=1)

    @Rule(AND(Fact(question=True),Fact(orderQuestion=1)))
    def askLightsComeOn(self):
        query = "\nQuando accendi l'interruttore dei fanali che succede?\n"
        query+="\t(1) si accendono\n\t(2) non succede nulla\n\t(3) a volte si accendono a volte no"
        self.declare(Fact(light=ask_question(query)))
        self.declare(Fact(orderQuestion=2))

    @Rule(AND(Fact(question=True),Fact(orderQuestion=2)))
    def askGasTank(self):
        query = "\nControllando il serbatoio noti che:\n"
        query+="\t(1) non e' vuoto\n\t(2) e' vuoto\n\t(3) non ne sono sicuro"
        self.declare(Fact(gas=ask_question(query)))
        self.declare(Fact(orderQuestion=3))

    @Rule(AND(Fact(question=True),Fact(orderQuestion=3)))
    def askEngineCranks(self):
        query = "\nCosa succede quando giri la chiave per provare a mettere in moto la macchina?\n"
        query+="\t(1) il motore gira normalmente\n\t(2) il motore gira lentamente\n"
        query += "\t(3) a volte gira bene a volte male\n\t(4) non succede nulla"
        self.declare(Fact(engineCrank=ask_question2(query)))
        self.declare(Fact(orderQuestion=4))

    @Rule(AND(Fact(question=True),Fact(orderQuestion=4)))
    def askLightsDim(self):
        query = "\nQuando provi a mettere in moto la macchina noti che le luci:\n"
        query+="\t(1) diventano piu' fioche\n\t(2) non diventano piu' fioche\n\t(3) a volte si' a volte no"
        self.declare(Fact(lightDim=ask_question(query)))
        self.declare(Fact(orderQuestion=5))

    @Rule(AND(Fact(question=True),Fact(orderQuestion=5)))
    def askFuelSmell(self):
        query = "\nQuando provi a mettere in moto la macchina senti odore di carburante:\n"
        query+="\t(1) si'\n\t(2) no\n\t(3) a volte si' a volte no"
        self.declare(Fact(fuelSmell=ask_question(query)))   

    @Rule(OR(Fact(light=2),
    (AND(Fact(engineCrank=4), Fact(light=1)))))
    def batteryDead(self):
        self.declare(Fact(batteryDead=True))
        print("La batteria probabilmente e' rotta")

    @Rule(Fact(batteryDead=True))
    def replaceBattery(self):
        print("Si consiglia di sostituire la batteria.")
        self.reset()

    @Rule(AND(OR(Fact(light=1),Fact(light=2),Fact(light=3)), OR(Fact(engineCrank=1),
     Fact(engineCrank=2), Fact(engineCrank=3)), Fact(gas=2)))
    def outOfGas(self):
        self.declare(Fact(outOfGas=True))
        print("E' terminato il carburante")

    @Rule(Fact(outOfGas=True))
    def refuelGas(self):
        print("Si consiglia fare rifornimento di carburante.")
        self.reset()

    @Rule(OR( Fact(light=3),
     AND(Fact(light=1), Fact(engineCrank=2), Fact(gas=1),
     OR(Fact(lightDim=1), Fact(lightDim=3)))))
    def batteryWeak(self):
        self.declare(Fact(batteryWeak=True))
        print("La batteria e' scarica")

    @Rule(Fact(batteryWeak=True))
    def rechargeBattery(self):
        print("Si consiglia di ricaricare la batteria.")
        self.reset()

    @Rule(AND(Fact(light=1), Fact(engineCrank=1), Fact(gas=1),
     OR(Fact(fuelSmell=1), Fact(fuelSmell=3))))
    def engineIsFlooded(self):
        self.declare(Fact(engineIsFlooded=True))
        print("E' entrato troppo carburante nel motore. Il motore e' ingolfato")

    @Rule(Fact(engineIsFlooded=True))
    def restartFloodedCar(self):
        print("Si consiglia di attendere 10 minuti e di riprovare ad accendere l'auto.")
        self.reset()

    @Rule(OR(
    AND(Fact(light=1), Fact(engineCrank=2), Fact(gas=1),
     Fact(lightDim=2)),
     AND(Fact(light=1), Fact(gas=3), OR(Fact(engineCrank=2),  Fact(engineCrank=1)) ),
     AND(Fact(light=1), Fact(engineCrank=3), OR( Fact(gas=1), Fact(gas=3)) ),
     AND(Fact(light=1), Fact(engineCrank=1), Fact(gas=1), Fact(fuelSmell=2) )
    ))
    def notIdentified(self):
        self.declare(Fact(notIdentified=True))
        print("Nessun problema identificato")

    @Rule(Fact(notIdentified=True))
    def selectOperation(self):
        query = "Quale operazione vuoi effettuare?\n" 
        query += "\t(1) Cercare un meccanico\n\t(2) Riprovare il test\n\t" +"(3) Terminare il programma"
        answer = ask_question(query)
        if (answer == 1):
            navigator = Navigator()
            navigator.askOperation()
        elif(answer == 2):
            self.reset()
            self.run()
            

def main():
    expert_system()

if __name__ == '__main__':
    main()