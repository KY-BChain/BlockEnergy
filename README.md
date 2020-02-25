# BlockEnergy
A Blcokchain and AI based renewables, carbon credit / tax and offsetting project for our efforts to combat global climate change

A Business Case

Our business case will be a prosumer scenario for renewable energy trading. We will assume that the distributor runs the energy market and uses monetary incentives to balance the production and consumption of electricity.

This is similar but not identical to the real world energy markets out there. I’ve made the use case more generic because a blockchain based energy market has some computational constraints.

In a real world market the producers bet the price at which they want to produce energy for a given timeframe. The retailers buy or not specific bets from producers, usually just choosing by the lowest price available. This is exactly how a security trading market works, but that happens to be computationally too intensive for current blockchain platforms.

Design

For the simplest implementation of this energy market we will use some ERC20 token as currency, and two variables to represent the production and consumption loads in the network. We will split time into arbitrary units and aim for the production and consumption load to be as balanced as possible for each time unit.

I’m going to take some inspiration on the uniswap market and use a simple price formula that reduces the electricity price when there are more producers than consumers for a given time unit. This way, cheaper electricity will incentivize consumers to consume more and producers to produce less, balancing the network. Conversely, the price rises as the number of consumers will decrease and the number of producers will increase due to the higher prices.
In all transactions the distribution network will be one of the counterparts. The distribution network will set the price. Producers will sell electricity to the distribution network. Consumers will buy electricity from the distribution network.

Before you think that I’m centralizing the distribution network, I’m not. The physical distribution network that routes energy remains unchanged, but the financial distribution network that routes money between prosumers becomes a decentralized smart contract.

I’m removing many complex features to focus on the market mechanism. I believe it is possible to implement a national energy market on the blockchain, but for the purposes of this article we must remain with a simple scenario. I’ll discuss some of the missing parts later in the article.
Implementation

The main benefit of a uniswap-style market is that it is very simple. In our case the whole energy trading market fits in less than 100 lines with comments. I’ll explain here the key features and then paste the whole contract. Apologies if you have to switch back and forth a few times.

For its implementation I’m going to make the market inherit from both ERC20 and Whitelist. ERC20 gives us the tools to have a currency for payments. Whitelist allows us to restrict the market only to identified consumers and producers.

As for uniswap, the market needs to be seeded with an amount of currency. This is because there might be more producers than consumers, and the market pays to producers and charges consumers. There needs to be a bit of a margin there.

The prices are calculated by two simple formulas based on the difference between the production and consumption loads. When the consumption and production loads are exactly matched the price is a chosen base level. Please ignore all the casting between types, it’s just to protect against overflow and negative prices.

This mechanism is very simple, which suits the limited computational power of blockchain. At the same time it encourages production and consumption to be balanced. Destabilizing the network in either direction has a monetary cost.
It’s important to realize that the smart contract controls the money flow, and that production and consumption orders will usually be filled for future time slots. The physical distribution network will have some knowledge of proposed consumption and production loads and can take actions to curtail them if required to balance the network.

The production of energy is allowed only to identified producers, and they just need to state their intention to produce and will immediately receive the money. Obviously this is a gross simplification and in real life the money would be held into escrow until it is certified that the power was produced.

The consumption of energy works in the same way. The consumers state their intentions and pay the price determined by the network. In real life there might be some refund if the power is not actually consumed.

Further work

There are some features that haven’t been implemented for the sake of brevity. The most important of them are as follows.

    There isn’t an escrow mechanism to ensure that producers only get paid for energy they produce, as opposed to promised to produce.
    There isn’t a guard against putting orders for production or consumption in the past.
    Neither production nor consumption orders can be cancelled. This would be needed for example for unplanned maintenance.
    The pricing formula has been simplified and would need mathematical modelling.
    There is no mechanism for minting tokens except for the constructor, so the contract supply can’t be modified and customers can’t actually get funds.
    The currency contract should be passed on as an address in the constructor, instead of using inheritance.
    The production and consumption orders should be allowed to be for an energy amount which is in a range proportional to the current load. The current implementation would have poor performance on a national scale.
