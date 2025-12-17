from datetime import datetime
from models import Order, Product, product_order
from models import Category, Order, Prediction,Product
from config_db import get_db
import pandas as pd
from config_db import SessionLocal
import numpy as np
session = SessionLocal()


dict_products={
    "salades": ["Salade Thon","Salade Poulet"],
    "sandwiches": [
        "Sandwiches poulet crudités",
        "Sandwiches thon crudités",
        "Sandwiches végétarien",
        "Sandwiches poulet mexicain",
        "Sandwiches chèvre miel crudités",
        "Sandwiches poulet curry",
        "Sandwiches saumon",
        "Panini 4 fromages",
        "Panini poulet Kebab"
    ],
    "viennoiseries": [
        "Pain au chocolat",
        "Croissant",
        "Pains suisses",
    ],
}

def create_categories():
    global session
    for category in dict_products.keys():
        cat = Category(name=category)
        session.add(cat)
    session.commit()


def create_products():
    global session
    for key, products in dict_products.items():
        for product_name in products:
            category = session.query(Category).filter_by(name=key).first()
            product = Product(name=product_name, category=category)
            session.add(product)
    session.commit()


from models import DayEnum

DAY_MAP = {
    "Lundi": DayEnum.MONDAY,
    "Mardi": DayEnum.TUESDAY,
    "Mercredi": DayEnum.WEDNESDAY,
    "Jeudi": DayEnum.THURSDAY,
    "Vendredi": DayEnum.FRIDAY,
    "Samedi": DayEnum.SATURDAY,
    "Dimanche": DayEnum.SUNDAY,

}



def import_orders_from_df(df: pd.DataFrame):
    PRODUCT_COLUMNS = [
        col for col in df.columns
        if col not in ["Jour", "Date"]
    ]
    global session        
    for _, row in df.iterrows():
        order_date = datetime.strptime(row["Date"], "%d/%m/%Y").date()

        order = Order(
            date=order_date,
            day=DAY_MAP[str(row["Jour"]).strip()]
        )
        session.add(order)
        session.commit()

        for product_name in PRODUCT_COLUMNS:
            qty = int(row[product_name])
            if qty <= 0 or np.isnan(qty):
                continue
            
            product = session.get(Product, product_name)
            if not product:
                print(f"⚠ Missing product: {product_name}")
                continue

            session.execute(
                product_order.insert().values(
                    order_id=order.id,
                    product_id=product.name,
                    quantity=qty
                )
            )


# if __name__ == "__main__":
# create_categories()
# create_products()
# import_orders_from_df(
#     pd.read_csv("static/data_base/Final_Dataset.csv")
# )
# create_order()
# session.close()