
## Steps

### 1. Query Parsing - SQLGlot

- A SQL-like language will be created using SQLGlot. The SQLGlot parser will convert the query into an abstract syntax tree (AST)
- We can walk this AST to identify components such as tables, columns and functions
- This is where the UDFs like CLUSTER and SCATTER are created

### 2. Data Access Layer

- This layer is dedicated to reading data from a database. SQLGlot can't read data by itself, so this layer is responsible for reading data from a DB and transforming into a pandas DataFrame
- Solutions such as DuckDB can be used to read efficiently data from sources
- This layer can be implemented as an abstraction, so that any engine can be used

### 3. Execution

- **Execution Engine:**  
  Build an execution engine that will:
  - Interpret the query plan generated in the parsing step.
  - Decide the order of operations (e.g., reading the data first, then applying UDFs).
- **UDF Mapping:**  
  For every special function (e.g., `CLUSTER`, `SCATTER`):
  - **Registration:**  
    Map the SQL function names to actual Python functions. For example, `CLUSTER` might correspond to a Python function that runs a clustering algorithm (like K-Means) on the specified column.
  - **Execution:**  
    Once the data is loaded, invoke these Python functions with the data. The `CLUSTER` function would process the column values and return a clustering result.
  - **Visualization:**  
    If `SCATTER` is used, call a visualization library (e.g., matplotlib, seaborn) to generate the scatter plot. The function can then either display the plot or return it as an image.



### 4. Integration and Workflow

- **Workflow Overview:**
  1. **User Input:**  
     The user submits a query.
  2. **Parsing:**  
     The query is parsed using SQLGLot to generate an AST.
  3. **Query Planning:**  
     Analyze the AST and decide the steps needed (data retrieval, UDF processing, visualization).
  4. **Data Retrieval:**  
     Use the data access layer to load the relevant table data.
  5. **UDF Execution:**  
     Apply the UDFs (`CLUSTER` and/or `SCATTER`) to the data.  
     - For `CLUSTER`: perform clustering on the data column.
     - For `SCATTER`: generate a scatter plot visualization.
  6. **Output:**  
     Return the clustering results or display the visualization as required.
