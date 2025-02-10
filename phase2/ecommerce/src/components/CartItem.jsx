import React from 'react';

function CartItem({ item, onRemoveFromCart }) {
  return (
    <div>
      <h4>{item.name}</h4>
      <p>Price: ${item.price}</p>
      <p>Quantity: {item.quantity}</p>
      <button onClick={() => onRemoveFromCart(item.id)}>Remove</button>
    </div>
  );
}

export default CartItem;


