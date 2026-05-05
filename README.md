# MarmaraCargo Logistics Network Optimization

## 1. Real-World Problem Context
In the highly competitive e-commerce sector, offering fast and reliable "Same-Day Delivery" is a critical factor for customer satisfaction. Operating in the Anatolian Side of Istanbul, **MarmaraCargo** faces intense and unpredictable traffic conditions while transporting high-priority deliveries from its Main Distribution Center to end-customer zones. Inefficient route selection leads to Service Level Agreement (SLA) violations, increased fuel costs, and poor resource utilization. A data-driven logistics information system is required to optimize delivery routes dynamically.

## 2. Problem Definition
The objective of this project is to determine the theoretical shortest (fastest) path for a delivery vehicle traveling from the Main Distribution Center (Tuzla) to the Customer Delivery Zone (Pendik West). The problem aims to minimize the total travel time (in minutes) by navigating through various regional hubs, transfer points, and local stations, thereby providing a reliable baseline for MarmaraCargo's routing software.

## 3. Network Model
The problem is formulated as a **Directed Weighted Graph**:
*   **Nodes ($V$):** Represent the physical logistics facilities (distribution centers, hubs, stations).
*   **Edges ($E$):** Represent the road connections (highways, local roads, arteries) between these facilities.
*   **Weights ($W$):** Represent the historical average travel time in minutes for each specific road segment.

## 4. Nodes and Edges
The network consists of **7 nodes** and **9 edges**. The data is stored in the `data/marmaracargo_edges.csv` file. 

### Dataset Column Explanations & Units of Measurement
The dataset is structured with the following columns to properly represent the network:

| Column Name | Data Type | Meaning & Unit of Measurement |
| :--- | :--- | :--- |
| `source_node` | String | The ID of the starting node for the edge (e.g., N0). |
| `target_node` | String | The ID of the ending node for the edge (e.g., N1). |
| `source_label` | String | The readable, real-world name of the starting facility. |
| `target_label` | String | The readable, real-world name of the ending facility. |
| `travel_time_minutes` | Integer | **(Numerical Attribute):** The average travel time required to traverse the edge. **Unit: Minutes.** |
| `route_type` | String | Categorization of the road type (e.g., Highway, Local Route). |
| `notes` | String | Additional context regarding traffic density or road conditions. |

### Data Assumptions (Assumptions Behind the Data)
To mathematically model this real-world scenario using Dijkstra's algorithm, the following assumptions were made regarding the dataset:
1.  **Historical Averages:** The `travel_time_minutes` values represent historical average driving times under normal weather conditions. Real-time dynamic traffic anomalies (like sudden accidents) are not factored into the base dataset.
2.  **Directed Graph (One-Way Flow):** The edges are assumed to be directed (from Source to Target) reflecting the forward flow of logistics deliveries. Return trips are not modeled in this specific routing problem.
3.  **No Node Delay:** The algorithm strictly optimizes for transit time on the edges. Loading, unloading, and processing times at the transfer points (nodes) are assumed to be constant and are excluded from the edge weights.
4.  **No Capacity Constraints:** It is assumed that the delivery vehicle has sufficient capacity to carry the VIP order, and the roads have no restrictions preventing the vehicle's passage.

## 5. Selected Algorithm
**Dijkstra's Shortest Path Algorithm** was selected for this problem. Since time (minutes) is used as the edge weight and there are no negative weights in travel time, Dijkstra's algorithm is the most efficient and mathematically sound method to find the single-source shortest path in this directed graph.

## 6. Python Implementation
The solution is implemented in Python. The core algorithm and graph structures are built using the `networkx` library. The network topology and the highlighted shortest path are visualized using the `matplotlib` library. Data ingestion from the CSV file is handled dynamically using Python's built-in `csv` module, ensuring that the script adapts automatically if the data changes.

## 7. Results
The algorithm successfully analyzed all possible routes. Based on the current traffic and travel time data, the model identified **two equally fast optimal paths**:
*   **Fastest Route Alternative 1:** N0 $\rightarrow$ N1 $\rightarrow$ N3 $\rightarrow$ N5 $\rightarrow$ N6
*   **Fastest Route Alternative 2:** N0 $\rightarrow$ N2 $\rightarrow$ N4 $\rightarrow$ N5 $\rightarrow$ N6
*   **Total Travel Time:** 82 Minutes

The visual representation of the network can be found in the `results/marmaracargo_network_visualization.png` file.

## 8. Managerial Interpretation
The mathematical result of 82 minutes and the discovery of two equally optimal routes provide excellent strategic insights for MarmaraCargo management:
1.  **Dual-Route Strategy (Redundancy):** Having two optimal routes (both 82 minutes) is a significant operational advantage. The dispatch system can split the VIP delivery volume equally between the N1-N3 corridor and the N2-N4 corridor, preventing congestion at any single transfer point.
2.  **Vulnerability Shift:** With the travel time on the N4-N5 local route increasing to 19 minutes, the northern highway route (N1-N3) has become just as competitive as the coastal alternative. Management should monitor real-time traffic; if the coastal road (N2-N4) experiences even a 1-minute delay, the fleet should be dynamically redirected to the N1-N3 highway route.
3.  **Critical Bottleneck (N5 to N6):** Regardless of the chosen path, both optimal routes must pass through the `N5 -> N6` segment (Local Station to Delivery Zone), which takes 20 minutes. This last-mile segment is the ultimate bottleneck. Investments in electric cargo bikes or extra couriers specifically for this neighborhood step will yield the highest ROI in reducing overall delivery times.
4.  **SLA Establishment:** The 82-minute theoretical minimum provides a realistic baseline to establish a "120-Minute VIP Delivery Guarantee," allowing a safe 38-minute buffer for loading, unloading, and unexpected delays.

## 9. How to Run the Code
To run this project on your local machine, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Python installed.
3. Install the required dependencies:
   ```bash
   pip install networkx matplotlib pandas
4. Execute the Python script from the root directory of the project:
    python src/solution.py
5. The console will display the step-by-step route and alternative comparisons. The output graph will be saved in the `results/` folder.

## 10. References
*   Course materials, lecture slides, and notes from the Management Information Systems - Network Optimization module.
*   Official documentation for Python libraries (`networkx`, `matplotlib`, `pandas`).