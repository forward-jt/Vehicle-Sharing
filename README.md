# Vehicle-Sharing
# Circular Economy with Vehicle Sharing

The project for operating research.<br>
Dec 26,2023/ by 黃睿澤、吳紹維
## Outline
* Motivation and Background
* Question Definition
    * Assumption
    * Definition
* Method
    * Build AVSE Network
    * Binary Integer Programing Model
    * Equivalent Linear Programing Model
* Evaluation
    * Dataset
    * Result
* Conclusion
* Reference

## Motivation and Background
The high convenience of owning a private vehicle for mobility has led to an increasing rate of private vehicle ownership today. However, this trend has resulted in issues such as high expenses, increased resource consumption, environment cost.

One solution to address this is through the utilization of vehicle sharing.By employing multiple shared vehicles within a designated area to serve the population, this approach provides a level of convenience similar to private car ownership while simultaneously reducing the number of private vehicles within cities.
The benefits it can bring include reducing cost expenditures, maximizing product durability and recyclability, lowering environmental costs while enhancing vehicle utilization rates.

The challenge, however, is to improve the quality of the service.

## Qusetion Definition

### Definition
We will provide the customers' pickup locations, destinations, and times, as well as the number of available vehicles within the entire system.
The vehicles within the dispatch system will be assigned to fulfill the service demand. 
The object is to increase profit and reduce costs.

### Assumption
* Self-driving vehicles：Robust self-contained system, without the need to consider human erratic behavior
* Rides are not shared（Two services can not be served by the same vehicle simultaneously﹚：The vehicle can serve different customers but can only serve one group of customers at a time.
* Customers pay for the travel distance：The cost is directly proportional to the distance traveled.
* Constant maintenance cost：The maintenance cost of the vehicle remains fixed since the vehicle is dispatched every day.
* Constant moving speed：The vehicle's movement speed is fixed.



 
## Method
The figure below illustrates the methodology framework, divided into two stages. The first stage, the Single-horizon model, involves constructing a Binary Integer Programming Model and converting it into a Linear Programming Model. The second stage considers variations in time slots to construct the Linear Programming Model.

![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/MethodologyFramework.png)


### Notation


* $S$：The set of services<br>
   * $i,j$：The indices into the set $S$<br>
   * $i^{+},i^{-}$：The nodes represents the start & the end of the service 𝑖, respectively<br>
   * $l^{+},l^{-}$：The pickup and drop off location of the service 𝑖, respectively<br>
      * $|𝑙_{𝑎}−𝑙_{𝑏} |, |𝑙_{𝑏}  −𝑙_{𝑎} |$: The distance between location 𝑎 and 𝑏<br>
   * $t^{+},t^{-}$：: The pickup and drop off time of the service 𝑖, respectively<br>
* $o,d$：The virtual nodes represent origin & destination, respectively
* $N={i^{+},i^{-}|∀ 𝑖∈𝑆}∪{𝑜, 𝑑}$：The set of nodes
* $E$：The set of edges
   * $e_{a,b}$：The edge between node 𝑎 and 𝑏
   * $W_{a,b}$：The weight of the edge between node 𝑎 and 𝑏
* $v$：The velocity of vehicles
* $n$：The number of vehicles

### Gather Information into a Graph
Edges are categorized into five types, as explained below: 
![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/Single-horizon%20model%20Edge.png)
The following will describe the five types of edges:
* Dispatching: This edge represents the movement from the starting point to the service's pickup location.The weight is a fixed dispatching cost plus moving cost.
* Serving: This edge represents completing the service.As the objective is to minimize the cost, the weight for this edge will be the obtained profit with a minus sign.
* Relocating: When a vehicle finishes its current service and relocates within a feasible time to another service, this edge is formed.The criteria for this edge consider whether the vehicle can arrive at the new service's pickup location on time.The weight is moving cost.
* Collecting: After completing a service, the vehicle returns to the collection point.The weight of this edge represents the cost incurred from the movement.
* Virtual: This edge is used to balance the number of vehicles. Vehicles that are not in use will be assigned to this edge.

### Binary Integer Programming Model
Based on the aforementioned graph, construct a Binary Integer Programming Model:
* Decision variables
  * $y_{a,b}, ∀ 𝑒_{𝑎,𝑏}∈𝐸$：Whether $𝑒_{𝑎,𝑏}$ is selected<br>
    
The decision variable y represents whether a service is selected. If y equals 1, it indicates that the service has been chosen.

* Objective function
   * $Min(cost-profit+penalty)$
      * $𝑐𝑜𝑠𝑡−𝑝𝑟𝑜𝑓𝑖𝑡=∑_{𝑒_{𝑎,𝑏}∈𝐸}．𝑊_{𝑎,𝑏}．𝑦_{𝑎,𝑏}$
      * $𝑝𝑒𝑛𝑎𝑙𝑡𝑦=∑_{∀ 𝑖∈𝑆}．−𝑊_{𝑖^{+},𝑖^{−}}．(1 −𝑦_{𝑖^{+},𝑖^{−}})$<br>

The objective is to minimize costs.Therefore, the objective function subtracts the earned profits from the costs and includes the penalty for services that weren't selected.
The Cost and Profit are derived by multiplying the weights(w) with the variable y.

