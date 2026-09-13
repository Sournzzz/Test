let books = []
const inputBook = document.getElementById("input-book")
const submitBtn = document.getElementById("submit-btn")
const listBook = document.getElementById("list-book")

submitBtn.addEventListener("click", () => {
  let book_el = document.createElement("li");
  book_el.textContent = inputBook.value
  listBook.appendChild(book_el)
  inputBook.value = "";

})




