window.onload = function() {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

    let stripe;
    fetch('/get_pk')
      .then((response) => response.json())
      .then((data) => {
        stripe = Stripe(data.pk);
        console.log("Success getting Stripe Public Key");
      })
      .catch((err) => {
      console.error(err);
      console.error("Stripe Public Key getting error");
    });
  
  
  const buyForms = document.querySelectorAll('.buyForm');
  for (let index = 0; index < buyForms.length; index += 1) {
    const buyForm = buyForms[index];
    buyForm.addEventListener('submit', (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      const sending_form = e.target;
      const pk = parseInt(sending_form.id.replace('buyForm', ''));
      const csrftoken = getCookie('csrftoken');

      fetch('/orders/' + pk, {
        method: 'GET',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
      })
        .then((response) => {
          console.log(response)
          return response.json();
        })
        .then((data) => {
          console.log(data);
        })
        .catch((err) => {
          console.error(err);
        });
    });
  }
};
  