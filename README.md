# Airline Customer Satisfaction Analysis

### 1. Project Overview
This project examines airline customer satisfaction data to uncover patterns and trends that offer valuable insights for business decision-making. The process involves data cleaning, exploratory data analysis (EDA), and creating visualizations to gain a deeper understanding of sales performance over time. Additionally, an ETL process is implemented using DAGs, with data validation carried out through **Great Expectations**.

---

### 2. Project Structure
```bash
├── images/                         # Contains images for the project (e.g., dashboards)
├── P2M3_vincar_DAG.py              # Python script for DAG and ETL process
├── P2M3_vincar_GX.ipynb            # Jupyter notebook for data exploration and validation using Great Expectations
├── P2M3_vincar_data_clean.csv      # Cleaned dataset
├── P2M3_vincar_data_raw.csv        # Raw dataset
├── README.md                       # Project README file
```

---

### 3. ETL Process and DAG Workflow
The project uses an **ETL (Extract, Transform, Load)** process orchestrated by a **DAG** file to automate the workflow. The steps in the DAG workflow are:

1. **Load CSV into PostgreSQL**:
   - The raw sales data (CSV) is loaded into a PostgreSQL database.
   
2. **Fetch Data from PostgreSQL**:
   - Data is fetched from PostgreSQL for further processing.

3. **Preprocessing**:
   - **Handling Missing Values**: Missing values are addressed using various imputation methods.
   - **Handling Duplicates**: Duplicate records are identified and removed.
   - **Column Renaming**: All column names are converted to lowercase, and spaces are replaced with underscores for consistency.

4. **Upload Data to Elasticsearch**:
   - The cleaned and processed data is uploaded to **Elasticsearch** for indexing and further analysis.

The DAG file that handles this ETL process is located in the repository under `P2M3_vincar_DAG.py`.

---

### 4. Analysis and Insights
The project focuses on:
- Analyzing customer satisfaction levels to increase retention
- Visualizing satisfaction levels by satsfied and disatisfied customers
- Identifying key drivers of satisfaction and areas of improvement

---

### 5. Results

![Dashboard](https://github.com/vincar12/ETL-airflow-elastic-kibana/blob/main/images/Full%20Dashboard.png)

1. **Proportion of Loyal Customers**: 81.69% of the customers surveyed categorize themselves as loyal. Disloyal Customers represent 18.31% of the total, this group still offers room for improvement and retention efforts

2. **Proportion of Satisfied Customers**: Satisfied Customers only make up 54.74% of the total, which means that slightly more than half of the customers are satisfied with their experience. Dissatisfied Customers account for 45.26% of the total, indicating that nearly half of the customer base is unhappy. Addressing the concerns of dissatisfied customers could help increase overall satisfaction and customer retention

3. **Satisfaction Levels in Satisfied and Dissatisfied Customers**: There is a clear difference in how satisfied versus dissatisfied customers perceive the different service aspects, with satisfied customers consistently giving higher scores across categories. This indicates a need to focus on improving specific services to enhance the experience for dissatisfied customers

4. **Satisfaction Levels in each Class**: The difference in the satisfaction levels of seat comfort and dining quality is not significant between each class, and that they are uniformly relatively low satisfaction. Business class passengers should have a privilege on these categories, similar satisfaction levels across classes suggests a possible mismatch between passenger expectations and their experiences, particularly in Business Class.

5. **Customer Age Distribution**: The age of customers are skewed towards younger and middle-aged individuals, with the highest concentration of customers in the age range of 20-50 years. There is a noticeable peak at around age 25 and another smaller peak around age 40. The number of customers declines steadily after age 60, with very few customers above the age of 70. This distribution suggests that the business likely attracts a younger to middle-aged demographic, with fewer older customers.

6. **Flight Time Convenience Satisfaction**: The satisfaction levels on the convenience of the flight times in both satisfied and dissatisfied customers average at just under 60%. Over 40% of customers feel that the flight times available for purchase are not convenient to their expectations.

---

### 6. Conclusion
Based on the analysis of the customer survey data, important insights can be taken. It can be concluded that although the proportion of loyal customers is high at 81%; the proportion of satisfied customers is much below expected, only 55% of all customers surveyed. Several factors affect the satisfaction of customers, these factors are inflight service and entertainments, online services, and the check-in service. Improvement must be done on categories that the business class should have privilege on, such as seat comfort as well as meal service. The scheduling of flights are still below the satisfactory level expected.

---

### 7. References
- Dataset: [Airline Customer Satisfaction Dataset](https://www.kaggle.com/datasets/sjleshrac/airlines-customer-satisfaction/data)
- Tools: Python, Pandas, Docker, Airflow, GreatExpectation, ElasticSearch, Kibana
