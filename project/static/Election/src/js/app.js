App = {
  web3Provider: null,
  contracts: {},
  account: '0x0',

  init: function() {
    return App.initWeb3();
  },

  // Get our web3 instance
  initWeb3: function() {
    if (typeof web3 !== 'undefined') {
      // If a web3 instance is already provided by Meta Mask browser extension.
      App.web3Provider = web3.currentProvider;
      web3 = new Web3(web3.currentProvider);
    } else {
      // Specify default if no web3 instance provided
      App.web3Provider = new Web3.providers.HttpProvider('http://localhost:7545');
      web3 = new Web3(App.web3Provider);
    }
    return App.initContract();
  },

  // Load Election contract
  initContract: function() {
    $.getJSON("/static/Election/build/contracts/Election.json", function(election) {
      // Start a new truffle contract from the election.json artifact
      App.contracts.Election = TruffleContract(election);
      // Connect to provider to interact with contract
      App.contracts.Election.setProvider(App.web3Provider);

      App.listenForEvents();

      return App.render();
    });
  },

  // Listen for events coming from the contract
  listenForEvents: function(){
    App.contracts.Election.deployed().then(function(instance) {
      instance.voteEvent({}, {
        fromBlock: 'latest',
        toBlock: 'latest'
      }).watch(function(error, event) {
        console.log("event", event);
        // Re-render on event(vote) occurance
        App.render();
      });
    });
  },

  // Display data to the webpage
  render: function() {
    var electionInstance;
    var loader = $("#loader");
    var content = $("#content");
    var voting = $("#voting");
    var voted = $("#voted");

    loader.show();
    voting.show();
    content.hide();
    voted.hide();
  

    // Load in account data
    web3.eth.getCoinbase(function(err, account) {
      if (err === null) {
        App.account = account;
        $("#accountAddress").html("Your Account: " + account);
      }
    });

    // Load in contract data
    App.contracts.Election.deployed().then(function(instance) {
      electionInstance = instance;
      return electionInstance.candidatesCount();
    }).then(function(candidatesCount) {
      var candidatesSelect = $('#candidatesSelect');
      var candidatesResults = $("#candidatesResults");
      candidatesResults.empty();
      candidatesSelect.empty();
     

      for (var i = 1; i <= candidatesCount; i++) {
        electionInstance.candidates(i).then(function(candidate) {
          var id = candidate[0];
          var name = candidate[1];
          var voteCount = candidate[2];

          // Render candidate's results
          var candidateTemplate = "<tr><th>" + id + "</th><td>" + name + "</td><td>" + voteCount + "</td></tr>";
          candidatesResults.append(candidateTemplate);

          // Render candidate options
          var candidateOption ="<option name='candidateOption" + id + "' value='" + id + "'>" + name + "</option>";
          candidatesSelect.append(candidateOption);
        });
      }
      return electionInstance.voters(App.account);
    }).then(function(hasVoted) {
      if(hasVoted){
        voting.hide();
        voted.show();
      }
      loader.hide();
      content.show();
    }).catch(function(error) {
      console.warn(error);
    });
  },

  castVote: function() {
    var candidateId = $('#candidatesSelect').val();
    App.contracts.Election.deployed().then(function(instance) {
      return instance.vote(candidateId, { from: App.account });
    }).then(function(result) {
      //votes update
      $('#content').hide();
      $('#loader').show();
    }).catch(function(err){
      console.error(err);
    });
  }
};


$(function() {
  $(window).load(function() {
    App.init();
  });
});
