# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, month

# Create a SparkSession with S3 configurations
spark = SparkSession.builder \
    .appName("S3 Data Analysis using Spark SQL") \
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

    # Register the DataFrame as a SQL temporary view to run SQL queries
    transformed_data.createOrReplaceTempView("sales_data")

    # Task 4: Data Analysis Using Spark SQL (5 Queries)
    
    print("\n** 1. Identify Top-Performing Regions **")
    top_performing_regions = spark.sql("""
        SELECT customer_location, SUM(total_amount) AS total_revenue
        FROM sales_data
        GROUP BY customer_location
        ORDER BY total_revenue DESC
        LIMIT 5
    """)
    top_performing_regions.show()

    print("\n** 2. Analyze Month-over-Month Revenue Growth **")
    month_over_month_growth = spark.sql("""
        SELECT Year, Month, 
               SUM(total_amount) AS monthly_revenue,
               LAG(SUM(total_amount)) OVER (ORDER BY Year, Month) AS previous_month_revenue,
               ROUND(
                   (SUM(total_amount) - LAG(SUM(total_amount)) OVER (ORDER BY Year, Month)) / 
                   LAG(SUM(total_amount)) OVER (ORDER BY Year, Month) * 100, 2
               ) AS revenue_growth_percentage
        FROM sales_data
        GROUP BY Year, Month
        ORDER BY Year, Month
    """)
    month_over_month_growth.show()

    print("\n** 3. Determine the Most Popular Product Categories **")
    most_popular_product_categories = spark.sql("""
        SELECT product_category, COUNT(*) AS total_sales
        FROM sales_data
        GROUP BY product_category
        ORDER BY total_sales DESC
        LIMIT 5
    """)
    most_popular_product_categories.show()

    print("\n** 4. Top 5 Customers by Total Transaction Value **")
    top_5_customers = spark.sql("""
        SELECT customer_id, SUM(total_amount) AS total_spent
        FROM sales_data
        GROUP BY customer_id
        ORDER BY total_spent DESC
        LIMIT 5
    """)
    top_5_customers.show()

    print("\n** 5. Identify the Most Used Payment Methods **")
    payment_method_usage = spark.sql("""
        SELECT payment_method, COUNT(*) AS total_transactions, 
               SUM(total_amount) AS total_revenue
        FROM sales_data
        GROUP BY payment_method
        ORDER BY total_revenue DESC
    """)
    payment_method_usage.show()

except Exception as e:
    print(f"Error encountered: {e}")

finally:
    # Stop Spark session
    spark.stop()

