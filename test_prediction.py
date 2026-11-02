from src.pipeline.predict_pipeline import PredictPipeline, CustomData

data = CustomData(
    gender="male",
    race_ethnicity="group A",
    parental_level_of_education="bachelor's degree",
    lunch="standard",
    test_preparation_course="completed",
    reading_score=75,
    writing_score=80
)

df = data.get_data_as_data_frame()

print("Input Data:")
print(df)

prediction = PredictPipeline().predict(df)

print("Predicted Maths Score:", prediction)