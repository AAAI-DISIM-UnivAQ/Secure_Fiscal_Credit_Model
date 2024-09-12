import random

import mesa
from algosdk.v2client import algod
from mesa import DataCollector

from .algo import send_transaction


# Class for managing Global Data structures
class DataManagerAgent:
    def __init__(self):
        # List of Paperwork Agents
        self.pwork_agents = []

        # List of Technicains Agents
        self.tech_agents = []

        # Dictionary of Paperwork Agents' current states. Structure is [paperwork agent, status].
        # Modified by Paperwork Agents
        self.pwork_agents_states = {}

        # Dictionary of last asseverated states by Technicians. Structure is [paperwork agent, status].
        # Modified by Technician Agents
        self.tech_asseverations = {}

        # Dictionary of last payments received by General Contractor. Structure is [paperwork agent, status].
        # Modified by General Contractors
        self.gc_payments_status = {}

        # self.financial_agents_matrix = []     # Matrice contenente i pagamenti fatti sui vari sal dele varie pratiche

        # Oredered list of possible states a Paperwork can take
        self.pwork_possible_states = ["Open", "Ant", "Sal1", "Sal2", "Eow", "Archived"]

    # Methods on Paperwork Agents' list
    def add_pwork_to_list(self, agent):
        self.pwork_agents.append(agent)

    def get_pwork_from_list(self, unique_id):
        return self.pwork_agents[unique_id]

    """
        if unique_id in self.paperwork_agents:
            return self.paperwork_agents[unique_id]
        else:
            return None
    """

    def update_pwork_in_list(self, unique_id, data):
        self.pwork_agents[unique_id] = data

    """
        if unique_id in self.paperwork_agents:
            self.paperwork_agents[unique_id] = data
        else:
            return None
    """

    def get_pwork_list(self):
        return self.pwork_agents

    # Methods on the Paperwork Agent Status dictionary containing the current states of Paperwork Agents.
    def add_pwork_status_to_dict(self, unique_id, status):
        self.pwork_agents_states[unique_id] = status

    def get_pwork_status_from_dict(self, unique_id):
        return self.pwork_agents_states[unique_id]

    """    
        if unique_id in self.paperwork_agents_states:
            return self.paperwork_agents_states[unique_id]
        else:
            print("Id Paperwork non pesente!")
            return None
    """

    def update_pwork_status_in_dict(self, unique_id, data):
        # if unique_id in self.paperwork_agents_states:
        self.pwork_agents_states[unique_id] = data

    def get_pwork_status_dict(self):
        return self.pwork_agents_states

    # Methods on the Technician Agent dictionary containing Agent Paperwork and its latest asseverated state
    def add_tech_asseveration_to_dict(self, unique_id, data):
        self.tech_asseverations[unique_id] = data

    def get_tech_asseveration_from_dict(self, unique_id):
        return self.tech_asseverations[unique_id]

    """
        if unique_id in self.technician_asseverations:
            return self.technician_asseverations[unique_id]
        else:
            print("Id Asseverazione tecnica  non pesente!")
            return None
    """

    def update_tech_asseveration_in_dict(self, unique_id, data):
        self.tech_asseverations[unique_id] = data

    """    
        if unique_id in self.technician_asseverations:
            self.technician_asseverations[unique_id] = data
    """

    def get_tech_asseverations_dict(self):
        return self.tech_asseverations

    # Methods on Technical Agents' list
    def add_tech_to_list(self, agent):
        self.tech_agents.append(agent)

    def get_tech_from_list(self, unique_id):
        return self.tech_agents[unique_id]

    """
        if unique_id in self.paperwork_agents:
            return self.paperwork_agents[unique_id]
        else:
            eturn None
    """

    def update_tech_in_list(self, unique_id, data):
        self.tech_agents[unique_id] = data

    """
        if unique_id in self.paperwork_agents:
            self.paperwork_agents[unique_id] = data
        else:
            return None
    """

    def get_tech_list(self):
        return self.tech_agents

    # Methods on Payments Status dictionary containing Agent Paperwork and related last paid status
    def add_gc_payment_to_dict(self, unique_id, data):
        self.gc_payments_status[unique_id] = data

    def get_gc_payment_from_dict(self, unique_id):
        return self.gc_payments_status[unique_id]

    """
        if unique_id in self.technician_asseverations:
            return self.technician_asseverations[unique_id]
        else:
            print("Id Asseverazione tecnica  non pesente!")
            return None
    """

    def update_gc_payment_in_dict(self, unique_id, data):
        self.gc_payments_status[unique_id] = data

    """    
        if unique_id in self.technician_asseverations:
            self.technician_asseverations[unique_id] = data
    """

    def get_gc_payment_dict(self):
        return self.gc_payments_status


