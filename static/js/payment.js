paypal.Buttons({
    createOrder: () => {
        return fetch('http://localhost:8000/payment', {
            // body: JSON.stringify({data:"order"}),
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST"
        }).then((res) => {
            return res.json();
        }).then((data) => {
            console.log(data);
            return data.order_id;
            // Use the key sent by your server's response, ex. 'id' or 'token'
        }).catch(err => console.log(err))
    },
    onApprove: (data) => {
        console.log(data);
        return fetch('http://localhost:8000/execute_payment', {
            body: JSON.stringify({
                orderID: data.orderID,
                payerId: data.payerID
            }),
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST"
        }).then((res) => {
            return res.json();
        }).then((data) => {
            console.log(data);
        }).catch(err => console.log(err))
    }
}).render('#paypal-button-container'); // Display payment options on your web page