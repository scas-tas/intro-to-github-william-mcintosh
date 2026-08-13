def add_item(inv: dict, name: str, quantity: int) -> None:
    count = inv.get(name, 0)
    inv[name] = count + quantity

 
def remove_item(inv: dict, name: str, quantity: int) -> None:
    if name in inv:
        inv[name] -= quantity


 
def get_stock_report(inv: dict) -> str:
        report = []
        for name, quantity in sorted(inv.items()):
            if quantity > 0:
                report.append(f"{name}: {inv[name]}")
        return "\n".join(report)



def test_cases():
    inv = {}
    add_item(inv, "apples", 10)
    add_item(inv, 'bananas', 5)
    print(get_stock_report(inv)) # EXPECTED apples: 10 \n bananas: 5

    add_item(inv, 'apples', 5)
    remove_item(inv, 'bananas', 10)
    print(get_stock_report(inv)) # EXPECTED apples: 15 \n (no bananas)

    remove_item(inv, 'oranges', 3)
    print(get_stock_report(inv)) # EXPECTED apples: 15 \n (no error no oranges)

test_cases()