# IE Sustainability Datathon March 2026

## IE Datathon March 2026: Intelligent Electric Mobility – Iberdrola

### THE CHALLENGE: DESIGNING TOMORROW'S CHARGING NETWORK

*"Connecting the present with the energy of the future"*

---

## Table of Contents

1. [Introduction to the challenge](#1-introduction-to-the-challenge)
2. [Scope of Analysis](#2-scope-of-analysis)
3. [Datathon objectives](#3-datathon-objectives)
4. [Key references and Data Sources](#4-key-references-and-data-sources)
   - 4.1 [Main Data Sources](#41-main-data-sources)
   - 4.2 [Additional Data Sources](#42-additional-data-sources)
   - 4.3 [Innovation & Creative Problem Solving: The Role of Assumptions](#43-innovation--creative-problem-solving-the-role-of-assumptions)
5. [The submissions: Content to be delivered](#5-the-submissions-content-to-be-delivered)
   - 5.1 [Deliverable 1: Code files](#51-deliverable-1-code-files)
   - 5.2 [Deliverable 2: Output datasets (Charging Network Proposal)](#52-deliverable-2-output-datasets-charging-network-proposal)
   - 5.3 [Deliverable 3: BI Visualization](#53-deliverable-3-bi-visualization)
   - 5.4 [Deliverable 4: Analytical Report (Executive Summary)](#54-deliverable-4-analytical-report-executive-summary)
   - 5.5 [Deliverable 5: Final Presentation (Pitch)](#55-deliverable-5-final-presentation-pitch)
6. [Evaluation Criteria](#6-evaluation-criteria)
   - 6.1 [Overall Weighting](#61-overall-weighting)
   - 6.2 [Technical Component + BI Visualization (50%)](#62-technical-component--bi-visualization-50)
   - 6.3 [Analytical Report & Presentation (50%)](#63-analytical-report--presentation-50)
   - 6.4 [Eligibility and Penalties](#64-eligibility-and-penalties)
   - 6.5 [Tie-Breaking Criteria](#65-tie-breaking-criteria)

---

## 1. Introduction to the challenge

Road transport plays a vital role in connecting people, goods, and economies across the globe. However, it also represents a significant source of carbon emissions. The transition toward electric mobility is key for a sustainable future. As the European Union and the world push for ambitious climate objectives, the rapid growth of electric vehicles (EVs) on our roads demands a robust, smart, and strategically distributed charging infrastructure.

Unlike traditional refueling networks, EV charging must be intricately linked with the electrical grid. One of the greatest hurdles to this transition is not just deciding where a charging point is geographically convenient, but understanding where the electrical grid can actually support it without facing severe congestion.

This datathon challenges participants to use real-world public datasets to explore how we can realistically build the charging network of tomorrow. Teams are invited to design data-driven solutions that help plan the necessary infrastructure, optimizing the location of public-use charging points on interurban transport routes with the fewest stations possible, while simultaneously analyzing grid capacity limitations.

Yet, this is not a conventional datathon. It is not only about programming or coding models; it is about research, strategy, and innovation. Participants are expected to think critically, combine data-driven evidence with business acumen, and apply both human intelligence and artificial intelligence to tackle one of the most complex real-world challenges of our time.

We are not just looking for a script; we are looking for a usable final product that generates real business impact. The ability to ask the right questions, identify appropriate data sources, justify assumptions, and communicate actionable insights through a clear Business Intelligence (BI) visualization will be as valuable as any line of code.

---

## 2. Scope of Analysis

The analysis must focus on the interurban transport network in Spain.

> **Important:** Proposed charging stations must be located on interurban roads (autopistas, autovías, or carreteras nacionales) as classified in the Ministry of Transport dataset. Stations within urban road sections are excluded regardless of municipality size.

While urban centres currently concentrate the highest volume of electric vehicles, the true bottleneck for massive EV adoption lies in long-distance travel and the phenomenon known as "range anxiety." For this reason, teams must specifically exclude large urban centers from their primary focus, concentrating instead on modeling and optimizing connectivity between cities, regions, and major transport corridors.

Furthermore, this challenge introduces a critical layer of real-world complexity: the model cannot solely rely on traffic volumes, route distances, or geometrical placement. It must inherently incorporate the capacity and potential congestion of the electrical distribution grid. The electrical grid is not a homogenous blanket of infinite energy; its capacity varies drastically across the territory. A geographically perfect location for a charging station based on highway traffic might be entirely unfeasible if the local electrical substation lacks the capacity to support high-power chargers. Participants must navigate this intersection between transport geography and energy infrastructure.

### Target Horizon: 2027 Strategy

The analysis and the proposed charging network must be designed for a **2027 operational scenario**. Participants must use the predictive models developed in the mandatory Open Data exercise (GitHub) to project EV adoption and charging demand for this specific year.

The goal is to identify where Iberdrola must prioritize its infrastructure deployment in the immediate short-term to meet the upcoming demand and regulatory requirements. This timeframe ensures that the proposed solutions are actionable, realistic, and aligned with current market growth and EU transport regulations.

---

## 3. Datathon objectives

You are not just asked to code; you are expected to analyze like data scientists, think like infrastructure planners, and propose viable, scalable strategies. The best solutions will balance the needs of EV drivers with the physical limitations of the power grid.

### Objective 1: Charging Network Optimization (Primary Objective)

Participants must propose the optimal location for public-use charging points along interurban transport routes. The ultimate goal is efficiency: **you must aim to deploy the lowest possible number of charging stations necessary to adequately cover the mobility demand.**

*Deep Dive: "Optimal" in this context means maximizing utilization rates and driver convenience while minimizing the capital expenditure required for excessive infrastructure. Teams should consider variables such as average EV autonomy, seasonal traffic fluctuations, major transit corridors, and the spacing required to prevent drivers from being stranded. The resulting network should be sparse enough to be economically viable, but dense enough to guarantee a seamless journey across Spain.*

**Expected Output:**

1. Global Network KPIs (The Scorecard): A summary row that evaluates the overall optimization and strategic impact of the solution. See Deliverable 2, File 1 for the exact structure.
2. A structured dataset containing the geographic coordinates of all proposed charging stations, the number of chargers per location, and the grid viability status. See Deliverable 2, File 2 for the exact structure.

### Objective 2: Grid Viability Analysis (Secondary Objective)

Even the most elegant geographical model fails if there is no power to plug into. Teams must identify areas within the network that currently limit the deployment of charging infrastructure due to electrical grid congestion.

*Deep Dive: By crossing mobility data with the provided grid capacity maps from major distributors (such as i-DE, Endesa, and Viesgo), participants must analyze and calculate the critical zones where it will be absolutely necessary to reinforce the electrical infrastructure. You are looking for the "friction points"—locations where high charging demand collides with low grid hosting capacity. Documenting these bottlenecks is just as important as placing the chargers themselves.*

**Expected Output:**

A geospatial analysis identifying the specific nodes or regions where grid capacity restricts deployment. This will feed directly into your BI Visualization. See Deliverable 2, File 3 for the exact structure.

### Objective 3: Strategy and Value Proposition

Data without interpretation is just noise. Based on the quantitative analysis and the bottlenecks identified in the previous objectives, teams must propose clear, actionable strategies to optimize the distribution of new charging points.

*Deep Dive: We expect teams to formulate a strategic narrative. If a highly transited route cannot support fast chargers due to grid congestion, what is the workaround? How should the rollout be phased over the coming years as EV adoption grows? Your strategic proposals should demonstrate a deep understanding of the trade-offs between user demand, infrastructure costs, and grid limitations, delivering a final value proposition that a company like Iberdrola could realistically consider.*

**Expected Output:**

An actionable strategic roadmap, integrated into your final Analytical Report and Pitch, detailing how Iberdrola should phase the deployment of these chargers to balance user demand with grid limitations.

---

## 4. Key references and Data Sources

The solution must be formulated using real data. While we provide a foundational set of main and additional public information sources regarding mobility and the electrical system, this is just the starting point. To build a highly realistic and viable solution, teams must cross-reference geographic mobility metrics with the physical limitations of the energy sector.

Furthermore, **innovation and independent research will be highly rewarded.** We strongly encourage teams to identify and integrate extra data from official or highly reputable sources that enrich their analysis. The more informed, nuanced, and creative your data strategy is, the higher your solution will be valued in the evaluation criteria. Going beyond the provided datasets to uncover new variables or perspectives is a key differentiator for winning proposals. **Please ensure that all data sources used, whether provided in this document or discovered independently, are explicitly documented, properly cited, and referenced in your final Analytical Report.**

### 4.1 Main Data Sources

These are the foundational datasets required to build the core of your geographic and demand models:

1. **Road Routes | Ministry of Transport and Sustainable Mobility:** This dataset provides the foundational geographical network. Teams should use it to map the primary interurban arteries, understand traffic flows, and determine the structural backbone of their proposed charging network. It is not just about lines on a map; it is about understanding where the highest volume of long-distance transit occurs.

   **Sources:** Road Routes | Ministry of Transport and Sustainable Mobility

2. **Electric vehicle charging points - Datasets | National Access Point for Traffic and Mobility:** Knowing where chargers already exist is crucial to avoid redundancies and identify current coverage gaps. Teams must establish this baseline infrastructure before proposing new additions, ensuring their optimization model only suggests new stations where there is a demonstrable deficit.

   **Sources:** Electric vehicle charging points - Datasets | National Access Point for Traffic and Mobility

3. **Route to electrification: Deciphering the growth of electric vehicles in Spain through data analytics | datos.gob.es:**

   > **Mandatory Requirement:** This constitutes a core technical element of the Datathon. Teams are required to fork the official GitHub repository. The specific output of this repository, which estimates the growth of electric cars in the coming years, must serve as the foundational input for your model. **Please ensure this integration is explicitly referenced in your Google Colab notebook/s and your Analytical Report.**

   *Technical recommendation: Teams should fork the official GitHub repository that contains exercise 3 of Open Data (datos.gob.es). You must use the output of that repository as the input for your solution, and is properly referenced in both your Google Colab notebook/s and your Analytical Report.*

   **Sources:** Route to electrification: Deciphering the growth of electric vehicles in Spain through data analytics | datos.gob.es

### 4.2 Additional Data Sources

To build a highly realistic and viable solution, teams should consult additional sources, particularly those that cross-reference geographic mobility metrics with the physical limitations of the energy sector:

#### Electrical Distribution and Grid Capacity

A geographically perfect location for a charger is useless if the local grid cannot support the power load. The three distributors below provide downloadable datasets with node-level capacity data, including geographic coordinates and available capacity in MW. Teams should use these to identify where high-power connections are viable and where they will cause network congestion.

1. **IBERDROLA: i-DE (Consumption capacity map):** Essential for identifying the consumption capacity constraints of the grid in regions managed by Iberdrola. The downloadable dataset provides substation-level data including available capacity (MW) and geographic coordinates.

   **Sources:** Consumption capacity map | i-DE - Iberdrola Group

2. **ENDESA: e-distribución (Network capacity nodes):** Provides node-level access capacity, allowing teams to assess the viability of connecting new energy-intensive infrastructure in Endesa's distribution areas. Historical access capacity documents are available for download in CSV and XLSX format.

   **Sources:** Historical access capacity documents

3. **VIESGO: Interactive grid map:** Provides substation-level capacity data for Viesgo's distribution network in northern Spain, critical for cross-referencing geographical charging needs with electrical supply capabilities.

   **Sources:** Interactive grid map | Viesgo Distribución

4. **Vehicle registrations in Spain (DGT):** This provides the historical and current context of the vehicle fleet. By analyzing monthly registration trends, teams can gauge the localized pace of EV adoption across different provinces, allowing them to weight their charging demand forecasts geographically.

   **Sources:** Vehicle registrations in Spain (DGT)
   - https://www.dgt.es/microdatos/salida/2025/6/vehiculos/matriculaciones/export_mensual_mat_202506.zip
   - https://www.dgt.es/microdatos/salida/2025/7/vehiculos/matriculaciones/export_mensual_mat_202507.zip
   - https://www.dgt.es/microdatos/salida/2025/8/vehiculos/matriculaciones/export_mensual_mat_202508.zip
   - https://www.dgt.es/microdatos/salida/2025/9/vehiculos/matriculaciones/export_mensual_mat_202509.zip
   - https://www.dgt.es/microdatos/salida/2025/10/vehiculos/matriculaciones/export_mensual_mat_202510.zip
   - https://www.dgt.es/microdatos/salida/2025/11/vehiculos/matriculaciones/export_mensual_mat_202511.zip

5. **Electric car charging points | datos.gob.es (e.g., Municipal Dataset of Vigo):** While national registries provide the macro picture, teams are encouraged to search for **local open data portals** (like the provided example from Vigo, and other municipalities on datos.gob.es). These local datasets can help validate national figures, identify unregistered regional chargers, and provide granular insights to enrich your model.

   **Sources (e.g., Municipal Dataset of Vigo):** Electric car charging points | datos.gob.es

### 4.3 Innovation & Creative Problem Solving: The Role of Assumptions

One of the core values of this Datathon is **innovation**. We highly value your ability to navigate complex, real-world scenarios where data might be imperfect or incomplete. This is where your strategic creativity comes into play.

If, during your analysis, you encounter a lack of granular detail of any kind, we **encourage you to take the lead and make informed assumptions**. We want to see how you bridge those gaps using your research and analytical intuition.

To ensure your brilliance is properly evaluated, please adhere to the following in your **Analytical Report**:

1. **Document Your Logic:** Clearly state any proxy values or assumptions you have used (e.g., how you translated grid capacity data into a classification threshold).
2. **Show Your Research:** Back your assumptions with industry standards, external sources, or technical reports, and cite them clearly.
3. **The Expert Perspective:** Explain why your assumption makes sense in the context of real infrastructure planning.
4. **Our Evaluation Philosophy:** We do not just look for the right number, we look for the most robust and well-justified reasoning. Your ability to maintain a solid model in the face of data scarcity is a key indicator of high-level professional talent and will be highly rewarded in the final scoring.

---

## 5. The submissions: Content to be delivered

In this section, the contents of the technical deliverables that students must complete to participate in this challenge are described.

> ⚠️ **Important:** All deliverables must be submitted via the Final Submission Form, clearly indicating the team name. Any violation of the delivery criteria will result in the **disqualification of the team.**

### 5.1 Deliverable 1: Code files

The code developed to address the problem should be properly commented and clearly presented, using **Google Colab**, alternating between code and explanatory text.

> ⚠️ **Important:** The outputs of the execution must be fully visible, including a printout of the structure and format of the resulting output files — otherwise, the team may be disqualified. Teams that fail to clearly document and justify all assumptions made in the model, or that submit a final output that deviates from the specified table format and structure, will be **disqualified** from the final evaluation.

### 5.2 Deliverable 2: Output datasets (Charging Network Proposal)

To ensure comparability across teams, participants must generate **3 clean output datasets in CSV format**, named exactly **File 1, File 2, and File 3**, containing the following information:

#### FILE 1: Global Network KPIs (Summary Scorecard)

A single summary row that evaluates the overall optimization and strategic impact of the solution. **File name: File 1 (.csv)**

| Field | Data Type | How it is obtained |
|---|---|---|
| `total_proposed_stations` | Integer | Row count of File 2. Reflects the total number of new charging sites proposed. |
| `total_existing_stations_baseline` | Integer | Count of interurban charging stations from the National Access Point dataset, filtered to autopistas, autovías, and carreteras nacionales only. |
| `total_friction_points` | Integer | Row count of File 3. Reflects the total number of identified grid bottleneck locations. |
| `total_ev_projected_2027` | Integer | Direct output of the mandatory GitHub fork (datos.gob.es repository). Projected total EV fleet in Spain for 2027. |

#### File 2: Proposed Charging Locations (Objective 1)

A detailed list of every new charging station proposed by the team. **File name: File 2 (.csv)**

| Field | Data Type | Description |
|---|---|---|
| `location_id` | String | Unique identifier assigned sequentially by the team (e.g., IBE_001, IBE_002). |
| `latitude` | Float | Geographic latitude of the proposed site in decimal degrees (WGS84). |
| `longitude` | Float | Geographic longitude of the proposed site in decimal degrees (WGS84). |
| `route_segment` | String | Official designation of the interurban road as classified in the Ministry of Transport dataset (e.g., A-3, AP-7, N-2). |
| `n_chargers_proposed` | Integer | Number of individual charging points at this site. Must be justified in the Analytical Report based on projected local demand. |
| `grid_status` | Categorical | Grid capacity classification at this location based on distributor data. Teams must define and document their own thresholds in the Analytical Report. Accepted values: **Sufficient**, **Moderate**, **Congested**. |

#### FILE 3: Friction Points (Objective 2)

A specific log of "Friction Points" — locations where demand exists but the grid requires reinforcement. **Only locations classified as Moderate or Congested in File 2 are to be included in File 3.** **File name: File 3 (.csv)**

| Field | Data Type | Description |
|---|---|---|
| `bottleneck_id` | String | Unique identifier assigned sequentially by the team (e.g., FRIC_001, FRIC_002). |
| `latitude` | Float | Geographic latitude of the bottleneck location in decimal degrees (WGS84). |
| `longitude` | Float | Geographic longitude of the bottleneck location in decimal degrees (WGS84). |
| `route_segment` | String | Official designation of the interurban road as classified in the Ministry of Transport dataset (e.g., A-3, AP-7, N-2). |
| `distributor_network` | String | Name of the electricity distribution operator for this area. Accepted values: **i-DE**, **Endesa**, or **Viesgo**. |
| `estimated_demand_kw` | Float | Projected power demand at this location. Calculated as `n_chargers_proposed × 150 kW`. The 150 kW standard per charger is fixed for all teams. |
| `grid_status` | Categorical | Grid capacity classification. Only **Moderate** or **Congested** are valid in this file. Locations classified as Sufficient in File 2 must not appear here. |

#### Mandatory Rules for Output Standardization

- **Rule 1 – grid_status classification:** `grid_status` must be assigned based on the *Capacidad disponible / Available capacity (MW)* field from the corresponding distributor's dataset (i-DE, Endesa, or Viesgo). Teams must identify the nearest substation to each proposed location, define their own classification thresholds, and document both the spatial matching methodology and the threshold justification in the Analytical Report.

- **Rule 2 – Standard power per charger:** The standard power capacity per charger is fixed at **150 kW**. All teams must use this value to calculate `estimated_demand_kw` as `n_chargers_proposed × 150 kW`. No other value is accepted.

- **Rule 3 – File 3 scope:** Only locations classified as **Moderate** or **Congested** in File 2 must appear in File 3. A location with `grid_status = Sufficient` cannot be logged as a friction point.

### 5.3 Deliverable 3: BI Visualization

Teams must deliver a visualization geolocating all proposed charging stations from File 2, submitted as a single self-contained file or app. Visualization is a key component for the jury to evaluate the spatial logic and strategic impact of each proposal.

#### Key Requirements

- **Required information:** Geolocation of the stations, route segment, number of proposed chargers, and grid status.
- **Accessibility:** The file must open directly, without requiring any software installation, proprietary licenses, or login credentials.
- **Self-Contained Data:** All coordinates and data points must be embedded within the file or app to ensure it remains fully functional when shared or moved between devices.

#### Required Visual Layer

All proposed charging stations from File 2 must be plotted on a map of Spain, colour-coded by grid status:
- 🟢 **Green:** Sufficient
- 🟡 **Yellow:** Moderate
- 🔴 **Red:** Congested

> **Note:** The above represents the minimum required visualization. Teams are strongly encouraged to go beyond this baseline by adding additional layers, data overlays, filters, or any other visual elements that enrich the analysis and strengthen the strategic narrative. Innovation in visualization will be positively valued by the jury.

#### Accepted Format

Any file or app format is accepted, provided it meets the accessibility and self-containment requirements above.

> **Critical:** Submissions that require the jury to install software (e.g., Power BI Desktop files), log into a cloud platform, or provide credentials of any kind will be **automatically disqualified.**

### 5.4 Deliverable 4: Analytical Report (Executive Summary)

A clear, professional report (3–5 pages) detailing the analysis, the methodology used, and the strategic proposals.

- **Crucial:** This document must explicitly detail all the restrictions, assumptions (e.g., EV battery range, charging times, grid capacity thresholds), and limitations encountered during the execution of the model. The classification thresholds used to assign `grid_status` must be justified here with supporting evidence. All external data sources must be properly cited.

### 5.5 Deliverable 5: Final Presentation (Pitch)

A structured presentation to effectively communicate the solution to the jury. The presentation will be delivered by the finalist teams during the closing event and should last a **maximum of 5 minutes**. It must synthesize both the technical robustness of the model and the strategic business recommendations for Iberdrola.

---

## 6. Evaluation Criteria

Having described the objectives, dataset information, and technical delivery requirements in the previous sections, this section outlines the evaluation criteria.

The evaluation will be based equally on **technical excellence (50%)** and **communication and strategic insight (50%)**, in alignment with the required deliverables: the code, the three output datasets (Global KPIs Scorecard, Proposed Charging Locations, and Grid Bottleneck Analysis), the BI Visualization, the Analytical Report (3–5 pages), and the Final Presentation (ppt/pdf).

### 6.1 Overall Weighting

| Component | Weight |
|---|---|
| Technical Component + BI Visualization | 50% |
| Analytical Report & Presentation | 50% |

- **Technical Component + BI Visualization: 50% of the final grade** — Evaluates the team's analytical reasoning, clarity of logic, code quality, use of credible data sources and assumptions, and the quality of the visualization (map) delivered.
- **Analytical Report & Presentation: 50% of the final grade** — Evaluates the team's ability to synthesize technical findings into clear, evidence-based strategic insights and communicate them effectively to Iberdrola.

### 6.2 Technical Component + BI Visualization (50%)

#### T1 — Problem Understanding and Assumptions

Clarity in defining the interurban charging network problem and documenting all assumptions (EV autonomy ranges, charging demand per station, grid capacity thresholds derived from distributor maps, etc.), supported by credible references. Logical consistency between assumptions, data sources, and proposed outputs. Missing or poorly documented assumptions will be penalized.

#### T2 — Data Exploration and Quality of Sources

Appropriate use of the mandatory datasets (Ministry of Transport road network, National Access Point charging baseline, datos.gob.es GitHub fork) and any additional sources identified independently. Clear justification for chosen datasets and discussion of limitations, biases, or data gaps. Innovation in sourcing additional relevant data will be positively valued.

#### T3 — Methodology: Network Optimization and Grid Viability Analysis

Sound and coherent methodology for proposing the optimal charging station locations (Objective 1) and identifying friction points where demand exceeds grid capacity (Objective 2). The design must demonstrate clear reasoning behind station placement, spacing logic relative to EV autonomy, and the crossing of mobility data with distributor capacity datasets. The methodology must be reproducible, traceable, and clearly explained.

#### T4 — Output Dataset Compliance

Accurate generation of the three required output files in strict compliance with the specified structure and field definitions. All mandatory standardization rules must be respected: `grid_status` classification based on distributor data with documented thresholds, `estimated_demand_kw` calculated as `n_chargers_proposed × 150 kW`, and File 3 containing only locations classified as Moderate or Congested. Any deviation from the required format may result in disqualification.

#### T5 — Code Quality and Reproducibility

Code must be clean, properly commented, and clearly organized in Google Colab, alternating code and explanatory text. All cells must be executed and all outputs must be fully visible, including printed verification of the structure and format of each output file.

#### B4 — BI Visualization

The visualization (map) must clearly display all proposed charging stations from File 2, colour-coded by `grid_status` (Green: Sufficient / Yellow: Moderate / Red: Congested), in a visually coherent and immediately interpretable way. It has to show at least: geolocation of the stations, route segment, number of proposed chargers (per station), and grid status. The jury will assess whether the spatial logic of the proposal is self-evident from the visualization alone.

Additional layers, data overlays, or visual enhancements beyond the minimum requirement will be positively valued. Any format is allowed; however, submissions that require software installation, login credentials, or an active internet connection will receive a score of **zero** for this criterion.

### 6.3 Analytical Report & Presentation (50%)

#### B1 — Integration Between Technical and Strategic Analysis

The Analytical Report (3–5 pages) must demonstrate how the quantitative outputs from the network optimization and grid viability analysis support the team's strategic conclusions for Iberdrola. Assumptions, parameters, and sources must be explicitly connected to the proposed charging network and friction point identification.

#### B2 — Coherence and Feasibility of the Strategic Roadmap

The proposed deployment strategy should be realistic and reflect a sound understanding of the trade-offs between EV driver demand, infrastructure costs, and grid limitations. Limitations and uncertainties must be clearly acknowledged. The phased rollout plan must be actionable within the 2027 target horizon.

#### B3 — Strategic Relevance and Business Value for Iberdrola

Ability to extract meaningful insights from the data and articulate their implications for Iberdrola's infrastructure investment decisions. The proposal must demonstrate how the identified friction points and proposed stations translate into a concrete, prioritized deployment strategy that a company like Iberdrola could realistically act upon.

#### B5 — Clarity and Persuasiveness of the Presentation

The final pitch (maximum 5 minutes) must be visually coherent, concise, and persuasive. Focus on key takeaways, clarity of communication, and a data-supported narrative that connects the technical model to the business opportunity for Iberdrola.

#### B6 — Formal Compliance and Citation

Strict adherence to submission formats and deadlines. All data sources and references must be properly cited in the Analytical Report. Failure to comply may result in disqualification.

### 6.4 Eligibility and Penalties

To be eligible for evaluation, teams must submit all required deliverables: the code (in Google Colab) with visible outputs, the three output datasets in the exact required structure, the BI Visualization, the Analytical Report, and the Final Presentation.

**Grounds for disqualification include but are not limited to:**

- Missing or undocumented assumptions
- Output datasets not following the required structure or field definitions
- `grid_status` classification thresholds not defined or not justified in the Analytical Report
- `estimated_demand_kw` not calculated using the fixed 150 kW standard
- File 3 containing locations classified as Sufficient
- Missing or invisible code outputs
- BI Visualization requiring software installation or login credentials
- Failure to submit the Analytical Report or Final Presentation

### 6.5 Tie-Breaking Criteria

In case of a tie, teams will be ranked based on:

1. Integration and coherence of the Analytical Report (B1)
2. Clarity and persuasiveness of the Final Presentation (B5)
3. Code quality and reproducibility (T5)
4. BI Visualization (Map) (B4)
5. Accuracy and compliance of the three output datasets (T4)
