import math
import random


def calculate_grid_dimensions(num_students):
    """Calculate optimal grid dimensions that are as close to a rectangle as possible."""
    sqrt = math.sqrt(num_students)
    rows = round(sqrt)
    cols = math.ceil(num_students / rows)

    # Ensure we have enough spots
    while rows * cols < num_students:
        cols += 1

    return rows, cols


def create_seating_arrangement(student_names):
    """Create a seating arrangement grid from a list of student names."""
    # Shuffle the student names
    shuffled_students = student_names.copy()
    random.shuffle(shuffled_students)

    # Calculate grid dimensions
    rows, cols = calculate_grid_dimensions(len(student_names))

    # Create the grid
    grid = []
    student_idx = 0

    for i in range(rows):
        row = []
        for j in range(cols):
            if student_idx < len(shuffled_students):
                row.append(
                    {
                        "name": shuffled_students[student_idx],
                        "position": {"row": i, "col": j},
                    }
                )
                student_idx += 1
            else:
                row.append(None)  # Empty seat
        grid.append(row)

    return {
        "grid": grid,
        "rows": rows,
        "cols": cols,
        "total_students": len(student_names),
    }
