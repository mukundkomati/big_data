# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, year, month, sum, avg, when, floor, hour, to_date, from_unixtime, unix_timestamp
)

# Create a SparkSession
spark = SparkSession.builder \
    .appName("S3 Data Ingestion and Processing") \
    .config("spark.master", "local") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", 
            "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .getOrCreate()

# S3 file paths
input_file_path = "s3a://bda-msk-output/online_retail_sales_dataset.csv"  # S3 input file
output_train_path = "s3a://bda-msk-output/processed-data/train_data"     # S3 output path for train data
output_test_path = "s3a://bda-msk-output/processed-data/test_data"       # S3 output path for test data

try:
    # Task 1: Data Ingestion from S3
    # Read the CSV file from S3
    data = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(input_file_path)

    # Add derived columns for analysis
    data = data.withColumn("transaction_date", to_date(col("timestamp"), "M/d/yy H:mm")) \
               .withColumn("Year", year(col("transaction_date"))) \
               .withColumn("Month", month(col("transaction_date"))) \
               .withColumn("Hour", hour(from_unixtime(unix_timestamp(col("timestamp"), "M/d/yy H:mm")))) \
               .withColumn("Six_Hour_Batch", floor(col("Hour") / 6))  # Divide hour into 6-hour intervals

    # Task 2: Aggregation
    aggregated_data = data.groupBy("Year", "Month", "Six_Hour_Batch", "customer_location") \
        .agg(
            avg("customer_age").alias("avg_customer_age"),  # Average customer age
            sum("total_amount").alias("total_revenue"),  # Total revenue
            sum(when(col("customer_gender") == "Male", 1).otherwise(0)).alias("male_count"),  # Male count
            sum(when(col("customer_gender") == "Female", 1).otherwise(0)).alias("female_count"),  # Female count
            sum(when(col("product_category") == "Beauty & Personal Care", 1).otherwise(0)).alias("beauty_care_count"),
            sum(when(col("product_category") == "Books", 1).otherwise(0)).alias("books_count"),
            sum(when(col("product_category") == "Clothing", 1).otherwise(0)).alias("clothing_count"),
            sum(when(col("product_category") == "Electronics", 1).otherwise(0)).alias("electronics_count"),
            sum(when(col("product_category") == "Home & Kitchen", 1).otherwise(0)).alias("home_kitchen_count"),
            sum(when(col("product_category") == "Sports & Outdoors", 1).otherwise(0)).alias("sports_outdoors_count")
        )

    # Task 3: Split into Train and Test Datasets
    train_data, test_data = aggregated_data.randomSplit([0.75, 0.25], seed=42)  # 75%-25% split

    # Save the train dataset to S3
    train_data.write \
        .option("header", "true") \
        .csv(output_train_path)

    # Save the test dataset to S3
    test_data.write \
        .option("header", "true") \
        .csv(output_test_path)

    print(f"Train data successfully written to {output_train_path} on S3")
    print(f"Test data successfully written to {output_test_path} on S3")

except Exception as e:
    print(f"Error encountered: {e}")

finally:
    # Stop Spark session
    spark.stop()