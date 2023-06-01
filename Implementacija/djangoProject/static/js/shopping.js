$(document).ready(function () {

    //updating the sumPrice of a single row in cart(a wine)
    //returns calculated global sum(whole cart) after this change
    function updatePrices(priceElement, quantityInput, sumPriceElement, priceTotalValue) {
        let priceValue = $(priceElement).text();
        let quantityValue = $(quantityInput).val();
        let sumPriceValue = quantityValue * priceValue;
        priceTotalValue += sumPriceValue;
        $(sumPriceElement).text(sumPriceValue + ' RSD');
        return priceTotalValue;
    }

    //dynamically changes the sumPrices and handles quantity changes in cart
    function sumPriceCalculation() {
        let quantityInputs = $('[name="quantity"]');
        let priceElements = $('.price');
        let sumPriceElements = $('.sumPrice');
        let priceTotalElement = $('#priceTotal');
        let priceTotalValue = 0;

        quantityInputs.each(function (i) {
            //initial values on load
            priceTotalValue = updatePrices(priceElements[i], this, sumPriceElements[i], priceTotalValue);
            //handles quantity field changes
            $(this).on('input', function () {
                if ($(this).val() <= 0 || $(this).val()==='')
                    $(this).val(1);
                let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
                //changes in database
                let itemId = $(this).data('item-id');
                let newQuantity = $(this).val()
                $.ajax({
                    url: '/shopping/shoppingCart/changeQuantity',
                    method: 'POST',
                    data: {
                        itemId: itemId,  // Send the item ID to the server
                        newQuantity: newQuantity,
                        csrfmiddlewaretoken: csrfToken,
                    }
                });
                //changes the sumPrices
                priceTotalValue = 0;
                quantityInputs.each(function (j) {
                    priceTotalValue = updatePrices(priceElements[j], this, sumPriceElements[j], priceTotalValue);
                });
                priceTotalElement.text(priceTotalValue + ' RSD');
            });
            //handles updating the total sum when a row is deleted
            $('.close').on('click', function () {
                $(this).closest('tr').find('.price').text('0');
                quantityInputs = $('[name="quantity"]');
                priceElements = $('.price');
                sumPriceElements = $('.sumPrice');
            })
        });

        priceTotalElement.text(priceTotalValue + ' RSD');
    }

    //handles deleting a row in cart
    function deleteCartItem() {
        $('.close').on('click', function () {
            let itemId = $(this).data('item-id');
            let currentSum = parseInt($(this).closest('tr').find('.sumPrice').text().split(' ')[0]);
            let newTotal = parseInt($('#priceTotal').text()) - currentSum;
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

    //handles the buying
    function buyItems() {
        $('#buy').on('click', function () {
            let theTotal = parseInt($('#priceTotal').text());
            if (isNaN(theTotal)) theTotal = 0;
            if (theTotal === 0)
                return;
            //getting arrays of data to send via email
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
                    sumPrices: sumPriceValues,
                    theTotal: theTotal,
                    csrfmiddlewaretoken: csrfToken,
                }
            });
        });
    }

    //handles adding a wine in cart in 'vinoPojedinacanPrikaz.html'
    function addToCart() {
         $('#addWineButton').on('click', function () {
             $('#confirmationText').show();
             let quantity = $('[name="quantity"]').val();
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

    //handles reservation missing fields
    function missingInfoReservation() {
        const radioButtons = document.querySelectorAll('input[type="radio"][required]');
        const radioGroup = document.getElementsByName('obilazak');

        radioGroup.forEach(function(radio) {
            console.log(radioGroup.length)
            radio.addEventListener('input', function() {
                // resetRadioValidity
                radioGroup.forEach(function(r) {
                    r.setCustomValidity('');
                })
            });
        });
    }

    if (document.URL.match("shoppingCart")) {
        sumPriceCalculation();
        deleteCartItem();
        buyItems();
    }
    else if (document.URL.match("wine")) {
        addToCart();
    }
    else if (document.URL.match("detour")) {
        missingInfoReservation();
    }
})