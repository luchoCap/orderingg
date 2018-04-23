const API = (function () {
    /**
     * Obtiene una orden desde el backend
     *
     * @param {Number} orderId id de la orden
     */
    function getOrder(orderId) {
        return fetch('/order/1')
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Obtiene todos los productos desde el backend
     *
     */
    function getProducts() {
        return fetch('/product')
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Obtiene todos los productos pertenecientes a una orden desde el backend
     *
     */
    function getOrderProduct(orderId, productId) {
        return fetch(`/order/${ orderId }/product/${ productId }`)
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Edita un producto de una orden
     *
     */
    function editProduct(orderId, productId, quantity, product) {
        const data = JSON.stringify({ quantity: quantity, product: product })

        return fetch(`/order/${ orderId }/product/${ productId }`,
            {
                method: 'PUT',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: data
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }

    /**
     * Agrega un producto a una orden
     **/
    function addProduct(orderId, product, quantity) {
        const data = JSON.stringify({ quantity: quantity, product: product })

        return fetch(`/order/${ orderId }/product`,
            {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: data
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }

    return {
        getOrder,
        getProducts,
        getOrderProduct,
        editProduct,
        addProduct
    }
})()
