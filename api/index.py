from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows only GET requests
    allow_headers=["*"],  # Allows all headers
)


def read_students_data():
    students = []
    with open("q-fastapi.csv", mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            students.append({"studentId": int(row["studentId"]), "class": row["class"]})
    return students


@app.get("/api")
async def get_students(request: Request):
    classes = request.query_params.getlist("class")
    students_data = read_students_data()
    if classes:
        filtered_students = [
            student for student in students_data if student["class"] in classes
        ]
        return {"students": filtered_students}
    return {"students": students_data}


# To run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
