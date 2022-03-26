import time
from scripts.helpful_script import getAccount
from brownie import network, interface, TokenA, TokenB, config


def addLiquidity():
    account = getAccount()  # get account
    tokenAContract = TokenA.deploy({"from": account})  # deploy Contract of Token A
    tokenBContract = TokenB.deploy({"from": account})  # deploy Contract of Token B
    factoryContract = interface.Factory(
        config["networks"][network.show_active()]["factory"]
    )  # get contract from ABI
    routerContract = interface.Router(
        config["networks"][network.show_active()]["router"]
    )
    pairAddressTx = factoryContract.createPair(
        tokenAContract.address, tokenBContract.address, {"from": account}
    )  # create pair token
    pairAddressTx.wait(1)  # wait 1 block
    pairAddress = pairAddressTx.events["PairCreated"]["pair"]  # get pair from events
    print(pairAddress)
    approveA = tokenAContract.approve(
        routerContract.address, 20000, {"from": account}
    )  # approve tokens
    approveA.wait(1)
    approveB = tokenBContract.approve(routerContract.address, 20000, {"from": account})
    approveB.wait(1)
    # add liquidty
    addLiquidityTx = routerContract.addLiquidity(
        tokenAContract.address,
        tokenBContract.address,
        20000,
        20000,
        20000,
        20000,
        account.address,
        time.time(),
        {"from": account, "allow_revert": True},
    )
    addLiquidityTx.wait(1)
    pairContract = interface.Pair(pairAddress)
    balance = pairContract.balanceOf(account.address)  # LP TOKENS
    print(balance)


def main():
    addLiquidity()
