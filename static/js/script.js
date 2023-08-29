const options = { day: 'numeric', month: 'long', year: 'numeric' };
const date = new Date();
const formattedDate = date.toLocaleDateString('en-US', options);
document.querySelector('#current_date').textContent = formattedDate;
console.log(formattedDate);
