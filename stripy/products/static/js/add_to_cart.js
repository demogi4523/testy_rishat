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
  
    const addToCartForms = document.querySelectorAll('.addToCartForm');
    for (let index = 0; index < addToCartForms.length; index += 1) {
      const addToCartForm = addToCartForms[index];
      addToCartForm.addEventListener('submit', (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        const sending_form = e.target;
        console.log(sending_form);
        const pk = parseInt(sending_form.id.replace('addToCartForm', ''));
        const csrftoken = getCookie('csrftoken');
        const amount = sending_form.children[1].value;
  
        fetch('/cart_add/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
          },
          mode: 'same-origin',
          body: JSON.stringify({ pk, amount })
        })
          .then((response) => {
            console.log(response);
            sending_form.children[1].value = 1;
            alert('Added successfully!!!');
          });
      });
    }
  };
    