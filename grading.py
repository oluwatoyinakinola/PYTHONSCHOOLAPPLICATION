def assign_grade(score):
    if score < 60:
        return 'F'
    elif 60 <= score < 70:
        return 'C'
    elif 70 <= score < 80:
        return 'B'
    elif 80 <= score <= 100:
        return 'A'
    else:
        raise ValueError("Invalid score")
