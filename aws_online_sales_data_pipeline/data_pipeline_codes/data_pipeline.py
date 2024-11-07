# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, sum, desc, to_date

# Create a SparkSession with S3 configurations
spark = SparkSession.builder \
    .appName("S3 Data Ingestion and Processing") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.506") \
    .getOrCreate()

# S3 bucket file path
s3_bucket_path = "s3a://bda-pipeline-msk/online_retail_sales_dataset.csv"

try:
    # Task 1: Data Ingestion
    # Read the CSV file from S3
    data = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(s3_bucket_path)

    # Confirm successful ingestion
    print("\nSample data from the CSV file:")
    data.show(5)

    print("\nSchema of the CSV file:")
    data.printSchema()

    # Task 2: Data Processing
    ## Data Transformation: Create Year and Month columns
    transformed_data = data.withColumn("transaction_date", to_date(col("timestamp"), "M/d/yy H:mm")) \
                           .withColumn("Year", year(col("transaction_date"))) \
                           .withColumn("Month", month(col("transaction_date")))

    ## Data Aggregation
    # 1. Total revenue by customer location
    total_revenue_by_location = transformed_data.groupBy("customer_location") \
        .agg(sum("total_amount").alias("Total_Revenue"))

    # 2. Monthly spending trends
    monthly_spending_trends = transformed_data.groupBy("Year", "Month") \
        .agg(sum("total_amount").alias("Monthly_Spending"))

    # 3. Top 10 customers by total transaction value
    top_10_customers = transformed_data.groupBy("customer_id") \
        .agg(sum("total_amount").alias("Total_Transaction_Value")) \
        .orderBy(desc("Total_Transaction_Value")) \
        .limit(10)

    # Show aggregated data
    print("Total Revenue by Customer Location:")
    total_revenue_by_location.show()

    print("Monthly Spending Trends:")
    monthly_spending_trends.show()

    print("Top 10 Customers by Total Transaction Value:")
    top_10_customers.show()

    # Task 3: Store Processed Data Back to S3
    # S3 bucket output path
    s3_output_path = "s3a://bda-pipeline-msk-output/processed-data"

    # Save the processed data to S3 as CSV files
    total_revenue_by_location.write \
        .option("header", "true") \
        .csv(f"{s3_output_path}/total_revenue_by_location")

    monthly_spending_trends.write \
        .option("header", "true") \
        .csv(f"{s3_output_path}/monthly_spending_trends")

    top_10_customers.write \
        .option("header", "true") \
        .csv(f"{s3_output_path}/top_10_customers")

    print(f"Data successfully written to {s3_output_path} on S3")

except Exception as e:
    print(f"Error encountered: {e}")

finally:
    # Stop Spark session
    spark.stop()

