from csv import DictReader
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker


class MenuDisplay:
    def __init__(self):
        self.main_menu = "MAIN MENU\n" \
                         "0 Exit\n" \
                         "1 CRUD operations\n" \
                         "2 Show top ten companies by criteria\n"

        self.crud_menu = "\nCRUD MENU\n" \
                         "0 Back\n" \
                         "1 Create a company\n" \
                         "2 Read a company\n" \
                         "3 Update a company\n" \
                         "4 Delete a company\n" \
                         "5 List all companies\n"

        self.top_ten_menu = "\nTOP TEN MENU\n" \
                            "0 Back\n" \
                            "1 List by ND/EBITDA\n" \
                            "2 List by ROE\n" \
                            "3 List by ROA\n"

    def display_main_menu(self):
        print(self.main_menu)

    def display_crud_menu(self):
        print(self.crud_menu)

    def display_top_ten_menu(self):
        print(self.top_ten_menu)


class CRUD:
    def __init__(self):
        self.session = Session()

    def create_company(self):
        # table companies
        ticker = input("Enter ticker (in the format 'MOON'):\n")
        name = input("Enter company (in the format 'Moon Corp'):\n")
        sector = input("Enter industries (in the format 'Technology'):\n")
        # table financial
        financial_data = CRUD.financial_display()

        company_obj = Company(ticker=ticker, name=name, sector=sector)
        financial_obj = Financial(ticker=ticker, **financial_data)

        self.session.add(company_obj)
        self.session.add(financial_obj)
        self.session.commit()

        print("Company created successfully!\n")
        main()

    @staticmethod
    def financial_display() -> dict:
        financial_data_keys = []
        financial_data = {}
        [financial_data_keys.append(Financial.__table__.columns.keys()[i])
         for i in range(1, len(Financial.__table__.columns))]
        for key in financial_data_keys:
            if "_" in key:
                key = key.replace("_", " ")
            financial_data[key] = input(f"Enter {key} (in the format '987654321'):\n")
        financial_data = {key.replace(" ", "_"): value for key, value in financial_data.items() if " " in key}
        return financial_data

    @staticmethod
    def query_company() -> list:
        while True:
            name_input = str(input("Enter company name:\n"))
            company_list = session.query(Company, Financial).join(Financial, Company.ticker == Financial.ticker).\
                filter(Company.name.ilike(f"%{name_input}%")).all()

            if not company_list:
                print("Company not found!\n")
                main()
            for index, (company, financial) in enumerate(company_list):
                print(f"{index} {company.name}")
            return company_list

    def read_company(self):
        company_list = CRUD.query_company()
        num_input = int(input("Enter company number:\n"))
        company, financial = company_list[num_input]
        pe, ps, pb, nd_ebitda, roe, roa, la = None, None, None, None, None, None, None
        if financial.market_price is not None and financial.net_profit is not None:
            pe = round(financial.market_price / financial.net_profit, 2)
        if financial.market_price is not None and financial.sales is not None:
            ps = round(financial.market_price / financial.sales, 2)
        if financial.market_price is not None and financial.assets is not None:
            pb = round(financial.market_price / financial.assets, 2)
        if financial.net_debt is not None and financial.ebitda is not None:
            nd_ebitda = round(financial.net_debt / financial.ebitda, 2)
        if financial.equity is not None and financial.net_profit is not None:
            roe = round(financial.net_profit / financial.equity, 2)
        if financial.net_profit is not None and financial.assets is not None:
            roa = round(financial.net_profit / financial.assets, 2)
        if financial.liabilities is not None and financial.assets is not None:
            la = round(financial.liabilities / financial.assets, 2)
        print(f"\n{company.ticker} {company.name}\n"
              f"P/E = {pe}\n"
              f"P/S = {ps}\n"
              f"P/B = {pb}\n"
              f"ND/EBITDA = {nd_ebitda}\n"
              f"ROE = {roe}\n"
              f"ROA = {roa}\n"
              f"L/A = {la}\n")
        main()

    def update_company(self):
        company_list = CRUD.query_company()
        num_input = int(input("Enter company number:\n"))
        company, financial = company_list[num_input]
        financial_data = CRUD.financial_display()
        for key, value in financial_data.items():
            setattr(financial, key, value)
        self.session.commit()
        print("Company updated successfully!\n")
        main()

    def delete_company(self):
        company_list = CRUD.query_company()
        num_input = int(input("Enter company number:\n"))
        company, financial = company_list[num_input]
        session.expunge(financial)
        session.expunge(company)
        self.session.delete(financial)
        self.session.delete(company)
        self.session.commit()
        print("Company deleted successfully!\n")
        main()

    def list_all_companies(self):
        print("COMPANY LIST")
        list_companies = self.session.query(Company).all()
        list_companies.sort(key=lambda x: x.ticker)
        for company in list_companies:
            print(f"{company.ticker} {company.name} {company.sector}")
        main()

    def menu_options(self):
        while True:
            user_input = input("Enter an option:\n")
            if user_input == "0":
                return
            elif user_input == "1":
                self.create_company()
            elif user_input == "2":
                self.read_company()
            elif user_input == "3":
                self.update_company()
            elif user_input == "4":
                self.delete_company()
            elif user_input == "5":
                self.list_all_companies()
            else:
                print("Invalid option!\n")


def top_ten_menu():
    while True:
        user_input = input("Enter an option:\n")
        if user_input == "0":
            return
        elif user_input in ["1", "2", "3"]:
            print("Not implemented!\n")
            return
        else:
            print("Invalid option!\n")


def main():
    while True:
        MenuDisplay().display_main_menu()
        user_input = input("Enter an option:\n")
        if user_input == "0":
            print("Have a nice day!")
            exit()
        elif user_input == "1":
            MenuDisplay().display_crud_menu()
            CRUD().menu_options()
        elif user_input == "2":
            MenuDisplay().display_top_ten_menu()
            top_ten_menu()
        else:
            print("Invalid option!\n")


if __name__ == "__main__":
    print("Welcome to the Investor Program!\n")
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

        ticker = Column(String, ForeignKey('companies.ticker'), primary_key=True)
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
            if not session.query(Company).filter_by(ticker=company['ticker']).first():
                company_obj = Company(**company)
                session.add(company_obj)
            session.commit()

    with open("financial.csv") as financial_info:
        financials = DictReader(financial_info, delimiter=",")
        for financial in financials:
            for key, value in financial.items():
                if value == "":
                    financial[key] = None
            if not session.query(Financial).filter_by(ticker=financial['ticker']).first():
                financial_obj = Financial(**financial)
                session.add(financial_obj)
            session.commit()
    main()