class SB110Model(mesa.Model):
    """Model with agents."""

    def __init__(
        self,
        gc_threshold,
        tech_threshold,
        open_amount,
        ant_amount,
        sal1_amount,
        sal2_amount,
        eow_amount,
        tech_amount,
    ):
        dm = DataManagerAgent()

        self.gc_threshold = gc_threshold
        self.tech_threshold = tech_threshold
        self.open_amount = open_amount
        self.ant_amount = ant_amount
        self.sal1_amount = sal1_amount
        self.sal2_amount = sal2_amount
        self.eow_amount = eow_amount
        self.tech_amount = tech_amount

        self.num_agents = 11

        # Grid setup for graphical representation and agent placement
        self.grid = mesa.space.SingleGrid(500, 500, False)  # non toroidale

        (
            c_condo_via_roma,
            c_condo_via_salaria,
            f_univaq,
            gc_letteri,
            p_condo_roma,
            p_condo_salaria,
            p_condo_vetoio,
            p_condo_rivera,
            p_condo_pontieri,
            t_de_gasperis,
            t_facchini,
        ) = self.init_test(
            dm,
            self.grid,
            self.gc_threshold,
            self.tech_threshold,
            self.open_amount,
            self.ant_amount,
            self.sal1_amount,
            self.sal2_amount,
            self.eow_amount,
            self.tech_amount,
        )

        # Adding Paperwork Agents to the list of active paperworks
        dm.add_pwork_to_list(p_condo_roma)
        dm.add_pwork_to_list(p_condo_salaria)
        dm.add_pwork_to_list(p_condo_rivera)
        dm.add_pwork_to_list(p_condo_pontieri)
        dm.add_pwork_to_list(p_condo_vetoio)

        # Adding Technicians Agents to the list of technicians
        dm.add_tech_to_list(t_de_gasperis)
        dm.add_tech_to_list(t_facchini)

        # Initialization of technicians' asseverations to "Open" and inserting into the dictionary
        dm.add_tech_asseveration_to_dict(8, "Open")
        dm.add_tech_asseveration_to_dict(9, "Open")
        dm.add_tech_asseveration_to_dict(10, "Open")
        dm.add_tech_asseveration_to_dict(11, "Open")
        dm.add_tech_asseveration_to_dict(12, "Open")

        # Initialization of states in the Paperwok status dictionary
        dm.add_pwork_status_to_dict(8, "Open")
        dm.add_pwork_status_to_dict(9, "Open")
        dm.add_pwork_status_to_dict(10, "Open")
        dm.add_pwork_status_to_dict(11, "Open")
        dm.add_pwork_status_to_dict(12, "Open")

        # Initialization of states in the Payment status dictionary
        dm.add_gc_payment_to_dict(8, "Open")
        dm.add_gc_payment_to_dict(9, "Open")
        dm.add_gc_payment_to_dict(10, "Open")
        dm.add_gc_payment_to_dict(11, "Open")
        dm.add_gc_payment_to_dict(12, "Open")

        # Mesa scheduler setting - I activate agent types one at a time.
        self.schedule = mesa.time.RandomActivationByType(self)

        # Adding Agents in the Scheduler
        self.schedule.add(f_univaq)
        self.schedule.add(t_facchini)
        self.schedule.add(t_de_gasperis)
        self.schedule.add(gc_letteri)
        self.schedule.add(c_condo_via_salaria)
        self.schedule.add(c_condo_via_roma)
        self.schedule.add(p_condo_roma)
        self.schedule.add(p_condo_salaria)
        self.schedule.add(p_condo_vetoio)
        self.schedule.add(p_condo_pontieri)
        self.schedule.add(p_condo_rivera)

        # Adding Paperwork Agents on the Grid
        self.grid.place_agent(p_condo_roma, (p_condo_roma.unique_id, 0))
        self.grid.place_agent(p_condo_salaria, (p_condo_salaria.unique_id, 0))
        self.grid.place_agent(p_condo_salaria, (p_condo_vetoio.unique_id, 0))
        self.grid.place_agent(p_condo_salaria, (p_condo_pontieri.unique_id, 0))
        self.grid.place_agent(p_condo_salaria, (p_condo_rivera.unique_id, 0))

        self.datacollector = DataCollector(
            model_reporters={"GC_Wealth": SB110Model.compute_gc},
            agent_reporters={"Wealth": "wealth"},  # "Wealth": "wealth"
        )
        """
        self.datacollector = DataCollector(
            {
            "GC_Wealth": SB110Model.compute_gc
            }
        )
        """

    def init_test(
        self,
        dm,
        grid,
        tech_threshold,
        gc_threshold,
        open_amount,
        ant_amount,
        sal1_amount,
        sal2_amount,
        eow_amount,
        tech_amount,
    ):
        # Creation of Agents of the various types
        f_fin_1 = FinancialAgent(1, self, "Univaq Bank", dm)
        t_tech_1 = TechnicianAgent(
            2,
            self,
            "Ing Facchini",
            dm,
            "YX2YR7OCYEZTSUAUISDAEFZEMF5HXVQB4QLXYH2OD3NHPJEC26AN54E62Q",
            "LCQA+ZZ6A+XpeRP1O+/KkRYk6mCHnSuVKp47oJLeyBzF9Yj9wsEzOVAURIYCFyRhenvWAeQXfB9OHtp3pILXgA==",
            tech_threshold,
        )
        t_tech_2 = TechnicianAgent(
            3,
            self,
            "Ing De Gasperis",
            dm,
            "SUWKED3FYJYXOUH3WLQCZX6CPQ5RRWHAICKWI4OSG3RYDHBW6KSL24AURE",
            "p3F137DWKDqi0EubwW2Nzik6jQdRKZ89YxOrmVbVKrqVLKIPZcJxd1D7suAs38J8OxjY4ECVZHHSNuOBnDbypA==",
            tech_threshold,
        )
        gc_general_1 = GeneralContractorAgent(
            4,
            self,
            "Letteri Costruzioni Spa",
            dm,
            "4YTGV7MY4W5FSJKPN3FGG6IPOBOUJLJFOYO6SEIAO26SNNINIO5FMYFR3E",
            "P3C5tD+LngNzPBWh/rLne1sqhT/fOU6qy63BU8tNdt7mJmr9mOW6WSVPbspjeQ9wXUStJXYd6REAdr0mtQ1Dug==",
            gc_threshold,
            open_amount,
            ant_amount,
            sal1_amount,
            sal2_amount,
            eow_amount,
        )
        c_client_1 = ClientAgent(6, self, "Condominio Via Salaria", dm)
        c_client_2 = ClientAgent(7, self, "Condominio Via Roma", dm)

        # Creating Test Paperwork Agents
        total_amount = int(
            random.uniform(50, 100) * 100000
        )  # generation of casual total value of the works
        p_paper_1 = PaperworkAgent(
            8,
            self,
            "Pratica SB110 Condo Via Roma",
            c_client_2.unique_id,
            t_tech_1.unique_id,
            gc_general_1.unique_id,
            dm,
            grid,
            "BYRXMTOQEFSYHW3477TUFISFG64IIYSIC3VWAQXRNYBC25TTQGPYMUYLDA",
            "i+Usy5wSSrRzTw4EVm4s1vPkr7uX12kPt/SP0AnvM9gOI3ZN0CFlg9t8/+dCokU3uIRiSBbrYELxbgItdnOBnw==",
            total_amount,
            open_amount,
            ant_amount,
            sal1_amount,
            sal2_amount,
            eow_amount,
            tech_amount,
        )

        total_amount = int(random.uniform(50, 100) * 100000)
        p_paper_2 = PaperworkAgent(
            9,
            self,
            "Pratica SB110 Condo Via Salaria",
            c_client_1.unique_id,
            t_tech_1.unique_id,
            gc_general_1.unique_id,
            dm,
            grid,
            "2AWUAEN2QVV4UOE5D3KABJX7GQ6CD63NFUQY7GFTPYUD2ZL5O3CFFJ3BVY",
            "+IVWWBuyRIJKS2CxziOblb6aA8HDfHCUgn3tI9BCWv7QLUARuoVryjidHtQApv80PCH7bS0hj5izfig9ZX12xA==",
            total_amount,
            open_amount,
            ant_amount,
            sal1_amount,
            sal2_amount,
            eow_amount,
            tech_amount,
        )
        total_amount = int(random.uniform(50, 100) * 100000)
        p_paper_3 = PaperworkAgent(
            10,
            self,
            "Pratica SB110 Condo Via Vetoio",
            c_client_2.unique_id,
            t_tech_2.unique_id,
            gc_general_1.unique_id,
            dm,
            grid,
            "5KBDDDYK3PGOCKHUOKII5MU34WP4JBHY7OGHCHGNLPRRV4BAO7DRMNLBQM",
            "FUB4rJF0UuzSJdBGmswps6IbXK6tBodxLOsOB6NyaXzqgjGPCtvM4Sj0cpCOspvln8SE+PuMcRzNW+Ma8CB3xw==",
            total_amount,
            open_amount,
            ant_amount,
            sal1_amount,
            sal2_amount,
            eow_amount,
            tech_amount,
        )
        total_amount = int(random.uniform(50, 100) * 100000)
        p_paper_4 = PaperworkAgent(
            11,
            self,
            "Pratica SB110 Condo Piazza Rivera",
            c_client_1.unique_id,
            t_tech_2.unique_id,
            gc_general_1.unique_id,
            dm,
            grid,
            "OYRE4O32VQ2AICID53BJIZS3DTSWSPIIVW3JRMQR5LL554ZEHG3GCL4DXQ",
            "bKUz/Z4n8IpCvsoDa/NTudJaNKrY/GN3EDG+2+b2yfR2Ik47eqw0BAkD7sKUZlsc5Wk9CK22mLIR6tfe8yQ5tg==",
            total_amount,
            open_amount,
            ant_amount,
            sal1_amount,
            sal2_amount,
            eow_amount,
            tech_amount,
        )
        total_amount = int(random.uniform(50, 100) * 100000)
        p_paper_5 = PaperworkAgent(
            12,
            self,
            "Pratica SB110 Condo Piazzale Pontieri",
            c_client_2.unique_id,
            t_tech_2.unique_id,
            gc_general_1.unique_id,
            dm,
            grid,
            "TGK6VHLDVS46OXBOUERJLIUHFK7PRMARTJM3PXTPRJMOQ63RBM2CQJBHNI",
            "4aEIHnkSYsygwxekEprU+n6+qMZtE6m808Sz14x53RCZleqdY6y551wuoSKVoocqvviwEZpZt95viljoe3ELNA==",
            total_amount,
            open_amount,
            ant_amount,
            sal1_amount,
            sal2_amount,
            eow_amount,
            tech_amount,
        )

        return (
            c_client_2,
            c_client_1,
            f_fin_1,
            gc_general_1,
            p_paper_1,
            p_paper_2,
            p_paper_3,
            p_paper_4,
            p_paper_5,
            t_tech_2,
            t_tech_1,
        )

    def step(self):
        # Advance the model by one step
        self.schedule.step()
        # Activate Data collector
        self.datacollector.collect(self)
        # if <condition> self.running = False

    # Function to retrieve relevant information for Mesa datacollector module
    def compute_gc(model):
        agent_wealths = [agent.wealth for agent in model.schedule.agents]
        x = sorted(agent_wealths)
        N = model.num_agents
        # B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
        avg = sum(xi for i, xi in enumerate(x)) / N
        return avg

    # def compute_gc(model):
    # pass


