// Add product row
$("#addProduct").click(function () {
    $("#products").append(`
      <div class="row mb-2">
        <div class="col-md-6">
          <input class="form-control" name="product_id[]" placeholder="Product ID">
        </div>
        <div class="col-md-6">
          <input class="form-control" name="quantity[]" placeholder="Quantity">
        </div>
      </div>
    `);
});

// Calculate paid amount from denominations
$(".denom-input").on("input", function () {
    let total = 0;

    $(".denom-input").each(function () {
        let count = parseInt($(this).val()) || 0;
        let value = parseInt($(this).data("value"));
        total += count * value;
    });

    $("#paid_amount").val(total);
});

// Submit form via AJAX
$("#billingForm").submit(function (e) {
    e.preventDefault();

    $.ajax({
        url: "/generate-bill/",
        method: "POST",
        data: $(this).serialize(),
        success: function (res) {
            window.location.href = "/bill/" + res.bill_id + "/";
        }
    });
});
