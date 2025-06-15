const form = document.getElementById("commentForm");
const commentsDiv = document.getElementById("comments");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  await fetch("/comment", {
    method: "POST",
    body: formData
  });
  form.reset();
  loadComments();
});

function loadComments() {
  fetch("/comments")
    .then(res => res.json())
    .then(data => {
      commentsDiv.innerHTML = "";
      data.forEach(item => {
        const div = document.createElement("div");
        div.className = "comment";
        div.innerHTML = `
          <p>${item.timestamp}</p>
          <p>${item.content}</p>
          ${item.media ? renderMedia(item.media) : ""}
        `;
        commentsDiv.appendChild(div);
      });
    });
}

function renderMedia(file) {
  const ext = file.split('.').pop().toLowerCase();
  if (['mp4', 'mov'].includes(ext)) {
    return `<video controls src="/static/uploads/${file}"></video>`;
  } else {
    return `<img src="/static/uploads/${file}">`;
  }
}

loadComments();
setInterval(loadComments, 3000);