"""
GENERAL CONTRACTOR AGENT
"""


class GeneralContractorAgent(mesa.Agent):
    """Agent representing a General Contractor."""

    def __init__(
        self,
        unique_id,
        model,
        name,
        dm,
        wallet,
        private_key,
        gc_threshold,
        open_amount,
        ant_amount,
        sal1_amount,
        sal2_amount,
        eow_amount,
    ):
        super().__init__(unique_id, model)
        self.wallet = wallet
        self.name = name
        self.dm = dm
        self.private_key = private_key
        self.amount = 0
        self.gc_threshold = gc_threshold
        self.dict_imports = {
            "Open": open_amount,
            "Ant": ant_amount,
            "Sal1": sal1_amount,
            "Sal2": sal2_amount,
            "Eow": eow_amount,
        }

        # Opening socket with Algorand testnet client
        self.algod_address = "http://localhost:4001"
        self.algod_token = (
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        )
        self.algod_client = algod.AlgodClient(self.algod_token, self.algod_address)

        self.wealth = 0

    def step(self):
        disclaimer = (
            "Hi, I am General Contractor agent "
            + str(self.unique_id)
            + ". Il mio nome è: "
            + self.name
            + "."
        )
        CRED = "\33[31m"
        CEND = "\033[0m"
        print(f"{CRED} {disclaimer} {CEND}")

        # Scroll active Paperworks
        for agent in self.dm.get_pwork_list():
            # Check if Paperwork is assigned to current General Contractor
            if agent.general_contractor == self.unique_id:
                # Extract current Paperwork status
                status = str(self.dm.get_gc_payment_from_dict(agent.unique_id))

                # choose = input("Paperwork " + str(agent.unique_id) + " " + str(agent.name) + " my payment status is: " + status + " Certify new payment status? Y/n: ")

                # Random simulation of General Contractor approving a new payment
                approval = random.uniform(0, 1)
                # print(f"Success threshold: {agent.get_gc_treshold()} -approval {approval}")
                # self.choose = approval < agent.get_gc_treshold()
                print(f"Success threshold: {self.gc_threshold} -approval {approval}")
                self.choose = approval < self.gc_threshold
                if self.choose:  # Success of approval, GC Agent pays the work done
                    # General Contractor update new payed status (next in possible status array)
                    pos = int(self.dm.pwork_possible_states.index(status))
                    new_status = self.dm.pwork_possible_states[pos + 1]
                    amount = int(
                        self.dict_imports[new_status] * agent.total_amount
                    )  # amount = input("Amount to transfer: ")  # private_key = input("Insert your private key: ")due as an anticipation
                    # print(str(amount) +"/n")
                    print(f"The amount sent is: {amount}%n")
                    print(f"The total amount of the Paperwork is: {agent.total_amount}")
                    # Update status of paperwork in Payments dictionary
                    self.dm.update_gc_payment_in_dict(agent.unique_id, new_status)

                    # Send payment to Paperwork Agent
                    send_transaction(
                        self.private_key, self.wallet, agent.wallet, amount
                    )
                    pwork_account_info = self.algod_client.account_info(agent.wallet)
                    print(
                        "Amount sent: "
                        + str(amount)
                        + " Paperwork Account blance: {} microAlgos".format(
                            pwork_account_info.get("amount")
                        )
                        + "\n"
                    )
                    print(
                        f"Paperwork New payment state is: {new_status}"
                    )  # + " new paperwork balance is: " + str(agent.wallet))
                    gc_account_info = self.algod_client.account_info(self.wallet)
                    self.wealth = gc_account_info.get("amount")
                    print(
                        "-------------------------------------------------------------------------------------------"
                    )
                    # agent.set_gc_treshold(0) # if approved reset to zero probability threshold
                else:
                    # Probability of approval increase to simulate a real scenario
                    # t = agent.get_gc_treshold() + 0.05
                    # agent.set_gc_treshold(t)
                    pass

        return


