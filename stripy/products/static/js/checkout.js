window.onload = function() {
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


const buyForm = document.querySelector('#buyForm');
buyForm.addEventListener('submit', (e) => {
  e.preventDefault();
  e.stopPropagation();
  
  const amount = document.querySelector("#amount").value;
  
  const item_url = location.protocol + '//' + location.host + location.pathname.replace('items', 'item') + "?amount=" + amount;
  
  fetch(item_url)
    .then((response) => response.json())
    .then((data) => {
      const stripeCheckoutSessionId = data.StripeCheckoutSessionId;
      console.log(stripeCheckoutSessionId);
      console.log("Stripe Checkout Session Id getting success");
      console.log(stripe);
      stripe.redirectToCheckout({
        sessionId: stripeCheckoutSessionId,
      });
    })
    .catch((err) => {
      console.error(err);
      console.error("Stripe Checkout Session Id getting error");
    });
  });

};
