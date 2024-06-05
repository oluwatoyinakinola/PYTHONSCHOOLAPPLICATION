def calculate_grade(score):
    if score < 60:
        return 'F'
    elif score < 70:
        return 'C'
    elif score < 80:
        return 'B'
    else:
        return 'A'

def calculate_average(scores):
    if scores:
        return sum(scores) / len(scores)
    else:
        return 0
