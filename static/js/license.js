const half_usd_button = document.getElementById("half-usd-btn");
const one_usd_button = document.getElementById("one-usd-btn");
const two_and_half_usd_button = document.getElementById("two-and-half-usd-btn");
const AmountOfGigaByteMonth = document.getElementById("AmountOfGigaByteMonth");
const amountOfWon = document.getElementById("amountOfWon");

half_usd_button.addEventListener("click", half_usd_button_pressed);
one_usd_button.addEventListener("click", one_usd_button_pressed);
two_and_half_usd_button.addEventListener("click", two_and_half_usd_button_pressed);

function half_usd_button_pressed() {
  AmountOfGigaByteMonth.innerText = "10GB/월";
  amountOfWon.innerText = "500원";
  // amountOfWon.style.marginLeft = "70px";
}
function one_usd_button_pressed() {
  AmountOfGigaByteMonth.innerText = "300GB/월";
  amountOfWon.innerText = "9,900원";
  // amountOfWon.style.marginLeft = "10px";
}

// function two_and_half_usd_button_pressed() {
//   AmountOfGigaByteMonth.innerText = "1,000GB/월";
//   amountOfWon.innerText = "27,900  원";
// }

//Comming Soon 버튼 눌리게 하시고 싶으시면 22번째 줄부터 25번째 줄을 주석 해제하시면 됩니다.
