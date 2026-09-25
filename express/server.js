const express = require("express");
const cors = require("cors")

const app = express();
const port = 3000;

app.use(express.json());
app.use(cors({
  origin: "http://127.0.0.1:9999"
}));

app.post("/", async (req, res) => {
  console.log("POST RECIBIDO");
  console.log(req.body);
  const response = await fetch("http://127.0.0.1:8001/books", {
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(req.body)
  });

  const data = await response.json()
  //res.status(response.status).json(data) THIS IS FOR LATER WHEN FASTAPI IS ALREADY IMPLEMENTED
});

app.listen(port, () => {
  console.log(`listening on http://localhost:${port}`);
});

