const express = require("express");
const app = express();
const port = 3000;

app.use(express.json());

app.post("/", (req, res) => {
  console.log("POST RECIBIDO");
  console.log(req.body);
  res.sendStatus(200);
});

app.listen(port, () => {
  console.log(`listening on http://localhost:${port}`);
});
