def tokenHunter(i):
    notional=1000
    """step 1- for each market, open the position to long with notional of 1k, leverage = 3x to safe as default """
    #after the new emission schedule and new block time for wash trade (100 blocks < 20 minutes)
    #then we will repeat 3 * 24 = 72 trades a day = 36 pair trades a day = daily volume = 72k per market     
    for k in range(0,36):
        vault[pair]['apy_history'][i] = apy_history[pair][i]
        vault[pair]['side'][i] =1
        maxNotional = 0.1*(amm[pair]['Staked_amount'][i]+amm[pair]['net_exposure'][i]+amm[pair]['Unrealized_PnL'][i]) 
        if maxNotional > vault_summary['Cash_reserves'][i]/10*3: 
            maxNotional = vault_summary['Cash_reserves'][i]/10*3
        else:
            pass
        #expected cost 
        """step 2a - evaluate if the maximum token reward to be received over next 24 hours are big enough to cover the cost of the trade
        trading fee can be called from chain directly instead of calcualted from formula 
        slippage can be called from chain directly instead of calcualted from formula 
        """
        trading_fee = notional*amm[pair]['Quote_initial'][i]*0.01*0.01*2 #round trip estimated trading fee
        #slippage = R'/R - 1 (long)
        estimated_slippage = ((amm[pair]['Staked_amount_Long'][i]+notional)/(amm[pair]['Staked_amount_Short'][i])/amm[pair]['Ratio'][i]-1)*notional
        #expected USDC cost for a pair of wash trade (long and short) 
        expected_cost = trading_fee+estimated_slippage #round trip cost based on notional
        """step 2b - judge the expected maximum trading reward to be received over next 24 hours because trading volumes will receive trading reward for next 24 hours
        coefficient is dynamic as our emission schedule and allocation of trading reward across markets will change 
        max_reward_24hr for the next 2k of wash trade = coefficient_market * 60 *60 *24 * (cumulaitve_trading_volume of this vault wallet+2k)/(cumulative trading volume of this market+2k)
        judge the value of the reward in USDC = max_reward_24hr for next 2k of wash trade * current STRP price 
        if reward value in USDC > expected cost in USDC, then put on the long, and then wait for >100 blocks to close the trade 
        """
        #plug in the parameter from the smart contract of thet reward emission coefficient to be received 
        """below expected_return is the value to show as expected return % of the vault
        APY% of token hunter = expected return / 24 * 365 
        """
        expected_return = (vault[pair]['cumulative_Trading_vol'][i]+2000)/(2000+amm[pair]['cumulative_Trading_Vol_rebased_agg'][i])*0.0052829645937523*60*60*24*uniswap_market['STRP_Price'][i]
        #find the notional amount that maximize the (expected return - expected cost)
        #if expected net return < 0 (max initial value), then don't put on teh trade 
        if (expected_return - expected_cost)>0: 
        else:               
            pass            
        #assume 20 minutes later (aka block number > 100)
        #CLOSE THE LONG POSITION
        """MAKE SURE MORE THAN 100 BLOCKS PASSED FROM LAST TRADE OF THIS WALLET:
        (1) If the vault can own 2 wallet addresses, then it can open long and short at the same time over 2 wallets and close the position 100 blocks later, because accont A and B are perfectly hedged against each other, then there is zero market risk. But 2 wallet under 1 vault is not covered in the current vault structure, so we won't consider to optimize on this front until later
        (2) because the positions are closed within 20 minutes, so there is hardly any trading PnL, but paying trading fee and slippage to AMM, so LP price of the vault drops to 0 over time, while the return are all reflected in STRP rewards for which we won't sell on behalf of vault investors. It depends on the vault investors to claim and sell after they withdraw from the vault. Therefore, token hunter vault is not fully compatible with USDC_PRICING_BASED vault right now 
            
        """
        """step 3 - close the position and wait for another 20 minutes (100 blocks) until next pair of wash trade (long and short)"""
        if vault[pair]['avg_price'][i]!=0.0:
        else:
            """step 4 - if no position to be closed, then repeat step 2a and 2b to see if any position to be put on if strp reward to be received over next 24 hr > expected cost
            