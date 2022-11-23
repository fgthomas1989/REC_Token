pragma solidity ^0.5.0;

import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

contract RECToken {
    using SafeMath for uint;

	address payable owner = msg.sender;
	string public symbol = "RECT";

    mapping(address => uint) balances;

    function balance(address user) public view returns(uint) {
        return balances[user];
    }

    function transfer(address user,address recipient, uint value) public {
    require(balances[user] >= value, "You don't have those many tokens!");
	balances[user] = balances[user].sub(value);
	balances[recipient] = balances[recipient].add(value);
    }

    function purchase(address user,address reciepient, uint value) public {
    require(reciepient == owner, "Select our address to buy!");
    balances[reciepient] = balances[reciepient].sub(value);
    balances[user] = balances[user].add(value);
    }

    function mint(address recipient, uint value) public {
    require(msg.sender == owner, "You do not have permission to mint tokens!");
    balances[recipient] = balances[recipient].add(value);
    }

    function claim(address user,uint value) public {
    require(balances[user] >= value, "You don't have those many tokens!");
    balances[user] = balances[user].sub(value);
    }
}



