Price Calculator
beginner

Price Calculator
================

Calculate discount, tax, and final price with small functions.

Start building, submit solution and get feedback from the community.

Start Working
Price Calculator
================

You are calculating the final price for a product after discount and tax. The discount is applied first, and tax is calculated on the discounted price.

Write these functions:

* `calculateDiscount(price, discountPercent)` should return the discount amount.
* `calculateTax(priceAfterDiscount, taxPercent)` should return the tax amount.
* `calculateFinalPrice(price, discountPercent, taxPercent)` should subtract the discount, add tax, and return the final price.
* `createPriceSummary(price, discountPercent, taxPercent)` should return an object with `price`, `discount`, `tax`, and `finalPrice`.

Sample checks:

js

```
console.log(createPriceSummary(100, 20, 10));console.log(createPriceSummary(200, 25, 5));console.log(createPriceSummary(50, 0, 10));
```

Expected output:

txt

```
{ price: 100, discount: 20, tax: 8, finalPrice: 88 }{ price: 200, discount: 50, tax: 7.5, finalPrice: 157.5 }{ price: 50, discount: 0, tax: 5, finalPrice: 55 }
```

Do not hardcode the example values. The functions should work for other prices and percentages too.

Solution

Solution:

js

```
function calculateDiscount(price, discountPercent) {  return (price * discountPercent) / 100;}function calculateTax(priceAfterDiscount, taxPercent) {  return (priceAfterDiscount * taxPercent) / 100;}function calculateFinalPrice(price, discountPercent, taxPercent) {  const discount = calculateDiscount(price, discountPercent);  const priceAfterDiscount = price - discount;  const tax = calculateTax(priceAfterDiscount, taxPercent);  return priceAfterDiscount + tax;}function createPriceSummary(price, discountPercent, taxPercent) {  const discount = calculateDiscount(price, discountPercent);  const priceAfterDiscount = price - discount;  const tax = calculateTax(priceAfterDiscount, taxPercent);  const finalPrice = calculateFinalPrice(price, discountPercent, taxPercent);  return {    price,    discount,    tax,    finalPrice,  };}console.log(createPriceSummary(100, 20, 10));console.log(createPriceSummary(200, 25, 5));console.log(createPriceSummary(50, 0, 10));
```

