import path, { dirname } from "path";
import express from "express";
import bodyParser from "body-parser";
import imageDataURI from "image-data-uri";
import { execFile } from "child_process";

const port = process.env.PORT || 3000;
const publicPath = path.resolve(__dirname, "../build");
const app = express();

app.use(bodyParser.json());
app.post("/api/print", async (req, res) => {
  const filename = path.resolve(__dirname, "../tmp/", uuidv4());

  await imageDataURI.outputFile(req.body.black, filename + "_black.png");
  await imageDataURI.outputFile(req.body.red, filename + "_red.png");

  execFile(
    "python",
    [
      path.join(__dirname, "python/main.py"),
      filename + "_black.png",
      filename + "_red.png"
    ],
    (err, result) => {
      console.log(err);
      console.log(result);
    }
  );
  console.log("python");
  res.send({ success: true });
});

app.use(express.static(publicPath));

app.listen(port, () =>
  console.log("Paint started on http://localhost:" + port)
);

function uuidv4() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
    var r = (Math.random() * 16) | 0,
      v = c == "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}
