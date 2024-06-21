async function autocompleteSearch() {
  const query = document.getElementById("search").value;
  const response = await fetch(`/autocomplete?query=${query}`);
  const suggestions = await response.json();
  let suggestionsList = document.getElementById("suggestions");
  suggestionsList.innerHTML = "";
  suggestions.forEach((title) => {
    let option = document.createElement("option");
    option.value = title;
    suggestionsList.appendChild(option);
  });
}

async function getRecommendations() {
  const title = document.getElementById("search").value;
  if (title) {
    $.get("/recommend", { title: title }, function (data) {
      const tbody = document.querySelector("#recommendations1");
      tbody.innerHTML = "";
      data.slice(0, 5).forEach((book) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${book.Judul}</td>
          <td><button class="btn btn-primary" onclick="viewBook('${book.Judul}')">View</button></td>
        `;
        tbody.appendChild(tr);
      });
    });
  }
}

function viewBook(title) {
  $.get("/details", { title: title }, function (data) {
    if (data.error) {
      alert(data.error);
    } else {
      let details = `
        <tr><th>NoPanggil</th><td>${data.NoPanggil}</td></tr>
        <tr><th>NoInduk</th><td>${data.NoInduk}</td></tr>
        <tr><th>TglOlah</th><td>${data.TglOlah}</td></tr>
        <tr><th>NRP</th><td>${data.NRP}</td></tr>
        <tr><th>Nama</th><td>${data.Nama}</td></tr>
        <tr><th>Jurusan</th><td>${data.Jurusan}</td></tr>
        <tr><th>Judul</th><td>${data.Judul}</td></tr>
        <tr><th>Pembimbing1</th><td>${data.Pembimbing1}</td></tr>
        <tr><th>Pembimbing2</th><td>${data.Pembimbing2}</td></tr>
        <tr><th>Pembimbing3}</th><td>${data.Pembimbing3}</td></tr>
        <tr><th>Keywords</th><td>${data.Keywords}</td></tr>
        <tr><th>Abstrak</th><td>${data.Abstrak}</td></tr>
      `;
      $("#bookDetails").html(details);
      $("#bookModal").css("display", "block");
    }
  });
}

function closeModal() {
  $("#bookModal").css("display", "none");
}

window.onclick = function (event) {
  if (event.target == document.getElementById("bookModal")) {
    closeModal();
  }
};

async function searchBooks() {
  const query = document.getElementById("search2").value;
  const response = await fetch(`/search_books?query=${query}`);
  const books = await response.json();
  const tbody = document.querySelector("#recommendations2Body");
  tbody.innerHTML = "";
  books.forEach((book) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${book.Judul}</td>
      <td><button class="btn btn-primary" onclick="viewBook('${book.Judul}')">View</button></td>
    `;
    tbody.appendChild(tr);
  });
}