"""
TECHNICIAN AGENT
"""


class TechnicianAgent(mesa.Agent):
    """Agent representing a combination of Project Designer and Accountant."""

    def __init__(self, unique_id, model, name, dm, wallet, private_key, tech_threshold):
        super().__init__(unique_id, model)
        self.name = name
        self.dm = dm
        self.wallet = wallet
        self.private_key = private_key
        self.choose = False  # accettazione passaggio stato pratica
        self.wealth = 0
        self.tech_threshold = tech_threshold

    def step(self):
        disclaimer = (
            "Hi, I am Technician agent "
            + str(self.unique_id)
            + ". Il mio nome è: "
            + self.name
            + "."
        )
        CBLUE = "\33[34m"
        CEND = "\033[0m"
        print(f"{CBLUE} {disclaimer} {CEND}")

        # Scroll active Paperworks
        for agent in self.dm.get_pwork_list():
            # Check if Paperwork is assigned to current technician
            if agent.technician == self.unique_id:
                # Extract current Paperwork status
                status = str(self.dm.get_pwork_status_from_dict(agent.unique_id))
                # choose = input("Paperwork " + str(agent.unique_id) + " " + str(agent.name) + " my assevered status is: " + status + " Certify next status? Y/n: ") # opzione scelta manualr
                # Random simulation of Technician approving a new status
                approval = random.uniform(0, 1)
                # print(f"Soglia successo: {agent.get_tech_treshold()} -approval {approval}")
                # self.choose = approval < agent.get_tech_treshold()
                print(f"Success threshold: {self.tech_threshold} -approval {approval}")
                self.choose = approval < self.tech_threshold
                # Success of approval, Tech Agent asseverates a new status
                if self.choose:
                    # Technician inserts new assevered status
                    pos = int(self.dm.pwork_possible_states.index(status))
                    new_status = self.dm.pwork_possible_states[pos + 1]

                    # Update status of paperwork in Asseveration dictionary
                    self.dm.update_tech_asseveration_in_dict(
                        agent.unique_id, new_status
                    )
                    print(f"New Asseveration state is: {new_status}")
                    print(
                        "-------------------------------------------------------------------------------------------"
                    )
                    # agent.set_tech_treshold (0) # if approved reset to zero probability threshold
                else:
                    pass
                    # Probability of approval increase to simulate a real scenario
                    # t = agent.get_tech_treshold() + 0.05
                    # agent.set_tech_treshold(t)
        return


