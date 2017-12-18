/**
 * Copyright 2017 Aly Shmahell
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy
 * of the License at http:#www.apache.org/licenses/LICENSE-2.0 . Unless
 * required by applicable law or agreed to in writing, software distributed
 * under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 * CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
 * 
 * Author: Aly Shmahell
 */

import java.util.*;
import java.io.*;

public class zeroSumBot {

  public static void DoTurn(PlanetWars pw) {
 
    /**
     * Initial Parameters
     */
    Random rand = new Random();
    Planet base = null;
    Planet target = null;
    int baseFleet = 0;
    boolean AttackMode = false;
    
    /***
     * Optimized Parameters : generated by the Genetic Algorithm to be used as seed for the Stochastic Parameters
     * "o" prefix is notation for Optimized
     * "R" affix is notation for Range of stocasticity
     */
    /**
     * optimized for Player's total number of ships to total ship production ratio
     */
    double oPWNumShipsProduction1 = 0.6552286530005225;
    /**
     * optimized for player's base planet's total number of ships
     */
    int oPNumShips = 37;
    /**
     * optimized for player's base planet's growth rate
     */
     int oPGrowthRate = 27;
    /**
     * optimized for enemy's target planet's total number of ships
     */
    int oENumShips = 21;
    /**
     * optimized for enemy's target planet's growth rate
     */
    int oEGrowthRate = 28;
    /**
     * optimized for neutrals' target planet's total number of ships
     */
    int oNNumShips = 34;
    /**
     * optimized for neutrals' target planet's growth rate
     */
    int oNGrowthRate = 34; 
    /**
     * optimized for good striking distance
     */
    int oDistance = 14;
    /**
     * optimized for player's division of base ships into remaining base ships and base fleet
     */
     int fleetDivider = 3;
    /**
     * mapDispersion
     */
     int oLocalMinima = 51;
    
    /**
     * attack mode selection
     */
    if( (double) pw.NumShips(1)/(1+pw.Production(1)) > oPWNumShipsProduction1)
    	AttackMode = true;
    else
    	AttackMode = false;
   
    /**
     * base selection
     */
    for(Planet p : pw.MyPlanets()){
      if(base==null){
          if(p.NumShips() > oPNumShips && p.GrowthRate() > oPGrowthRate)
      	      base = p;
      }
      else if(p.NumShips() > base.NumShips() && p.GrowthRate() > base.GrowthRate())
      	  	  base = p;
     }
    /**
     * base force selection
     */
    if(base==null)
    {
    	double baseScore = Double.MIN_VALUE;
        for (Planet p : pw.MyPlanets()) {
            double score = (double) p.NumShips() / (1 + p.GrowthRate());
            if (score > baseScore) {
                baseScore = score;
                base = p;
            }
        }
    }
    if(base==null)
    	return;
    /**
     * fleet selection
     */
    baseFleet = (int) base.NumShips()/fleetDivider;
    
    /**
     * finding map dispersion
     */
     int localMinima = 0;
     Planet closestEnemy = null;
     double closestEnemyScore = Double.MAX_VALUE;
        for (Planet e : pw.EnemyPlanets()) {
            double score = (double) pw.Distance(base,e);
            if (score < closestEnemyScore) {
                closestEnemyScore = score;
                closestEnemy = e;
            }
        }
     if(closestEnemy==null)
        	return;
     localMinima =  pw.Distance(base,closestEnemy);
     
     /**
      * choosing target
      */
    if(AttackMode == true){
    	/**
    	 * target selection from enemy or Neutral
    	 */
    	 if(localMinima < oLocalMinima)
    	 {
			for(Planet e : pw.EnemyPlanets()){
			  if(target==null){
				  if(e.NumShips() < oENumShips && e.GrowthRate() < oEGrowthRate && pw.Distance(base,e) < oDistance)
					  target = e;
			  }
			  else if(e.NumShips() < target.NumShips() && e.GrowthRate() < target.GrowthRate() && pw.Distance(base,e) < pw.Distance(base,target))
					  target = e;
			 } 
    	 }
		else
		{
			for(Planet n : pw.NeutralPlanets()){
			  if(target==null){
				  if(n.NumShips() < oENumShips && n.GrowthRate() < oEGrowthRate  && pw.Distance(base,n) < oDistance)
					  target = n;
			  }
			  else if(n.NumShips() < target.NumShips() && n.GrowthRate() < target.GrowthRate() && pw.Distance(base,n) < pw.Distance(base,target))
					  target = n;
			 } 
		}
		/**
		 * target force selection from Not My Planets in case of no target
		 */
		if(target == null)
		{
			double npScore = Double.MIN_VALUE;
			for (Planet np : pw.NotMyPlanets()) {
				double score;
				if (localMinima < oLocalMinima)
				    score = (double) (1 + np.GrowthRate()) / (np.NumShips() * pw.Distance(base,np));
			    else
				    score = (double) 1 / pw.Distance(base,np);
				if (score > npScore) {
					npScore = score;
					target = np;
				}
			}	
		}
    }
    
    if(AttackMode == false){
		/**
		 * ally selection
		 */
		for(Planet p : pw.MyPlanets()){
		  if(target==null){
			  if(p.NumShips() < oPNumShips && p.GrowthRate() < oPGrowthRate  && pw.Distance(base,p) < oDistance)
				  target = p;
		  }
		  else if(p.NumShips() < target.NumShips() && p.GrowthRate() < target.GrowthRate() && pw.Distance(base,p) < pw.Distance(base,target))
				  target = p;
		 }
		/**
		 * ally force selection
		 */
		if(target==null)
		{
			double targetScore = Double.MIN_VALUE;
			for (Planet p : pw.MyPlanets()) {    
				double score;
				if(localMinima < oLocalMinima)
				    score = (double) (1 + p.GrowthRate()) / (p.NumShips() * pw.Distance(base,p));
			    else
			    	score = (double) 1 / pw.Distance(base,p);
				if (score > targetScore) {
					targetScore = score;
					target = p;
				}
			}
		}     
    }
    
    /**
     * send fleet from base to target
     */
    if (base != null && target != null)
      pw.IssueOrder(base, target, baseFleet);
    else
    	return;
  }
  
  public static void main(String[] args) {
    String line = "";
    String message = "";
    int c;
    try {
      while ((c = System.in.read()) >= 0) {
        switch (c) {
          case '\n':
            if (line.equals("go")) {
            PlanetWars pw = new PlanetWars(message);
            DoTurn(pw);
            pw.FinishTurn();
            message = "";
          } else {
            message += line + "\n";
          }
          line = "";
          break;
          default:
            line += (char) c;
            break;
        }
      }
    } catch (Exception e) {
    }
  }
}
