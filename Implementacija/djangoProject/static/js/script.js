$(document).ready(function () {

    $('#quantity').on('input', function () {
        $('#confirmationText').hide();
        let quantity = parseInt($('#quantity').val());
        console.log(quantity)
        let max = parseInt($('#quantity').attr('max'));
        if (document.URL.match("celebration")) {
            if (quantity > max)
                $('#quantity').val(max);
            else if (quantity < 1 || $('#quantity').val() === '')
                $('#quantity').val(1);
        }
    });

    $('.quantity-right-plus').click(function (e) {
        $('#confirmationText').hide();
        // Stop acting like a button
        e.preventDefault();

        let quantity = parseInt($('#quantity').val());
        let newQuantity = quantity + 1;
        let max = parseInt($('#quantity').attr('max'));

        if (document.URL.match("celebration")) {
            if (quantity > max)
                $('#quantity').val(max);
            else if (quantity < max)
                $('#quantity').val(newQuantity);
        }
        else
            $('#quantity').val(newQuantity);

    });

    $('.quantity-left-minus').click(function (e) {
        $('#confirmationText').hide();
        // Stop acting like a button
        e.preventDefault();

        let quantity = parseInt($('#quantity').val());

        if (quantity > 1) {
            $('#quantity').val(quantity - 1);
        }

    });

});