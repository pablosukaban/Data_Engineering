import requests

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print("Error executing request")
    data = None

html = ""
if data is not None:
    html = """
    <html>
    <head>
        <title>Task 6</title>
    </head>
    <body>
        <h1>Users</h1>
        <ul>
    """

    for item in data:
        html += f"<li>{item['name']}</li>"

    html += """
        </ul>
    </body>
    </html>
    """

with open("result.html", "w") as file:
    file.write(html)