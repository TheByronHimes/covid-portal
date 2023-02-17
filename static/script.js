async function poll () {
    console.log("sending request...");
    await fetch('/msg')
    .then((response) => response.json())
    .then((data) => console.log(data));
    poll();
}

//poll();