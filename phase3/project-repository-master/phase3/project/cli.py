import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migrations.models import Base, Restaurant, MenuItem
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    pass

@cli.command()
def initdb():
    Base.metadata.create_all(engine)
    click.echo('Initialized the database.')

@cli.command()
@click.argument('name')
@click.argument('location')
def add_restaurant(name, location):
    restaurant = Restaurant(name=name, location=location)
    session.add(restaurant)
    session.commit()
    click.echo(f'Added restaurant {name}.')

@cli.command()
@click.argument('restaurant_id', type=int)
@click.argument('name')
@click.argument('price', type=int)
def add_menu_item(restaurant_id, name, price):
    menu_item = MenuItem(name=name, price=price, restaurant_id=restaurant_id)
    session.add(menu_item)
    session.commit()
    click.echo(f'Added menu item {name}.')

@cli.command()
def list_restaurants():
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        click.echo(f"{restaurant.id}: {restaurant.name} - {restaurant.location}")

@cli.command()
@click.argument('restaurant_id', type=int)
def list_menu_items(restaurant_id):
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    for item in menu_items:
        click.echo(f"{item.id}: {item.name} - ${item.price/100:.2f}")

if __name__ == '__main__':
    cli()
