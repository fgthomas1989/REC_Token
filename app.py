import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from web3 import Web3
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
from pathlib import Path
import json

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


totalsupply = contract.functions.balance(w3.eth.accounts[0]).call() + contract.functions.balance(w3.eth.accounts[1]).call() + contract.functions.balance(w3.eth.accounts[2]).call() + contract.functions.balance(w3.eth.accounts[3]).call() + contract.functions.balance(w3.eth.accounts[4]).call() + contract.functions.balance(w3.eth.accounts[5]).call() + contract.functions.balance(w3.eth.accounts[6]).call() + contract.functions.balance(w3.eth.accounts[7]).call() + contract.functions.balance(w3.eth.accounts[8]).call() + contract.functions.balance(w3.eth.accounts[9]).call()

if user == owner:
    st.write('REC Token Company Account')
    st.write('The Total Supply of the REC Token is',totalsupply)
else:
    def buy():
        energy = st.number_input('Enter amount of energy generated')
        if st.button("Purchase"):
            contract.functions.purchase(user,owner, int(energy)).transact({'from': user})
        st.sidebar.markdown("Buy a Renewable Energy Certificate (REC) Token on the basis of your energy generation!")

    def transfer():
        recipient = st.text_input('Enter recipient account')
        value = st.number_input('Enter amount to transfer')
        if st.button("Transfer"):
            contract.functions.transfer(user,recipient, int(value)).transact({'from': user, 'gas': 1000000})
        st.sidebar.markdown("Transfer your REC tokens!")

    def checkbalance():
        st.write('Your REC Token balance is', contract.functions.balance(user).call())
        st.sidebar.markdown("Check your REC Token Balance️!")

    def claim():
        claim = st.number_input('Enter amount of energy used')
        if st.button('claim'):
            contract.functions.claim(user,int(claim)).transact({'from': user})
        st.sidebar.markdown("Claim your REC Token usage!")

    page_names_to_funcs = {"Purchase": buy, "Transfer": transfer, "Check Balance": checkbalance,"Claim Tokens": claim}
    selected_page = st.sidebar.selectbox("What would you like to do?", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()




