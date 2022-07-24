import Web3 from 'web3';
import {
    LimitOrderProtocolFacade,
    LimitOrder,
    LimitOrderSignature,
    Web3ProviderConnector
} from '@1inch/limit-order-protocol';

const walletAddress = '0xhhh...';
const contractAddress = '0x5fa31604fc5dcebfcac2481f9fa59d174126e5e6';

const order: LimitOrder = {...};
const signature: LimitOrderSignature = '...';

const makerAmount = '400000000';
const takerAmount = '0';
const thresholdAmount = '600000000';

const connector = new Web3ProviderConnector(new Web3('...'));
const limitOrderProtocolFacade = new LimitOrderProtocolFacade(contractAddress, connector);

const callData = limitOrderProtocolFacade.fillLimitOrder(
    order,
    signature,
    makerAmount,
    takerAmount,
    thresholdAmount
);

sendTransaction({
    from: walletAddress,
    gas: 210_000, // Set your gas limit
    gasPrice: 40000, // Set your gas price
    to: contractAddress,
    data: callData,
});