* Constraints
   * $y_{a,b}$=0 or 1,∀ $𝑒_{𝑎,𝑏}$∈𝐸 −{$𝐸_{𝑜,𝑑}$}<br>
    If $y$ equals 1, it indicates that the service has been chosen.<br>
   * $y_{o,d}≤=n$<br>
    The number of unassigned vehicles will be less than the total number of vehicles.<br>
   * $∑_{𝑖∈𝑆}𝑦_{𝑜,𝑖^{+}} +𝑦_{𝑜,𝑑}=𝑛$<br>
    The sum of assigned and unassigned vehicles will be equal to the total number of vehicles.<br>
   * $∑_{𝑏∈𝑁}𝑦_{𝑏,𝑎}=∑_{𝑏∈𝑁}𝑦_{𝑎,𝑏},∀𝑎∈𝑁 −${𝑜, 𝑑}<br>
  This formula is used to balance the flow of each node.<br>
   * $∑_{𝑖∈𝑆}𝑦_{𝑖^{−},𝑑}+𝑦_{𝑜,𝑑}=𝑛$<br>
   The total of vehicles completing assignments and those being unassigned and recovered will equal the total number of vehicles.<br>


The constraints are as follows:<br>
1.If y equals 1, it indicates that the service has been chosen.<br>
2.The number of unassigned vehicles will be less than the total number of vehicles.<br>
3.The sum of assigned and unassigned vehicles will be equal to the total number of vehicles.<br>
4.This formula is used to balance the flow of each node.<br>
5.The total of vehicles completing assignments and those being unassigned and recovered will equal the total number of vehicles.<br>

### Constraint Coefficient Matrix Is Totally Unimodular

Integer programming is difficult to solve, so we need to find a way to convert it into a linear model to enhance solving efficiency. 
If the constraint coefficient matrix of the linear programming module is totally unimodular, it can be proven that all solutions correspond to integers. Following the reverse condition, if the constraint coefficient matrix of the Integer Programming Model is totally unimodular, it can be transformed into a linear programming module.
Here are the three conditions that Matrix A must satisfy to be considered Totally Unimodular:
![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/Constraint%20Coefficient%20Matrix%20Is%20Totally%20Unimodular.png) 

The paper mentions that the aforementioned constraints can be transformed into Totally Unimodular, allowing relaxation of the decision variables (changed to >= 0), thereby converting it into an Integer Programming Model.

### Linear Programming Model
Here is the revised Linear Programming Model with decision variables replaced by 'x' instead of the original 'y':

![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/Linear%20Programming%20Model.png)

The first constraint is relaxed to be <=1, while the rest of the constraints remain unchanged.

### The Latest Served Services are included in New Cycle
Next, we will introduce the scenario where time is divided into multiple time slots, as this situation better reflects the problems encountered in real-life situations.
Considering the time slot, the edge graph is as follows: 

![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/Multi-horizon%20model%20Edge.png)

This diagram uses 'K' to denote the last service of the previous time slot and the first service of the next time slot.

### Linear Programming Model for Multiple Timeslots
The linear programming model considering timeslots is exactly the same here, except for an additional constraint, which is the last constraint below. 'k-' denotes the transition from completing services in the previous round to starting services in the next round. Since 'k-' node has no input flow in this round but must have an output flow, this constraint is necessary.

![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/Linear%20Programming%20Model%20for%20Multiple%20Timeslots.png)



## Evaluation
### New York Taxi Dataset
The dataset we utilized is from the New York Taxi Dataset, collected by the New York City Taxi and Limousine Commission. We utilized the 'Pick up' and 'Drop off' times from this dataset. Regarding the location, we selected regions. Consequently, we further identified the centers of each region to calculate distances.

### Requires Only 1/3 Vehicles Compared to 1-man-1-vehicle
![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/RequiresVehicles.png)

In this chart, it can be observed that as the number of services increases, the Vehicles/Services ratio rapidly decreases, requiring approximately only one-third of the vehicles to meet the demand.

### Required Vehicles Reduces as Speed Increases
![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/Required%20Vehicles%20Reduces%20as%20Speed%20Increases.png)

We were curious about how different speeds of each vehicle would impact our model. Therefore, we conducted tests for various speeds and found that as the speed increased, the number of vehicles needed to meet service requirements decreased. However, the difference compared to the previous scenario was not significant.


### Profit Only Reduces Slightly for Multiple Timeslots
![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/Profit%20Only%20Reduces%20Slightly%20for%20Multiple%20Timeslots.png)

We compare two different versions of the model. The blue line represents the global optimal solution, while the red line depicts the smaller model for each time period solved within hourly intervals. We can observe the profit displayed here. In comparison to the global optimum, the profit only decreases slightly, but it still maintains a fairly good performance compared to the optimal solution.


## Conclusion
Our conclusion is that sharing contributes to higher vehicle utilization rates. As observed in the evaluation section, we can see that compared to scenarios with one car per service, only half or a third of the vehicles are needed. The increased vehicle utilization also reduces societal and environmental costs. Additionally, the vehicle utilization rate further decreases with an increase in vehicle speed. When comparing the global optimal model with the smaller model for each time period, the profit only slightly decreases.

## Future Research
After analyzing vehicle speed and demand, this study found that higher speeds require fewer vehicles. However, it did not consider the negative impacts of speed. In the future, there is potential to enhance the objective function by adding a penalty-related function concerning speed. This function would be related to the speed, following quadratic functions or similar methods to model penalties.

  
## Resources
* [Designing optimal autonomous vehicle sharing and reservation systems: A linear programming approach](https://www.sciencedirect.com/science/article/pii/S0968090X17302322?casa_token=jjseGP72pYAAAAAA:kXwFtWkj0CzlnhZvTzHuJ03hc2j4h-JgGh3Grc_laNBF_2r-m2Rf-S-iZQBNZ-THtNiiMoIvq_Pq)
* [On-demand high-capacity ride-sharing via dynamic trip-vehicle assignment](https://www.pnas.org/doi/abs/10.1073/pnas.1611675114)
* [Shared Autonomous Taxi System and Utilization of Collected Travel-Time Information](https://www.hindawi.com/journals/jat/2018/8919721/)
