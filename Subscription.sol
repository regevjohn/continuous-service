pragma solidity ^0.5.9;
pragma experimental ABIEncoderV2;

// this is a skeleton file for the channel contract. Feel free to change as you wish. 
contract Subscription{

    address payable public provider;
    address payable public customer;
    Validator public validator;
    uint public appeal_period_len;
    uint256 public cost;
    uint public blocks_per_service;
    uint public max_queries;
    
    uint256 provider_balance;
    uint256 costumer_balance;
    uint start_of_service_block;
    uint full_end_of_service_block;
    
    uint max_answered;
    
    // APPEALS
    uint end_of_service_block;
    bool costumer_appeal;
    bytes32[] question_appealed;
    bytes32[] questions_hashes_appealed;
    uint unanswered_appealed;
    bytes32[] answer_resolved;
    uint8 v_appealed;
    bytes32 r_appealed;
    bytes32 s_appealed;
    
    // DEMANDS
    uint end_of_demand_block;
    bool provider_demand;
    bytes32[] question_demanded;
    bytes32[] questions_hashes_demanded;
    uint unanswered_demanded;
    bytes32[] answer_demanded;
    uint8 v_provided;
    bytes32 r_provided;
    bytes32 s_provided;
    
    function get_question_demanded() view external returns(bytes32[] memory){
        return question_demanded;
    }
    
    function get_answer_demanded() view external returns(bytes32[] memory){
        return answer_demanded;
    }
    
    function get_question_hashes_demanded() view external returns(bytes32[] memory){
        return questions_hashes_demanded;
    }
    
    function get_unanswered_demanded() view external returns(uint){
        return unanswered_demanded;
    }
    
    function get_v_provided() view external returns(uint8){
        return v_provided;
    }
    
    function get_r_provided() view external returns(bytes32){
        return r_provided;
    }
    
    function get_s_provided() view external returns(bytes32){
        return s_provided;
    }
    
    function get_v_appealed() view external returns(uint8){
        return v_appealed;
    }
    
    function get_r_appealed() view external returns(bytes32){
        return r_appealed;
    }
    
    function get_s_appealed() view external returns(bytes32){
        return s_appealed;
    }
    
    function is_customer_appealing() view external returns(bool){
        return costumer_appeal;
        //return address(this).balance;
    }
    
    function is_provider_demanding() view external returns(bool){
        return provider_demand;
        //return address(this).balance;
    }
    
    function get_start_of_service_block() view external returns(uint){
        return start_of_service_block;
    }
    
    function get_end_of_service_block() view external returns(uint){
        return end_of_service_block;
    }
    
    function get_question_appealed() view external returns(bytes32[] memory){
        return question_appealed;
    }
    
    function get_answer_resolved() view external returns(bytes32[] memory){
        return answer_resolved;
    }
    
    function get_validator_address() view external returns(address){
        return address(validator);
    }
    
    function is_active() view public returns(bool){
        return end_of_service_block > block.number;
    }

    //Notice how this modifier is used below to restrict access. Create more if you need them!
    modifier onlyOwners{
        require(msg.sender == provider || msg.sender == customer,
            "Only an owner can call this function.");
        _;
    }
    
    modifier onlyProvider{
        require(msg.sender == provider,
            "Only the costumer can call this function.");
        _;
    }
    
    modifier onlyCostumer{
        require(msg.sender == customer,
            "Only the costumer can call this function.");
        _;
    }
    
    modifier appealing {
        require(costumer_appeal,
            "Can't use this function while not appealing.");
        _;
    }
    
    modifier notAppealing {
        require(!costumer_appeal,
            "Can't use this function while appealing.");
        _;
    }
    
    modifier demanding {
        require(provider_demand,
            "Can't use this function while not demanding.");
        _;
    }
    
    modifier notDemanding {
        require(!provider_demand,
            "Can't use this function while demanding.");
        _;
    }
    
    modifier active{
        require(is_active(),
            "Can't use this function when not active.");
        _;
    }
    
    modifier notActive{
        require(!is_active(),
            "Can't use this function when active.");
        _;
    }
    
    constructor(address payable _costumer, uint _appeal_period_len, uint256 _cost, uint256 _blocks_per_service, address _validator, uint _max_queries) public{
        //creates a new channel
        provider = msg.sender;
        customer = _costumer;
        appeal_period_len = _appeal_period_len;
        cost = _cost;
        blocks_per_service = _blocks_per_service;
        validator = Validator(_validator);
        
        max_queries = _max_queries;
        
        end_of_service_block = 0;
        full_end_of_service_block = 0;
        end_of_demand_block = 0;
        provider_balance = 0;
        costumer_balance = 0;
        max_answered = 0;
        costumer_appeal = false;
    }
    
    function activate() notActive onlyCostumer payable public {
        costumer_balance += msg.value;
        if(costumer_balance >= cost) {
            costumer_balance -= cost;
            provider_balance += cost;
            end_of_service_block = block.number + blocks_per_service;
            start_of_service_block = block.number;
            full_end_of_service_block = end_of_service_block;
            end_of_demand_block = end_of_service_block;
            costumer_appeal = false;
        }
    }
    
    function try_appeal(bytes32[] memory question, bytes32[] memory questions_hashes, uint unanswered, uint8 v, bytes32 r, bytes32 s) notAppealing active onlyCostumer view public returns(bool) {
        require(max_answered <= questions_hashes.length - unanswered, "Can't appeal on less answered questions than shown before");
        require(validator.is_valid_question(question), "Question should be valid.");
        require(verifySig(questions_hashes, unanswered, v, r, s, customer), "Hashes are not signed correctly"
            );
        bool in_hashes = false;
        bytes32 hash = hash_question(question);
        for(uint i = questions_hashes.length - unanswered; i < questions_hashes.length; i+=1) {
            if(hash == questions_hashes[i]) {
                in_hashes = true;
            }
        }
        require(in_hashes, "Question is not in the unanswered hashes provided");
        return true;
    }
    
    function appeal(bytes32[] calldata question, bytes32[] calldata questions_hashes, uint unanswered, uint8 v, bytes32 r, bytes32 s) notAppealing active onlyCostumer external {
        require(
            try_appeal(question, questions_hashes, unanswered, v, r, s), "Couldn't appeal");
            
        bool in_hashes = false;
        bytes32 hash = hash_question(question);
        for(uint i = questions_hashes.length - unanswered; i < questions_hashes.length; i+=1) {
            if(hash == questions_hashes[i]) {
                in_hashes = true;
            }
        }
        require(in_hashes, "question appealed must be in unanswered hashess");
        costumer_appeal = true;
        questions_hashes_appealed = questions_hashes;
        unanswered_appealed = unanswered;
        v_appealed = v;
        r_appealed = r;
        s_appealed = s;
        if(end_of_service_block > block.number + appeal_period_len) {
            end_of_service_block = block.number + appeal_period_len;
        }
        provider_balance -= cost;
        costumer_balance += cost;
        question_appealed = question;
        max_answered = questions_hashes.length - unanswered;
    }
    
    function dismiss(bytes32[] calldata questions_hashes, uint unanswered, uint8 v, bytes32 r, bytes32 s) appealing active onlyOwners external{
        require(verifySig(questions_hashes, unanswered, v, r, s, customer), "Hashes are not signed correctly");
        if(max_answered <= questions_hashes.length - unanswered) {
            max_answered = questions_hashes.length - unanswered;
        }
        require(is_hashes_newer(questions_hashes_appealed, unanswered_appealed, questions_hashes, unanswered)
                || !is_hashes_newer(questions_hashes, unanswered, questions_hashes_appealed, unanswered_appealed), "dismiss with older signature");
        end_of_service_block = full_end_of_service_block;
        provider_balance += cost;
        costumer_balance -= cost;
        costumer_appeal = false;
        delete answer_resolved;
    }
    
    function is_hashes_newer(bytes32[] memory old_hashes, uint old_unanswered, bytes32[] memory new_hashes, uint new_unanswered) pure internal returns(bool){
       bool in_other;
       bytes32 hash1;
       bytes32 hash2;
       for(uint i = 0; i < old_hashes.length - old_unanswered; i += 1) {
           hash1 = old_hashes[i];
           in_other = false;
           for(uint j = 0; j < new_hashes.length - new_unanswered; j += 1) {
               hash2 = new_hashes[j];
               if(hash1 == hash2) {
                   in_other = true;
                   break;
               }
           }
           if(!in_other) {
               return false;
           }
       }
       for(uint i = old_hashes.length - old_unanswered; i < old_hashes.length; i += 1) {
           hash1 = old_hashes[i];
           in_other = false;
           for(uint j = 0; j < new_hashes.length; j += 1) {
               hash2 = new_hashes[j];
               if(hash1 == hash2) {
                   in_other = true;
                   break;
               }
           }
           if(!in_other) {
               return false;
           }
       }
       return true;
    }
    
    function resolve(bytes32[] calldata answer) appealing active onlyOwners external{
        require(validator.is_answer_correct(question_appealed, answer), "Answer should match question.");
        end_of_service_block = full_end_of_service_block;
        provider_balance += cost;
        costumer_balance -= cost;
        costumer_appeal = false;
        answer_resolved = answer;
    }
    
    function demand_signature(bytes32[] calldata question, bytes32[] calldata questions_hashes, uint unanswered, uint8 v, bytes32 r, bytes32 s, bytes32[] calldata answer) notDemanding active onlyProvider external{
        require(validator.is_answer_correct(question, answer), "Answer should match question.");
        require(verifySig(questions_hashes, unanswered, v, r, s, customer), "Hashes are not signed correctly");
        bool in_hashes = false;
        bytes32 hash = hash_question(question);
        for(uint i = questions_hashes.length - unanswered; i < questions_hashes.length; i+=1) {
            if(hash == questions_hashes[i]) {
                in_hashes = true;
            }
        }
        require(in_hashes, "Question is not in the unanswered hashes provided");
        
        provider_demand = true;
        questions_hashes_demanded = questions_hashes;
        unanswered_demanded = unanswered;
        question_demanded = question;
        answer_demanded = answer;
        end_of_demand_block = block.number + appeal_period_len;
        max_answered = questions_hashes.length - unanswered;
    }
    
    function provide_signature(bytes32[] calldata questions_hashes, uint unanswered, uint8 v, bytes32 r, bytes32 s) demanding active onlyOwners external{
        require(verifySig(questions_hashes, unanswered, v, r, s, customer), "Hashes are not signed correctly");
        
        bool in_hashes = false;
        bytes32 hash = hash_question(question_demanded);
        for(uint i = 0; i < questions_hashes.length - unanswered; i+=1) {
            if(hash == questions_hashes[i]) {
                in_hashes = true;
            }
        }
        require(in_hashes, "Question is not in the answered hashes provided");
        require(is_hashes_newer(questions_hashes_demanded, unanswered_demanded, questions_hashes, unanswered), "Can't provide older or different signature");
        
        provider_demand = false;
        max_answered = questions_hashes.length - unanswered;
        questions_hashes_demanded = questions_hashes;
        unanswered_demanded = unanswered;
        v_provided = v;
        r_provided = r;
        s_provided = s;
    }
    
    function exec_demand() demanding onlyOwners external{
        if(can_exec_demand()) {
            end_of_service_block = block.number;
            full_end_of_service_block = block.number;
            if(costumer_appeal) {
                provider_balance += cost;
                costumer_balance -= cost;
                costumer_appeal = false;
            }
        }
    }
    
    function can_exec_demand() view public returns(bool){
        return end_of_demand_block <= block.number && provider_demand;
    }
    
    function overflow(bytes32[] calldata questions_hashes, uint unanswered, uint8 v, bytes32 r, bytes32 s) active onlyOwners external{
        require(verifySig(questions_hashes, unanswered, v, r, s, customer), "Hashes are not signed correctly");
        require(questions_hashes.length - unanswered > max_queries, "didnt reach max queries");
         if(costumer_appeal) {
                provider_balance += cost;
                costumer_balance -= cost;
                costumer_appeal = false;
            }
        end_of_service_block = block.number;
        full_end_of_service_block = block.number;
    }
    
    function hash_question(bytes32[] memory question) pure public returns(bytes32) {
        bytes32 hash = keccak256(abi.encodePacked(question));
        return hash;
    }
    
    function verifySig(bytes32[] memory questions_hashes, uint unanswered, uint8 v, bytes32 r, bytes32 s, address signerPubKey) view public returns(bool) {
        bytes32 hashMsg = keccak256(abi.encodePacked(questions_hashes, unanswered, address(this)));
        bytes32 msgDigest = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", hashMsg));
        return ecrecover(msgDigest, v, r, s) == signerPubKey;
    }
    
    function get_other_owner() onlyOwners view public returns(address){
        if(msg.sender == customer) {
            return provider;
        }
        else {
            if(msg.sender == provider) {
                return customer;
            }
        }
        return address(this);
    }
    
    function withdraw_funds_amount() view onlyOwners public returns(uint){
        //withdraws the money of msg.sender to the address he requested. Only used after appeals are done.
        if(msg.sender == provider) {
            uint to_pay = provider_balance;
            if(end_of_service_block > block.number && !costumer_appeal) {
                to_pay = provider_balance - cost;
            }
            return to_pay;
        }
        if(msg.sender == customer) {
            uint to_pay = costumer_balance;
            if(end_of_service_block > block.number && costumer_appeal) {
                to_pay = costumer_balance - cost;
            }
            return to_pay;
        }
        return 0;
    }

    function withdraw_funds(address payable dest_address) onlyOwners external{
        //withdraws the money of msg.sender to the address he requested. Only used after appeals are done.
        if(msg.sender == provider) {
            uint to_pay = provider_balance;
            if(end_of_service_block > block.number && !costumer_appeal) {
                to_pay = provider_balance - cost;
            }
            provider_balance -= to_pay;
            dest_address.transfer(to_pay);
            return;
        }
        if(msg.sender == customer) {
            uint to_pay = costumer_balance;
            if(end_of_service_block > block.number && costumer_appeal) {
                to_pay = costumer_balance - cost;
            }
            costumer_balance -= to_pay;
            dest_address.transfer(to_pay);
            return;
        }
    }

    function () external payable{
        if(msg.sender == customer) {
            costumer_balance += msg.value;
        }
        else {
            if(msg.sender == provider) {
                revert();
            } 
            else {
                revert();
            }
        }
    }
}

contract Validator{
    function is_valid_question(bytes32[] calldata question) pure external returns(bool);
    function is_answer_correct(bytes32[] calldata question, bytes32[] calldata answer) pure external returns(bool);
}