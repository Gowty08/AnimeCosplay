// Enhanced JavaScript for MongoDB integration
document.addEventListener('DOMContentLoaded', function() {
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            const productId = productCard.dataset.productId;
            const productName = productCard.querySelector('.product-title').textContent;
            
            // Send AJAX request to add to cart
            fetch('/add_to_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `product_id=${productId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`${productName} added to cart!`);
                    // Update cart count
                    const cartCountElements = document.querySelectorAll('.cart-count');
                    cartCountElements.forEach(element => {
                        element.textContent = data.cart_count;
                    });
                }
            });
        });
    });
    
    // Quantity buttons in cart
    const quantityBtns = document.querySelectorAll('.quantity-btn');
    quantityBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.quantity-input');
            let value = parseInt(input.value);
            
            if (this.textContent === '+') {
                value++;
            } else if (this.textContent === '-' && value > 1) {
                value--;
            }
            
            input.value = value;
            
            // Update quantity in server
            const cartItem = this.closest('.cart-item');
            const productId = cartItem.dataset.productId;
            
            fetch('/update_cart_quantity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `product_id=${productId}&quantity=${value}`
            });
            
            updateCartTotals();
        });
    });
    
    // Remove item buttons
    const removeItemBtns = document.querySelectorAll('.remove-item');
    removeItemBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const cartItem = this.closest('.cart-item');
            const productId = cartItem.dataset.productId;
            
            // Send AJAX request to remove from cart
            fetch('/remove_from_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `product_id=${productId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    cartItem.style.opacity = '0';
                    setTimeout(() => {
                        cartItem.remove();
                        updateCartTotals();
                        
                        // If no items left, show empty cart message
                        if (document.querySelectorAll('.cart-item').length === 0) {
                            document.querySelector('.cart-items').innerHTML = 
                                '<p class="empty-cart">Your cart is empty. <a href="/products">Continue shopping</a></p>';
                            document.querySelector('.cart-summary').style.display = 'none';
                        }
                    }, 300);
                    
                    // Update cart count
                    const cartCountElements = document.querySelectorAll('.cart-count');
                    cartCountElements.forEach(element => {
                        element.textContent = data.cart_count;
                    });
                }
            });
        });
    });
    
    function updateCartTotals() {
        // Calculate and update cart totals
        let subtotal = 0;
        document.querySelectorAll('.cart-item').forEach(item => {
            const priceText = item.querySelector('.cart-item-price').textContent;
            const price = parseFloat(priceText.replace('$', ''));
            const quantity = parseInt(item.querySelector('.quantity-input').value);
            subtotal += price * quantity;
        });
        
        const shipping = 15.00;
        const tax = subtotal * 0.08;
        const total = subtotal + shipping + tax;
        
        // Update summary
        document.querySelector('.summary-item:nth-child(1) span:last-child').textContent = '$' + subtotal.toFixed(2);
        document.querySelector('.summary-item:nth-child(3) span:last-child').textContent = '$' + tax.toFixed(2);
        document.querySelector('.summary-total span:last-child').textContent = '$' + total.toFixed(2);
    }
});