"""
PAPERWORK AGENT
"""


class PaperworkAgent(mesa.Agent):
    """Agent representing a SB110 Paperwork."""

    def __init__(
        self,
        unique_id,
        model,
        name,
        client,
        technician,
        general_contractor,
        dm,
        grid,
        wallet,
        private_key,
        total_amount,
        open_amount,
        ant_amount,
        sal1_amount,
        sal2_amount,
        eow_amount,
        tech_amount,
    ):
        super().__init__(unique_id, model)
        self.wallet = wallet  # set balance of paperwork process to 0
        self.name = name
        self.client = client
        self.technician = technician
        self.general_contractor = general_contractor
        self.dm = dm
        self.grid = grid
        self.private_key = private_key
        self.total_amount = total_amount
        self.wealth = 0
        self.tech_amount = (
            tech_amount  # Percentage of Technician due to asseveration and project
        )

        # self.model = SB110Model
        # self.status = dm.get_paperwork_status_from_dict(self.unique_id)

        self.dict_imports = {
            "Open": open_amount,
            "Ant": ant_amount,
            "Sal1": sal1_amount,
            "Sal2": sal2_amount,
            "Eow": eow_amount,
        }

        # Opening socket with Algorand testnet client
        self.algod_address = "http://localhost:4001"
        self.algod_token = (
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        )
        self.algod_client = algod.AlgodClient(self.algod_token, self.algod_address)

    """
    
    Da vedere come integrare con la test net
    accounts = localnet.kmd.get_accounts()
    sender = accounts[0]

    app_client = client.ApplicationClient(
        client=localnet.get_algod_client(),
        app=app,
        sender=sender.address,
        signer=sender.signer_new,
    )
    
    def set_gc_treshold(self, t):
        self.gc_treshold = t

    def get_gc_treshold(self):
        return self.gc_treshold

    def set_tech_treshold(self, t):
        self.tech_treshold = t

    def get_tech_treshold(self):
        return self.tech_treshold
    """

    def step(self):
        agent_wallet = None
        disclaimer = (
            "Hi, I am Paperwork agent "
            + str(self.unique_id)
            + " related to "
            + self.name
            + ". My status is "
            + str(self.dm.get_pwork_status_from_dict(self.unique_id))
            + ". My total value is: "
            + str(self.total_amount)
        )
        CVIOLET = "\33[35m"
        CEND = "\033[0m"
        print(f"{CVIOLET} {disclaimer} {CEND}")

        # Extract current Technician asseveration status
        assevered_status = str(self.dm.get_tech_asseveration_from_dict(self.unique_id))

        # Extract current payed status
        payed_status = str(self.dm.get_gc_payment_from_dict(self.unique_id))

        # Extract current Paperwork status
        status = str(self.dm.get_pwork_status_from_dict(self.unique_id))

        print(
            "Situazione stati: " + assevered_status + " " + payed_status + " " + status
        )
        evaluate_passage = (status != assevered_status) and (
            assevered_status == payed_status
        )
        """
        Codice smart contract

        evaluate_passage = app_client.call(update_state, actual=status, assevered=assevered_status, payed=payed_status).return_value
        print(return_value)
        """

        if status == "Archived":
            return  # Paperwork filed do nothing
        elif evaluate_passage:
            # If the assevered status is different from the current status and payment has arrived update
            self.dm.update_pwork_status_in_dict(self.unique_id, assevered_status)
            print(
                f"Verifica stato :  {str(self.dm.get_pwork_status_from_dict(self.unique_id))}"
            )

            # Payment to tech agent asseverating  !! inserire qui la selezione dell'agente tech da pagare !!
            tech_amount = int(
                self.tech_amount
                * self.dict_imports[assevered_status]
                * self.total_amount
            )
            print(f"Import of Technician invoice: {tech_amount}")
            for agent in self.dm.get_tech_list():
                print(f"{agent.unique_id} - {self.technician}")
                if agent.unique_id == self.technician:
                    agent_wallet = agent.wallet
                    send_transaction(
                        self.private_key, self.wallet, agent_wallet, tech_amount
                    )
                    print(f"I'm paying : {tech_amount} to technician {self.technician}")
                else:
                    print("Tecnichian agent not present!")

            # Visualisation of Paperwork on grid
            for agent in self.dm.get_pwork_list():
                if agent.unique_id == self.unique_id:
                    print(f"{agent}")
                    self.grid.move_agent(
                        agent,
                        (
                            self.unique_id,
                            self.dm.pwork_possible_states.index(assevered_status),
                        ),
                    )
            print(
                f"Agent moved in: {self.unique_id} , {self.dm.pwork_possible_states.index(assevered_status)}"
            )
            print(
                "-------------------------------------------------------------------------------------------"
            )
            return
        pwork_account_info = self.algod_client.account_info(self.wallet)
        self.wealth = pwork_account_info.get("amount")
        """
        elif (self.status == "Open") and (assevered_status != "Open"):
            # Pratica aperta, controllare se Financial ha versato anticipo (step 10) in caso  status in "Anticipation"
            return self.dm.update_paperwork_status_in_dict[self.unique_id, assevered_status] 
        elif self.status == "Anticipation":
            # Verificare asserverazione Technician  lavori eseguiti fino a SAL 1, Verificare se  SAl 1 pagato,  
            in caso  status in SAL 1
            return  
        elif self.status == "SAL1":
            # Verificare asserverazione Technician  lavori eseguiti fino a SAL 2, Verificare se  SAl pagato, 
            in caso  status in SAL 2
            return  
        elif self.status == "SAL2":
            # Verificare asserverazione Technician  lavori eseguiti fino a EOW, Verificare se  EOW è pagato
            return  
        elif self.status == "EOW":
            return  # Verificare se fatturazione OK, modificare status in Archived
        """


class FinancialAgent(mesa.Agent):
    """Agent representing a Financial Institution."""

    def __init__(self, unique_id, model, name, dm):
        super().__init__(unique_id, model)
        self.wallet = 0
        self.name = name
        self.dm = dm
        self.wealth = 0

    def step(self):
        disclaimer = (
            "Hi, I am Financial agent " + str(self.unique_id) + " " + self.name + "."
        )
        CGREEN = "\33[32m"
        CEND = "\033[0m"
        print(f"{CGREEN} {disclaimer} {CEND}")


class ClientAgent(mesa.Agent):
    """Agent representing an Homeowner Client."""

    def __init__(self, unique_id, model, name, dm):
        super().__init__(unique_id, model)
        self.wallet = 0
        self.name = name
        self.dm = dm
        self.wealth = 0
        # da vedere se servono come parametri
        # self.technician = technician
        # self.general_contractor = general_contractor

    def step(self):
        disclaimer = (
            "Hi, I am Client agent " + str(self.unique_id) + " " + self.name + "."
        )
        CYELLOW = "\33[33m"
        CEND = "\033[0m"
        print(f"{CYELLOW} {disclaimer} {CEND}")
