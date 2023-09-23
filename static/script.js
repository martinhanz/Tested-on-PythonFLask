document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('prediction-form').addEventListener('submit', function(e) {
        e.preventDefault();

    var less = document.getElementById('less-input').value;
    var stock = document.getElementById('stock-input').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/predict_production', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var resultDiv = document.getElementById('defuzz-value');
                resultDiv.innerHTML = 'Prediksi Jumlah Produksi: ' + response.production;
            }
        }
    };
    var data = JSON.stringify({'less': less, 'stock': stock });
    xhr.send(data);
    });
});