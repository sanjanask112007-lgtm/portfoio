
import numpy as np
import pandas as pd

PASS_MARK = 35

def calculate_grade(average):
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    elif average >= 50:
        return "E"
    else:
        return "F"

def calculate_status(row, subjects):
    for subject in subjects:
        if row[subject] < PASS_MARK:
            return "Fail"
    return "Pass"


def load_data():
    try:
        df = pd.read_csv("students.csv")
    except FileNotFoundError:
        print("Error: students.csv file not found!")
        raise SystemExit(1)

    required_columns = [
        "Student_ID", "Name", "Department",
        "Python", "Statistics", "Database", "Attendance"
    ]

    for column in required_columns:
        if column not in df.columns:
            print(f"Error: Missing column {column}")
            raise SystemExit(1)

    if df.empty:
        print("Error: Dataset is empty!")
        raise SystemExit(1)

    subjects = ["Python", "Statistics", "Database"]

    for subject in subjects + ["Attendance"]:
        df[subject] = pd.to_numeric(df[subject], errors="coerce")

    if df[subjects + ["Attendance"]].isnull().any().any():
        print("Error: Marks and attendance must be numeric.")
        raise SystemExit(1)

    if ((df[subjects] < 0) | (df[subjects] > 100)).any().any():
        print("Error: Subject marks must be between 0 and 100.")
        raise SystemExit(1)

    if ((df["Attendance"] < 0) | (df["Attendance"] > 100)).any():
        print("Error: Attendance must be between 0 and 100.")
        raise SystemExit(1)

    return df, subjects

def process_data(df, subjects):
    df = df.copy()

    df["Total"] = df[subjects].sum(axis=1)

    marks = df[subjects].to_numpy()
    df["Average"] = np.round(np.mean(marks, axis=1), 2)

    df["Grade"] = df["Average"].apply(calculate_grade)

    df["Result"] = df.apply(
        lambda row: calculate_status(row, subjects),
        axis=1
    )

    return df

def show_student_summary(df):
    columns = [
        "Student_ID", "Name", "Department",
        "Total", "Average", "Grade", "Result", "Attendance"
    ]

    print("\n" + "=" * 95)
    print("          STUDENT PERFORMANCE SUMMARY")
    print("=" * 95)

    print(df[columns].to_string(index=False))

def show_class_analysis(df, subjects):
    print("\n" + "=" * 50)
    print("          CLASS PERFORMANCE ANALYSIS")
    print("=" * 50)

    total_students = len(df)
    class_average = df["Average"].mean()
    highest_average = df["Average"].max()
    lowest_average = df["Average"].min()

    pass_count = (df["Result"] == "Pass").sum()
    fail_count = (df["Result"] == "Fail").sum()
    pass_percentage = (pass_count / total_students) * 100

    print(f"Total students       : {total_students}")
    print(f"Overall class average: {class_average:.2f}")
    print(f"Highest average      : {highest_average:.2f}")
    print(f"Lowest average       : {lowest_average:.2f}")
    print(f"Students passed      : {pass_count}")
    print(f"Students failed      : {fail_count}")
    print(f"Pass percentage      : {pass_percentage:.2f}%")

    print("\n" + "-" * 50)
    print("SUBJECT-WISE PERFORMANCE")
    print("-" * 50)

    subject_averages = df[subjects].mean().sort_values(
        ascending=False
    )

    for subject, average in subject_averages.items():
        print(f"{subject:15s}: {average:.2f}")

    print(
        f"\nBest-performing subject: "
        f"{subject_averages.idxmax()}"
    )

    print("\n" + "-" * 50)
    print("GRADE DISTRIBUTION")
    print("-" * 50)

    grade_counts = df["Grade"].value_counts()

    for grade in ["A", "B", "C", "D", "E", "F"]:
        count = grade_counts.get(grade, 0)
        print(f"Grade {grade}: {count} student(s)")

    print("\n" + "-" * 50)
    print("TOP 3 PERFORMING STUDENTS")
    print("-" * 50)

    top_students = df.nlargest(3, "Average")

    print(
        top_students[
            ["Student_ID", "Name", "Average", "Grade"]
        ].to_string(index=False)
    )

    print("\n" + "-" * 50)
    print("ATTENDANCE ANALYSIS")
    print("-" * 50)

    average_attendance = df["Attendance"].mean()
    print(f"Average attendance: {average_attendance:.2f}%")

    low_attendance = df[df["Attendance"] < 75]

    if low_attendance.empty:
        print("All students have attendance of at least 75%.")
    else:
        print("Students with attendance below 75%:")

        print(
            low_attendance[
                ["Student_ID", "Name", "Attendance"]
            ].to_string(index=False)
        )

def save_results(df):
    output_file = "student_analysis_results.csv"

    df.to_csv(output_file, index=False)

    print(f"\nResults saved successfully to {output_file}")


def main():
    print("=" * 50)
    print(" STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 50)

    df, subjects = load_data()

    print("\nDATASET PREVIEW")
    print("-" * 50)
    print(df.head().to_string(index=False))

    print(f"\nNumber of student records: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")

    results = process_data(df, subjects)

    show_student_summary(results)
    show_class_analysis(results, subjects)

    save_results(results)

    print("\nProject executed successfully!")

if __name__ == "__main__":
    main()
