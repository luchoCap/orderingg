(function () {
    const $totalPrice = document.querySelector('#total-price');

    // Estado de la aplicacion
    const state = {
        products: API.getProducts(),
        selectedProduct: null,
        quantity: 0,
        order: API.getOrder()
    }
    window.onChangeQunatity=actualizar;

    const refs = {}

    /**
     * Actualiza el valor del precio total
     **/
    function updateTotalPrice() {
        try {
            const totalPrice = state.selectedProduct.price * state.quantity;
            $totalPrice.innerHTML = `Precio total: $ ${totalPrice}`
        } catch (e) {
            $totalPrice.innerHTML = '';
        }
    }

    /**
     * Dispara la actualizacion del precio total del producto
     * al cambiar el producto seleccionado
     **/
    function onProductSelect(selectedProduct) {
        state.selectedProduct = selectedProduct;
        updateTotalPrice();
    }
     function actualizar(selectedProduct) {
        state.selectedProduct = selectedProduct;
    }

    /**
     * Dispara la actualizacion del precio total del producto
     * al cambiar la cantidad del producto
     **/
    function onChangeQunatity(quantity) {
        state.quantity = quantity;
        updateTotalPrice();
    }

    function onEditProduct() {
        API.editProduct(1, state.selectedProduct.id, state.quantity)
            .then(function (r) {
                API.getOrder().then(function (data) {
                    refs.table.update(data);
                });

                refs.modal.close();
            });
    }

    /**
     * Agrega un producto a una orden
     *
     **/
    function onAddProduct() {
        return API.addProduct(1, state.selectedProduct, state.quantity)
            .then(function (r) {
                if (r.error) {
                    return Promise.reject({
                        msg: "No puede existir 2 productos iguales en una orden"
                    });
                }

                API.getOrder().then(function (data) {
                    refs.table.update(data);
                });

                refs.modal.close();
            })
            .catch(function (err) {
                if (err.msg) {
                    return Promise.reject(err);
                }
                return Promise.reject({
                    msg: "Seleccione un producto"
                });
            });
    }

    function onDeleteProduct(productId) {
        API.deleteProduct(1, productId)
            .then(function (r) {
                if (r.error) {
                    console.error(r.error);
                } else {
                    API.getOrder().then(function (data) {
                        refs.table.update(data);
                    });
                }
            });
    }

    function onEditProduct(){
        productID = document.getElementById('select-prod').value;
        cantidad = document.getElementById('quantity').value;


        API.editProduct(1,productID,cantidad,API.getOrderProduct(1,productID))
         .then(function (r) {
                if (r.error) {
                    console.error(r.error);
                } else {
                    API.getOrder().then(function (data) {
                        refs.table.update(data);
                    });

                    refs.modal.close();
                }
            });
    }

    /**
     * Inicializa la aplicacion
     **/
    function init() {
        refs.modal = Modal.init({
            el: '#modal',
            products: state.products,
            onProductSelect: onProductSelect,
            onChangeQunatity: onChangeQunatity,
            onAddProduct: onAddProduct,
            onEditProduct: onEditProduct
        });

        // Inicializamos la tabla
        refs.table = Table.init({
            el: '#orders',
            data: state.order
        });

        refs.global = {
            onDeleteProduct
        }
    }

    init();
    window.refs = refs;
})()