# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WHbQS7KSWRJfhCuSQqHANBBbx9MxahWX
"""

!pip install streamlit

from google.colab import files
uploaded = files.upload()

!unzip best_bot_detector_model.zip

import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel
from pyspark.sql.functions import concat_ws
import pandas as pd

spark = SparkSession.builder.appName("BotDetectionApp").getOrCreate()

from pyspark.ml.pipeline import PipelineModel

model = PipelineModel.load("/content/content/best_bot_detector_model")

st.title("🤖 Social Media Bot Detector")
st.write("Enter a Twitter profile's info and get bot/human prediction!")

username = st.text_input("Username")
description = st.text_area("Profile Description / Bio")
tweet_text = st.text_area("Recent Tweet")

if st.button("Detect"):
    if username.strip() == "" and description.strip() == "" and tweet_text.strip() == "":
        st.warning("Please enter at least one input.")
    else:
        # Convert to Spark DataFrame
        input_df = pd.DataFrame([{
            "username": username,
            "description": description,
            "tweet_text": tweet_text
        }])
        spark_df = spark.createDataFrame(input_df)

        # Combine text columns (same as training step)
        spark_df = spark_df.fillna("")
        spark_df = spark_df.withColumn("combined_text", concat_ws(" ", "username", "description", "tweet_text"))

        # Run prediction
        prediction = model.transform(spark_df).select("prediction").collect()[0][0]
        label = "🧠 Human" if prediction == 0 else "🤖 Bot"

        st.success(f"Prediction: **{label}**")

