pragma solidity ^0.5.9;

// Files Validator

contract Validator{

    mapping(string => bytes32) public files_hashes;

	// add file to the validator
    function add_file_hash(string calldata _file_name, bytes32 _file_hash) external {
        files_hashes[_file_name] = _file_hash;
    }

	// a casting function
    function bytes32array_to_bytes(bytes32[] memory bytes32array) pure internal returns(bytes memory) {
        uint nonzero_bytes = uint8(bytes32array[0][0]);
        bytes memory _bytes = new bytes((bytes32array.length - 2) * 32 + nonzero_bytes);
        uint ind = 0;
        for (uint i = 0; i < bytes32array.length - 2; i++) {
            for(uint j = 0; j < 32; j++) {
                _bytes[ind] = bytes32array[i+1][j];
                ind = ind + 1;
            }
        }
        for (uint j = 0; j < nonzero_bytes; j++) {
            _bytes[ind] = bytes32array[bytes32array.length-1][j];
            ind = ind + 1;
        }
        return _bytes;
    }

	// check if a question is valid
    function is_valid_question(bytes32[] calldata _question) view external returns(bool){
        bytes memory question = bytes32array_to_bytes(_question);
        string memory file_name = string(question);
		// does the validator has the files' info?
        if (files_hashes[file_name] != bytes32(0)) {
            return true;
        }
        return false;
    }

	// check if the answer is valid (assuming the question is valid)
    function is_answer_correct(bytes32[] calldata _question, bytes32[] calldata _answer) view external returns(bool){
        bytes memory question = bytes32array_to_bytes(_question);
        bytes memory answer = bytes32array_to_bytes(_answer);
        string memory file_name = string(question);
		// does the files' hash correct?
        if (keccak256(answer) == files_hashes[file_name]) {
            return true;
        }
        return false;
    }
}