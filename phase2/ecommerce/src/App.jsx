import React, { useState, useEffect } from 'react';
import ProductList from './components/ProductList';
import Cart from './components/Cart';

function App() {
  const [cart, setCart] = useState([]);
  const [sortType, setSortType] = useState('name');
  const [searchQuery, setSearchQuery] = useState('');

  // Sample product data
  const products = [
    { id: 1, name: 'T-Shirt', price: 30 },
    { id: 2, name: 'Jeans', price: 50 },
    { id: 3, name: 'Sneakers', price: 80 },
    { id: 4, name: 'Hat', price: 20 },
    { id: 5, name: 'Socks', price: 10 }
  ];

  // Sort products based on selected type
  const sortedProducts = [...products].sort((a, b) => {
    if (sortType === 'name') return a.name.localeCompare(b.name);
    if (sortType === 'price') return a.price - b.price;
  });

  // Filter products based on search query
  const filteredProducts = sortedProducts.filter((product) =>
    product.name.toUpperCase().includes(searchQuery.toUpperCase())
  );

  // Load cart from localStorage on initial load
  useEffect(() => {
    const savedCart = JSON.parse(localStorage.getItem('cart')) || [];
    setCart(savedCart);
  }, []);

  // Save cart to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  // Add product to cart or update quantity if already in cart
  function handleAddToCart(product) {
    const existingProduct = cart.find((item) => item.id === product.id);
    if (existingProduct) {
      const updatedCart = cart.map((item) =>
        item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
      );
      setCart(updatedCart);
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
  }

  // Remove product from cart
  function handleRemoveFromCart(productId) {
    const updatedCart = cart.filter((item) => item.id !== productId);
    setCart(updatedCart);
  }

  return (
    <div>
      <h1>Simple E-Commerce Cart</h1>

      {/* Search and Sort */}
      <div>
        <input
          type="text"
          placeholder="Search products"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <select onChange={(e) => setSortType(e.target.value)}>
          <option value="name">Sort by Name</option>
          <option value="price">Sort by Price</option>
        </select>
      </div>

      {/* Product List */}
      <ProductList products={filteredProducts} onAddToCart={handleAddToCart} />

      {/* Cart */}
      <Cart cart={cart} onRemoveFromCart={handleRemoveFromCart} />
    </div>
  );
}

export default App;
