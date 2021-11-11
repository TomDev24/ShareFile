import click
from shareFile import create_app

app = create_app()

@app.cli.command("create-user")
@click.argument("name")
def create_user(name):
    print(name)

if __name__ == "__main__":
    app.run(debug=True)
