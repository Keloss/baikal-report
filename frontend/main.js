document.getElementById("btn").addEventListener("click", async () => {
  const start = document.getElementById("start").value;
  const end = document.getElementById("end").value;

  if (!start || !end) {
    alert("Выберите Начавло и конец периода");
    return;
  }

  const url = `/report?start=${start}&end=${end}`;

  const res = await fetch(url);
  const data = await res.json();

  let html = `
      <div class="table-responsive">
      <table class="table table-bordered table-striped">
        <thead class="table-dark">
          <tr>
            <th>Пользователь</th>
            <th>Событие</th>
            <th>Начало</th>
            <th>Конец</th>
          </tr>
        </thead>
        <tbody>
    `;

  for (const ev of data.events) {
    html += `
          <tr>
            <td>${ev.calendar}</td>
            <td>${ev.summary}</td>
            <td>${ev.start}</td>
            <td>${ev.end}</td>
          </tr>
        `;
  }

  html += `
        </tbody>
      </table>
      </div>
    `;

  document.getElementById("result").innerHTML = html;
});
