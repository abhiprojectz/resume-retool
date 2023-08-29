
function create_board() {

const board_name_x = document.getElementById('board_name');
const url = '/api/create_board';
const data = {
    board_name: board_name_x.value,
};

const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;


fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      window.location.href = '/dashboard/' + data.board_id + '/'; 
    })
    .catch(error => console.error(error));
    

}


function delete_all_boards() {
    const url = '/api/delete_all_boards';
  
    const data = {
      board_id: 00000,
    };
  
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
        var jsonData = data.output;
        location.reload();
            })
      .catch(error => console.error(error));
  
  }


  function delete_board(el) {
    const url = '/api/delete_board';
    var board_id = el.getAttribute('data-target');

    const data = {
      board_id: board_id,
    };
  
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
        var jsonData = data.output;
        location.reload();
            })
      .catch(error => console.error(error));
  
  }
