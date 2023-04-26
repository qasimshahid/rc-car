
const http = require('http');
const fs = require('fs');
const path = require('path');

const hostname = '127.0.0.1';
const port = 9532;

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    // serve the index.html file
    fs.readFile('index.html', (err, data) => {
      if (err) {
        res.statusCode = 500;
        res.setHeader('Content-Type', 'text/plain');
        res.end('Internal Server Error');
        return;
      }

      res.statusCode = 200;
      res.setHeader('Content-Type', 'text/html');
      res.end(data);
    });
  } else if (req.url === '/styles.css') {
    // serve the styles.css file
    fs.readFile('styles.css', (err, data) => {
      if (err) {
        res.statusCode = 500;
        res.setHeader('Content-Type', 'text/plain');
        res.end('Internal Server Error');
        return;
      }

      res.statusCode = 200;
      res.setHeader('Content-Type', 'text/css');
      res.end(data);
    });
  } else if (req.url.startsWith('/images/')) {
    // serve the image file
    const filePath = path.join(__dirname, req.url);
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.statusCode = 500;
        res.setHeader('Content-Type', 'text/plain');
        res.end('Internal Server Error');
        return;
      }

      res.statusCode = 200;
      res.setHeader('Content-Type', 'image/jpeg');
      res.end(data);
    });
  } else {
    res.statusCode = 404;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Not Found');
  }
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});


function changeStream() {
    const ipAddress = "";
    const currentSrc = document.getElementById('stream').getAttribute('src');
    let newSrc;
    if (currentSrc.endsWith('optimize1')) {
      newSrc = `http://${ipAddress}:8554/optimize2`;
    } else {
      newSrc = `http://${ipAddress}:8554/optimize1`;
    }
    document.getElementById('stream').setAttribute('src', newSrc);
  }

