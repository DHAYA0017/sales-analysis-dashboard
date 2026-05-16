import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_PATH = "Sales Dataset.csv"

df = None


# ------------------------
#Step 1: Load & Explore
#-------------------------
def load_and_explore():
    global df
    df = pd.read_csv(CSV_PATH)

    print("\n✅ Loaded:", CSV_PATH)
    print("\nFirst 5 rows:\n", df.head())
    print("\nShape (rows, cols):", df.shape)
    print("\nColumns:\n", list(df.columns))
    print("\nDtypes:\n", df.dtypes)


#--------------------------------
#Step 2: Clean & Preprocess
#--------------------------------
def clean_and_preprocess():
    global df
    if df is None:
        print("❌ First run Option 1 (Load & Explore).")
        return

    print("\nMissing values per column:\n", df.isnull().sum())

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)

    print("\n✅ Cleaning done. Updated dtypes:\n", df.dtypes)


#--------------------------------
#Step 3: Operational Insights
#--------------------------------
def analyze_payment_method_trends():
    global df
    if df is None:
        print("❌ First run Option 1 (Load & Explore).")
        return

    print("\nMost common Payment Methods:\n")
    print(df["PaymentMode"].value_counts())


def view_city_wise_orders():
    global df
    if df is None:
        print("❌ First run Option 1 (Load & Explore).")
        return

    print("\nTop 10 Cities by Order Count:\n")
    print(df["City"].value_counts().head(10))


def monthly_order_volume():
    global df
    if df is None:
        print("❌ First run Option 1 (Load & Explore).")
        return
    if "Year-Month" not in df.columns:
        print("❌ Run Option 2 (Clean & Preprocess) first.")
        return

    print("\nMonthly Order Volume:\n")
    print(df["Year-Month"].value_counts().sort_index())


#----------------------------
#Step 4: Product Analysis
#----------------------------
def find_premium_products_low_sales():
    global df
    if df is None:
        print("❌ First run Option 1 (Load & Explore).")
        return

    avg_price = df.groupby("Sub-Category")["Amount"].mean()
    total_qty = df.groupby("Sub-Category")["Quantity"].sum()
    product_table = pd.DataFrame({
        "Avg Price": avg_price,
        "Total Quantity": total_qty
    })

    product_table = product_table.sort_values(["Avg Price", "Total Quantity"], ascending=[False, True])

    print("\nHigh price but low sales (Top 10):\n")
    print(product_table.head(10))


# ----------------------------------
# Step 5: Visualizations (4 plots)
# ----------------------------------
def create_visualizations():
    global df
    if df is None:
        print("❌ First run Option 1 (Load & Explore).")
        return
    if "Year-Month" not in df.columns:
        print("❌ Run Option 2 (Clean & Preprocess) first.")
        return

    top10_rev = df.groupby("Sub-Category")["Amount"].sum().sort_values(ascending=False).head(10)
    plt.figure()
    top10_rev.plot(kind="bar")
    plt.title("Top 10 Products by Total Revenue")
    plt.xlabel("Sub-Category")
    plt.ylabel("Total Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    monthly = df["Year-Month"].value_counts().sort_index()
    plt.figure()
    plt.plot(monthly.index, monthly.values, marker="o")
    plt.title("Monthly Order Volume Over Time")
    plt.xlabel("Year-Month")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    top10_states = df.groupby("State")["Profit"].sum().sort_values(ascending=False).head(10)
    plt.figure()
    top10_states.sort_values().plot(kind="barh")
    plt.title("Top 10 States by Total Profit")
    plt.xlabel("Total Profit")
    plt.ylabel("State")
    plt.tight_layout()
    plt.show()

    pay_profit = df.groupby("PaymentMode")["Profit"].sum().sort_values(ascending=False)
    plt.figure()
    sns.barplot(x=pay_profit.index, y=pay_profit.values)
    plt.title("Total Profit by Payment Method")
    plt.xlabel("Payment Mode")
    plt.ylabel("Total Profit")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# -----------------------------
# Step 6: Export Reports
# -----------------------------
def export_business_reports():
    global df
    if df is None:
        print("❌ First run Option 1 (Load & Explore).")
        return
    if "Year-Month" not in df.columns:
        print("❌ Run Option 2 (Clean & Preprocess) first.")
        return


    top_products = df.groupby(["Category", "Sub-Category"])["Amount"].sum().sort_values(ascending=False).head(10)
    top_products = top_products.reset_index()
    top_products.columns = ["Top Product Category", "Sub-Category", "Total Revenue"]

    monthly_orders = df["Year-Month"].value_counts().sort_index().reset_index()
    monthly_orders.columns = ["Month", "Number of Orders"]
    monthly_orders = monthly_orders.head(10)

    final_report = pd.concat([top_products, monthly_orders], axis=1)

    final_report.to_csv("top_products_and_monthly_orders.csv", index=False)

    print("\n✅ Exported: top_products_and_monthly_orders.csv")
    print("\nPreview:\n", final_report)


# ----------------
#Menu
#-----------------
def menu():
    while True:
        print("\n" + "=" * 50)
        print("📊 Sales Analysis Dashboard")
        print("=" * 50)
        print("1) Load & Explore Sales Data")
        print("2) Clean & Preprocess the Data")
        print("3) Analyze Payment Method Trends")
        print("4) View City-Wise Order Performance")
        print("5) Find Premium Products with Low Sales")
        print("6) Create Visualizations")
        print("7) Monthly Order Volume")
        print("8) Export Business Reports (CSV)")
        print("0) Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            load_and_explore()
        elif choice == "2":
            clean_and_preprocess()
        elif choice == "3":
            analyze_payment_method_trends()
        elif choice == "4":
            view_city_wise_orders()
        elif choice == "5":
            find_premium_products_low_sales()
        elif choice == "6":
            create_visualizations()
        elif choice == "7":
            monthly_order_volume()
        elif choice == "8":
            export_business_reports()
        elif choice == "0":
            print("✅ Exit.")
            break
        else:
            print("❌ Invalid choice. Try again.")


menu()