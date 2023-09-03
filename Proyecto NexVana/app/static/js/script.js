document.addEventListener('DOMContentLoaded', function () {
    let loadMoreBtns = document.querySelectorAll(".load-more");
    
    loadMoreBtns.forEach((loadMoreBtn, index) => {
        let currentItem = 4;

        loadMoreBtn.onclick = () => {
            let boxes = [...document.querySelectorAll(`.box-container-${index + 1} .box-${index + 1}`)];
            for (var i = currentItem; i < currentItem + 4; i++) {
                if (boxes[i]) {
                    boxes[i].style.display = 'inline-block';
                }
            }
            currentItem += 4;
            if (currentItem >= boxes.length) {
                loadMoreBtn.style.display = 'none';
            }
        };
    });
    
    function irArriba(pxPantalla) {
        window.addEventListener('scroll', () => {
            var scroll = document.documentElement.scrollTop;
            var botonArriba = document.getElementById('botonArriba');

            if (scroll > pxPantalla) {
                botonArriba.style.right = '20px';
            } else {
                botonArriba.style.right = '-100px';
            }
        });
    }
    
    irArriba(1000);
});
