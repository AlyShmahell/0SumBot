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

public class zeroSumBot {
  
  public static void DoTurn(PlanetWars pw) {
    

    /*************************************************
     * find the strongest and allied planet
     */
    Planet strongestAllyPlanet = null;
    Planet weakestAllyPlanet = null;
    double strongestAllyPlanetScore = Double.MIN_VALUE;
    double weakestAllyPlanetScore = Double.MIN_VALUE;
    for (Planet p : pw.MyPlanets()) {
      double sscore = (double) p.NumShips();
      if (sscore > strongestAllyPlanetScore) {
        strongestAllyPlanetScore = sscore;
        strongestAllyPlanet = p;
      }
      double wscore = 1.0 / (1 + p.NumShips());
      if (wscore > weakestAllyPlanetScore) {
        weakestAllyPlanetScore = wscore;
        weakestAllyPlanet = p;
      }
    }
    
    /**
     * find the strongest and weakest enemy planet
     */
    Planet strongestEnemyPlanet = null;
    Planet weakestEnemyPlanet = null;
    double strongestEnemyPlanetScore = Double.MIN_VALUE;
    double weakestEnemyPlanetScore = Double.MIN_VALUE;
    for (Planet p : pw.EnemyPlanets()) {
      double sscore = (double) p.NumShips();
      if (sscore > strongestEnemyPlanetScore) {
        strongestEnemyPlanetScore = sscore;
        strongestEnemyPlanet = p;
      }
      double wscore = 1.0 / (1 + p.NumShips());
      if (wscore > weakestEnemyPlanetScore) {
        weakestEnemyPlanetScore = wscore;
        weakestEnemyPlanet = p;
      }
    }
    
    /**
     * find the strongest and neutral planet
     */
    Planet strongestNeutralPlanet = null;
    double strongestNeutralPlanetScore = Double.MIN_VALUE;
    Planet weakestNeutralPlanet = null;
    double weakestNeutralPlanetScore = Double.MIN_VALUE;
    for (Planet p : pw.NeutralPlanets()) {
      double sscore = (double) p.NumShips();
      if (sscore > strongestNeutralPlanetScore) {
        strongestNeutralPlanetScore = sscore;
        strongestNeutralPlanet = p;
      }
      double wscore = 1.0 / (1 + p.NumShips());
      if (wscore > weakestNeutralPlanetScore) {
        weakestNeutralPlanetScore = wscore;
        weakestNeutralPlanet = p;
      }
    }
    
    /*************************************************
     * find Planet Targetted by strongest enemy fleet
     */
    Fleet strongestEnemyFleet = null;
    double strongestEnemyFleetScore = Double.MIN_VALUE;
    for (Fleet f : pw.EnemyFleets()) {
      double score = (double) f.NumShips();
      if (score > strongestEnemyFleetScore) {
        strongestEnemyFleetScore = score;
        strongestEnemyFleet = f;
      }
    }
    Planet IndangeredPlanet = pw.GetPlanet(strongestEnemyFleet.DestinationPlanet());

    /*************************************************
     * choose source and destination planets for next attack order
     */
     Planet dest = null;
     Planet source = strongestAllyPlanet;
     int numShips = strongestAllyPlanet.NumShips()/2;
     if(IndangeredPlanet.Owner()==1 && IndangeredPlanet!=strongestAllyPlanet)
     	 if(strongestEnemyFleet.NumShips() > IndangeredPlanet.NumShips())
     	    if(numShips >  strongestEnemyFleet.NumShips())
     	       	   dest = IndangeredPlanet;
     else if(numShips > strongestEnemyPlanet.NumShips())
     	 dest = strongestEnemyPlanet;
     else
     	 dest = weakestEnemyPlanet;
 
    /*************************************************
     * send fleet from our source planet to the destination planet
     */
    if (source != null && dest != null) {
      pw.IssueOrder(source, dest, numShips);
    }
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
