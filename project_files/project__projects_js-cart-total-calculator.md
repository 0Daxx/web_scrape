Cart Total Calculator
beginner

Cart Total Calculator
=====================

Summarize cart totals from arrays of item objects.

Start building, submit solution and get feedback from the community.

Start Working
Cart Total Calculator
=====================

A cart contains items with a `price` and `quantity`. Build a summary that calculates subtotal, discount, tax, and final total.

Write these functions:

* `calculateSubtotal(items)` should add `price * quantity` for every item.
* `calculateDiscount(subtotal, discountPercent)` should return the discount amount.
* `calculateTax(amountAfterDiscount, taxPercent)` should return the tax amount after the discount.
* `createCartSummary(items, discountPercent, taxPercent)` should return an object with `subtotal`, `discount`, `tax`, and `total`.

Sample checks:

js

```
const cartItems = [  { name: 'Notebook', price: 10, quantity: 2 },  { name: 'Pen', price: 2, quantity: 5 },  { name: 'Bag', price: 30, quantity: 1 },];console.log(createCartSummary(cartItems, 10, 5));console.log(calculateSubtotal(cartItems));const singleItemCart = [{ name: 'Mouse', price: 25, quantity: 2 }];console.log(createCartSummary(singleItemCart, 0, 10));
```

Expected output:

txt

```
{ subtotal: 60, discount: 6, tax: 2.7, total: 56.7 }60{ subtotal: 50, discount: 0, tax: 5, total: 55 }
```

The subtotal must include every item and multiply each item's price by its quantity.

Solution

Solution:

js

```
function calculateSubtotal(items) {  let subtotal = 0;  for (const item of items) {    subtotal += item.price * item.quantity;  }  return subtotal;}function calculateDiscount(subtotal, discountPercent) {  return (subtotal * discountPercent) / 100;}function calculateTax(amountAfterDiscount, taxPercent) {  return (amountAfterDiscount * taxPercent) / 100;}function createCartSummary(items, discountPercent, taxPercent) {  const subtotal = calculateSubtotal(items);  const discount = calculateDiscount(subtotal, discountPercent);  const amountAfterDiscount = subtotal - discount;  const tax = calculateTax(amountAfterDiscount, taxPercent);  const total = amountAfterDiscount + tax;  return {    subtotal,    discount,    tax,    total,  };}const cartItems = [  { name: 'Notebook', price: 10, quantity: 2 },  { name: 'Pen', price: 2, quantity: 5 },  { name: 'Bag', price: 30, quantity: 1 },];console.log(createCartSummary(cartItems, 10, 5));console.log(calculateSubtotal(cartItems));const singleItemCart = [{ name: 'Mouse', price: 25, quantity: 2 }];console.log(createCartSummary(singleItemCart, 0, 10));
```

