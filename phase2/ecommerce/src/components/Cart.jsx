import React from 'react';
import CartItem from './CartItem';

function Cart({ cart, onRemoveFromCart }) {
  return (
    <div>
      <h2>Cart</h2>
      {cart.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <ul>
          {cart.map((item) => (
            <li key={item.id}>
              <CartItem item={item} onRemoveFromCart={onRemoveFromCart} />
            </li>
          ))}
        </ul>
      )}
      <p>Total: ${cart.reduce((acc, item) => acc + item.price * item.quantity, 0)}</p>
    </div>
  );
}

export default Cart;
