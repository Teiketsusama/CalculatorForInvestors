from csv import DictReader
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, create_engine
from sqlalchemy.orm import sessionmaker


# Create the companies table;
# Create the financial table;
Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)


class Financial(Base):
    __tablename__ = 'financial'

    ticker = Column(String, foreign_key="companies.ticker", primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


# Create an SQLite database — investor.db
engine = create_engine('sqlite:///investor.db')
Base.metadata.create_all(engine)

# Insert datasets to the tables
Session = sessionmaker(bind=engine)
session = Session()

# Read the data from the csv files
# Insert the data into the tables
with open("companies.csv") as company_info:
    companies = DictReader(company_info, delimiter=",")
    for company in companies:
        for key, value in company.items():
            if value == "":
                company[key] = None

        company_obj = Company(
            ticker=company["ticker"],
            name=company["name"],
            sector=company["sector"])
        session.add(company_obj)
        session.commit()


with open("financial.csv") as financial_info:
    financials = DictReader(financial_info, delimiter=",")
    for financial in financials:
        for key, value in financial.items():
            if value == "":
                financial[key] = None

        financial_obj = Financial(ticker=financial["ticker"], ebitda=financial["ebitda"], sales=financial["sales"],
                                    net_profit=financial["net_profit"], market_price=financial["market_price"],
                                    net_debt=financial["net_debt"], assets=financial["assets"],
                                    equity=financial["equity"], cash_equivalents=financial["cash_equivalents"],
                                    liabilities=financial["liabilities"])
        session.add(financial_obj)
        session.commit()


def main():
    print("Database created successfully!")


if __name__ == "__main__":
    main()
