pragma solidity ^0.8.0;

contract Factory {
  event PairCreated(address indexed token0, address indexed token1, address pair, uint);
  function createPair(address tokenA, address tokenB) external returns (address pair) {}
}