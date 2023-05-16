function changeStream() {
    const currentSrc = document.getElementById('stream').getAttribute('src');
    let newSrc;
    if (currentSrc.endsWith('cam1')) {
      newSrc = `http://G17:8889/cam2`;
    } else {
      newSrc = `http://G17:8889/cam1`;
    }
    document.getElementById('stream').setAttribute('src', newSrc);
  }

