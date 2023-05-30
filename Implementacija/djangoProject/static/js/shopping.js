$(document).ready(function () {

    function updatePrices(priceElement, quantityInput, sumPriceElement, priceTotalValue) {
        let priceValue = $(priceElement).text();
        let quantityValue = $(quantityInput).val();
        let sumPriceValue = quantityValue * priceValue;
        priceTotalValue += sumPriceValue;
        $(sumPriceElement).text(sumPriceValue + ' RSD');
        return priceTotalValue;
    }

    function sumPriceCalculation() {
        let quantityInputs = $('[name="quantity"]');
        let priceElements = $('.price');
        let sumPriceElements = $('.sumPrice');
        let priceTotalElement = $('#priceTotal');
        let priceTotalValue = 0;

        quantityInputs.each(function (i) {
            priceTotalValue = updatePrices(priceElements[i], this, sumPriceElements[i], priceTotalValue);

            $(this).on('input', function () {
                if ($(this).val() < 0)
                    $(this).val(1);
                priceTotalValue = 0;
                quantityInputs.each(function (j) {
                    priceTotalValue = updatePrices(priceElements[j], this, sumPriceElements[j], priceTotalValue);
                });
                priceTotalElement.text(priceTotalValue + ' RSD');
            });
        });

        priceTotalElement.text(priceTotalValue + ' RSD');
    }

    function deleteCartItem() {
        $('.close').on('click', function () {
            let itemId = $(this).data('item-id');
            let newTotal = parseInt($('#priceTotal').text()) - parseInt($(this).closest('tr').find('.sumPrice').text().split(' ')[0]);
            if (isNaN(newTotal)) newTotal = 0;
            $('#priceTotal').text(newTotal + ' RSD');

            // Send AJAX request to delete the item
            let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax({
                url: '/shopping/shoppingCart/deleteItem',  // shopping view that handles deletion
                method: 'POST',
                data: {
                    itemId: itemId,  // Send the item ID to the server
                    csrfmiddlewaretoken: csrfToken,
                }
            });
        });
    }

    function buyItems() {
        $('#buy').on('click', function () {
            let theTotal = parseInt($('#priceTotal').text());
            if (isNaN(theTotal)) theTotal = 0;
            if (theTotal === 0)
                return;
            let quantityInputs = $('[name="quantity"]');
            let quantityValues = quantityInputs.map(function () {
                return $(this).val();
            }).get();
            let sumPriceElements = $('.sumPrice');
            let sumPriceValues = sumPriceElements.map(function () {
                return parseInt($(this).text());
            }).get();

            // Send AJAX request to buy the items
            let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax({
                url: '/shopping/shoppingDone',  // shopping view that handles confirmation
                method: 'POST',
                data: {
                    quantities: quantityValues,
                    sumPrices: sumPriceValues,
                    theTotal: theTotal,
                    csrfmiddlewaretoken: csrfToken,
                }
            });
        });
    }

    function addToCart() {
        console.log("inAddToCart")
         $('#addVineButton').on('click', function () {
             console.log("clickedAdd")
             let quantity = $('[name="quantity"]');
             let idItem = $(this).data('item-id');
             let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
             $.ajax({
                url: '/shopping/addToCart',
                method: 'POST',
                data: {
                    idItem: idItem,
                    quantity: quantity,
                    csrfmiddlewaretoken: csrfToken,
                }
            });
         })
    }

    if (document.URL.match("shoppingCart")) {
        sumPriceCalculation();
        deleteCartItem();
        buyItems();
    }
    else if (document.URL.match("wine")) {
        addToCart();
    }
})