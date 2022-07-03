# Description

In Real Time Strategy (RTS) games players are placed on a map to gather resources, build units and attack their opponent. To achieve this as efficiently as possible, certain strategies are followed.

RTS games have a steep learning curve. Players need to manage their resources, follow a certain strategy and react to advances from their opponent. In team games they must cooperate with their teammates. A lot of decisions need to be made, many of which are made under pressure. Because of this, the play style varies drastically based on skill level [[6]](#6).

Understanding one’s own playstyle is crucial when trying to improve at an RTS game. It enables players to spot their weaknesses and highlights key game events [[1]](#1). A study including the RTS game StarCraft II has shown that players are primarily interested in seeing the impact of their decision, their current resources and their action sequencing [[3]](#3).
Age of Empires II Definitive Edition (AoE II DE) was released in 2019 and is a remake of the original Age of Empires II, which was released in 1999. Players choose a certain civilisation, which features specific bonuses, on a wide variety of maps and play- modes. The map can influence gameplay decisions drastically. For example, it influences when and which buildings and unit types are built, as well as which technologies are researched to improve certain aspects of your economy or military. At the end of a game a summary is displayed, and a replay file is created. The summary is not interactive and only highlights battles as key events displayed on a timeline.

Skill level is measured with ELO rating points (named after its creator Arpad Elo), which are comparable to MMR ratings in other games. Players are matched based on their ELO ratings for the chosen game mode. The rating increases or decreases based on a win or loss. The specific amount is determined by the player’s current ELO rating in relation to their opponent’s ELO rating.

There are not many tools available for AoE II DE players to analyse their replays. aoe2.net offers an API to fetch ELO development of players in recent games [[8]](#8). Similarly, aoestats displays win rates of different civilisations [[7]](#7). CaptureAge enables players to open games and analyse them [[9]](#9). Aoe2 Insights enables upload of a replay file and display key events directly on the website. Users can interact with the map and see player actions. It also guesses the chosen strategy. However, all other analysis components are static [[11]](#11). Existing solutions do not enable players to compare their gameplay with other replay data. Interactivity is also limited.

Multiplayer Online Battle Arena (MOBA) games are a subgenre of RTS games. Games such as Dota 2 and League of Legends are very popular. They differ from traditional RTS games in that players must focus on a single character and manage communication with their teammates. Due to their popularity, novel replay analysis tools exist, e.g., Stratz [[2]](#2), which allow for a swift understanding of player behaviour. Such a tool does not exist for AoE II DE.

Research for the RTS game StarCraft II by Kuan et al. (2017) [[4]](#4) has shown that utilising a heat map to display player action on game map is useful for players. This is especially the case when adding used units and strategies in an adjacent view [[4]](#4). Li et al. (2017) [[5]](#5) have shown that visual analysis of replay data can help understand game outcomes of MOBA games. Due to the similarities of MOBA and RTS games, this stirs up an interesting discussion about gameplay analysis.

Visualisation of AoE II DE replay data theoretically could be a very powerful tool to help players understand why games play out in a certain manner, as showcased by Kuan et al. (2017) [[4]](#4). Currently, there are a lot of unknowns regarding game play data, especially regarding comparisons in between replay files. Another unknown detail is which data sets should be highlighted to enable the best possible learning effect [[3]](#3).

The goal of this project is to visualise AoE II DE replay data in a comprehensible manner and make it comparable to other replay files. This would enable a straight-forward comparison of different skill levels. This includes - for example - average villager and building count over the course of games.

## References
<a id="1">[1]</a>
Medler, B. and Magerko, B. 2011. Analytics of Play: Using Information Visualization and Gameplay Practices for Visualizing Video Game Data.

<a id="2">[2]</a>
Stratz: 2022. https://stratz.com/welcome. Accessed: 2022-04-07.

<a id="3">[3]</a>
Wallner, G. et al. 2021. What players want: Information needs of players on post-game visualizations. Conference on Human Factors in Computing Systems - Proceedings (May 2021).

<a id="4">[4]</a>
Yen-Ting Kuan et al. 2017. Visualizing Real-Time Strategy Games: The Example of StarCraft II. IEEE Conference on Visual Analytics Science and Technology (VAST) (2017).

<a id="5">[5]</a>
Li, Q. et al. 2017. A Visual Analytics Approach for Understanding Reasons behind Snowballing and Comeback in MOBA Games. IEEE Transactions on Visualization and Computer Graphics. 23, 1 (Jan. 2017), 211–220. DOI:https://doi.org/10.1109/TVCG.2016.2598415.

<a id="6">[6]</a>
Ji-Lung Hsieh and Chuen-Tsai Sun 2008. Building a Player Strategy Model by Analyzing Replays of Real-Time Strategy Games. International Joint Conference on Neural Networks (2008), 3106–3111.

<a id="7">[7]</a>
aoestats: 2022. https://aoestats.io. Accessed: 2022-04-07.

<a id="8">[8]</a>
AoE2.net: 2022. https://aoe2.net. Accessed: 2022-04-07.

<a id="9">[9]</a>
CaptureAge: 2022. https://captureage.com. Accessed: 2022-04-07.

<a id="10">[10]</a>
AoE2.net: 2022. https://aoe2.net. Accessed: 2022-04-07.

<a id="11">[11]</a>
AoE2 Insights: 2022. https://www.aoe2insights.com. Accessed: 2022-04-07.