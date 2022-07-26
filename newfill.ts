import Web3 from 'web3';
import {
    LimitOrderBuilder,
    LimitOrderProtocolFacade,
    Web3ProviderConnector,
} from '@1inch/limit-order-protocol';

const contractAddress = '0x94Bc2a1C732BcAd7343B25af48385Fe76E08734f';
const walletAddress = '0xdF2D2F76E8E8827f92814E49e7D95Fc1e33E4148';
const chainId = 137;

const web3 = new Web3('...');
// You can create and use a custom provider connector (for example: ethers)
const connector = new Web3ProviderConnector(web3);

const limitOrderBuilder = new LimitOrderBuilder(
    contractAddress,
    chainId,
    connector
);

const limitOrderProtocolFacade = new LimitOrderProtocolFacade(
    contractAddress,
    connector
);

// Create a limit order and it's signature
const limitOrder = limitOrderBuilder.buildLimitOrder({
    makerAssetAddress: '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c',
    takerAssetAddress: '0x111111111117dc0aa78b770fa6a738034120c302',
    makerAddress: walletAddress,
    makerAmount: '100',
    takerAmount: '200',
    predicate: '0x',
    permit: '0x',
    interaction: '0x',
});
const limitOrderTypedData = limitOrderBuilder.buildLimitOrderTypedData(
    limitOrder
);
const limitOrderSignature = limitOrderBuilder.buildOrderSignature(
    walletAddress,
    limitOrderTypedData
);

// Create a call data for fill the limit order
const callData = limitOrderProtocolFacade.fillLimitOrder(
    limitOrder,
    limitOrderSignature,
    '100',
    '0',
    '50'
);

// Send transaction for the order filling
// Must be implemented
sendTransaction({
    from: walletAddress,
    gas: 210_000, // Set your gas limit
    gasPrice: 40000, // Set your gas price
    to: contractAddress,
    data: callData,
});