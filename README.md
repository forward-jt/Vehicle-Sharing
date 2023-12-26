# Vehicle-Sharing
# Circular Economy with Vehicle Sharing

The project for operating research.
Dec ,2023/ by 黃瑞澤、吳紹維
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

### Assumption
* Self-driving vehicles：Robust self-contained system, without the need to consider human erratic behavior
* Rides are not shared（Two services can not be served by the same vehicle simultaneously﹚：The vehicle can serve different customers but can only serve one group of customers at a time.
* Customers pay for the travel distance：The cost is directly proportional to the distance traveled.
* Constant maintenance cost：The maintenance cost of the vehicle remains fixed since the vehicle is dispatched every day.
* Constant moving speed：The vehicle's movement speed is fixed.

### Definition
We will provide the customers' pickup locations, destinations, and times, as well as the number of available vehicles within the entire system.
The vehicles within the dispatch system will be assigned to fulfill the service demand. 
The object is to increase profit and reduce costs.

 
## Method
The figure below illustrates the methodology framework, divided into two stages. The first stage, the Single-horizon model, involves constructing a Binary Integer Programming Model and converting it into a Linear Programming Model. The second stage considers variations in time slots to construct the Linear Programming Model.

![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/MethodologyFramework.png)


### Notation


### Gather Information into a Graph

The following will describe the five types of edges:
* Dispatching: This edge represents the movement from the starting point to the service's pickup location.The weight is a fixed dispatching cost plus moving cost.
* Serving: This edge represents completing the service.As the objective is to minimize the cost, the weight for this edge will be the obtained profit with a minus sign.
* Relocating: When a vehicle finishes its current service and relocates within a feasible time to another service, this edge is formed.The criteria for this edge consider whether the vehicle can arrive at the new service's pickup location on time.The weight is moving cost.
* Collecting: After completing a service, the vehicle returns to the collection point.The weight of this edge represents the cost incurred from the movement.
* Virtual: This edge is used to balance the number of vehicles. Vehicles that are not in use will be assigned to this edge.
![Image text](https://github.com/forward-jt/Vehicle-Sharing/blob/phase-2/img_storage/Single-horizon%20model%20Edge%20Graph.png)


  
## Resources
* [Designing optimal autonomous vehicle sharing and reservation systems: A linear programming approach](https://www.sciencedirect.com/science/article/pii/S0968090X17302322?casa_token=jjseGP72pYAAAAAA:kXwFtWkj0CzlnhZvTzHuJ03hc2j4h-JgGh3Grc_laNBF_2r-m2Rf-S-iZQBNZ-THtNiiMoIvq_Pq)
* [On-demand high-capacity ride-sharing via dynamic trip-vehicle assignment](https://www.pnas.org/doi/abs/10.1073/pnas.1611675114)
* [Shared Autonomous Taxi System and Utilization of Collected Travel-Time Information](https://www.hindawi.com/journals/jat/2018/8919721/)
