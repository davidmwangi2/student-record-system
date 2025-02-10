import React from 'react';
import Products from './Products';

function ProductList({ products, onAddToCart }) {
  return (
    <div>
      <h2>Product List</h2>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            <Products product={product} onAddToCart={onAddToCart} />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProductList;
