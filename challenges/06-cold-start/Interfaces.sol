// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

interface IInbox {
    function setAllowListEnabled(bool) external;
}

interface IInboxFull {
    function createRetryableTicket(
        address to,
        uint256 l2CallValue,
        uint256 maxSubmissionCost,
        address excessFeeRefundAddress,
        address callValueRefundAddress,
        uint256 gasLimit,
        uint256 maxFeePerGas,
        bytes calldata data
    ) external payable returns (uint256);
}
