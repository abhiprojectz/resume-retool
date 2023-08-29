var pdf_status = document.querySelector("#pdf_status");
pdf_status.style.display = "none";


const elements = document.querySelectorAll('.card_slides_item');
let activeElement;
elements.forEach(element => {
    element.addEventListener('click', () => {
      if (activeElement) {
        activeElement.classList.remove('active');
      }
      element.classList.add('active');
      activeElement = element;
    });
  });


function download_pdf() {
  const boardId = "your_board_id";
  var pdf_status = document.querySelector("#pdf_status");
  pdf_status.style.display = "block";
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  fetch("/api/download", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ board_id: board_id }),
  })
    .then((response) => response.blob())
    .then((blob) => {
      // Create a temporary URL for the blob
      const url = URL.createObjectURL(blob);

      // Create a link element and set its attributes
      const link = document.createElement("a");
      link.href = url;
      link.download = "output.pdf";

      // Append the link to the document body and click it programmatically
      document.body.appendChild(link);
      console.log(url);
      link.click();

      // Clean up the temporary URL
      URL.revokeObjectURL(url);
      pdf_status.style.display = "none";
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function change(divElement) {
  const input = document.getElementById("prompt_field");
  input.value = divElement.textContent.trim();

  const dataTarget = divElement.getAttribute("data-target");
  input.setAttribute("data-target", dataTarget);
}

function image_change(_id) {
  const input = document.getElementById("regenerate");
  input.setAttribute("data-target", _id);
}


function delete_all_slides() {
  const url = "/api/delete_all_slides";

  const data = {
    board_id: board_id,
  };

  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      var jsonData = data.output;
      location.reload();
    })
    .catch((error) => console.error(error));
}

function switch_fullscreen() {
  const element = document.documentElement; // This selects the entire HTML document
  if (element.requestFullscreen) {
    element.requestFullscreen();
  } else if (element.webkitRequestFullscreen) {
    /* Safari */
    element.webkitRequestFullscreen();
  } else if (element.msRequestFullscreen) {
    /* IE11 */
    element.msRequestFullscreen();
  }
}

// Define the applyChanges() function

function applyChanges() {
  const divs = document.querySelectorAll(".clickable-div");
  const input = document.getElementById("prompt_field");
  const inputTarget = input.getAttribute("data-target");
  divs.forEach((divElement) => {
    const targetId = divElement.getAttribute("data-target");
    if (targetId === inputTarget) {
      const url = "/api/update_text";

      const data = {
        slide_id: targetId,
        text_prompt: input.value,
      };

      const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0]
        .value;

      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => {
          var jsonData = data.result;
          console.log(input.value);
          divElement.textContent = input.value;
          input.value = "";
        })
        .catch((error) => console.error(error));
    }
  });
}

function add_slide(data_list) {
  // Get the slides container element
  const slides_container = document.getElementById("slides_container");

  // Create a new element
  const newElement = document.createElement("div");
  newElement.classList.add("col-md-6", "col-lg-3");

  // Set the new element's HTML content to the custom code inside a _context variable
  const customHTML = `
      <div class="card_slides_item">
        <div class="card-body" style="padding: 0; flex:0;">
          <span onclick="image_change(${data_list["slide_id"]})" class="avatar bg_m mb-3 rounded" id="slide_image" style="background-image: url(${data_list["slide_image"]})"></span>

          <div class="card_lane_items p-2">
            <span class="badge bg-purple-lt" id="slide_count">${data_list["slide_count"]}</span>
          </div>
        </div>

        <div class="d-flex p-2">
          <div class="card_item_bc">
            <div>
              <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-align-box-left-middle" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#6A27FF" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                <path d="M3 3m0 2a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2z" />
                <path d="M9 15h-2" />
                <path d="M13 12h-6" />
                <path d="M11 9h-4" />
              </svg>
            </div>

            <div class="clickable-div" data-target="${data_list["slide_id"]}" onclick="change(this)">${data_list["prompt_content"]}</div>
          </div>
        </div>
      </div>
    `;
  newElement.innerHTML = customHTML;

  const lastChild = slides_container.lastElementChild;

  // Append the new element to the container as the second last child
  slides_container.insertBefore(newElement, lastChild);
  const elements = document.querySelectorAll('.card_slides_item');
elements.forEach(element => {
    element.addEventListener('click', () => {
      if (activeElement) {
        activeElement.classList.remove('active');
      }
      element.classList.add('active');
      activeElement = element;
    });
  });
}

const container = document.querySelector("._ab");

// Get the input element with ID 'image_style'
const input = document.querySelector("#image_style");

// Add a click listener to all div elements inside the container
container.querySelectorAll("div").forEach((div) => {
  div.addEventListener("click", () => {
    // Set the value of the input element to the clicked div's textContent
    input.value = div.textContent.trim();
  });
});



function suggestai() {
    const loader = document.getElementById("loaderz");
    const imgBlock = document.getElementById("img_ai_block_1x");
    var modalx = document.getElementById("suggestModal");
    loader.style.display = "block";
    imgBlock.style.display = "none";
  
    const text_prompt = document.getElementById("suggest_content");
    const text_promptx = document.getElementById("text_content");

    const url = "/api/generate_suggestion";
  
    const data = {
      board_id: board_id,
    };
  
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        loader.style.display = "none";
        imgBlock.style.display = "block";
  
        var jsonData = data.output;

        text_prompt.value = jsonData.output;
        text_promptx.value = jsonData.output;

      })
      .catch((error) => {
        loader.style.display = "none";
        imgBlock.style.display = "block";
        console.error(error);
      });
}

