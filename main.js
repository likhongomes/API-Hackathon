//fetch required for CryptoCompare API
const fetch = require('node-fetch');

//URL to pull data from the CryptoCompare API
const url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,ETC&tsyms=USD';

//test getList function
getList().then(function (data){
    console.log(data);
});


//get a list of cryptocurrency prices
function getList(){

    //fetch data from CryptoCompare API
    return fetch(url)
    // Transform the data into json string
    .then((response) => {
     if(response.ok) {
       return response.json();
     } else {
       throw new Error('Server response wasn\'t OK');
     }
   })
   //return the data
    .then(function(data) {
       const list = data;
       return list;
    })
    //if error
    .catch(function(error){
      console.log(error);
    });
}

//Constructor holds the user's id and currency 
function user(id, usd){
    //a unique id
    this.id = id;
    //Money in USD
    this.usd = usd;
    //Bitcoin
    this.btc = 0;
    //Ethereum
    this.eth = 0;
    //Ethereum Classic
    this.etc = 0;
}

//function to buy cryptocurrency
function buy(){
  //TODO
}

//function to sell cryptocurrency
function sell(){
  //TODO
}





