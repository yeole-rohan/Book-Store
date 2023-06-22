var $ = jQuery.noConflict();
$(document).ready((function () {

    $(document).on('click', '#copyButton', function (event) {
        event.preventDefault()
        var codeSnippet = event.target.getAttribute('data-clipboard-text');
        copyToClipboard(codeSnippet);
    });

    function copyToClipboard(text) {
        navigator.clipboard.writeText(text)
            .then(function () {
                alert('Coupon Code copied!');
            })
            .catch(function (error) {
                console.error('Unable to copy coupon code:', error);
            });
    }
})(jQuery)
);
