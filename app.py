import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
from pathlib import Path
import json
from fpdf import FPDF
import base64
import plotly.express as px
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib


@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path('./contracts/compiled/RECToken_abi.json')) as f:
        rectabi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=rectabi
    )
    return contract


contract = load_contract()
accounts = w3.eth.accounts
owner = w3.eth.accounts[0]
user = st.text_input("Hey, enter your account details!", value=owner)
totalsupply = contract.functions.balance(w3.eth.accounts[0]).call() + contract.functions.balance(
    w3.eth.accounts[1]).call() + contract.functions.balance(w3.eth.accounts[2]).call() + contract.functions.balance(
    w3.eth.accounts[3]).call() + contract.functions.balance(w3.eth.accounts[4]).call() + contract.functions.balance(
    w3.eth.accounts[5]).call() + contract.functions.balance(w3.eth.accounts[6]).call() + contract.functions.balance(
    w3.eth.accounts[7]).call() + contract.functions.balance(w3.eth.accounts[8]).call() + contract.functions.balance(
    w3.eth.accounts[9]).call()


@st.cache
def create_download_link(val, filename):
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'


if user == owner:
    st.write('REC Token Company Account')
    st.write('The Total Supply of the REC Token is', totalsupply)
else:
    if user == w3.eth.accounts[1]:
        st.write("Nirav's Account")
    elif user == w3.eth.accounts[2]:
        st.write("Franco's Account")
    elif user == w3.eth.accounts[3]:
        st.write("Vivian's Account")
    elif user == w3.eth.accounts[4]:
        st.write("Sebastian's Account")
    elif user == w3.eth.accounts[5]:
        st.write("Abhir's Account")
    elif user == w3.eth.accounts[6]:
        st.write("Marghub's Account")
    elif user == w3.eth.accounts[7]:
        st.write("Bomin's Account")
    elif user == w3.eth.accounts[8]:
        st.write("Ashfaque's Account")
    elif user == w3.eth.accounts[9]:
        st.write("Columbia University's Account")

    st.write('The Total Supply of the REC Token is', totalsupply)


    @dataclass
    class Record:
        user: str
        recipient: str
        value: float


    @dataclass
    class Block:
        record: Record
        creator_id: int
        prev_hash: str = "0"
        timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
        nonce: int = 0

        def hash_block(self):
            sha = hashlib.sha256()

            record = str(self.record).encode()
            sha.update(record)

            creator_id = str(self.creator_id).encode()
            sha.update(creator_id)

            timestamp = str(self.timestamp).encode()
            sha.update(timestamp)

            prev_hash = str(self.prev_hash).encode()
            sha.update(prev_hash)

            nonce = str(self.nonce).encode()
            sha.update(nonce)

            return sha.hexdigest()


    @dataclass
    class PyChain:
        chain: List[Block]
        difficulty: int = 4

        def proof_of_work(self, block):
            calculated_hash = block.hash_block()
            num_of_zeros = "0" * self.difficulty
            while not calculated_hash.startswith(num_of_zeros):
                block.nonce += 1
                calculated_hash = block.hash_block()
            print("Wining Hash", calculated_hash)
            return block

        def add_block(self, candidate_block):
            block = self.proof_of_work(candidate_block)
            self.chain += [block]

        def is_valid(self):
            block_hash = self.chain[0].hash_block()

            for block in self.chain[1:]:
                if block_hash != block.prev_hash:
                    print("Blockchain is invalid!")
                    return False

                block_hash = block.hash_block()

            print("Blockchain is Valid")
            return True


    @st.cache(allow_output_mutation=True)
    def setup():
        print("Initializing Chain")
        return PyChain([Block("Genesis", 0)])


    pychain = setup()

    st.markdown("# Rec Token History")
    pychain_df = pd.DataFrame(pychain.chain).astype(str)
    st.write(pychain_df)

    st.sidebar.write("# Block Inspector")
    selected_block = st.sidebar.selectbox(
        "Which block would you like to see?", pychain.chain
    )

    st.sidebar.write(selected_block)


    def buy():
        energy = st.number_input('Enter amount of energy generated')
        if st.button("Purchase"):
            contract.functions.purchase(user, owner, int(energy)).transact({'from': user})
            prev_block = pychain.chain[-1]
            prev_block_hash = prev_block.hash_block()
            new_block = Block(
                record=(user, energy),
                creator_id=23,
                prev_hash=prev_block_hash
            )
            pychain.add_block(new_block)
        st.sidebar.markdown("Buy a Renewable Energy Certificate (REC) Token on the basis of your energy generation!")


    def transfer():
        recipient = st.text_input('Enter recipient account')
        value = st.number_input('Enter amount to transfer')

        if st.button("Transfer"):
            contract.functions.transfer(user, recipient, int(value)).transact({'from': user, 'gas': 1000000})
            prev_block = pychain.chain[-1]
            prev_block_hash = prev_block.hash_block()
            new_block = Block(
                record=Record(user, recipient, value),
                creator_id=23,
                prev_hash=prev_block_hash
            )
            pychain.add_block(new_block)

        st.sidebar.markdown("Transfer your REC tokens!")


    def checkbalance():
        st.write('Your REC Token balance is', contract.functions.balance(user).call())
        st.sidebar.markdown("Check your REC Token Balance️!")


    def claim():
        st.write("Fill in the form to generate your REC!")

        with st.form("Certificate"):
            claim = st.number_input('Energy Used')
            company_name = st.text_input("Company Name")
            location = st.text_input("Renewable Facility Location")
            fuel = st.selectbox("Type of Energy", ["Wind", "Solar"], index=0)
            submitted = st.form_submit_button("Submit")
            if submitted:
                contract.functions.claim(user, int(claim)).transact({'from': user})
                cert = FPDF()
                cert.add_page()
                cert.image('background.jpg', 0, 0)
                cert.set_font('Times', 'B', 40)
                cert.cell(50, 30, "Renewable Energy Certificate")
                cert.set_font('Arial', 'B', 15)
                cert.multi_cell(100, 50,
                                f"This is to certify that {company_name} has used {claim} MWH units of {fuel} Renewable Energy at {location}.",
                                align="C")
                html = create_download_link(cert.output(dest="S").encode("latin-1"), "Renewable Energy Certificate")
                st.markdown(html, unsafe_allow_html=True)

                prev_block = pychain.chain[-1]
                prev_block_hash = prev_block.hash_block()
                new_block = Block(
                    record=(user, claim),
                    creator_id=23,
                    prev_hash=prev_block_hash
                )
                pychain.add_block(new_block)

        st.sidebar.markdown("Claim your REC Token usage to get a Renewable Energy Certificate!")


    def distribution():
        st.write("Here's how the tokens are distributed!")
        data = dict(
            number=[totalsupply, contract.functions.balance(w3.eth.accounts[1]).call(),
                    contract.functions.balance(w3.eth.accounts[2]).call(),
                    contract.functions.balance(w3.eth.accounts[3]).call(),
                    contract.functions.balance(w3.eth.accounts[4]).call(),
                    contract.functions.balance(w3.eth.accounts[5]).call(),
                    contract.functions.balance(w3.eth.accounts[6]).call(),
                    contract.functions.balance(w3.eth.accounts[7]).call(),
                    contract.functions.balance(w3.eth.accounts[8]).call(),
                    contract.functions.balance(w3.eth.accounts[9]).call()],
            user=["Total Supply", "Nirav", "Franco", "Vivian", "Sebastian", "Abhir", "Marghub", "Bomin", "Aashfaque",
                  "Columbia University"])
        fig = px.funnel(data, x='number', y='user', color='user')
        st.plotly_chart(fig)
        st.sidebar.markdown("Check the token distribution across users!")


    page_names_to_funcs = {"Purchase": buy, "Transfer": transfer, "Check Balance": checkbalance, "Claim Tokens": claim,
                           'Check Distribution': distribution}
    selected_page = st.sidebar.selectbox("What would you like to do?", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()




