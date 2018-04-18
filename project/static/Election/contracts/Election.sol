pragma solidity ^0.4.2;


contract Election {
    // Model Candidate as a structure with: id / name / voteCount
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    // Storing Candidates (Mapping is a key value pair) 
    // Key is unsigned integer relating to candidate id. Value will be candidate structure type
    mapping(uint => Candidate) public candidates;

    // Storing Accounts that have voted (Mapping is a key value pair) 
    // Key is and address relating to a bool 
    mapping(address => bool) public voters;
    
    // Storing count of candidates
    // mapping has no way to determine size of mapping && can't be iterated over
    uint public candidatesCount;

    // Event for voting
    event voteEvent(
        uint indexed _candidateId
    );

    // Constructor
    function Election() public {
        addCandidate("Toasted");
        addCandidate("Not Toasted");
    }    

    // Adding Candidates - Private just for the contract
    // Increment candediate count, then initiate the candidate struct inside the candidate mapping
    function addCandidate(string _name) private {
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    // Voting - publicly accessed
    // Select candidate via candidate ID parameter, then increment their vote count.
    // Only lets a voter vote once by tracking their account number and checking a boolean
    function vote(uint _candidateId) public {
        // Require voter hasn't voted before
        require(!voters[msg.sender]);
        // Require that a candidate is in the pool
        require(_candidateId > 0 && _candidateId <= candidatesCount);
        // Once voted log the fact that the account has voted
        voters[msg.sender] = true;
        // Increment vote count for chosen candidate
        candidates[_candidateId].voteCount ++;
        // trigger voted event
        emit voteEvent(_candidateId);
    }
}