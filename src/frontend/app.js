let ipAddress = ""

function changeStream() {
    const currentSrc = document.getElementById('stream').getAttribute('src');
    let newSrc;
    if (currentSrc.endsWith('cam1')) {
      newSrc = `http://${ipAddress}:8554/cam2`;
    } else {
      newSrc = `http://${ipAddress}:8554/cam1`;
    }
    document.getElementById('stream').setAttribute('src', newSrc);
  }

