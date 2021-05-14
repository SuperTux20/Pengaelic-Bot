import { readdir } from "fs";

readdir(".", (err, files) => {
    console.log(files.length);
});

// var productTemplate = document.getElementsByClassName("store-list")[0].childNodes[1];
// var product;
// for (product = 0; product < productList.length; product++) {
//     var cloned = productTemplate.cloneNode(true);
//     cloned.childNodes[1].src = productList[product].image;
//     cloned.childNodes[3].innerHTML = productList[product].title;
//     cloned.childNodes[5].innerHTML = "$" + productList[product].price;
//     productTemplate.parentNode.appendChild(cloned);
// }
// productTemplate.remove();