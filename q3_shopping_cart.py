def add_item(item, cart=None):
    """
    Correct pattern: use None as the sentinel, then create a
    fresh list inside the function body each time it is needed.
    """
    if cart is None:
        cart = []          # brand-new list on every call
    cart.append(item)
    return cart


# ── PART C — Build the Cart ───────────────────────────────────

def create_cart(owner, discount=0):
    """
    Returns a fresh cart dict for each customer.
    discount=0 is SAFE because 0 is an immutable int — it cannot
    be mutated in place, so every call gets the same default value
    without any shared-state risk.
    """
    return {
        "owner":    owner,
        "items":    [],        # new list created fresh each call
        "discount": discount   # immutable int — no danger
    }


def add_to_cart(cart, name, price, qty=1):
    """
    Appends an item dict to cart["items"].
    qty=1 is safe for the same reason as discount=0 (immutable int).
    """
    cart["items"].append({"name": name, "price": price, "qty": qty})
    print(f'  [+] {qty}x "{name}" @ ₹{price:.2f} added to {cart["owner"]}\'s cart.')


def update_price(price_tuple, new_price):
    """
    Tuples are IMMUTABLE — once created their elements cannot be
    changed. Attempting to do so raises a TypeError at runtime.
    This is intentional: use a tuple when data must stay fixed
    (e.g. an (item, original_price) record that should never change).
    """
    try:
        price_tuple[0] = new_price          # ← this will raise TypeError
    except TypeError as e:
        print(f'  [TypeError] Cannot modify tuple: {e}')
        print(f'  Tuple remains unchanged: {price_tuple}')


def calculate_total(cart):
    """
    Loops over items, sums price * qty, then applies the discount %.
    """
    subtotal = sum(item["price"] * item["qty"] for item in cart["items"])
    discount_amount = subtotal * (cart["discount"] / 100)
    total = subtotal - discount_amount
    return subtotal, discount_amount, total


# ── DEMONSTRATION ─────────────────────────────────────────────

def print_cart(cart):
    subtotal, discount_amount, total = calculate_total(cart)
    print(f'\n  🛒  {cart["owner"]}\'s Cart  (discount: {cart["discount"]}%)')
    print('  ' + '-' * 40)
    for item in cart["items"]:
        print(f'  {item["qty"]}x  {item["name"]:<20} ₹{item["price"] * item["qty"]:.2f}')
    print('  ' + '-' * 40)
    print(f'  Subtotal  : ₹{subtotal:.2f}')
    if discount_amount:
        print(f'  Discount  : -₹{discount_amount:.2f}  ({cart["discount"]}% off)')
    print(f'  TOTAL     : ₹{total:.2f}')


def main():
    print('=' * 50)
    print('       SHOPPING CART SYSTEM')
    print('=' * 50)

    # ── Part A: demonstrate the bug ──────────────────
    print('\n⚠️  Part A — Buggy function output:')
    def add_item_buggy(item, cart=[]):
        cart.append(item)
        return cart

    print(' ', add_item_buggy("apple"))           # ['apple']
    print(' ', add_item_buggy("banana"))          # ['apple', 'banana'] ← BUG
    print(' ', add_item_buggy("milk", ["bread"])) # ['bread', 'milk']
    print(' ', add_item_buggy("eggs"))            # ['apple', 'banana', 'eggs'] ← BUG

    # ── Part B: fixed function ────────────────────────
    print('\n✅  Part B — Fixed function output:')
    print(' ', add_item("apple"))                 # ['apple']
    print(' ', add_item("banana"))                # ['banana']  ← fresh list!
    print(' ', add_item("milk", ["bread"]))       # ['bread', 'milk']
    print(' ', add_item("eggs"))                  # ['eggs']    ← fresh list!

    # ── Part C: two independent customers ────────────
    print('\n👤  Part C — Two independent carts:')

    alice_cart = create_cart("Alice", discount=10)
    bob_cart   = create_cart("Bob",   discount=0)

    print('\n  Adding items for Alice:')
    add_to_cart(alice_cart, "Laptop",    75000.00)
    add_to_cart(alice_cart, "Mouse",      1500.00, qty=2)
    add_to_cart(alice_cart, "USB Hub",    2000.00)

    print('\n  Adding items for Bob:')
    add_to_cart(bob_cart, "Headphones",  3500.00)
    add_to_cart(bob_cart, "Keyboard",    4500.00)

    # Prove carts are independent
    print('\n  🔍 Proving carts are independent:')
    print(f'  Alice has {len(alice_cart["items"])} items, Bob has {len(bob_cart["items"])} items.')
    print(f'  Same list object? {alice_cart["items"] is bob_cart["items"]}')  # must be False

    # Tuple immutability demo
    print('\n🔒  Tuple Immutability Demo:')
    price_record = ("Laptop", 75000.00)
    print(f'  Original tuple: {price_record}')
    update_price(price_record, 70000.00)

    # Print both carts
    print_cart(alice_cart)
    print_cart(bob_cart)

    print('\n' + '=' * 50)


main()


# ============================================================
#   DISCUSSION POINTS
# ============================================================

# Q1: Why is `discount=0` safe but `cart=[]` dangerous?
#     `discount=0` uses an immutable int. Even though the same 0 object
#     is reused as the default, you can never *mutate* an int in place —
#     reassigning discount inside the function just rebinds the local
#     variable; the default stays 0 forever.
#     `cart=[]` uses a mutable list. Python creates it once at function
#     definition time and reuses that exact object on every call that
#     omits cart. Any .append() permanently changes the shared object,
#     so state bleeds across calls.

# Q2: What is the difference between rebinding and mutating?
#     Rebinding  → making a variable point to a NEW object.
#                  e.g.  x = x + 1  (x now points to a different int)
#     Mutating   → changing the CONTENTS of the existing object in place.
#                  e.g.  my_list.append(5)  (same list object, new element)
#     Only mutable objects can be mutated. Rebinding never affects the
#     caller; mutating a mutable object always does.

# Q3: Which of these are mutable?
#     MUTABLE   : list ✅ | dict ✅ | set ✅
#     IMMUTABLE : tuple ❌ | str ❌ | int ❌

# Q4: When you pass a list into a function and modify it, do changes
#     reflect outside? Why?
#     YES. Python passes object *references*, not copies. Both the caller
#     and the function hold a reference to the same list in memory.
#     Calling .append() / .remove() etc. mutates that shared object, so
#     the caller sees the changes immediately. To avoid this, pass a copy:
#     func(my_list.copy()) or func(list(my_list)).