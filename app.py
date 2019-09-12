from flask import Flask
app = Flask(__name__)

template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<table>
    <tr><td>{}</td> <td>{}</td> <td>{}</td></tr>
    <tr><td>{}</td> <td>{}</td> <td>{}</td></tr>
    <tr><td>{}</td> <td>{}</td> <td>{}</td></tr>
</table>
</body>
</html>
"""


@app.route('/')
def main():
    html_content = template.format((1, 2, 3, 4, 5, 6, 7, 8, 9))
    return html_content
