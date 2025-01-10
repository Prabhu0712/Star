from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Basic Patterns
def square_pattern(rows):
    return "\n".join(["*" * rows for _ in range(rows)])

def right_angled_triangle(rows):
    return "\n".join(["*" * (i + 1) for i in range(rows)])

def inverted_right_angled_triangle(rows):
    return "\n".join(["*" * (rows - i) for i in range(rows)])

def pyramid_pattern(rows):
    return "\n".join([" " * (rows - i - 1) + "* " * (i + 1) for i in range(rows)])

def inverted_pyramid(rows):
    return "\n".join([" " * i + "* " * (rows - i) for i in range(rows)])

def diamond_pattern(rows):
    return "\n".join(
        [" " * (rows - i - 1) + "* " * (i + 1) for i in range(rows)] +
        [" " * (i + 1) + "* " * (rows - i - 1) for i in range(rows - 1)]
    )

# Hollow Patterns
def hollow_square(rows):
    return "\n".join(
        ["*" * rows if i == 0 or i == rows - 1 else "*" + " " * (rows - 2) + "*" for i in range(rows)]
    )

def hollow_pyramid(rows):
    return "\n".join(
        [" " * (rows - i - 1) + "*" if i == 0 else " " * (rows - i - 1) + "*" + " " * (2 * i - 1) + "*" for i in range(rows)]
    )

def hollow_inverted_pyramid(rows):
    return "\n".join(
        [" " * i + "*" + " " * (2 * (rows - i) - 3) + "*" if i < rows - 1 else " " * i + "*" for i in range(rows)]
    )

# Number-based Patterns
def numbered_pyramid(rows):
    return "\n".join([" " * (rows - i - 1) + " ".join(str(j + 1) for j in range(i + 1)) for i in range(rows)])

def pascals_triangle(rows):
    def fact(n):
        return 1 if n == 0 else n * fact(n - 1)
    return "\n".join(
        [" " * (rows - i - 1) + " ".join(str(fact(i) // (fact(j) * fact(i - j))) for j in range(i + 1)) for i in range(rows)]
    )

def floyds_triangle(rows):
    num = 1
    result = []
    for i in range(rows):
        result.append(" ".join(str(num + j) for j in range(i + 1)))
        num += i + 1
    return "\n".join(result)

# Special Patterns
def checkerboard_pattern(rows):
    return "\n".join(["".join("*" if (i + j) % 2 == 0 else " " for j in range(rows)) for i in range(rows)])

def spiral_square(rows):
    grid = [[" " for _ in range(rows)] for _ in range(rows)]
    top, left, bottom, right = 0, 0, rows - 1, rows - 1
    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            grid[top][i] = "*"
        top += 1
        for i in range(top, bottom + 1):
            grid[i][right] = "*"
        right -= 1
        for i in range(right, left - 1, -1):
            grid[bottom][i] = "*"
        bottom -= 1
        for i in range(bottom, top - 1, -1):
            grid[i][left] = "*"
        left += 1
    return "\n".join("".join(row) for row in grid)

def zigzag_pattern(rows):
    return "\n".join(["".join("*" if (i + j) % 4 == 0 or (i == 2 and j % 4 == 0) else " " for j in range(rows * 2)) for i in range(3)])

# Additional Patterns
def cross_pattern(rows):
    return "\n".join([" " * (rows // 2) + "*" + " " * (rows // 2) if i != rows // 2 else "*" * rows for i in range(rows)])

def plus_pattern(rows):
    return "\n".join([" " * (rows // 2) + "*" + " " * (rows // 2) if i != rows // 2 else "*" * rows for i in range(rows)])

def x_pattern(rows):
    return "\n".join([" " * i + "*" + " " * (rows - 2 * i - 1) + "*" if i != rows // 2 else " " * i + "*" for i in range(rows)])

def hollow_diamond(rows):
    return "\n".join(
        [" " * (rows - i - 1) + "*" + " " * (2 * i - 1) + "*" if i != 0 else " " * (rows - i - 1) + "*" for i in range(rows)] +
        [" " * (i + 1) + "*" + " " * (2 * (rows - i - 2) - 1) + "*" if i != rows - 2 else " " * (i + 1) + "*" for i in range(rows - 1)]
    )

def hollow_right_angled_triangle(rows):
    return "\n".join(["*" if i == 0 or i == rows - 1 else "*" + " " * (i - 1) + "*" for i in range(rows)])

def hollow_inverted_right_angled_triangle(rows):
    return "\n".join(["*" if i == 0 or i == rows - 1 else "*" + " " * (rows - i - 2) + "*" for i in range(rows)])

# Patterns dictionary
PATTERNS = {
    "Basic Patterns": {
        "Square Pattern": square_pattern,
        "Right-angled Triangle": right_angled_triangle,
        "Inverted Right-angled Triangle": inverted_right_angled_triangle,
        "Pyramid Pattern": pyramid_pattern,
        "Inverted Pyramid": inverted_pyramid,
        "Diamond Pattern": diamond_pattern,
    },
    "Hollow Patterns": {
        "Hollow Square": hollow_square,
        "Hollow Pyramid": hollow_pyramid,
        "Hollow Inverted Pyramid": hollow_inverted_pyramid,
        "Hollow Diamond": hollow_diamond,
        "Hollow Right-angled Triangle": hollow_right_angled_triangle,
        "Hollow Inverted Right-angled Triangle": hollow_inverted_right_angled_triangle,
    },
    "Number-based Patterns": {
        "Numbered Pyramid": numbered_pyramid,
        "Pascal's Triangle": pascals_triangle,
        "Floyd's Triangle": floyds_triangle,
    },
    "Special Patterns": {
        "Checkerboard Pattern": checkerboard_pattern,
        "Spiral Square": spiral_square,
        "Zigzag Pattern": zigzag_pattern,
        "Cross Pattern": cross_pattern,
        "Plus Pattern": plus_pattern,
        "X Pattern": x_pattern,
    },
}

@app.route("/", methods=["GET"])
def index():
    pattern_names = {category: list(patterns.keys()) for category, patterns in PATTERNS.items()}
    return render_template("index.html", patterns=pattern_names)

@app.route("/generate-pattern", methods=["POST"])
def generate_pattern():
    data = request.get_json()
    category = data.get("category")
    pattern = data.get("pattern")
    rows = int(data.get("rows", 0))

    if not category or not pattern or rows <= 0:
        return jsonify({"result": "Invalid input. Please check your inputs and try again."})

    try:
        result = PATTERNS[category][pattern](rows)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)