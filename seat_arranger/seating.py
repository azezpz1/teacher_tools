import math
import random
import logging

logger = logging.getLogger("seat_arranger")


def calculate_grid_dimensions(num_students):
    """Calculate optimal grid dimensions that are as close to a rectangle as possible."""
    logger.info(f"Calculating grid dimensions for {num_students} students")
    sqrt = math.sqrt(num_students)
    rows = round(sqrt)
    cols = math.ceil(num_students / rows)

    # Ensure we have enough spots
    while rows * cols < num_students:
        cols += 1

    logger.info(f"Calculated dimensions: {rows} rows x {cols} columns")
    return rows, cols


def create_seating_arrangement(student_names, width, depth, layout):
    """Create a seating arrangement grid respecting the table layout."""
    logger.info(
        f"Creating seating arrangement for {len(student_names)} students in a {width}x{depth} grid"
    )

    # Shuffle the student names
    shuffled_students = student_names.copy()
    random.shuffle(shuffled_students)
    logger.info("Student names shuffled")

    # Create the grid
    grid = []
    student_idx = 0
    empty_seats = 0
    placed_students = 0

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
                    placed_students += 1
                else:
                    # Empty seat at a valid table
                    row.append(
                        {
                            "name": "Empty Seat",
                            "position": {"row": i, "col": j},
                            "empty": True,
                        }
                    )
                    empty_seats += 1
            else:
                # No table at this position
                row.append(None)
        grid.append(row)

    logger.info(
        f"Seating arrangement created: {placed_students} students placed, {empty_seats} empty seats"
    )
    return {
        "grid": grid,
        "rows": depth,
        "cols": width,
        "total_students": len(student_names),
    }
