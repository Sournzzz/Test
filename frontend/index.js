const bookForm = document.getElementById("book-create");
const bookSubmitted = document.getElementById("book-submitted");

const testHeaders = new Headers();
testHeaders.append("Content-Type", "application/json");

async function logBook(event) {
  event.preventDefault();

  const formData = new FormData(bookForm);
  const bookInput = {};

  for (const [key, value] of formData) {
    if (value.toString().length > 0) {
      bookInput[key] = value.toString();
    }
  }

  bookSubmitted.textContent = `${Object.entries(bookInput)}`;

  console.log("Antes del fetch")

  const response = await fetch(
    "http://localhost:3000/", {
    method: "POST",
    headers: testHeaders,
    body: JSON.stringify(bookInput)
  });
}

console.log("Despues del fetch")

bookForm.addEventListener("submit", logBook);


