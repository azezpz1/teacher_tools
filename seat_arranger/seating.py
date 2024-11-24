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


def create_seating_arrangement(student_names, width, depth, layout):
    """Create a seating arrangement grid respecting the table layout."""
    # Shuffle the student names
    shuffled_students = student_names.copy()
    random.shuffle(shuffled_students)

    # Create the grid
    grid = []
    student_idx = 0

    for i in range(depth):
        row = []
        for j in range(width):
            layout_idx = i * width + j
            if layout[layout_idx]:  # If there's a table at this position
                if student_idx < len(shuffled_students):
                    # Add a student
                    row.append(
                        {
                            "name": shuffled_students[student_idx],
                            "position": {"row": i, "col": j},
                        }
                    )
                    student_idx += 1
                else:
                    # Empty seat at a valid table
                    row.append(
                        {
                            "name": "Empty Seat",
                            "position": {"row": i, "col": j},
                            "empty": True,
                        }
                    )
            else:
                # No table at this position
                row.append(None)
        grid.append(row)

    return {
        "grid": grid,
        "rows": depth,
        "cols": width,
        "total_students": len(student_names),
    }
