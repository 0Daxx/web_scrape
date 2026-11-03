Order Status Helper
beginner

Order Status Helper
===================

Summarize nested order data for a support dashboard.

Start building, submit solution and get feedback from the community.

Start Working
Order Status Helper
===================

Summarize an order object for a support dashboard. The final summary should expose payment status, shipping status, item count, and whether the order needs attention.

Write these functions:

* `isPaid(order)` should return `true` when `payment.status` is `"paid"`.
* `hasShipped(order)` should return `true` when `shipping.status` is `"shipped"`.
* `getDeliveryMessage(order)` should return a shipping message and include `estimatedDelivery` when the order has shipped.
* `needsAttention(order)` should return `true` when the order is unpaid or has not shipped.
* `createOrderSummary(order)` should return `id`, `customerName`, `paid`, `shipped`, `itemCount`, `deliveryMessage`, and `needsAttention`.

Sample checks:

js

```
const order = {  id: 'ORD-1001',  customer: {    name: 'Ava Stone',    email: 'ava@example.com',  },  payment: {    status: 'paid',  },  shipping: {    status: 'shipped',    estimatedDelivery: '2026-06-18',  },  items: [    { name: 'Notebook', quantity: 2 },    { name: 'Pen Set', quantity: 1 },  ],};console.log(createOrderSummary(order));console.log(isPaid(order));console.log(hasShipped(order));const pendingOrder = {  ...order,  payment: { status: 'unpaid' },  shipping: { status: 'processing', estimatedDelivery: '2026-06-18' },};console.log(needsAttention(pendingOrder));console.log(getDeliveryMessage(pendingOrder));
```

Expected output:

txt

```
{ id: "ORD-1001", customerName: "Ava Stone", paid: true, shipped: true, itemCount: 3, deliveryMessage: "Order shipped. Estimated delivery: 2026-06-18.", needsAttention: false }truetruetrueOrder has not shipped yet.
```

For `itemCount`, add item quantities instead of counting item rows.

Solution

Solution:

js

```
function isPaid(order) {  return order.payment.status === 'paid';}function hasShipped(order) {  return order.shipping.status === 'shipped';}function getDeliveryMessage(order) {  if (hasShipped(order)) {    return `Order shipped. Estimated delivery: ${order.shipping.estimatedDelivery}.`;  }  return 'Order has not shipped yet.';}function needsAttention(order) {  return !isPaid(order) || !hasShipped(order);}function createOrderSummary(order) {  let itemCount = 0;  for (const item of order.items) {    itemCount += item.quantity;  }  return {    id: order.id,    customerName: order.customer.name,    paid: isPaid(order),    shipped: hasShipped(order),    itemCount,    deliveryMessage: getDeliveryMessage(order),    needsAttention: needsAttention(order),  };}const order = {  id: 'ORD-1001',  customer: {    name: 'Ava Stone',    email: 'ava@example.com',  },  payment: {    status: 'paid',  },  shipping: {    status: 'shipped',    estimatedDelivery: '2026-06-18',  },  items: [    { name: 'Notebook', quantity: 2 },    { name: 'Pen Set', quantity: 1 },  ],};console.log(createOrderSummary(order));console.log(isPaid(order));console.log(hasShipped(order));const pendingOrder = {  ...order,  payment: { status: 'unpaid' },  shipping: { status: 'processing', estimatedDelivery: '2026-06-18' },};console.log(needsAttention(pendingOrder));console.log(getDeliveryMessage(pendingOrder));
```