function generate_script() {
  const loader = document.getElementById("loadery");
  const imgBlock = document.getElementById("img_ai_block_1");
  var modalx = document.getElementById("scriptModal");
  loader.style.display = "block";
  imgBlock.style.display = "none";

  const text_prompt = document.getElementById("text_content");
  const languageSelect = document.getElementById("language");
  const framesCountSelect = document.getElementById("count_frames");

  const url = "/api/generate_text";

  const data = {
    board_id: board_id,
    text_prompt: text_prompt.value,
    language: languageSelect.value,
    count_frames: framesCountSelect.value,
  };

  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      loader.style.display = "none";
      imgBlock.style.display = "block";

      var jsonData = data.output;
      const slideCount = jsonData.length;

      const divElement = document.querySelector("#slides_container");
      const childNodes = divElement.childNodes;
      let count = 0;
      for (let i = 0; i < childNodes.length; i++) {
        const childNode = childNodes[i];
        if (
          childNode.nodeType === Node.ELEMENT_NODE &&
          childNode.matches(".col-md-6.col-lg-3:not([id])")
        ) {
          count++;
        }
      }


      jsonData.forEach((res, index) => {
        add_slide({
          slide_id: res.slide_id,
          slide_image: res.slide_image,
          prompt_content: res.prompt_content,
          slide_count: count,
        });
        count++;
      });
      const modalBackdrop = document.querySelector(".modal-backdrop.show");
      modalBackdrop.remove();
      const bodyElement = document.querySelector("body");
      bodyElement.classList.remove("modal-open");
      bodyElement.style.overflow = "";
      bodyElement.style.paddingRight = "";
      modalx.style.display = "none";
    })
    .catch((error) => {
      loader.style.display = "none";
      imgBlock.style.display = "block";
      console.error(error);
    });
}

function increaseWidth() {
  const elements = document.querySelectorAll(".col-md-6.col-lg-3");
  elements.forEach((element) => {
    const currentWidth = element.offsetWidth;
    const newWidth = currentWidth + 80;
    element.style.width = `${newWidth}px`;
  });
}

function decreaseWidth() {
  const elements = document.querySelectorAll(".col-md-6.col-lg-3");
  elements.forEach((element) => {
    const currentWidth = element.offsetWidth;
    const newWidth = currentWidth - 100;
    element.style.width = `${newWidth}px`;
  });
}

function page_reload() {
  location.reload();
}

function generate_images(el) {
  if (el.getAttribute("data-target")) {
    const slide_id = el.getAttribute("data-target");
    const image_style = document.getElementById("image_style").value;
    const url = "/api/generate_image";
    var modalx = document.querySelector("#imageModal");
    const loader = document.getElementById("loaderx");
    const imgBlock = document.getElementById("img_ai_block");

    loader.style.display = "block";
    imgBlock.style.display = "none";

    const data = {
      slide_id: slide_id,
      image_style: image_style,
    };

    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0]
      .value;

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        var jsonData = data.output;
        loader.style.display = "none";
        imgBlock.style.display = "block";
        location.reload();
      })
      .catch((error) => console.error(error));

  } else {
    //const text_prompt = document.getElementById('text_content');
    const image_style = document.getElementById("image_style").value;
    const url = "/api/generate_all_images";

    const data = {
      board_id: board_id,
      image_style: image_style,
    };

    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0]
      .value;

    const loader = document.getElementById("loaderx");
    const imgBlock = document.getElementById("img_ai_block");

    loader.style.display = "block";
    imgBlock.style.display = "none";

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        var jsonData = data.result;
        location.reload();
        loader.style.display = "none";
        imgBlock.style.display = "block";
      })
      .catch((error) => {
        console.error(error);
        loader.style.display = "none";
        imgBlock.style.display = "block";
      });
  }
}

function create_board_slide(data) {
  const url = "/api/create_board_slide";

  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((error) => console.error(error));
}

function add_blank_frame() {
  const data = {
    board_id: board_id,
    slide_image: "blank.png",
    prompt_content: "Edit the Script",
  };

  const divElement = document.querySelector("#slides_container");
  const childNodes = divElement.childNodes;
  let count = 0;
  for (let i = 0; i < childNodes.length; i++) {
    const childNode = childNodes[i];
    if (
      childNode.nodeType === Node.ELEMENT_NODE &&
      childNode.matches(".col-md-6.col-lg-3:not([id])")
    ) {
      count++;
    }
  }

  create_board_slide(data)
    .then(function (res) {
      if (res && res.slide_id && res.prompt_content) {
        add_slide({
          slide_id: res.slide_id,
          slide_image: res.slide_image,
          prompt_content: res.prompt_content,
          slide_count: count + 1,
        });
      } else {
        console.log("Error: slide_id or prompt_content is undefined.");
      }
    })
    .catch(function (error) {
      console.log("Error: " + error.message);
    });
}
